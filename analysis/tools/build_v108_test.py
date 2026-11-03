"""Package exact official v108 gameplay with the existing isolated test identity."""
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v106_test import certificate, digest, KEY, PACKAGE, PORT
from build_channel360 import TOOLS, apktool, run
from offline_android.pack_payload import verify_payload

BASE = ROOT / 'build/金箍棒3.87离线正式版v108.apk'
PREVIOUS = ROOT / 'build/金箍棒ol测试版-v106.apk'
APK = ROOT / 'build/金箍棒ol测试版-v108.apk'
WORK = ROOT / '.runtime/v108-test'
EVIDENCE = ROOT / 'analysis/evidence/v108_test'
VERSION_NAME = '3.87-test.108.1'


def main():
    assert not APK.exists(), 'Refusing to overwrite the published test APK'
    assert KEY.is_file(), 'Existing test signing key required'
    base_hash, old_hash = digest(BASE.read_bytes()), digest(PREVIOUS.read_bytes())
    assert base_hash == 'c3005ec187e15c9c5b7e963b1976211c4fe65bdcb9cd873dbab65dfced179350'
    assert old_hash == '07fd7ed429333501167921ea5279d0f6db95aacb40f856292d2e209007a320c6'
    WORK.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    from analysis.tools import build_v106_test as adapter
    adapter.BASE, adapter.WORK = BASE, WORK
    adapter.native_adapter()
    with zipfile.ZipFile(BASE) as base, zipfile.ZipFile(PREVIOUS) as old:
        with zipfile.ZipFile(io.BytesIO(base.read('assets/offline/program.zip'))) as p:
            entries = {n: p.read(n) for n in p.namelist()}
        original = dict(entries)
        with zipfile.ZipFile(io.BytesIO(old.read('assets/offline/program.zip'))) as p:
            legacy = p.read('offline_android/test_edition_seed.py').decode()
            # Freeze the original starter's 299-ascension allowance under v108.
            assert legacy.count('sum(f.EVOLVE_COST[n] for q, n in f.EVOLVE_POINTS if q == 5)') == 1
            legacy = legacy.replace('sum(f.EVOLVE_COST[n] for q, n in f.EVOLVE_POINTS if q == 5)',
                                    'sum(f.EVOLVE_COST[n] for n in range(1, 300))')
            entries['offline_android/test_edition_seed.py'] = legacy.encode()
            entries['network_redirect/login.html'] = p.read('network_redirect/login.html')
        entries['offline_android/test_edition_v108.py'] = (ROOT / 'offline_android/test_edition_v108.py').read_bytes()
        backend = entries['offline_android/backend.py'].decode()
        for old_text, new_text in [('PORT = 18770', f'PORT = {PORT}'),
                ("self.files_dir / 'save'", "self.files_dir / 'test-save-v106'"),
                ('from network_redirect.accounts import Accounts',
                 'from offline_android.test_edition_v108 import fixed_accounts_class\n        Accounts = fixed_accounts_class()')]:
            assert backend.count(old_text) == 1
            backend = backend.replace(old_text, new_text)
        entries['offline_android/backend.py'] = backend.encode()
        changed = sorted(n for n in entries if entries[n] != original.get(n))
        assert set(changed) == {'offline_android/backend.py', 'offline_android/test_edition_seed.py',
                               'offline_android/test_edition_v108.py', 'network_redirect/login.html'}
        manifest = json.loads(entries['payload-manifest.json'])
        indexed = {r['path']: r for r in manifest['files']}
        for name in changed:
            data = entries[name]
            indexed[name] = dict(path=name, size=len(data), sha256=digest(data), source='v108-isolated-test')
        manifest['files'] = sorted(indexed.values(), key=lambda r: r['path'])
        manifest['bundle_id'] = digest(json.dumps(manifest['files'], sort_keys=True, separators=(',', ':')).encode())
        manifest.update(player_database='files/test-save-v106/game.sqlite3', loopback_port=PORT)
        entries['payload-manifest.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
        with zipfile.ZipFile(WORK / 'program.zip', 'w', zipfile.ZIP_DEFLATED) as p:
            for name, data in entries.items():
                assert Path(name).suffix not in ('.db', '.sqlite3', '.pyc')
                p.writestr(name, data)
                path = WORK / 'program' / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
        verify_payload(WORK / 'program')
        decoded, framework = WORK / 'decoded', ROOT / '.runtime/tools/apktool-framework'
        apktool('d', '-f', '-s', '-p', framework, '-o', decoded, PREVIOUS)
        meta = decoded / 'apktool.yml'
        content = meta.read_text()
        for key, value in [('versionCode', '108'), ('versionName', VERSION_NAME)]:
            content, count = re.subn(r'(?m)^  ' + key + r':.*$', '  ' + key + ': ' + value, content)
            assert count == 1
        meta.write_text(content)
        apktool('b', '-p', framework, '-o', WORK / 'shell.apk', decoded)
        with zipfile.ZipFile(WORK / 'shell.apk') as shell:
            replacements = {'AndroidManifest.xml': shell.read('AndroidManifest.xml')}
        # Reuse the isolated Java shell; compile the exact v108 native adapter with the test port.
        for name in ('resources.arsc', 'classes.dex', 'classes2.dex'):
            replacements[name] = old.read(name)
        replacements['lib/armeabi-v7a/liboffline.so'] = (WORK / 'liboffline.so').read_bytes()
        runtime_hash = digest(base.read('assets/offline/runtime.zip'))
        assert old.read('assets/offline/runtime.zip') == base.read('assets/offline/runtime.zip')
        program_hash = digest((WORK / 'program.zip').read_bytes())
        replacements.update({'assets/offline/program.zip': (WORK / 'program.zip').read_bytes(),
            'assets/offline/build.properties': f'program_sha256={program_hash}\nruntime_sha256={runtime_hash}\nversion_code=108\n'.encode()})
        with zipfile.ZipFile(WORK / 'unsigned.apk', 'w') as out:
            for entry in base.infolist():
                if not entry.filename.startswith('META-INF/'):
                    out.writestr(entry, replacements.get(entry.filename, base.read(entry)))
    run(TOOLS / 'zipalign', '-f', '4', WORK / 'unsigned.apk', WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', KEY, '--ks-key-alias', 'test106',
        '--ks-pass', 'pass:test-edition-only', '--out', APK, WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'verify', '--verbose', APK)
    run(TOOLS / 'zipalign', '-c', '4', APK)
    assert certificate(APK) == certificate(PREVIOUS) != certificate(BASE)
    badging = subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(APK)], text=True)
    assert f"package: name='{PACKAGE}' versionCode='108' versionName='{VERSION_NAME}'" in badging
    assert "application-label:'金箍棒ol测试版'" in badging
    assert 'android.permission.WRITE_EXTERNAL_STORAGE' not in badging
    with zipfile.ZipFile(BASE) as base, zipfile.ZipFile(APK) as result:
        assert result.testzip() is None
        changed_apk = sorted(n for n in base.namelist() if not n.startswith('META-INF/') and base.read(n) != result.read(n))
        assert set(changed_apk) == set(replacements)
    assert digest(BASE.read_bytes()) == base_hash and digest(PREVIOUS.read_bytes()) == old_hash
    report = dict(apk=APK.name, apk_sha256=digest(APK.read_bytes()), apk_bytes=APK.stat().st_size,
        baseline=BASE.name, baseline_sha256=base_hash, previous_test_sha256=old_hash,
        package=PACKAGE, version_code=108, version_name=VERSION_NAME, port=PORT,
        certificate_sha256=certificate(APK), program_sha256=program_hash,
        player_database=f'/data/user/0/{PACKAGE}/files/test-save-v106/game.sqlite3',
        fixed_account='v106_fixed_test', initialize_only_once=True, supply_revision=108,
        existing_progress_preserved=True, contains_player_database=False, baselines_preserved=True, native_adapter_matches_v108_except_port=True,
        changed_apk_entries=changed_apk, changed_program_entries=changed + ['payload-manifest.json'])
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    APK.with_suffix('.manifest.json').write_text(rendered)
    APK.with_suffix('.apk.sha256').write_text(report['apk_sha256'] + '  ' + APK.name + '\n')
    (EVIDENCE / 'build-validation.json').write_text(rendered)
    (EVIDENCE / 'badging.txt').write_text(badging)
    print(rendered)


if __name__ == '__main__':
    main()
