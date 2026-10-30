"""Replace local v106 downloads only after staged package and save validation."""
import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v106_latest import WORK, EVIDENCE, ARCHIVE, NAME, FORMAL, BASE_HASH
from offline_android.pack_payload import collect_files
from network_redirect.summon import client_source, load_rules


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    read = lambda name: json.loads((EVIDENCE / name).read_text())
    build = read('build-validation.json')
    payload = read('payload-save-validation.json')
    protocol = read('protocol-validation.json')
    device = read('device-validation.json')
    ui = read('startup-ui-validation.json')
    sha = build['apk_sha256']
    assert sha == payload['apk_sha256'] == protocol['apk_sha256'] == device['apk_sha256'] == ui['apk_sha256']
    assert payload['all_existing_database_values_preserved']
    assert payload['all_database_tables_equal_after_restart']
    assert protocol['passed'] and protocol['tests'] >= 200 and protocol['actual_packaged_modules'] >= 50
    assert device['same_version_update'] and device['save_byte_identical_after_install_start_and_stop']
    assert device['new_program_ready']
    assert ui['cold_start_native_branding_verified'] and ui['no_external_ui_patch'] and ui['no_lua_error']
    assert ui['save_hash_after_ui'] == device['baseline']['sha256']
    log = (EVIDENCE / 'android-tests.log').read_text()
    assert 'Ran 5 tests' in log and '\nOK\n' in log
    for name, path in collect_files().items():
        if name != 'network_redirect/login.html':
            assert digest(path) == digest(WORK / 'payload-new' / name), 'Source changed: ' + name
    assert client_source(load_rules()) == (WORK / 'payload-new/offline_client.lua').read_text()
    assert digest(ARCHIVE / FORMAL) == BASE_HASH
    assert digest(ROOT / 'build' / FORMAL) == BASE_HASH
    assert digest(WORK / NAME) == sha
    notes = WORK / 'v106更新说明.txt'
    assert sha in notes.read_text() and '天命石' in notes.read_text()
    # Both established download names refer to the same verified official APK.
    shutil.copy2(WORK / NAME, WORK / FORMAL)
    for name in (NAME, FORMAL):
        (WORK / (name + '.sha256')).write_text(sha + '  ' + name + '\n')
    with zipfile.ZipFile(WORK / (FORMAL + '.zip'), 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.write(WORK / FORMAL, FORMAL)
    with zipfile.ZipFile(WORK / (FORMAL + '.zip')) as archive:
        assert archive.testzip() is None
        assert hashlib.sha256(archive.read(FORMAL)).hexdigest() == sha
    staged = [NAME.replace('.apk', '.manifest.json'), NAME + '.sha256', NAME + '.idsig',
              'v106更新说明.txt', FORMAL + '.sha256', FORMAL + '.zip', NAME, FORMAL]
    for name in staged:
        source = WORK / name
        target = ROOT / 'build' / name
        temporary = target.with_name(target.name + '.publishing')
        shutil.copy2(source, temporary)
        assert digest(temporary) == digest(source)
        temporary.replace(target)
    report = dict(published=True, apk_sha256=sha, apk_bytes=build['apk_bytes'],
                  downloads=[str(Path('build') / name) for name in (NAME, FORMAL, FORMAL + '.zip')],
                  previous_release_archive=str(ARCHIVE.relative_to(ROOT)),
                  packaged_protocol_tests=protocol['tests'], five_feature_groups_verified=True,
                  same_version_save_preservation_verified=True)
    (EVIDENCE / 'published-release.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
