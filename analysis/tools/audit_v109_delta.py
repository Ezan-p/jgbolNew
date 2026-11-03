"""Compare actual release payloads, using the latest Tangwang-updated v108 as baseline."""
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v109 import BASE, OUTPUT, EVIDENCE
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
            assert [r['path'] for r in changes if r['status'] == 'removed'] == ['analysis/npc_design/rank_elite/catalog.json']
            assert not any(r['path'].startswith('client/') for r in changes)
            for name, source in collect_files().items():
                if name != 'network_redirect/login.html':
                    assert new.read(name) == source.read_bytes(), name
    build = json.loads((EVIDENCE / 'build-validation.json').read_text())
    assert [r['path'] for r in changes] == build['changed_program_entries']
    report = dict(baseline_sha256=sha(BASE.read_bytes()), apk_sha256=sha(OUTPUT.read_bytes()),
                  comparison='actual v108 APK versus actual v109 APK',
                  added=sum(r['status'] == 'added' for r in changes),
                  modified=sum(r['status'] == 'modified' for r in changes), removed=1, retired_resource="Old five-elite index replaced by rank_500/catalog.json",
                  current_sources_match=True, client_assets_unchanged=True, changes=changes)
    (EVIDENCE / 'v108-to-v109-delta.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'changes'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
