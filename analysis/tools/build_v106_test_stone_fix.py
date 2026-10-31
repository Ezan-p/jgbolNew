"""Apply only the stone repair to the independent test edition; retain its save/seed."""
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v106_test import certificate, digest, KEY, PACKAGE
from analysis.tools.build_v106 import badging
from build_channel360 import TOOLS, run
from offline_android.pack_payload import verify_payload

BASE = ROOT / 'build/金箍棒ol测试版-v106.apk'
APK = ROOT / 'build/金箍棒ol测试版-v106-神石修复.apk'
WORK = ROOT / '.runtime/v106-test-stone-fix'
EVIDENCE = ROOT / 'analysis/evidence/stone_refine_fix/test_edition'


def main():
    baseline_hash = digest(BASE.read_bytes())
    assert baseline_hash == '07fd7ed429333501167921ea5279d0f6db95aacb40f856292d2e209007a320c6'
    assert not APK.exists() and KEY.is_file()
    WORK.mkdir(parents=True, exist_ok=True); EVIDENCE.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(BASE) as base:
        with zipfile.ZipFile(io.BytesIO(base.read('assets/offline/program.zip'))) as old:
            entries = {n: old.read(n) for n in old.namelist()}
        original = dict(entries)
        adapter = entries['network_redirect/equipment_client.lua']
        updated = (ROOT/'network_redirect/equipment_client.lua').read_bytes()
        assert entries['offline_client.lua'].count(adapter) == 1
        entries['offline_client.lua'] = entries['offline_client.lua'].replace(adapter, updated)
        for name in ('network_redirect/equipment.py', 'network_redirect/equipment_client.lua',
                     'analysis/configs/stone/stone_reborn_cost_worth.csv'):
            entries[name] = (ROOT/name).read_bytes()
        manifest = json.loads(entries['payload-manifest.json'])
        indexed = {row['path']: row for row in manifest['files']}
        changed = sorted(n for n in entries if entries[n] != original.get(n))
        for name in changed:
            data = entries[name]
            indexed[name] = dict(path=name, size=len(data), sha256=digest(data), source='stone-refinement-fix')
        manifest['files'] = sorted(indexed.values(), key=lambda row: row['path'])
        manifest['bundle_id'] = digest(json.dumps(manifest['files'], sort_keys=True, separators=(',', ':')).encode())
        entries['payload-manifest.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode()
        with zipfile.ZipFile(WORK/'program.zip', 'w', zipfile.ZIP_DEFLATED) as program:
            for name, data in entries.items():
                program.writestr(name, data)
                path = WORK/'program'/name
                path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
        verify_payload(WORK/'program')
        program_hash = digest((WORK/'program.zip').read_bytes())
        runtime_hash = digest(base.read('assets/offline/runtime.zip'))
        replacements = {'assets/offline/program.zip': (WORK/'program.zip').read_bytes(),
            'assets/offline/build.properties': f'program_sha256={program_hash}\nruntime_sha256={runtime_hash}\nversion_code=106\n'.encode()}
        with zipfile.ZipFile(WORK/'unsigned.apk', 'w') as out:
            for entry in base.infolist():
                if not entry.filename.startswith('META-INF/'):
                    out.writestr(entry, replacements.get(entry.filename, base.read(entry)))
    run(TOOLS/'zipalign', '-f', '4', WORK/'unsigned.apk', WORK/'aligned.apk')
    run(TOOLS/'apksigner', 'sign', '--ks', KEY, '--ks-key-alias', 'test106',
        '--ks-pass', 'pass:test-edition-only', '--out', APK, WORK/'aligned.apk')
    assert certificate(APK) == certificate(BASE)
    assert badging(APK) == badging(BASE)
    run(TOOLS/'apksigner', 'verify', '--verbose', APK)
    run(TOOLS/'zipalign', '-c', '4', APK)
    with zipfile.ZipFile(BASE) as base, zipfile.ZipFile(APK) as out:
        assert out.testzip() is None
        names = lambda z: {n for n in z.namelist() if not n.startswith('META-INF/')}
        assert names(base) == names(out)
        changed_apk = sorted(n for n in names(base) if base.read(n) != out.read(n))
        assert set(changed_apk) == set(replacements)
    assert digest(BASE.read_bytes()) == baseline_hash
    report = dict(apk=APK.name, apk_sha256=digest(APK.read_bytes()), apk_bytes=APK.stat().st_size,
        baseline_sha256=baseline_hash, package=PACKAGE, version_code=106, version_name='3.87-test.106.1',
        certificate_sha256=certificate(APK), program_sha256=program_hash,
        changed_apk_entries=changed_apk, changed_program_entries=changed+['payload-manifest.json'],
        player_database='files/test-save-v106/game.sqlite3', existing_test_seed_and_backend_unchanged=True,
        same_version_update=True, contains_player_database=False)
    text = json.dumps(report, ensure_ascii=False, indent=2)+'\n'
    (EVIDENCE/'build-validation.json').write_text(text)
    APK.with_suffix('.manifest.json').write_text(text)
    APK.with_suffix('.apk.sha256').write_text(report['apk_sha256']+'  '+APK.name+'\n')
    print(text)


if __name__ == '__main__':
    main()
