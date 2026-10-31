"""Read shipped overlays and reproduce the stone level rejection in temporary saves."""
import ast
import base64
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'tests'), str(ROOT / 'analysis/tools')]
from luajit_static import parse, listing
from test_equipment import EquipmentTests
from network_redirect import equipment

OUT = ROOT / 'analysis/evidence/stone_level_mismatch'
ALPHABET = 'yfglmnovwxapzdechijkqrstbuHOMICDJPQRSTUVWXYZABKEFGLN39+0126-4785'


def index(raw):
    version, encoded = raw.decode().split('\n', 1)
    decoded = base64.b64decode(encoded.translate(str.maketrans(
        ALPHABET + '_', 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='))).decode('gb18030')
    return version, dict(line.split('====')[:2] for line in decoded.splitlines())


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    if (1, 13) in equipment.STONE_REBORN:
        raise SystemExit('Historical failure audit requires the pre-fix backend. Use verify_v106_stone_fix.py for the repaired build; preserved evidence was not changed.')
    OUT.mkdir(parents=True, exist_ok=True)
    packages = []
    for filename in ('金箍棒3.87离线正式版v106.apk', '金箍棒ol测试版-v106.apk'):
        path = ROOT / 'build' / filename
        with zipfile.ZipFile(path) as apk, zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as program:
            prefix = 'client/release_w/'
            version, mapping = index(program.read(prefix + 'index.txt'))
            files = []
            for logical in ('csv_config/stone_reborn_cost_worth.csv', 'csv_config/stone_cost_worth.csv',
                            'lua/ui/stoneCastUI.lua', 'lua/ui/stoneUI.lua', 'lua/data.lua'):
                physical = mapping[logical]
                raw = program.read(prefix + physical)
                files.append(dict(logical=logical, physical=physical, sha256=sha(raw)))
                name = Path(logical).name
                if name.endswith('.csv'):
                    output = raw.decode('utf-8-sig')
                else:
                    chunk = parse(raw)
                    output = '\n'.join('NUMERIC proto%d %r' % (p['id'], p['numbers']) for p in chunk['protos']) + '\n' + listing(chunk)
                    name += '.txt'
                dest = OUT / name
                if packages:
                    assert dest.read_text() == output.replace('\r\n', '\n'), logical
                else:
                    dest.write_text(output)
            matches = {}
            for relative in ('network_redirect/equipment.py', 'network_redirect/summon.py',
                             'analysis/configs/stone_reborn_cost_worth.csv', 'server_config/stone_rules.json'):
                matches[relative] = program.read(relative) == (ROOT / relative).read_bytes()
                if relative == 'network_redirect/summon.py':
                    def rows_function(source):
                        return ast.dump(next(n for n in ast.parse(source).body
                                             if isinstance(n, ast.FunctionDef) and n.name == 'rows'))
                    matches['summon.rows_function_matches'] = rows_function(program.read(relative)) == rows_function((ROOT / relative).read_bytes())
                else:
                    assert matches[relative], (filename, relative)
            packages.append(dict(apk=filename, sha256=sha(path.read_bytes()), overlay_version=version,
                                 overlay_files=files, backend_matches_workspace=matches))

    cases = []
    for kind in (1, 2, 3):
        for level in (10, 11, 12, 13):
            test = EquipmentTests()
            try:
                test.setUp()
                target = test.add(1089 + kind, level=level)
                test.add(1089 + kind, level=level)
                test.add(1089 + kind, level=level)
                before = test.b.profile()
                events = test.stone(5, target)
                after = test.b.profile()
                event, data = events[-1]
                if level < 12:
                    assert event == 83 and data['result'] == 1, events
                    assert test.get(target)['level'] == level + 1
                else:
                    assert event == 55 and '灵石升华或提炼等级无效' in str(data), events
                    assert before == after
                cases.append(dict(kind=kind, current_level=level, request=dict(flag=5, src_count=0,
                    src_list=[], stone_pos=0, equip_order=0), event=event, data=data,
                    target_level_after=test.get(target)['level'], save_unchanged=before == after))
            finally:
                test.doCleanups()

    active = list(csv.DictReader((OUT / 'stone_reborn_cost_worth.csv').open(newline='')))
    missing = [r for r in active if (int(r['stone_type']), int(r['level'])) not in equipment.STONE_REBORN]
    rate_errors = []
    for kind in (1, 2, 3):
        for level in (13, 14):
            try:
                equipment.stone_rate(kind, level)
            except KeyError as error:
                rate_errors.append(dict(kind=kind, level=level, error=repr(error)))
    report = dict(date='2026-10-31', scope='Local APK bytes and disposable database binary protocol requests',
                  device_ui_test_performed=False, player_save_modified=False, packages=packages,
                  missing_backend_rows=missing, protocol_cases=cases, missing_attribute_rates=rate_errors)
    (OUT / 'audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('Verified two APK overlays; 12 protocol cases passed; six missing recipe rows and six missing attribute coefficients confirmed.')


if __name__ == '__main__':
    main()
