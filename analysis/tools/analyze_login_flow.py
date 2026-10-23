"""Reproduce login-flow evidence by parsing local bytecode; never execute Lua."""
from pathlib import Path
import base64
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile

from luajit_static import parse, listing, decode, static_tables

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.patch_server_list import patch
OUT = ROOT / 'analysis/evidence/login_flow'
ALPHABET = 'yfglmnovwxapzdechijkqrstbuHOMICDJPQRSTUVWXYZABKEFGLN39+0126-4785'
TERMS = ['getServerList', 'getLastServerList', 'getHash', 'player.Login',
         'player.GetUserList', 'player.CreateUser', 'user.UserLogin',
         'user.GetUserInfo', 'LoginOk', 'GetUserList', 'CreateUser',
         'UserLogin', 'GetUserInfo', 'type_enum_role']
# Original source start lines identify the functions reviewed in the report.
SELECT = {
    'lua/net/network.lua': [178, 203, 710, 1246, 2236, 2277, 2346, 2394, 2593],
    'lua/ui/loginUI.lua': [76, 124, 599, 635, 1381],
    'lua/base/setting.lua': [36, 132],
    'lua/event_mgr.lua': [288, 300, 316, 325],
    'lua/ui/mainUI.lua': [203],
    'lua/ui/guideUI.lua': [205, 274, 1320, 2477],
    'lua/ui/systemSetUI.lua': [334, 630],
    'lua/update/update_mgr.lua': [158],
    'lua/ui/mapUI.lua': [341],
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    release = ROOT / 'jgbol3.87/assets/release_'
    header, encoded = (release / 'index.txt').read_text().split('\n', 1)
    index = base64.b64decode(encoded.translate(str.maketrans(
        ALPHABET + '_', 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')),
        validate=True).decode('gb18030')
    rows = [line.split('====') for line in index.splitlines()]
    config = json.loads((ROOT / 'game.json').read_text())
    apk_path = ROOT / config['apk']
    results = {'method': 'offline static parsing; no Lua execution or network',
               'resource_version_header': header,
               'apk': str(apk_path.relative_to(ROOT)),
               'apk_sha256': sha(apk_path.read_bytes()),
               'files': [], 'literal_search': {term: [] for term in TERMS}}
    excerpts = []
    chunks = {}
    with zipfile.ZipFile(apk_path) as apk:
        for logical, physical, _ in rows:
            if not logical.endswith('.lua'):
                continue
            raw = (release / physical).read_bytes()
            chunk = parse(raw)
            chunks[logical] = chunk
            current = apk.read('assets/release_/' + physical)
            current_chunk = parse(current)
            if logical == 'lua/update/update_mgr.lua':
                results['server_list_patch_matches'] = current == patch(raw)
            results['files'].append({
                'logical': logical, 'physical': physical,
                'original_sha256': sha(raw), 'current_apk_sha256': sha(current),
                'same_as_original': raw == current,
                'prototype_count': len(chunk['protos']),
            })
            strings = [k for p in current_chunk['protos'] for k in p['kgc'] if isinstance(k, str)]
            for term in TERMS:
                hits = sorted({k for k in strings if term in k})
                if hits:
                    results['literal_search'][term].append({'file': logical, 'constants': hits})
            if logical not in SELECT:
                continue
            text = listing(chunk)
            previous = ROOT / 'analysis/evidence/lua_named' / (logical + '.txt')
            assert text == previous.read_text(), logical
            blocks = re.split(r'\n(?=FUNCTION proto)', text)[1:]
            found = []
            for p, block in zip(chunk['protos'], blocks):
                if p['line'] in SELECT[logical]:
                    found.append(p['line'])
                    excerpts.append('\n===== ' + logical + ' =====\n' + block)
            assert set(found) == set(SELECT[logical]), (logical, found)
        native = 'lib/armeabi/libxiyoujilua.so'
        raw_native = (ROOT / 'jgbol3.87' / native).read_bytes()
        results['native'] = {'sha256': sha(raw_native),
                             'same_as_original': raw_native == apk.read(native)}
    results['lua_count'] = len(results['files'])
    results['changed_lua'] = [r['logical'] for r in results['files'] if not r['same_as_original']]
    assert results['changed_lua'] == ['lua/update/update_mgr.lua']
    assert results['server_list_patch_matches'] and results['native']['same_as_original']
    # Literal TDUP -> GSET pairs in common_def; no function calls evaluated.
    common = chunks['lua/common/common_def.lua']
    p = common['protos'][common['root']]
    tables = {}
    for before, after in zip(p['code'], p['code'][1:]):
        op, a, _, _, d = decode(before)
        op2, a2, _, _, d2 = decode(after)
        if op == 'TDUP' and op2 == 'GSET' and a == a2:
            tables[p['kgc'][d2]] = p['kgc'][d]['value']
    wanted = {
        'platform_type': ['p360_na', 'wdj_a2'],
        'common_event_type': ['login_request'],
        'client_common_event': ['p360_na_account_login', 'wdj_new_login'],
        'login_code': ['success'],
        'new_role_guide': ['modify_name', 'pick_cortege_one', 'take_task_prize'],
    }
    results['constants'] = {group: {k: tables[group][k] for k in names}
                            for group, names in wanted.items()}
    protocol = static_tables(chunks['lua/common/msg_def.lua'])
    ids = {1001, 1002, 1016, 1017, 1018, 1020, 1023, 1204, 2996, 2998, 2999, 3001, 3002, 3103, 3104, 3105}
    results['messages'] = []
    for group in ['gscl_msg', 'lscl_msg', 'gsls_msg']:
        names = {v: k for k, v in protocol[group + '_id'].items()}
        for msg in protocol[group].values():
            if msg['id'] in ids:
                results['messages'].append(dict(msg, group=group, name=names[msg['id']],
                                                field_count=len(msg['def'].split(','))))
    (OUT / 'lua_excerpts.txt').write_text('\n'.join(excerpts))
    # Save the 360 Java bridge evidence already decoded by the project.
    smali = ROOT / '.runtime/channel360/decoded/smali/com/syyx/sdkproxy'
    for name in ['ThirdPartyAPI.smali', 'ThirdPartyAPI$1.smali', 'ThirdPartyAPI$3.smali']:
        shutil.copyfile(smali / name, OUT / name)
    objdump = subprocess.check_output(['xcrun', '--find', 'llvm-objdump'], text=True).strip()
    asm = []
    for start, end in [('0xff8f8', '0xffb78'), ('0x100d38', '0x100dac')]:
        asm.append(subprocess.check_output([
            objdump, '-d', '--triple=thumbv7-none-linux-gnueabi', '--demangle',
            '--start-address=' + start, '--stop-address=' + end,
            str(ROOT / 'jgbol3.87/lib/armeabi/libxiyoujilua.so')], text=True))
    (OUT / 'native_hash.asm').write_text('\n'.join(asm))
    (OUT / 'verification.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: results[k] for k in ['lua_count', 'changed_lua', 'native', 'constants']},
                     ensure_ascii=False, indent=2))
    print('1017 fields:', next(m['field_count'] for m in results['messages'] if m['id'] == 1017))


if __name__ == '__main__':
    main()
