"""Publish the local v108 APK only after package, save, device and UI checks."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v108 import BASE, OUTPUT, WORK, EVIDENCE
from offline_android.pack_payload import collect_files
from network_redirect.summon import client_source, load_rules


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    read = lambda n: json.loads((EVIDENCE / n).read_text())
    build = read('build-validation.json')
    payload = read('payload-save-validation.json')
    protocol = read('protocol-validation.json')
    device = read('device-validation.json')
    ui = read('startup-ui-validation.json')
    lua = read('lua-validation.json')
    sha = digest(OUTPUT)
    assert all(r['apk_sha256'] == sha for r in [build, payload, protocol, device, ui, lua])
    assert build['version_code'] == 108 and build['home_version_label'] == 'v108'
    assert payload['only_documented_additive_migration']
    assert payload['all_database_tables_equal_after_restart']
    assert payload['all_existing_database_values_preserved'] and payload['source_qa_save_unchanged']
    assert protocol['passed'] and protocol['tests'] >= 400 and protocol['actual_packaged_modules'] >= 50
    assert device['replacement_install'] and device['version_code'] == 108
    assert device['save_byte_identical_after_install_start_and_stop'] and device['new_program_ready']
    assert ui['cold_start_native_branding_verified'] and ui['no_external_ui_patch'] and ui['no_lua_error']
    assert ui['save_hash_after_ui'] == device['baseline']['sha256']
    assert lua['checks']['bundle_compiles_and_home_version_is_v108']
    android = (EVIDENCE / 'android-tests.log').read_text()
    assert 'Ran 5 tests' in android and '\nOK\n' in android
    for name, path in collect_files().items():
        if name != 'network_redirect/login.html':
            assert digest(path) == digest(WORK / 'payload-new' / name), 'Source changed: ' + name
    assert client_source(load_rules()) == (WORK / 'payload-new/offline_client.lua').read_text()
    assert digest(BASE) == build['baseline_sha256']
    target = ROOT / 'build' / OUTPUT.name
    assert not target.exists(), 'Refusing to replace an existing release'
    shutil.copy2(OUTPUT, target)
    assert digest(target) == sha
    for suffix in ['.manifest.json', '.apk.sha256', '.apk.idsig']:
        source = OUTPUT.with_suffix(suffix)
        if source.exists():
            shutil.copy2(source, target.with_suffix(suffix))
    archive = target.with_suffix('.apk.zip')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(target, target.name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and hashlib.sha256(z.read(target.name)).hexdigest() == sha
    report = dict(published=True, apk_sha256=sha, apk_bytes=target.stat().st_size,
                  downloads=[str(p.relative_to(ROOT)) for p in (target, archive)],
                  version_code=108, packaged_protocol_tests=protocol['tests'],
                  baseline_preserved=True, save_preservation_verified=True, home_version_verified='v108')
    (EVIDENCE / 'published-release.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
