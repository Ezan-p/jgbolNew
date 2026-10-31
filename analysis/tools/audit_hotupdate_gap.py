"""Read-only comparison of original 1205..1263 resources and shipped v107.

Writes only audit artifacts. Does not start a game, open saves or change rules.
Cached original ZIPs must already exist; all are checked against the manifest.
"""
import argparse
import base64
import collections
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile

from luajit_static import parse, listing, static_tables, decode

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'analysis/evidence/hotupdate_gap_20261031'
ALPHABET = 'yfglmnovwxapzdechijkqrstbuHOMICDJPQRSTUVWXYZABKEFGLN39+0126-4785'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def index(raw):
    version, encoded = raw.decode().split('\n', 1)
    text = base64.b64decode(encoded.translate(str.maketrans(
        ALPHABET + '_', 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='))).decode('gb18030')
    return int(re.search(r'\d+', version)[0]), {p[0]: p[1] for line in text.splitlines() if len(p := line.split('====')) >= 2}


def table(raw):
    for encoding in ('utf-8-sig', 'gb18030'):
        try:
            return list(csv.reader(io.StringIO(raw.decode(encoding), newline=None)))
        except UnicodeDecodeError:
            pass
    raise ValueError('Unknown CSV encoding')


def diff_rows(old, new):
    a, b = collections.Counter(map(tuple, old[1:])), collections.Counter(map(tuple, new[1:]))
    return dict(old_rows=len(old)-1, new_rows=len(new)-1,
                removed_or_changed=sum((a-b).values()), added_or_changed=sum((b-a).values()),
                header_changed=old[0] != new[0])


def write_inventory(report):
    """Generate exhaustive inventory; judgments are dated manual annotations."""
    judgments={
        'achievements_config.csv':'缺580～590及563～565次数扩展；achievements.py读旧表',
        'assist_shop_config.csv':'当前无加载；独立入口／结算待核，勿直接当成完整功能缺失',
        'babel_secret_tower_floor_prize.csv':'通天秘境缺失；1353操作12～14拒绝',
        'babel_tower_floor_prize.csv':'当前上限60，缺61～70层',
        'cards_letter.csv':'功能已有：activity_tangwang以规则覆盖为末版8字',
        'cards_tip.csv':'末版3组合已有；奖励采用离线配置',
        'charge_gift_config.csv':'首充已实现；仍采用旧奖励',
        'cortege/cortege_base_0.csv':'8001～8004改动；蟠桃会已有专项离线首领设计',
        'cortege_devolve.csv':'缺121～499飞升回收；不要混同五选四星神仙回收',
        'cortege_evolution.csv':'飞升上限仍299，缺300～499',
        'cortege_evolve_config.csv':'飞升培养点仍止于299档',
        'cortege_experience.csv':'五品质均止于300级，缺301～600',
        'cortege_reborn_config.csv':'仍14名；缺新增11名转生，影响六耳逆天前置',
        'dream_prize_config.csv':'梦境旧玩法1325本体无路由',
        'exchange_zone.csv':'已有多层覆盖与离线改动；不能按基础表判定未实现',
        'ext_skill.csv':'仍旧8条参数／机制；含中毒20万／三回合／叠层差异',
        'ext_skill_lock_cost.csv':'已有第五槽但最多锁3槽；缺第4档1000元宝',
        'fate_star_transform.csv':'缺1359命星转换与1376转换符',
        'gold_rush_config.csv':'淘金1207本体无路由；后续9档未接',
        'hill_top_prize.csv':'万寿山1323本体无路由；后续6档未接',
        'hole/garden_seed_config.csv':'仍旧种植时间／消耗／产出',
        'item_base.csv':'专门合并1370～1375；缺1376～1378',
        'item_name.csv':'同物品基础表；有图标文案不代表来源与结算实现',
        'ling_effect.csv':'强壮7→2未同步；另一处改名的机制需核',
        'material_transform.csv':'缺1378×20＋50万银两合紫色命星',
        'material_transform_index.csv':'缺命星合成类别10',
        'newbie_content9.csv':'梦境说明改奖；旧梦境活动本体未接',
        'prey_week_rank.csv':'猎魂已有；周榜仍旧7档奖励值',
        'skill_base.csv':'缺11定义；治疗效果部分已有，原获取与专用表现待核',
        'skill_name.csv':'新增慈心善佑；不能据此认定可学习／可掉落',
        'spring_card_config.csv':'原表未直接加载；国庆三组合已由唐王代码实现',
        'star_config.csv':'占星已有；16～29星位新碎片1378来源未接',
        'stone_cost_worth.csv':'基础表旧；高阶提炼实际改读专用表，不能单列为缺13／14级',
        'stone_reborn_cost_worth.csv':'已由stone/专表实现到14级，专表与1263一致',
        'summer_cards_tip.csv':'夏日1331未接；此表仅奖励提示，不足证明完整奖池',
        'tongtianta_score_awards.csv':'缺20／40／60／70四档结算；具体领取时机待核',
    }
    fate={'cor_level_effect_config.csv','faterebuild_cort_active.csv','faterebuild_cort_property.csv',
          'faterebuild_unblock_effect.csv','jp_level_effect_config.csv','level_effect_config.csv',
          'rebuild_material_costs.csv','rebuild_material_zs_costs.csv','select_effect_config.csv','stars_effect_config.csv'}
    lines=['# 原服热更新差异逐文件清单','',
           '日期：2026-10-31。范围：原服资源1205→1263，与v107实际载荷／当前工作区对照。', '',
           '主结论、玩法影响、证据边界和优先级见[差异审计报告](原服后续热更新与v107离线版差异审计.md)。', '',
           '本附录由`analysis/tools/audit_hotupdate_gap.py`生成；数字来自实际包，功能判断为本次人工审计注释，不会因未来代码变化自动更新。', '',
           '## 1. 全部57张变化CSV','',
           '行数不含表头；洞府建筑表包含0级。新表在1205行数记0。服务端列仅指同路径基础表，专项覆盖须看最后一列。CSV按解析后的表头及逐行内容比较，避免把BOM／换行差异当规则变化。', '',
           '| 原服逻辑表／末版证据 | 修改版本 | 1205→1263行数 | 当前基础表行数 | 实际分类与依据 |',
           '|---|---|---:|---:|---|']
    for row in report['csv']:
        name=row['logical'].removeprefix('csv_config/')
        if name in judgments: judgment=judgments[name]
        elif name in fate: judgment='fate_rebuild/专项目录有1263同表；主体已接，加载与公式边界见主报告'
        elif name.startswith('hole/'): judgment='高阶洞府数据未同步；主殿／药园／神庙扩建及相关材料／倍率缺口'
        elif name.startswith('newbie_'): judgment='1215新版新手目标活动未接；不是原天书／引导／1131福利'
        else: raise AssertionError('Unclassified CSV: '+name)
        path='../analysis/evidence/hotupdate_gap_20261031/official_csv/'+name
        lines.append(f"| [{name}]({path}) | {'、'.join(map(str,row['versions']))} | {row['old_rows']}→{row['new_rows']} | {row['workspace_rows'] if row['workspace_rows'] is not None else '无'} | {judgment} |")
    lines+=['','## 2. 全部58份变化Lua','',
            '58份均已随v107携带。此表仅列资源变化与关键业务定位；没有逐函数证明其所有服务端行为均已恢复。除新增7份外均为旧脚本修改。', '',
            '| 逻辑路径 | 修改版本 | 是否新文件 | 审计说明 |','|---|---|---|---|']
    notes={'lua/ui/newbieUI.lua':'新手目标／积分／每日活动／购买未接',
           'lua/ui/mxTransformUI.lua':'命星转换1359未接',
           'lua/ui/tongtiantaSecretUI.lua':'通天秘境1353/12～14未接',
           'lua/ui/tongtiantaUI.lua':'塔70层、阶段奖励扩展未接',
           'lua/ui/fateRebuildUI.lua':'1357主体已接；前置名单和成就有断点',
           'lua/ui/soulUI.lua':'三魂主体已接；不是独立全缺系统',
           'lua/ui/soulSevenUI.lua':'七魄主体已接；新增成就未接',
           'lua/ui/homeUI.lua':'客户端建筑已扩展，服务端仍旧20级',
           'lua/ui/feishengUI.lua':'客户端后续飞升界面已有，服务端仍299',
           'lua/skill/skill_11.lua':'新治疗表现；服务端缺11定义，已有部分治疗机制',
           'lua/common/msg_def.lua':'新增1354～1360与类型130，需按方向和业务分类',
           'lua/ui/playerCenterUI.lua':'中途修改，末版已回到1205内容',
           'lua/ui/stoneUI.lua':'13→14入口已由离线补丁接通',
           'lua/ui/stoneCastUI.lua':'高阶配方已接，原链最高14级',
           'lua/ui/springCardUI.lua':'国庆三组合已由离线唐王模块承接'}
    for row in report['lua']:
        lines.append(f"| `{row['logical']}` | {'、'.join(map(str,row['versions']))} | {'新增' if row['new_file'] else '修改'} | {notes.get(row['logical'],'资源已打包；不能仅按文件变化推断功能完成度')} |")
    lines+=['','## 3. 全部56个增量包','',
            '每包大小／MD5／CRC均通过；下表修改资源数含新增。包名、大小、MD5与SHA-256完整值在[audit.json](../analysis/evidence/hotupdate_gap_20261031/audit.json)。', '',
            '| 起始→目标 | 原包名 | 字节数 | 修改资源／其中新增 |',
            '|---|---|---:|---:|']
    for package in report['packages']:
        lines.append(f"| {package['start']}→{package['end']} | `{package['file']}` | {package['size']} | {package['changed']}／{package['added']} |")
    lines+=['','## 4. 其他187项资源及全量证据','',
            '其他资源包含图像、图集、布局、字符串等，全部逻辑路径、首次变化和版本历史保存在JSON的`other_resources`与`history`，不把每张图片单独算成一个新增玩法。', '',
            '- [全资源历史及末版核对](../analysis/evidence/hotupdate_gap_20261031/audit.json)',
            '- [1263直接发包引用](../analysis/evidence/hotupdate_gap_20261031/client_request_references.json)',
            '- [1263协议定义](../analysis/evidence/hotupdate_gap_20261031/protocol_tables_1263.json)',
            '- [当前有效规则、路由与内存探针](../analysis/evidence/hotupdate_gap_20261031/backend_audit.json)',
            '- [原服变化CSV副本](../analysis/evidence/hotupdate_gap_20261031/official_csv)',
            '- [关键客户端Lua静态反汇编](../analysis/evidence/hotupdate_gap_20261031/lua)', '']
    (ROOT/'docs/原服热更新差异逐文件清单.md').write_text('\n'.join(lines))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', type=Path, default=Path('/private/tmp/jgb-hotupdate'))
    parser.add_argument('--manifest', type=Path, default=ROOT/'analysis/evidence/ascension_hotupdate_20261031/update_list.txt')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = args.manifest.read_bytes()
    (OUT/'update_list.txt').write_bytes(manifest)
    records = [(int(a), int(b), n, int(size), md5) for a,b,n,size,md5 in re.findall(
        r'\{\s*(\d+),\s*(\d+),\s*"([^"]+)",\s*(\d+),\s*"([a-f0-9]+)"', manifest.decode())
        if 1205 <= int(a) < int(b) <= 1263]
    base = ROOT/'jgbol3.87/assets/release_'
    version, initial = index((base/'index.txt').read_bytes())
    assert version == 1205
    available = {name: base/name for name in set(initial.values())}
    current = dict(initial)
    history, packages = collections.defaultdict(list), []
    for start, end, filename, size, md5 in records:
        assert start == version, (start, version)
        raw = (args.cache/filename).read_bytes()
        assert len(raw) == size and hashlib.md5(raw).hexdigest() == md5, filename
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            assert archive.testzip() is None
            next_version, next_index = index(archive.read('index.txt'))
            assert next_version == end
            changed = [name for name in next_index if current.get(name) != next_index[name]]
            removed = sorted(set(current)-set(next_index))
            for name in archive.namelist():
                if name.endswith('.data'):
                    available[name] = (args.cache/filename, name)
            def read_resource(physical):
                source = available[physical]
                if isinstance(source, Path):
                    return source.read_bytes()
                with zipfile.ZipFile(source[0]) as z:
                    return z.read(source[1])
            for logical in changed:
                entry = dict(version=end, kind='added' if logical not in current else 'changed',
                             physical=next_index[logical])
                if logical.endswith('.csv'):
                    new = table(read_resource(next_index[logical]))
                    old = table(read_resource(current[logical])) if logical in current else [new[0]]
                    entry.update(diff_rows(old,new))
                history[logical].append(entry)
            packages.append(dict(start=start,end=end,file=filename,size=size,md5=md5,sha256=sha(raw),
                                 crc_passed=True,changed=len(changed),added=sum(n not in current for n in changed),
                                 removed=removed))
            current, version = next_index, end
    assert version == 1263 and len(packages) == 56
    apk_path = ROOT/'build/金箍棒3.87离线正式版v107.apk'
    with zipfile.ZipFile(apk_path) as apk, zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as program:
        client_version, client_index = index(program.read('client/release_w/index.txt'))
        assert client_version == 1263
        def shipped(logical):
            physical = client_index[logical]
            overlay = 'client/release_w/'+physical
            return program.read(overlay) if overlay in program.namelist() else apk.read('assets/release_/'+physical)
        protocols = static_tables(parse(shipped('lua/common/msg_def.lua')))
        (OUT/'protocol_tables_1263.json').write_text(json.dumps(protocols,ensure_ascii=False,indent=2)+'\n')
        common_chunk = parse(shipped('lua/common/common_def.lua'))
        root = common_chunk['protos'][common_chunk['root']]
        common = {}
        for instruction, following in zip(root['code'],root['code'][1:]):
            op,a,b,c,d=decode(instruction)
            op2,a2,b2,c2,d2=decode(following)
            if op=='TDUP' and op2=='GSET' and a==a2:
                common[root['kgc'][d2]]=root['kgc'][d]['value']
        (OUT/'common_tables_1263.json').write_text(json.dumps(common,ensure_ascii=False,indent=2)+'\n')
        references = collections.defaultdict(list)
        request_names = protocols['gscl_msg_id'] | protocols['lscl_msg_id']
        selected = {'common/msg_def','common/common_def','ui/soulUI','ui/soulSevenUI','ui/newbieUI',
                    'ui/mxTransformUI','ui/tongtiantaSecretUI','ui/tongtiantaUI','ui/fateRebuildUI',
                    'ui/springCardUI','skill/skill_11','ui/wakeUI','skill/skillExt','unit/charecter','ui/homeUI'}
        for logical in sorted(client_index):
            if not logical.endswith('.lua'):
                continue
            text = listing(parse(shipped(logical)))
            if logical.removeprefix('lua/').removesuffix('.lua') in selected:
                dest=OUT/'lua'/logical.removeprefix('lua/')
                dest=dest.with_suffix('.lua.txt')
                dest.parent.mkdir(parents=True,exist_ok=True)
                dest.write_text(text)
            lines=text.splitlines()
            for i,line in enumerate(lines):
                if "'main_server_send_msg'" not in line:
                    continue
                for candidate in lines[i+1:i+13]:
                    if ' CALL ' in candidate or candidate.startswith('FUNCTION'):
                        break
                    match=re.search(r"'(msg_\w+)'",candidate)
                    if match and match[1] in request_names:
                        references[request_names[match[1]]].append(dict(logical=logical,name=match[1],instruction=candidate.strip()))
        (OUT/'client_request_references.json').write_text(json.dumps(references,ensure_ascii=False,indent=2)+'\n')
        csvs, lua, resources = [], [], []
        for logical in sorted(history):
            official = read_resource(current[logical]) if logical in current else None
            entry = dict(logical=logical,first_changed=history[logical][0]['version'],
                         versions=[h['version'] for h in history[logical]],new_file=logical not in initial,
                         original_sha256=sha(official) if official is not None else None,
                         apk_client_matches=logical in client_index and shipped(logical) == official)
            if logical.endswith('.csv') and official is not None:
                new = table(official)
                old = table((base/initial[logical]).read_bytes()) if logical in initial else [new[0]]
                relative = 'analysis/configs/'+logical.removeprefix('csv_config/')
                path = ROOT/relative
                workspace = table(path.read_bytes()) if path.is_file() else None
                payload = table(program.read(relative)) if relative in program.namelist() else None
                entry.update(diff_rows(old,new))
                entry.update(workspace_rows=len(workspace)-1 if workspace else None,
                             workspace_equals_original=workspace == new,
                             payload_rows=len(payload)-1 if payload else None,
                             payload_equals_original=payload == new,
                             workspace_payload_equal=workspace == payload)
                if workspace is not None:
                    entry['workspace_diff']=diff_rows(workspace,new)
                dest = OUT/'official_csv'/logical.removeprefix('csv_config/')
                dest.parent.mkdir(parents=True,exist_ok=True)
                with dest.open('w',encoding='utf-8',newline='') as f:
                    csv.writer(f).writerows(new)
                csvs.append(entry)
            elif logical.endswith('.lua'):
                lua.append(entry)
            else:
                resources.append(entry)
        relevant = {}
        for name in program.namelist():
            if name.startswith(('network_redirect/','server_config/','analysis/configs/')) and name.endswith(('.py','.lua','.csv','.json')):
                path=ROOT/name
                if path.is_file() and path.read_bytes()!=program.read(name):
                    relevant[name] = dict(workspace_sha256=sha(path.read_bytes()),payload_sha256=sha(program.read(name)))
        report = dict(date='2026-10-31',source_url='http://jgbupdate02.shangyoo.com/update/jgb/update_list.txt',
                      manifest_sha256=sha(manifest),base_version=1205,final_version=version,
                      apk=apk_path.name,apk_sha256=sha(apk_path.read_bytes()),apk_client_version=client_version,
                      base_resource_count=len(initial),final_resource_count=len(current),
                      changed_resource_count=len(history),new_resource_count=len(set(current)-set(initial)),
                      final_changed_resource_count=sum(initial.get(k)!=v for k,v in current.items()),
                      returned_to_base=[k for k in history if k in initial and initial[k]==current[k]],
                      removed_resource_count=len(set(initial)-set(current)),packages=packages,
                      csv=csvs,lua=lua,other_resources=resources,history=dict(history),
                      workspace_payload_differences=relevant,
                      caveat='CSV mismatch is a review candidate, not by itself proof of missing functionality; alternate loaders and deliberate local rules require manual review.')
    (OUT/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    write_inventory(report)
    print(json.dumps({k:report[k] for k in ('changed_resource_count','new_resource_count','removed_resource_count')},ensure_ascii=False))
    print('CSV',len(csvs),'Lua',len(lua),'Other',len(resources),'Workspace/payload differences',len(relevant))
    for row in csvs:
        print(row['first_changed'],row['logical'],row['old_rows'],'->',row['new_rows'],
              'server='+str(row['workspace_rows']),'match='+str(row['workspace_equals_original']))
    print('LUA:',[(r['logical'],r['versions'],r['new_file']) for r in lua])


if __name__ == '__main__':
    main()
