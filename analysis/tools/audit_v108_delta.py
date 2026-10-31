"""Compare actual release payloads, without treating the v106 Git HEAD as v107."""
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v108 import BASE, OUTPUT, EVIDENCE
from offline_android.pack_payload import collect_files


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    changes = []
    with zipfile.ZipFile(BASE) as old_apk, zipfile.ZipFile(OUTPUT) as new_apk:
        with zipfile.ZipFile(io.BytesIO(old_apk.read('assets/offline/program.zip'))) as old, \
                zipfile.ZipFile(io.BytesIO(new_apk.read('assets/offline/program.zip'))) as new:
            names = set(old.namelist()) | set(new.namelist())
            for name in sorted(names):
                before = old.read(name) if name in old.namelist() else None
                after = new.read(name) if name in new.namelist() else None
                if before != after:
                    changes.append(dict(path=name, status='added' if before is None else
                                        'removed' if after is None else 'modified',
                                        old_sha256=sha(before) if before is not None else None,
                                        new_sha256=sha(after) if after is not None else None))
            assert not any(r['status'] == 'removed' for r in changes)
            assert not any(r['path'].startswith('client/') for r in changes)
            for name, source in collect_files().items():
                if name != 'network_redirect/login.html':
                    assert new.read(name) == source.read_bytes(), name
    build = json.loads((EVIDENCE / 'build-validation.json').read_text())
    assert [r['path'] for r in changes] == build['changed_program_entries']
    report = dict(baseline_sha256=sha(BASE.read_bytes()), apk_sha256=sha(OUTPUT.read_bytes()),
                  comparison='actual v107 APK versus actual v108 APK',
                  added=sum(r['status'] == 'added' for r in changes),
                  modified=sum(r['status'] == 'modified' for r in changes), removed=0,
                  current_sources_match=True, client_assets_unchanged=True, changes=changes)
    (EVIDENCE / 'v107-to-v108-delta.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'changes'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
