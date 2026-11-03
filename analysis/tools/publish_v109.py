"""Publish v109 locally after actual-payload, save, Lua and QA-device checks."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v109 import BASE, OUTPUT, WORK, EVIDENCE
from offline_android.pack_payload import collect_files
from network_redirect.summon import client_source, load_rules


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    read = lambda name: json.loads((EVIDENCE / name).read_text())
    build = read('build-validation.json')
    payload = read('payload-save-validation.json')
    protocol = read('protocol-validation.json')
    lua = read('lua-validation.json')
    device = read('device-validation.json')
    ui = read('startup-ui-validation.json')
    delta = read('v108-to-v109-delta.json')
    sha = digest(OUTPUT)
    assert all(r['apk_sha256'] == sha for r in (build, payload, protocol, lua, device, ui, delta))
    assert delta['current_sources_match'] and delta['client_assets_unchanged'] and delta['removed'] == 1
    assert build['version_code'] == 109 and build['home_version_label'] == 'v109'
    assert build['baseline_preserved'] and build['original_game_java_native_runtime_video_unchanged']
    assert payload['only_documented_migrations'] and payload['all_database_tables_equal_after_restart']
    assert payload['save_backend_unchanged'] and payload['source_qa_save_unchanged']
    assert protocol['passed'] and protocol['tests'] >= 1040 and protocol['actual_packaged_modules'] >= 100
    assert {'test_rank_rewards', 'test_activity_dream', 'test_activity_save_monkey',
            'test_upgrade_probability', 'test_combat_essence_matrix'} <= set(protocol['suites'])
    assert lua['passed'] and lua['checks']['bundle_compiles_home_v109_and_hidden_entries']
    assert device['replacement_install'] and device['version_code'] == 109
    assert device['save_byte_identical_after_install_start_and_stop'] and device['new_program_ready']
    assert ui['cold_start_native_branding_verified'] and ui['no_lua_error']
    assert ui['save_hash_after_ui'] == device['baseline']['sha256']
    assert 'Ran 5 tests' in (EVIDENCE / 'android-tests.log').read_text()
    assert '\nOK\n' in (EVIDENCE / 'android-tests.log').read_text()
    # Preserve the tested twelve-group snapshot while concurrent later work
    # remains in the workspace for the next release.
    deferred = {
        'network_redirect/activity_babel.py',
        'network_redirect/combat_power.py',
        'analysis/npc_design/rank_500/catalog.json',
        'analysis/npc_design/rank_500/profiles.json',
    }
    drift = []
    for name, path in collect_files().items():
        if name != 'network_redirect/login.html':
            packaged = WORK / 'payload-new' / name
            assert packaged.is_file(), name
            current_sha, packaged_sha = digest(path), digest(packaged)
            if current_sha != packaged_sha:
                assert name in deferred, 'Unexpected additional source change: '+name
                drift.append(dict(path=name, packaged_sha256=packaged_sha, workspace_sha256=current_sha))
    assert {row['path'] for row in drift} == deferred
    snapshot = dict(apk_sha256=sha, tested_snapshot_preserved=True,
                    scope='The twelve update groups requested before the build started',
                    deferred_changes='Later Babel daily shop refresh and Bagua/formation stat calculation with NPC power regeneration',
                    workspace_edits_preserved=True, files=drift)
    (EVIDENCE / 'frozen-snapshot.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2)+'\n')
    assert client_source(load_rules()) == (WORK / 'payload-new/offline_client.lua').read_text()
    assert digest(BASE) == build['baseline_sha256']
    target = ROOT / 'build' / OUTPUT.name
    assert not target.exists(), 'Refusing to overwrite a release'
    shutil.copy2(OUTPUT, target)
    assert digest(target) == sha
    for suffix in ('.manifest.json', '.apk.sha256', '.apk.idsig'):
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
                  version_code=109, packaged_protocol_tests=protocol['tests'],
                  baseline_preserved=True, save_preservation_verified=True, home_version_verified='v109',
                  frozen_scope_snapshot=True, deferred_workspace_files=sorted(deferred))
    (EVIDENCE / 'published-release.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
