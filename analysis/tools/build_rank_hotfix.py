"""Apply only the mixed-key formation fix to the preserved offline v105 APK."""
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from build_channel360 import TOOLS, run
from build_offline import SIGNING_KEY, signer_certificate


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    base = ROOT / 'build/金箍棒3.87-离线单机-arm32-v105.apk'
    output = ROOT / 'build/金箍棒3.87-离线单机-arm32-v105-封神榜修复.apk'
    work = ROOT / '.runtime/rank-hotfix'
    work.mkdir(exist_ok=True)
    if output.exists():
        raise ValueError('Refusing to overwrite an existing hotfix APK')
    signer_certificate(base)
    source_name = 'network_redirect/formation.py'
    fixed = (ROOT / source_name).read_bytes()
    with zipfile.ZipFile(base) as apk:
        original_program = apk.read('assets/offline/program.zip')
        program = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(original_program)) as old, zipfile.ZipFile(program, 'w') as new:
            previous = old.read(source_name).decode()
            expected = previous.replace('import csv\n', 'import copy\nimport csv\n').replace(
                '    before = json.dumps(role, sort_keys=True)',
                '    # Fresh battle effects mix numeric action indices with named metadata.\n'
                '    # Compare the detached state directly: JSON key sorting cannot order those\n'
                '    # keys, and persistence must not be required before formation migration.\n'
                '    before = copy.deepcopy(role)').replace(
                '    return before != json.dumps(role, sort_keys=True)', '    return before != role')
            assert expected.encode() == fixed, 'Unexpected changes outside the targeted fix'
            manifest = json.loads(old.read('payload-manifest.json'))
            entry = next(row for row in manifest['files'] if row['path'] == source_name)
            entry.update(size=len(fixed), sha256=digest(fixed))
            manifest['bundle_id'] = digest(json.dumps(manifest['files'], sort_keys=True, separators=(',', ':')).encode())
            replacements = {source_name: fixed, 'payload-manifest.json': json.dumps(manifest, ensure_ascii=False, indent=2).encode()}
            for entry in old.infolist():
                new.writestr(entry, replacements.get(entry.filename, old.read(entry)))
        properties = apk.read('assets/offline/build.properties').decode().replace(
            digest(original_program), digest(program.getvalue()))
        assert digest(program.getvalue()) in properties
        replacements = {'assets/offline/program.zip': program.getvalue(),
                        'assets/offline/build.properties': properties.encode()}
        with zipfile.ZipFile(work / 'unsigned.apk', 'w') as new:
            for entry in apk.infolist():
                if not entry.filename.startswith('META-INF/'):
                    new.writestr(entry, replacements.get(entry.filename, apk.read(entry)))
    run(TOOLS / 'zipalign', '-f', '4', work / 'unsigned.apk', work / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', SIGNING_KEY, '--ks-key-alias', 'channel360',
        '--ks-pass', 'pass:local-test-only', '--out', output, work / 'aligned.apk')
    certificate = signer_certificate(output)
    run(TOOLS / 'zipalign', '-c', '4', output)
    with zipfile.ZipFile(base) as old, zipfile.ZipFile(output) as new:
        assert new.testzip() is None
        names = lambda z: {name for name in z.namelist() if not name.startswith('META-INF/')}
        assert names(old) == names(new)
        changed = sorted(name for name in names(old) if old.read(name) != new.read(name))
        assert changed == sorted(replacements)
    report = dict(base=base.name, base_sha256=digest(base.read_bytes()), apk=output.name,
                  sha256=digest(output.read_bytes()), certificate_sha256=certificate,
                  version_code=105, changed_apk_entries=changed,
                  changed_program_entries=[source_name, 'payload-manifest.json'])
    output.with_suffix('.manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    output.with_suffix('.apk.sha256').write_text(report['sha256'] + '  ' + output.name + '\n')
    print(output)


if __name__ == '__main__':
    main()
