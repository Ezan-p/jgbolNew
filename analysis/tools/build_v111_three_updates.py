"""Add only the three requested changes to the latest signed v111 release."""
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from build_channel360 import TOOLS, run
from build_offline import PACKAGE, SIGNING_KEY, signer_certificate
from offline_android.pack_payload import verify_payload

WORK = ROOT / '.runtime/v111-three-updates-20261110'
EVIDENCE = ROOT / 'analysis/evidence/v111-three-updates-20261110'
BASE = ROOT / 'build/金箍棒ol离线正式版v111.apk'
OUTPUT = WORK / BASE.name
ARCHIVE = ROOT / 'build/archive/v111-before-three-updates-20261110'
BASE_SHA = 'b97f7a8d234368f78be5d119e9aefd982794c86e14ad062059d349969fc0724f'
UPDATES = (
    'server_config/gift_code_rules.json',
    'network_redirect/abyss_client.lua',
    'network_redirect/activity_land.py',
    'network_redirect/activity_land_npc.py',
    'server_config/activity_rules.json',
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def report(name, data):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / (name + '.json')).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def build():
    assert not OUTPUT.exists(), 'Do not overwrite a candidate already under verification'
    assert digest(BASE.read_bytes()) == BASE_SHA
    WORK.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    backups = {}
    for path in sorted((ROOT / 'build').glob('*111*')):
        if not path.is_file() or '测试' in path.name:
            continue
        target = ARCHIVE / path.name
        if not target.exists():
            shutil.copy2(path, target)
        assert digest(target.read_bytes()) == digest(path.read_bytes())
        backups[path.name] = digest(path.read_bytes())
    report('original-release-backup', dict(directory=str(ARCHIVE.relative_to(ROOT)), files=backups))

    with zipfile.ZipFile(BASE) as apk:
        old_program = apk.read('assets/offline/program.zip')
        with zipfile.ZipFile(io.BytesIO(old_program)) as old:
            old.extractall(WORK / 'payload-old')
            old.extractall(WORK / 'source')
            replacements = {name: (ROOT / name).read_bytes() for name in UPDATES}
            for name, data in replacements.items():
                assert data != old.read(name), name
                (WORK / 'source' / name).write_bytes(data)
            before = json.loads(old.read('server_config/gift_code_rules.json'))
            after = json.loads(replacements['server_config/gift_code_rules.json'])
            assert len(before['codes']) == 80 and len(after['codes']) == 100
            assert after['codes'][:80] == before['codes']
            assert {k:v for k,v in before.items() if k not in ('codes','revision')} == {
                k:v for k,v in after.items() if k not in ('codes','revision')}
            activity_before = json.loads(old.read('server_config/activity_rules.json'))
            activity_after = json.loads(replacements['server_config/activity_rules.json'])
            assert activity_before.pop('land_guard_tier_by_type') == ['T1','T1','T2','T3']
            assert activity_after.pop('land_guard_tier_by_type') == ['T1','T1','T4','T5']
            assert activity_before == activity_after

            # Generate using only the frozen APK modules and the five explicit changes.
            code = ('import sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);'
                    'from network_redirect.summon import client_source,load_rules;'
                    'Path(sys.argv[2]).write_text(client_source(load_rules()))')
            subprocess.run([sys.executable, '-I', '-c', code, str(WORK / 'source'),
                            str(WORK / 'generated-client.lua')], check=True)
            replacements['offline_client.lua'] = (WORK / 'generated-client.lua').read_bytes()
            assert replacements['offline_client.lua'] != old.read('offline_client.lua')
            manifest = json.loads(old.read('payload-manifest.json'))
            for entry in manifest['files']:
                if entry['path'] in replacements:
                    data = replacements[entry['path']]
                    entry.update(size=len(data), sha256=digest(data))
            manifest['bundle_id'] = digest(json.dumps(manifest['files'], sort_keys=True,
                                                     separators=(',', ':')).encode())
            replacements['payload-manifest.json'] = (json.dumps(
                manifest, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()
            with zipfile.ZipFile(WORK / 'program.zip', 'w') as new:
                for entry in old.infolist():
                    new.writestr(entry, replacements.get(entry.filename, old.read(entry)))
        program = (WORK / 'program.zip').read_bytes()
        runtime_hash = digest(apk.read('assets/offline/runtime.zip'))
        outer_replacements = {
            'assets/offline/program.zip': program,
            'assets/offline/build.properties':
                f'program_sha256={digest(program)}\nruntime_sha256={runtime_hash}\nversion_code=111\n'.encode(),
        }
        with zipfile.ZipFile(WORK / 'unsigned.apk', 'w') as new:
            for entry in apk.infolist():
                if not entry.filename.startswith('META-INF/'):
                    new.writestr(entry, outer_replacements.get(entry.filename, apk.read(entry)))
    run(TOOLS / 'zipalign', '-f', '4', WORK / 'unsigned.apk', WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', SIGNING_KEY, '--ks-key-alias', 'channel360',
        '--ks-pass', 'pass:local-test-only', '--out', OUTPUT, WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'verify', '--verbose', OUTPUT)
    run(TOOLS / 'zipalign', '-c', '4', OUTPUT)
    assert signer_certificate(OUTPUT) == signer_certificate(BASE)
    badging = subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(OUTPUT)], text=True)
    assert f"package: name='{PACKAGE}' versionCode='111' versionName='3.87-offline.11'" in badging
    assert badging == subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(BASE)], text=True)
    (EVIDENCE / 'badging.txt').write_text(badging)
    with zipfile.ZipFile(OUTPUT) as apk, zipfile.ZipFile(BASE) as base, \
            zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as new, \
            zipfile.ZipFile(io.BytesIO(old_program)) as old:
        assert apk.testzip() is None and new.testzip() is None
        names = lambda z: {n for n in z.namelist() if not n.startswith('META-INF/')}
        assert names(apk) == names(base) and set(new.namelist()) == set(old.namelist())
        outer = sorted(n for n in names(apk) if apk.read(n) != base.read(n))
        assert set(outer) == set(outer_replacements)
        changed = sorted(n for n in new.namelist() if new.read(n) != old.read(n))
        assert set(changed) == set(replacements), changed
        assert not any(Path(n).suffix in ('.sqlite3','.db','.pyc') or 'save' in Path(n).parts
                       for n in new.namelist())
        new.extractall(WORK / 'payload-new')
    verify_payload(WORK / 'payload-old')
    verify_payload(WORK / 'payload-new')
    assert digest(BASE.read_bytes()) == BASE_SHA
    data = dict(apk_sha256=digest(OUTPUT.read_bytes()), apk_bytes=OUTPUT.stat().st_size,
        version_code=111, version_name='3.87-offline.11', home_version_label='v111', package=PACKAGE,
        baseline=str(BASE.relative_to(ROOT)), baseline_sha256=BASE_SHA,
        certificate_sha256=signer_certificate(OUTPUT), program_sha256=digest(program),
        runtime_sha256=runtime_hash, payload_bundle_id=manifest['bundle_id'],
        payload_files=len(manifest['files']), changed_apk_entries_from_v111=outer,
        changed_program_entries_from_v111=changed,
        source_hashes={n:digest(replacements[n]) for n in UPDATES}, contains_player_database=False,
        player_database='files/save/game.sqlite3', previous_80_gifts_unchanged=True,
        total_gift_codes=100, engine_client_runtime_native_java_preserved=True,
        feature_groups=3, release_revision='2026-11-10-three-updates-v111')
    report('build-validation', data)
    report('scope-validation', dict(apk_sha256=data['apk_sha256'], passed=True,
        changed_program_entries=changed, all_other_entries_byte_identical=True,
        previous_80_gifts_unchanged=True, only_land_guard_tiers_changed_in_activity_config=True))
    OUTPUT.with_suffix('.manifest.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    OUTPUT.with_suffix('.apk.sha256').write_text(data['apk_sha256']+'  '+OUTPUT.name+'\n')
    print(json.dumps({k:data[k] for k in ('apk_sha256','apk_bytes','changed_program_entries_from_v111')}, ensure_ascii=False))


if __name__ == '__main__':
    build()
