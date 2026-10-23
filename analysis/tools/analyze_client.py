"""Offline, read-only analysis of jgbol3.87; generated outputs default to analysis/."""
from pathlib import Path
import base64
import collections
import csv
import hashlib
import io
import json
import re
import zipfile
from luajit_static import parse, listing, decode, static_tables
import argparse
import tempfile
import subprocess
import os

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'jgbol3.87'
OUT = ROOT / 'analysis'
EVIDENCE = OUT / 'evidence'
ALPHABET = 'yfglmnovwxapzdechijkqrstbuHOMICDJPQRSTUVWXYZABKEFGLN39+0126-4785'

def save(name, obj):
    p = EVIDENCE / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def main():
    global OUT, EVIDENCE
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=OUT)
    args = parser.parse_args()
    OUT = args.output.resolve()
    EVIDENCE = OUT / 'evidence'
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    release = SRC / 'assets/release_'
    index = (release / 'index.txt').read_text()
    version, encoded = index.split('\n', 1)
    decoded = base64.b64decode(encoded.translate(str.maketrans(ALPHABET+'_', 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')), validate=True)
    decoded_text = decoded.decode('gb18030')
    (EVIDENCE / 'resource_index.decoded.txt').write_text(decoded_text)
    rows = [s.split('====') for s in decoded_text.splitlines()]
    assets, configs, scripts = [], [], []
    for logical, physical, declared in rows:
        p = release / physical
        data = p.read_bytes()
        assets.append({'logical': logical, 'physical': physical, 'declared_bytes': int(declared), 'actual_bytes': len(data), 'size_matches': len(data) == int(declared), 'sha256': hashlib.sha256(data).hexdigest(), 'content_md5_matches_name': hashlib.md5(data).hexdigest() == p.stem})
        if logical.endswith('.csv'):
            encoding = 'utf-8-sig'
            try: text = data.decode(encoding)
            except UnicodeDecodeError:
                encoding = 'gb18030'
                text = data.decode(encoding)
            table = list(csv.reader(io.StringIO(text, newline=None)))
            dest = OUT / 'configs' / Path(logical).relative_to('csv_config')
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(text, encoding='utf-8')
            configs.append({'logical': logical, 'physical': physical, 'encoding': encoding, 'columns': table[0], 'data_rows': len(table)-1, 'ragged_rows': [i for i, row in enumerate(table[1:],2) if len(row) != len(table[0])], 'sample': table[1:3]})
        if logical.endswith('.lua'):
            proto = parse(data)
            dest = EVIDENCE / 'lua_named' / (logical + '.txt')
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(listing(proto))
            names = {}
            root = proto['protos'][proto['root']]
            for i, ins in enumerate(root['code'][:-1]):
                op, a, b, c, d = decode(ins)
                op2, a2, b2, c2, d2 = decode(root['code'][i+1])
                if op == 'FNEW' and op2 == 'GSET' and a == a2:
                    names['proto'+str(root['kgc'][d]['id'])] = root['kgc'][d2]
            scripts.append({'logical':logical,'physical':physical,'protos':len(proto['protos']), 'functions':names})
    save('resource_inventory.json', assets)
    save('config_inventory.json', configs)
    save('script_inventory.json', scripts)
    msg_path = next(x['physical'] for x in assets if x['logical']=='lua/common/msg_def.lua')
    tables = static_tables(parse((release/msg_path).read_bytes()))
    save('protocol_tables.json', tables)
    md = ['# 金箍棒 3.87 协议定义表（静态提取）', '', '来源：`lua/common/msg_def.lua`；由常量传播恢复表构造，不执行 Lua。方向按表所属模块及名称理解，客户端收录的服务端协议不代表服务端实现已恢复。`base` 为基础结构 ID；原始类型记号保留，线格式仍需与 native 序列化代码对应。', '']
    for group, definitions in tables.items():
        if group != 'common_def' and not group.endswith('_msg'): continue
        ids = tables['common_id' if group=='common_def' else group+'_id']
        reverse = {v:k for k,v in ids.items()}
        md += ['## '+group, '', '| ID | 名称 | 基础结构 ID | 字段定义（原文） |', '|---|---|---|---|']
        for v in definitions.values():
            mid = int(v['id'])
            base = '-' if v.get('base') is None else str(int(v['base']))
            md.append(f'| {mid} | `{reverse.get(mid,"未命名")}` | {base} | `{v["def"].replace("|", "&#124;")}` |')
        md += ['']
    md += ['## 仅有 ID、未恢复字段布局的组', '',
           '`csdba_msg_id` 声明了 `msg_login_req=3701`、`msg_login_rsp=3702`，但样本没有对应 `csdba_msg` 字段表；不计入 269 条结构定义。', '',
           '## 原始定义注意事项', '',
           '`type_attach_data` 含重复字段名 `stone1_level`；`type_pp_http_response` 含 `user_name=S[32,uid=d`。此处保留样本原文，未擅自修正。', '',
           '完整 ID、类型和结构常量见 [protocol_tables.json](evidence/protocol_tables.json)。通用事件载体中的文本子协议不等于全部已恢复。', '']
    (OUT / '协议定义表.md').write_text('\n'.join(md))
    # Verify signed file digests in original extracted tree; no trust claim about publisher.
    manifest = (SRC/'META-INF/MANIFEST.MF').read_text().replace('\n ', '')
    signed = []
    for block in manifest.split('\n\n'):
        fields = dict(line.split(': ',1) for line in block.splitlines() if ': ' in line)
        if 'Name' not in fields: continue
        p = SRC / fields['Name']
        digest = fields.get('SHA1-Digest') or fields.get('SHA-1-Digest')
        assert digest is not None, fields
        signed.append({'path':fields['Name'],'exists':p.exists(),'sha1_matches':p.exists() and base64.b64encode(hashlib.sha1(p.read_bytes()).digest()).decode()==digest})
    save('signed_entries.json', signed)
    # Reconstructed inspection container; not an original distribution APK.
    with tempfile.TemporaryDirectory(prefix='jgbol387-static-') as temp:
        apk_path = Path(temp)/'inspection.apk'
        with zipfile.ZipFile(apk_path,'w',zipfile.ZIP_DEFLATED) as apk:
            for p in sorted(SRC.rglob('*')):
                if p.is_file() and p.name != '.DS_Store':
                    apk.write(p,p.relative_to(SRC).as_posix())
        with zipfile.ZipFile(apk_path) as apk:
            archive_bad = apk.testzip()
            entries = [i for i in apk.infolist() if not i.is_dir()]
            tree_mismatch = [i.filename for i in entries if apk.read(i.filename)!=(SRC/i.filename).read_bytes()]
        sdk = ROOT/'.runtime/sdk/build-tools/35.0.0'
        env = dict(os.environ, JAVA_HOME=str(ROOT/'.runtime/java/jdk-17.0.20.1+1/Contents/Home'))
        for filename, command in [
            ('apk_signature.txt',[str(sdk/'apksigner'),'verify','--verbose','--print-certs',str(apk_path)]),
            ('badging.txt',[str(sdk/'aapt'),'dump','badging',str(apk_path)]),
            ('manifest.txt',[str(sdk/'aapt'),'dump','xmltree',str(apk_path),'AndroidManifest.xml'])]:
            result=subprocess.run(command,env=env,capture_output=True,text=True)
            (EVIDENCE/filename).write_text(result.stdout+result.stderr)
            assert result.returncode == 0, (filename,result.stderr)
    (OUT/'配置表目录.md').write_text('\n'.join([
        '# 金箍棒 3.87 配置表目录','',
        f'共 {len(configs)} 张表。行数为 CSV 解析后的表头外记录，包含可能的空记录。编码标签为本次解码方式；UTF-8 副本保留字段内容，复合字段未强制转换。', '',
        '| 逻辑路径 | 数据行 | 解码方式 | 列数异常记录数 | UTF-8 副本 |',
        '|---|---:|---|---:|---|'] + [
        f"| `{x['logical']}` | {x['data_rows']} | {x['encoding']} | {len(x['ragged_rows'])} | [{Path(x['logical']).name}](configs/{Path(x['logical']).relative_to('csv_config').as_posix()}) |" for x in configs])+ '\n')
    key_files = ['AndroidManifest.xml','classes.dex','resources.arsc','lib/armeabi/libxiyoujilua.so','assets/release_/index.txt']
    summary = {
      'date':'2026-10-23','sample':'jgbol3.87','index_encoding':'gb18030','index_version':version,'logical_assets':len(assets),'physical_assets':len(set(x['physical'] for x in assets)),
      'release_files':len(list(release.iterdir())),'release_bytes':sum(p.stat().st_size for p in release.iterdir()),
      'unreferenced':sorted(set(p.name for p in release.iterdir())-set(x['physical'] for x in assets)),
      'index_copy_identical':(release/('index_'+version.split('====')[1]+'.txt')).read_bytes()==(release/'index.txt').read_bytes(),
      'logical_extensions':dict(collections.Counter(Path(x['logical']).suffix for x in assets)),
      'size_mismatches':sum(not x['size_matches'] for x in assets),'md5_name_matches':sum(x['content_md5_matches_name'] for x in assets),
      'config_count':len(configs),'config_rows':sum(x['data_rows'] for x in configs),'config_encodings':dict(collections.Counter(x['encoding'] for x in configs)),
      'config_ragged':{x['logical']:x['ragged_rows'] for x in configs if x['ragged_rows']},
      'lua_count':len(scripts),'lua_protos':sum(x['protos'] for x in scripts),
      'protocol_counts':{k:len(v) for k,v in tables.items()},
      'signed_entries':len(signed),'signed_errors':[x for x in signed if not x['sha1_matches']],
      'apk_crc_error':archive_bad,'apk_vs_tree_mismatches':tree_mismatch,'apk_entries':len(entries),
      'fingerprints':{f:hashlib.sha256((SRC/f).read_bytes()).hexdigest() for f in key_files},
      'apk_provenance':'temporary reconstructed container for static inspection; original APK not supplied',
    }
    save('summary.json', summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__ == '__main__': main()
