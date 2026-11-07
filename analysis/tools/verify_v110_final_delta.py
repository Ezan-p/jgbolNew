"""Transfer protocol results only after proving the final change is Android startup timeout."""
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v110 import OUTPUT, EVIDENCE


def main():
    first = ROOT / '.runtime/v110-build-r2' / OUTPUT.name
    digest = lambda data: hashlib.sha256(data).hexdigest()
    old_sha, new_sha = digest(first.read_bytes()), digest(OUTPUT.read_bytes())
    with zipfile.ZipFile(first) as old, zipfile.ZipFile(OUTPUT) as new:
        names = lambda z: {n for n in z.namelist() if not n.startswith('META-INF/')}
        assert names(old) == names(new)
        apk_delta = sorted(n for n in names(old) if old.read(n) != new.read(n))
        assert apk_delta == ['assets/offline/build.properties', 'assets/offline/program.zip'], apk_delta
        with zipfile.ZipFile(io.BytesIO(old.read('assets/offline/program.zip'))) as a, \
                zipfile.ZipFile(io.BytesIO(new.read('assets/offline/program.zip'))) as b:
            assert set(a.namelist()) == set(b.namelist())
            delta = sorted(n for n in a.namelist() if a.read(n) != b.read(n))
            assert delta == ['offline_android/backend.py', 'payload-manifest.json'], delta
            assert a.read('offline_android/backend.py').replace(b'port=PORT, timeout=90.0', b'port=PORT, timeout=180.0') == b.read('offline_android/backend.py')
    path = EVIDENCE / 'protocol-validation.json'
    protocol = json.loads(path.read_text())
    assert protocol['apk_sha256'] == old_sha and protocol['passed']
    # The protocol runner explicitly excludes Android runtime/packer tests.
    # Those are rerun separately against the final source and final APK/device.
    assert 'test_android_offline_backend' not in protocol['suites']
    (EVIDENCE / 'candidate1/protocol-validation.json').write_text(path.read_text())
    protocol.update(apk_sha256=new_sha, tested_apk_sha256=old_sha,
        validation_basis='All protocol modules, rules, data, client assets and generated Lua are byte-identical; only Android startup timeout changed from 90 to 180 seconds and is separately revalidated.',
        final_delta_proof='final-candidate-delta.json')
    path.write_text(json.dumps(protocol, ensure_ascii=False, indent=2)+'\n')
    report = dict(apk_sha256=new_sha, tested_apk_sha256=old_sha,
        all_protocol_modules_and_resources_byte_identical=True,
        changed_apk_entries=apk_delta, changed_program_entries=delta,
        only_change='Android backend startup timeout: 90 -> 180 seconds',
        final_android_runtime_tests='host-android-tests.log', final_device_report='device-validation.json')
    (EVIDENCE / 'final-candidate-delta.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
