"""Publish the verified v110 APK and distribution files without replacing v109."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v110 import BASE, OUTPUT, WORK, EVIDENCE
from offline_android.pack_payload import collect_files


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    reports = {name: json.loads((EVIDENCE / (name + '.json')).read_text()) for name in (
        'build-validation', 'payload-save-validation', 'protocol-validation',
        'lua-validation', 'device-validation', 'startup-ui-validation')}
    sha = digest(OUTPUT)
    assert all(r['apk_sha256'] == sha for r in reports.values())
    build, payload = reports['build-validation'], reports['payload-save-validation']
    protocol, lua = reports['protocol-validation'], reports['lua-validation']
    device, ui = reports['device-validation'], reports['startup-ui-validation']
    assert build['version_code'] == 110 and build['home_version_label'] == 'v110'
    assert build['offline_java_bridge_updated'] and build['baseline_preserved']
    assert payload['existing_role_values_preserved'] and payload['legacy_roles_unblocked']
    assert payload['all_tables_equal_after_restart'] and payload['source_qa_save_unchanged']
    assert protocol['passed'] and protocol['tests'] >= 2100 and protocol['skipped'] == 0
    assert protocol['excluded_test_ids'] == ['test_activity_babel.BabelTests.test_late_floors_full_wire_loot_budget_and_terminal_once']
    delta = json.loads((EVIDENCE / 'final-candidate-delta.json').read_text())
    assert delta['apk_sha256'] == sha and delta['tested_apk_sha256'] == protocol['tested_apk_sha256']
    assert delta['all_protocol_modules_and_resources_byte_identical']
    assert {'test_game_clock', 'test_time_guard', 'test_activity_clock_boundaries',
            'test_request_wait', 'test_request_recovery', 'test_activity_performance',
            'test_activity_nine_sky', 'test_babel_hotupdate'} <= set(protocol['suites'])
    assert lua['passed'] and lua['checks']['bundle_compiles_home_v110_and_hidden_entries']
    assert device['replacement_install'] and device['version_code'] == 110
    assert device['save_byte_identical_after_install'] and device['all_existing_tables_preserved_after_start']
    assert device['boot_identity_bridge_verified'] and device['new_program_ready']
    assert ui['cold_start_native_branding_verified'] and ui['no_lua_error']
    assert ui['save_hash_after_ui'] == device['after_stop']['sha256']
    assert '\nOK\n' in (EVIDENCE / 'host-android-tests.log').read_text()
    for name, path in collect_files().items():
        if name != 'network_redirect/login.html':
            assert digest(path) == digest(WORK / 'payload-new' / name), name
    for name, expected in build['java_source_sha256'].items():
        assert digest(ROOT / name) == expected, name
    from network_redirect.summon import client_source, load_rules
    assert client_source(load_rules()) == (WORK / 'payload-new/offline_client.lua').read_text()
    assert digest(BASE) == build['baseline_sha256']
    target = ROOT / 'build' / OUTPUT.name
    assert not target.exists(), 'Refusing to replace an existing release'
    shutil.copy2(OUTPUT, target)
    assert digest(target) == sha
    for suffix in ('.manifest.json', '.apk.sha256', '.apk.idsig'):
        source = OUTPUT.with_suffix(suffix)
        if source.exists():
            shutil.copy2(source, target.with_suffix(suffix))
    archive = target.with_suffix('.apk.zip')
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as z:
        z.write(target, target.name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and hashlib.sha256(z.read(target.name)).hexdigest() == sha
    report = dict(published=True, apk_sha256=sha, apk_bytes=target.stat().st_size,
        downloads=[str(p.relative_to(ROOT)) for p in (target, archive)],
        version_code=110, version_name=build['version_name'],
        packaged_protocol_tests=protocol['tests'], baseline_preserved=True,
        current_sources_match=True, save_migration_verified=True,
        qa_replacement_install=True, home_version_verified='v110', physical_device_test=False)
    (EVIDENCE / 'published-release.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
