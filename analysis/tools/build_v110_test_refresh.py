"""Package the ten post-v111 changes with the existing v110 test identity."""
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v106_test import KEY, PACKAGE, PORT, certificate, digest
from build_channel360 import TOOLS, run
from offline_android.pack_payload import collect_files, verify_payload

BASE = ROOT / 'build/金箍棒ol离线正式版v111.apk'
BASE_SHA = '73db499548a76eb6250c412cf2e341b3808616a52dedd62f6598e5711bf659a9'
PREVIOUS = ROOT / 'build/金箍棒ol测试版-v110-九幽宝图500.apk'
PREVIOUS_SHA = '60f32beb89174951d6e61fea9a13c61cb36fccda31f05da443faa90a2f781799'
WORK = ROOT / '.runtime/v110-test-refresh-20261110'
EVIDENCE = ROOT / 'analysis/evidence/v110-test-refresh-20261110'
APK = WORK / '金箍棒ol测试版-v110-20261110整合更新.apk'


def report(name, value):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / (name + '.json')).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    assert not APK.exists(), 'Do not replace an existing candidate'
    assert digest(BASE.read_bytes()) == BASE_SHA
    assert digest(PREVIOUS.read_bytes()) == PREVIOUS_SHA
    assert KEY.is_file()
    WORK.mkdir(parents=True, exist_ok=True)
    sources = collect_files()
    source_hashes = {n: digest(p.read_bytes()) for n, p in sources.items()}
    # The previous test shell was built from these exact native/Java sources.
    shell_meta = json.loads((ROOT / 'analysis/evidence/v110_test/build-validation.json').read_text())
    assert digest((ROOT / 'offline_android/native/offline.c').read_bytes()) == shell_meta['native_source_sha256']
    for name, sha in shell_meta['java_source_sha256'].items():
        assert digest((ROOT / name).read_bytes()) == sha, name
    with zipfile.ZipFile(BASE) as formal, zipfile.ZipFile(PREVIOUS) as old:
        with zipfile.ZipFile(io.BytesIO(formal.read('assets/offline/program.zip'))) as z:
            original = {n: z.read(n) for n in z.namelist()}
        entries = dict(original)
        entries.update({n: p.read_bytes() for n, p in sources.items()})
        # Only these implemented changes are authorized beyond latest formal v111.
        allowed = set('''network_redirect/activity.py network_redirect/activity_arena.py
network_redirect/activity_hunt.py network_redirect/activity_nine_sky.py
network_redirect/activity_party.py network_redirect/activity_undergo.py
network_redirect/backend.py network_redirect/equipment_crafting.py network_redirect/gift_codes.py
network_redirect/item_rewards.py network_redirect/journey.py network_redirect/login.html
network_redirect/moon_client.lua network_redirect/rice_client.lua
network_redirect/seasonal_craft_client.lua network_redirect/summon.py
network_redirect/level_card.py network_redirect/level_card_client.lua
analysis/configs/local_items/item_base.csv analysis/configs/local_items/item_name.csv
server_config/activity_rules.json server_config/gift_code_rules.json server_config/guild_rules.json
server_config/hunt_rules.json server_config/item_reward_rules.json server_config/nine_sky_rules.json
server_config/party_rules.json server_config/taixu_rules.json'''.split())
        delta = {n for n in sources if entries[n] != original.get(n)}
        assert delta <= allowed, sorted(delta - allowed)
        from network_redirect.summon import client_source, load_rules
        def branding(data):
            result, count = re.subn(rb"label\('v\d+',0\.75\)", b"label('v110',0.75)", data)
            assert count == 1
            return result
        entries['offline_client.lua'] = branding(client_source(load_rules()).encode())
        entries['network_redirect/login_branding_client.lua'] = branding(entries['network_redirect/login_branding_client.lua'])
        with zipfile.ZipFile(io.BytesIO(old.read('assets/offline/program.zip'))) as previous:
            for name in ('offline_android/test_edition_seed.py', 'network_redirect/login.html'):
                entries[name] = previous.read(name)
        # Current adapters preserve the original supply receipts and use trusted time.
        for name in ('offline_android/test_edition_v108.py', 'offline_android/test_edition_v110.py'):
            entries[name] = (ROOT / name).read_bytes()
            source_hashes[name] = digest(entries[name])
        backend = entries['offline_android/backend.py']
        for before, after in [(b'PORT = 18770', b'PORT = 18776'),
                (b"self.files_dir / 'save'", b"self.files_dir / 'test-save-v106'"),
                (b'from network_redirect.accounts import Accounts',
                 b'from offline_android.test_edition_v110 import fixed_accounts_class\n        Accounts = fixed_accounts_class()')]:
            assert backend.count(before) == 1
            backend = backend.replace(before, after)
        entries['offline_android/backend.py'] = backend
        changed = sorted(n for n in entries if entries[n] != original.get(n) and n != 'payload-manifest.json')
        manifest = json.loads(entries['payload-manifest.json'])
        indexed = {r['path']: r for r in manifest['files']}
        for name in changed:
            indexed[name] = dict(path=name, size=len(entries[name]), sha256=digest(entries[name]), source='v110-test-refresh-20261110')
        manifest['files'] = sorted(indexed.values(), key=lambda r: r['path'])
        manifest['bundle_id'] = digest(json.dumps(manifest['files'], sort_keys=True, separators=(',', ':')).encode())
        manifest.update(player_database='files/test-save-v106/game.sqlite3', loopback_port=PORT)
        entries['payload-manifest.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as z:
            for name, data in entries.items():
                assert Path(name).suffix not in ('.db', '.sqlite3', '.pyc') and 'save' not in Path(name).parts
                z.writestr(name, data)
        program = buffer.getvalue()
        runtime_hash = digest(old.read('assets/offline/runtime.zip'))
        assert old.read('assets/offline/runtime.zip') == formal.read('assets/offline/runtime.zip')
        replacements = {'assets/offline/program.zip': program,
            'assets/offline/build.properties': f'program_sha256={digest(program)}\nruntime_sha256={runtime_hash}\nversion_code=110\n'.encode()}
        with zipfile.ZipFile(WORK / 'unsigned.apk', 'w') as z:
            for entry in old.infolist():
                if not entry.filename.startswith('META-INF/'):
                    z.writestr(entry, replacements.get(entry.filename, old.read(entry)))
    run(TOOLS / 'zipalign', '-f', '4', WORK / 'unsigned.apk', WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', KEY, '--ks-key-alias', 'test106',
        '--ks-pass', 'pass:test-edition-only', '--out', APK, WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'verify', '--verbose', APK)
    run(TOOLS / 'zipalign', '-c', '4', APK)
    assert certificate(APK) == certificate(PREVIOUS) != certificate(BASE)
    badging = subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(APK)], text=True)
    assert f"package: name='{PACKAGE}' versionCode='110' versionName='3.87-test.110.1'" in badging
    assert badging == subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(PREVIOUS)], text=True)
    with zipfile.ZipFile(APK) as z, zipfile.ZipFile(PREVIOUS) as old:
        names = lambda a: {n for n in a.namelist() if not n.startswith('META-INF/')}
        assert z.testzip() is None and names(z) == names(old)
        actual = sorted(n for n in names(z) if z.read(n) != old.read(n))
        assert actual == sorted(replacements)
        with zipfile.ZipFile(io.BytesIO(z.read('assets/offline/program.zip'))) as p:
            p.extractall(WORK / 'program')
    verify_payload(WORK / 'program')
    assert all(digest((ROOT / n).read_bytes()) == sha for n, sha in source_hashes.items())
    assert digest(BASE.read_bytes()) == BASE_SHA and digest(PREVIOUS.read_bytes()) == PREVIOUS_SHA
    data = dict(apk=APK.name, apk_sha256=digest(APK.read_bytes()), apk_bytes=APK.stat().st_size,
        baseline=BASE.name, baseline_sha256=BASE_SHA, previous_test=PREVIOUS.name, previous_test_sha256=PREVIOUS_SHA,
        package=PACKAGE, version_code=110, version_name='3.87-test.110.1', port=PORT,
        certificate_sha256=certificate(APK), program_sha256=digest(program), bundle_id=manifest['bundle_id'],
        player_database='files/test-save-v106/game.sqlite3', supply_revision=108,
        contains_player_database=False, test_shell_byte_identical=True, requested_updates=10,
        workspace_source_sha256=source_hashes, changed_program_entries=changed,
        changed_apk_entries=actual, source_changes_over_latest_v111=sorted(delta))
    report('build-validation', data)
    (EVIDENCE / 'badging.txt').write_text(badging)
    APK.with_suffix('.manifest.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    APK.with_suffix('.apk.sha256').write_text(data['apk_sha256'] + '  ' + APK.name + '\n')
    print(json.dumps({k: data[k] for k in ('apk', 'apk_sha256', 'apk_bytes')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
