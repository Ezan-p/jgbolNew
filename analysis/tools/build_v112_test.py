"""Freeze current gameplay and retain the published test shell/save identity."""
import copy
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v106_test import KEY, PACKAGE, PORT, certificate, digest
from build_channel360 import TOOLS, apktool, run
from offline_android.pack_payload import collect_files, verify_payload

BASE = ROOT / 'build/金箍棒ol测试版-v111.apk'
BASE_SHA = '62f6ebd70c6c6d3fb49ae2b065711bfbd3432dc91e2a124942015f6c759a2513'
FORMAL = ROOT / 'build/金箍棒ol离线正式版v112.apk'
WORK = ROOT / '.runtime/v112-test-20261113'
EVIDENCE = ROOT / 'analysis/evidence/v112-test-20261113'
OUTPUT = WORK / '金箍棒ol测试版-v112.apk'
VERSION_NAME = '3.87-test.112.1'


def report(name, value):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / (name + '.json')).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def build():
    assert not OUTPUT.exists(), 'Do not overwrite a built candidate'
    assert digest(BASE.read_bytes()) == BASE_SHA and KEY.is_file()
    formal_sha = digest(FORMAL.read_bytes())
    WORK.mkdir(parents=True, exist_ok=True)
    sources = collect_files(ROOT)
    hashes = {}
    for name, source in sources.items():
        target = WORK / 'source' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        data = source.read_bytes()
        hashes[name] = digest(data)
        target.write_bytes(data)
    report('source-snapshot', dict(source_hashes=hashes))
    subprocess.run([sys.executable, '-I', '-c',
        'import sys;sys.path.insert(0,sys.argv[1]);'
        'from offline_android.pack_payload import build_payload;'
        'build_payload(sys.argv[3],root=sys.argv[2])',
        str(ROOT), str(WORK / 'source'), str(WORK / 'backend.zip')], check=True)
    with zipfile.ZipFile(BASE) as base, zipfile.ZipFile(FORMAL) as formal, \
            zipfile.ZipFile(io.BytesIO(base.read('assets/offline/program.zip'))) as old, \
            zipfile.ZipFile(WORK / 'backend.zip') as backend:
        old.extractall(WORK / 'payload-old')
        entries = {n: backend.read(n) for n in backend.namelist()}
        entries.update({n: old.read(n) for n in old.namelist() if n.startswith('client/')})
        assert base.read('assets/offline/runtime.zip') == formal.read('assets/offline/runtime.zip')
        runtime_hash = digest(base.read('assets/offline/runtime.zip'))
        for name in ('offline_android/test_edition_seed.py', 'offline_android/test_edition_v108.py',
                     'offline_android/test_edition_v110.py', 'network_redirect/login.html'):
            entries[name] = old.read(name)
        name = 'offline_android/test_edition_v112.py'
        entries[name] = (ROOT / name).read_bytes()
        hashes[name] = digest(entries[name])
        backend_source = entries['offline_android/backend.py']
        for before, after in [(b'PORT = 18770', b'PORT = 18776'),
                (b"self.files_dir / 'save'", b"self.files_dir / 'test-save-v106'"),
                (b'from network_redirect.accounts import Accounts',
                 b'from offline_android.test_edition_v112 import fixed_accounts_class\n        Accounts = fixed_accounts_class()')]:
            assert backend_source.count(before) == 1
            backend_source = backend_source.replace(before, after)
        entries['offline_android/backend.py'] = backend_source
        for name in ('offline_client.lua', 'network_redirect/login_branding_client.lua'):
            assert entries[name].count(b"label('v112',0.75)") == 1
        manifest = json.loads(entries['payload-manifest.json'])
        manifest['files'] = [dict(path=n, size=len(data), sha256=digest(data), source='v112-test')
                             for n, data in sorted(entries.items()) if n != 'payload-manifest.json'
                             and not n.startswith('client/')]
        manifest['bundle_id'] = digest(json.dumps(manifest['files'], sort_keys=True, separators=(',', ':')).encode())
        manifest.update(player_database='files/test-save-v106/game.sqlite3', loopback_port=PORT)
        entries['payload-manifest.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
        with zipfile.ZipFile(WORK / 'program.zip', 'w', zipfile.ZIP_DEFLATED) as payload:
            for name, data in entries.items():
                assert Path(name).suffix not in ('.db', '.sqlite3', '.pyc') and 'save' not in Path(name).parts
                payload.writestr(name, data)
        delta = sorted(n for n in set(entries) | set(old.namelist())
                       if n not in entries or n not in old.namelist() or entries[n] != old.read(n))
    decoded = WORK / 'decoded'
    framework = ROOT / '.runtime/tools/apktool-framework'
    apktool('d', '-f', '-s', '-p', framework, '-o', decoded, BASE)
    metadata = decoded / 'apktool.yml'
    content = metadata.read_text()
    for name, value in [('versionCode', '112'), ('versionName', VERSION_NAME)]:
        content, count = re.subn(r'(?m)^  ' + name + r':.*$', '  ' + name + ': ' + value, content)
        assert count == 1
    metadata.write_text(content)
    apktool('b', '-p', framework, '-o', WORK / 'shell.apk', decoded)
    program = (WORK / 'program.zip').read_bytes()
    with zipfile.ZipFile(WORK / 'shell.apk') as shell:
        replacements = {'AndroidManifest.xml': shell.read('AndroidManifest.xml'),
            'assets/offline/program.zip': program,
            'assets/offline/build.properties':
                f'program_sha256={digest(program)}\nruntime_sha256={runtime_hash}\nversion_code=112\n'.encode()}
    with zipfile.ZipFile(BASE) as base, zipfile.ZipFile(WORK / 'unsigned.apk', 'w') as out:
        for entry in base.infolist():
            if not entry.filename.startswith('META-INF/'):
                out.writestr(copy.copy(entry), replacements.get(entry.filename, base.read(entry)))
    run(TOOLS / 'zipalign', '-f', '4', WORK / 'unsigned.apk', WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', KEY, '--ks-key-alias', 'test106',
        '--ks-pass', 'pass:test-edition-only', '--out', OUTPUT, WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'verify', '--verbose', OUTPUT)
    run(TOOLS / 'zipalign', '-c', '4', OUTPUT)
    assert certificate(OUTPUT) == certificate(BASE) != certificate(FORMAL)
    badging = subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(OUTPUT)], text=True)
    assert f"package: name='{PACKAGE}' versionCode='112' versionName='{VERSION_NAME}'" in badging
    assert "application-label:'金箍棒ol测试版'" in badging
    with zipfile.ZipFile(OUTPUT) as apk, zipfile.ZipFile(BASE) as base, \
            zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as payload:
        assert apk.testzip() is None and payload.testzip() is None
        names = lambda z: {n for n in z.namelist() if not n.startswith('META-INF/')}
        assert names(apk) == names(base)
        actual = sorted(n for n in names(apk) if apk.read(n) != base.read(n))
        assert set(actual) == set(replacements), actual
        payload.extractall(WORK / 'payload-new')
    verify_payload(WORK / 'payload-new')
    shutil.copytree(ROOT / 'tests', WORK / 'tests', ignore=shutil.ignore_patterns('__pycache__'))
    assert digest(BASE.read_bytes()) == BASE_SHA and digest(FORMAL.read_bytes()) == formal_sha
    assert all(digest((ROOT / n).read_bytes()) == sha for n, sha in hashes.items())
    from offline_android.test_edition_v112 import ITEMS, MARKER
    data = dict(apk=OUTPUT.name, apk_sha256=digest(OUTPUT.read_bytes()), apk_bytes=OUTPUT.stat().st_size,
        previous_test=str(BASE.relative_to(ROOT)), previous_test_sha256=BASE_SHA,
        formal_baseline_sha256=formal_sha, package=PACKAGE, version_code=112, version_name=VERSION_NAME,
        home_version_label='v112', port=PORT, certificate_sha256=certificate(OUTPUT),
        player_database='files/test-save-v106/game.sqlite3', fixed_account='v106_fixed_test',
        supply_revision=108, grant_items=dict(ITEMS), grant_marker=MARKER,
        contains_player_database=False, test_native_java_runtime_resources_preserved=True,
        program_sha256=digest(program), runtime_sha256=runtime_hash,
        source_hashes=hashes, changed_apk_entries=actual, changed_program_entries=delta)
    report('build-validation', data)
    (EVIDENCE / 'badging.txt').write_text(badging)
    OUTPUT.with_suffix('.manifest.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    OUTPUT.with_suffix('.apk.sha256').write_text(data['apk_sha256'] + '  ' + OUTPUT.name + '\n')
    print(json.dumps({k: data[k] for k in ('apk', 'apk_sha256', 'apk_bytes')}, ensure_ascii=False))


if __name__ == '__main__':
    build()
