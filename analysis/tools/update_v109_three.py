"""Apply nine-sky, essence and rank updates to v109 without rebuilding Android."""
import argparse
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
from build_offline import SIGNING_KEY, signer_certificate
from offline_android.pack_payload import collect_files, verify_payload

WORK = ROOT / '.runtime/v109-latest-three-20261104'
EVIDENCE = ROOT / 'analysis/evidence/v109/latest-three-20261104'
RELEASE = ROOT / 'build/金箍棒3.87离线正式版v109.apk'
ARCHIVE = ROOT / 'build/archive/v109-before-latest-three-20261104'
BASE = ARCHIVE / RELEASE.name
APK = WORK / RELEASE.name
BASE_SHA = 'b88ec04b1f196dfbd727de9ae8320817c34f7710f895401d214d9d37ed4b6059'
SOURCES = (
    'network_redirect/activity.py',
    'network_redirect/activity_nine_sky.py',
    'network_redirect/activity_rank.py',
    'network_redirect/battle_replay_client.lua',
    'network_redirect/combat.py',
    'network_redirect/combat_engine.py',
    'network_redirect/rank_client.lua',
    'server_config/nine_sky_rules.json',
    'server_config/rank_rules.json',
)
SUITES = [
    'test_activity_nine_sky', 'test_nine_sky_battle', 'test_activity_rank',
    'test_rank_rewards', 'test_rank_promotion_reset', 'test_activity', 'test_tian_shu',
    'test_combat', 'test_combat_engine', 'test_combat_essence_matrix',
    'test_combat_essence_integrity', 'test_combat_loadout', 'test_combat_termination',
    'test_combat_round_limit', 'test_combat_lanes', 'test_essence_visuals',
    'test_essence_hotupdate', 'test_battle_replay', 'test_formation',
    'test_offline_backend', 'test_npc_players',
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def report(name, data):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def prepare():
    assert not APK.exists(), 'Candidate already exists'
    assert digest(RELEASE.read_bytes()) == BASE_SHA, 'Release baseline changed'
    WORK.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for source in [*RELEASE.parent.glob(RELEASE.stem + '.*'), ROOT / 'build/v109更新说明.txt']:
        target = ARCHIVE / source.name
        if target.exists():
            assert target.read_bytes() == source.read_bytes(), target
        else:
            shutil.copy2(source, target)
    certificate = signer_certificate(BASE)
    replacements = {name: (ROOT / name).read_bytes() for name in SOURCES}
    from network_redirect.summon import client_source, load_rules
    replacements['offline_client.lua'] = client_source(load_rules()).encode('utf-8')
    with zipfile.ZipFile(BASE) as old:
        original = old.read('assets/offline/program.zip')
        buffer = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(original)) as before, zipfile.ZipFile(buffer, 'w') as after:
            manifest = json.loads(before.read('payload-manifest.json'))
            assert set(replacements) <= {row['path'] for row in manifest['files']}
            for row in manifest['files']:
                if row['path'] in replacements:
                    data = replacements[row['path']]
                    assert data != before.read(row['path']), row['path']
                    row.update(size=len(data), sha256=digest(data))
            manifest['bundle_id'] = digest(json.dumps(manifest['files'], sort_keys=True,
                                                      separators=(',', ':')).encode())
            replacements['payload-manifest.json'] = (json.dumps(manifest, ensure_ascii=False,
                                                                sort_keys=True, indent=2) + '\n').encode()
            for entry in before.infolist():
                after.writestr(entry, replacements.get(entry.filename, before.read(entry)))
        program = buffer.getvalue()
        properties = old.read('assets/offline/build.properties').decode()
        assert properties.count(digest(original)) == 1
        properties = properties.replace(digest(original), digest(program))
        outer = {'assets/offline/program.zip': program,
                 'assets/offline/build.properties': properties.encode()}
        with zipfile.ZipFile(WORK / 'unsigned.apk', 'w') as after:
            for entry in old.infolist():
                if not entry.filename.startswith('META-INF/'):
                    after.writestr(entry, outer.get(entry.filename, old.read(entry)))
    run(TOOLS / 'zipalign', '-f', '4', WORK / 'unsigned.apk', WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', SIGNING_KEY, '--ks-key-alias', 'channel360',
        '--ks-pass', 'pass:local-test-only', '--out', APK, WORK / 'aligned.apk')
    assert signer_certificate(APK) == certificate
    run(TOOLS / 'apksigner', 'verify', '--verbose', APK)
    run(TOOLS / 'zipalign', '-c', '4', APK)
    badging = lambda p: subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(p)])
    assert badging(BASE) == badging(APK)
    with zipfile.ZipFile(BASE) as old, zipfile.ZipFile(APK) as new:
        assert new.testzip() is None
        names = lambda z: {n for n in z.namelist() if not n.startswith('META-INF/')}
        assert names(old) == names(new)
        changed = sorted(n for n in names(old) if old.read(n) != new.read(n))
        assert changed == sorted(outer), changed
        with zipfile.ZipFile(io.BytesIO(original)) as before, \
                zipfile.ZipFile(io.BytesIO(new.read('assets/offline/program.zip'))) as after:
            assert after.testzip() is None
            assert set(before.namelist()) == set(after.namelist())
            changed_program = sorted(n for n in after.namelist() if before.read(n) != after.read(n))
            assert changed_program == sorted(replacements), changed_program
            assert not any(Path(n).suffix in ('.db', '.sqlite3', '.pyc') or
                           'save' in Path(n).parts for n in after.namelist())
            after.extractall(WORK / 'program')
    verify_payload(WORK / 'program')
    checked = 0
    for name, path in collect_files().items():
        if name != 'network_redirect/login.html':
            assert path.read_bytes() == (WORK / 'program' / name).read_bytes(), name
            checked += 1
    from network_redirect.summon import client_source, load_rules
    assert client_source(load_rules()) == (WORK / 'program/offline_client.lua').read_text()
    result = json.loads(BASE.with_suffix('.manifest.json').read_text())
    result.update(release_revision='v109-latest-three-20261104', feature_groups=19,
        baseline=str(BASE.relative_to(ROOT)), baseline_sha256=BASE_SHA,
        apk_sha256=digest(APK.read_bytes()), apk_bytes=APK.stat().st_size,
        program_sha256=digest(program), payload_bundle_id=manifest['bundle_id'],
        changed_apk_entries=changed, changed_program_entries=changed_program,
        same_version_update=True, android_manifest_unchanged=True,
        save_schema_and_path_unchanged=True, contains_player_database=False,
        workspace_files_checked=checked, previous_evidence='analysis/evidence/v109/latest-update',
        update_evidence=str(EVIDENCE.relative_to(ROOT)))
    APK.with_suffix('.manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    APK.with_suffix('.apk.sha256').write_text(result['apk_sha256'] + '  ' + APK.name + '\n')
    report('build-validation.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def verify():
    worker = r'''
import hashlib, json, pathlib, sys, unittest
program, root, destination, sha, suites = sys.argv[1:]
sys.path[:0] = [program, str(pathlib.Path(root)/'tests'), root]
suites = json.loads(suites)
def cases(node):
    if isinstance(node, unittest.TestSuite):
        for child in node:
            yield from cases(child)
    else:
        yield node
unique = {c.id().removeprefix('tests.'): c for c in cases(unittest.defaultTestLoader.loadTestsFromNames(suites))}
result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(unique.values()))
modules = []
for name, module in list(sys.modules.items()):
    if name.startswith('network_redirect.') and getattr(module, '__file__', None):
        assert pathlib.Path(module.__file__).resolve().is_relative_to(pathlib.Path(program).resolve()), name
        modules.append(name)
pathlib.Path(destination).write_text(json.dumps(dict(apk_sha256=sha, passed=result.wasSuccessful(),
    tests=result.testsRun, suites=suites, test_ids=list(unique), actual_packaged_modules=modules,
    failures=len(result.failures), errors=len(result.errors), skipped=len(result.skipped)), indent=2)+'\n')
raise SystemExit(not result.wasSuccessful())
'''
    with (EVIDENCE / 'protocol-tests.log').open('w') as log:
        subprocess.run([sys.executable, '-I', '-c', worker, str(WORK / 'program'), str(ROOT),
                        str(EVIDENCE / 'protocol-validation.json'), digest(APK.read_bytes()),
                        json.dumps(SUITES)], stdout=log, stderr=subprocess.STDOUT, check=True)
    print((EVIDENCE / 'protocol-tests.log').read_text()[-1000:])
    verify_lua()


def retry_tls():
    """Retry only localhost tests denied socket binding by the sandbox."""
    original = EVIDENCE / 'protocol-initial-validation.json'
    current = EVIDENCE / 'protocol-validation.json'
    if not original.exists():
        shutil.copy2(current, original)
    initial = json.loads(original.read_text())
    assert initial['apk_sha256'] == digest(APK.read_bytes())
    assert not initial['passed'] and initial['errors'] == 5 and initial['failures'] == 0
    log = (EVIDENCE / 'protocol-tests.log').read_text()
    assert log.count("error while attempting to bind on address ('127.0.0.1', 0): operation not permitted") == 5
    worker = r'''
import json, pathlib, sys, unittest
program, root, initial_path, destination = sys.argv[1:]
sys.path[:0] = [program, str(pathlib.Path(root)/'tests'), root]
initial = json.loads(pathlib.Path(initial_path).read_text())
suite = unittest.defaultTestLoader.loadTestsFromName('test_offline_backend.TLSAndWireTests')
ids = [case.id() for case in suite]
assert len(ids) == 5 and set(ids) <= set(initial['test_ids'])
result = unittest.TextTestRunner(verbosity=2).run(suite)
for name, module in list(sys.modules.items()):
    if name.startswith('network_redirect.') and getattr(module, '__file__', None):
        assert pathlib.Path(module.__file__).resolve().is_relative_to(pathlib.Path(program).resolve()), name
initial.update(passed=result.wasSuccessful(), errors=len(result.errors), failures=len(result.failures),
    initial_errors=5, initial_failure_reason='sandbox denied localhost socket binding',
    rechecked_tests=result.testsRun, rechecked_test_ids=ids, retry_log='tls-retry-tests.log')
pathlib.Path(destination).write_text(json.dumps(initial, indent=2)+'\n')
raise SystemExit(not result.wasSuccessful())
'''
    with (EVIDENCE / 'tls-retry-tests.log').open('w') as log:
        subprocess.run([sys.executable, '-I', '-c', worker, str(WORK / 'program'), str(ROOT),
                        str(original), str(current)], stdout=log, stderr=subprocess.STDOUT, check=True)
    print((EVIDENCE / 'tls-retry-tests.log').read_text())


def verify_lua():
    worker = r"""
import hashlib, json, pathlib, sys
program, root, destination, sha = sys.argv[1:]
program, root = pathlib.Path(program), pathlib.Path(root)
sys.path[:0] = [str(program), str(root), '/private/tmp/jgbol-rank-lua']
from lupa.lua51 import LuaRuntime
from network_redirect import activity_rank
assert pathlib.Path(activity_rank.__file__).resolve().is_relative_to(program.resolve())
checks = {}
for name, source in [
    ('battle_replay', (program/'network_redirect/battle_replay_client.lua').read_text()),
    ('rank_500', activity_rank.client_source()),
]:
    value = LuaRuntime().execute((root/f'tests/{name}_client_regression.lua').read_text(), source)
    checks[name] = list(value.values()) if hasattr(value, 'values') else value
source = (program/'network_redirect/nine_sky_client.lua').read_text()
harness = (root/'tests/nine_sky_client_regression.lua').read_text()
value = LuaRuntime().execute(harness.replace('-- INSTALL_PATCH', source).replace('-- INSTALL_AGAIN', source))
checks['nine_sky'] = list(value.values()) if hasattr(value, 'values') else value
bundle = (program/'offline_client.lua').read_text()
LuaRuntime().execute('assert(loadstring(...))', bundle)
checks['full_bundle_compiles'] = True
vm = LuaRuntime()
vm.execute('''
LABELS={}
local scene={getChildByTag=function() return nil end,addChild=function() end}
package.loaded['update.updateUI']={create=function() end,g_self={main_scene=scene}}
package.loaded['update.update_ms']={d_u={createByStyle=function(spec)
  LABELS[#LABELS+1]=spec.string;return {} end}}
CCLayer={create=function() return {setTouchEnabled=function() end,addChild=function() end} end}
CCDirector={sharedDirector=function() return {getRunningScene=function() return scene end} end}
''')
assert vm.execute(bundle) == 'pending'
assert list(vm.globals().LABELS.values()) == ['离线版·非商业·仅供学习', 'v109', '开发者@Ezan']
checks['prelogin_shows_v109'] = True
pathlib.Path(destination).write_text(json.dumps(dict(apk_sha256=sha, passed=True,
    checks=checks, native_cocos=False), ensure_ascii=False, indent=2)+'\n')
print(json.dumps(checks, ensure_ascii=False))
"""
    with (EVIDENCE / 'lua-tests.log').open('w') as log:
        subprocess.run([sys.executable, '-I', '-c', worker, str(WORK / 'program'), str(ROOT),
                        str(EVIDENCE / 'lua-validation.json'), digest(APK.read_bytes())],
                       stdout=log, stderr=subprocess.STDOUT, check=True)
    print((EVIDENCE / 'lua-tests.log').read_text())


def publish():
    sha = digest(APK.read_bytes())
    validation = json.loads((EVIDENCE / 'protocol-validation.json').read_text())
    assert validation['passed'] and validation['apk_sha256'] == sha and validation['tests'] > 200
    assert json.loads((EVIDENCE / 'build-validation.json').read_text())['apk_sha256'] == sha
    lua = json.loads((EVIDENCE / 'lua-validation.json').read_text())
    assert lua['passed'] and lua['apk_sha256'] == sha
    verify_payload(WORK / 'program')
    from network_redirect.summon import client_source, load_rules
    assert client_source(load_rules()).encode() == (WORK / 'program/offline_client.lua').read_bytes()
    assert digest(BASE.read_bytes()) == digest(RELEASE.read_bytes()) == BASE_SHA
    for name in SOURCES:
        assert (ROOT / name).read_bytes() == (WORK / 'program' / name).read_bytes(), name
    archive = RELEASE.with_suffix('.apk.zip')
    temporary = archive.with_name(archive.name + '.tmp')
    with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(APK, APK.name)
    with zipfile.ZipFile(temporary) as z:
        assert z.testzip() is None and digest(z.read(APK.name)) == sha
    for suffix in ('.apk', '.manifest.json', '.apk.sha256', '.apk.idsig'):
        source, target = APK.with_suffix(suffix), RELEASE.with_suffix(suffix)
        staged = target.with_name(target.name + '.tmp')
        shutil.copy2(source, staged)
        staged.replace(target)
    temporary.replace(archive)
    assert digest(RELEASE.read_bytes()) == sha
    report('published-release.json', dict(published=True, apk_sha256=sha, version_code=109,
        same_version_update=True, protocol_tests=validation['tests'],
        baseline_preserved=str(BASE.relative_to(ROOT)), device_test_performed=False,
        downloads=[str(RELEASE.relative_to(ROOT)), str(archive.relative_to(ROOT))]))
    print(RELEASE)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['prepare', 'verify', 'retry_tls', 'publish'])
    globals()[parser.parse_args().stage]()
