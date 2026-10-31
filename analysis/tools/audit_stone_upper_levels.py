"""Audit current/historical local resources and reject unsupported refinement atomically."""
import csv
import hashlib
import io
import json
from pathlib import Path
import plistlib
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT/'analysis/tools'), str(ROOT/'tests')]
from audit_stone_level_mismatch import index
from test_equipment import EquipmentTests
from network_redirect import equipment

OUT = ROOT/'analysis/evidence/stone_upper_levels'
LOGICAL = 'csv_config/stone_reborn_cost_worth.csv'


def table_info(raw):
    rows = list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
    return dict(sha256=hashlib.sha256(raw).hexdigest(), rows=len(rows),
                levels_by_kind={kind:sorted(int(r['level']) for r in rows if int(r['stone_type'])==kind)
                                for kind in (1,2,3)})


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    historical = []
    for relative in ('.runtime/release_w', '.runtime/offline-toolchain/device-release_w', 'jgbol3.87/assets/release_'):
        root = ROOT/relative
        versions, tables, missing = [], {}, []
        for path in sorted(root.glob('index*.txt')):
            version, mapping = index(path.read_bytes())
            versions.append(version)
            physical = mapping.get(LOGICAL)
            if not physical:
                missing.append(dict(index=path.name, reason='no mapping'))
                continue
            resource = root/physical
            if not resource.is_file():
                # A historical index may reference a base resource instead.
                resource = ROOT/'jgbol3.87/assets/release_'/physical
            if not resource.is_file():
                missing.append(dict(index=path.name, physical=physical, reason='resource absent'))
                continue
            tables.setdefault(physical, dict(**table_info(resource.read_bytes()), indexes=[]))['indexes'].append(path.name)
        historical.append(dict(root=relative, index_count=len(versions), versions=sorted(set(versions)),
                               tables=tables, unresolved=missing))
    packages = []
    for name in ('金箍棒3.87离线正式版v106-神石修复.apk', '金箍棒ol测试版-v106-神石修复.apk'):
        path = ROOT/'build'/name
        with zipfile.ZipFile(path) as apk, zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as program:
            version, mapping = index(program.read('client/release_w/index.txt'))
            active = table_info(program.read('client/release_w/'+mapping[LOGICAL]))
            server = table_info(program.read('analysis/configs/stone/stone_reborn_cost_worth.csv'))
            assert active['levels_by_kind']==server['levels_by_kind']=={k:[11,12,13,14] for k in (1,2,3)}
            texts = {}
            for logical in ('v2/String.plist', 'v2/String2.plist'):
                physical = 'client/release_w/'+mapping[logical]
                raw = program.read(physical) if physical in program.namelist() else apk.read('assets/release_/'+mapping[logical])
                strings = plistlib.loads(raw)
                texts.update({k:v for k,v in strings.items() if k.startswith(('stone_tilianName','stone_ascName')) or k=='stoneCast4'})
            packages.append(dict(apk=name, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                                 overlay_version=version, active_table=active, server_table=server, strings=texts))
    cases = []
    for kind in (1,2,3):
        for level, mounted in ((14,False),(14,True),(15,False),(16,False),(20,False)):
            test=EquipmentTests()
            try:
                test.setUp()
                stone=test.add(1089+kind,level=level)
                test.add(1089+kind,level=level,count=5)
                if mounted:
                    gear=test.gear(kind,drill_count=1)
                    assert test.stone(2,gear,[stone],1)[-1][0]==83
                before=test.b.profile()
                event,data=test.stone(5,stone,pos=1 if mounted else 0)[-1]
                assert event==55 and data['op_string']=='灵石已达到提炼上限'
                assert before==test.b.profile()
                cases.append(dict(kind=kind,source_level=level,mounted=mounted,event=event,
                                  message=data['op_string'],save_unchanged=True))
            finally:
                test.doCleanups()
    report=dict(date='2026-10-31',scope='Local resources only; no claim about unavailable later official versions',
                historical_resources=historical,packages=packages,backend_max_level=equipment.STONE_MAX_LEVEL,
                protocol_cases=cases,player_saves_modified=False)
    (OUT/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    for entry in historical:
        print(entry['root'], 'indexes:',entry['index_count'],'unique tables:',len(entry['tables']),'unresolved:',len(entry['unresolved']))
    print('Two repaired APKs: max recipe level 14; 15 terminal/unsupported-level protocol cases passed.')


if __name__=='__main__':
    main()
