"""Verify rebirth roster provenance, runtime and Android packaging inputs offline."""
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon, reborn, fate_rebuild
from offline_android.pack_payload import collect_files
from audit_hotupdate_gap import index, table


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    evidence = ROOT/'analysis/evidence/hotupdate_gap_20261031'
    previous = json.loads((evidence/'audit.json').read_text())
    name = 'cortege_reborn_config.csv'
    logical = 'csv_config/' + name
    history = previous['history'][logical]
    report = dict(date='2026-10-31', classification='A: original client data; B: local save migration',
                  versions=[], added=[], apk_rebuilt=False)
    latest = None
    for change in history:
        package = next(p for p in previous['packages'] if p['end'] == change['version'])
        archive_path = Path('/private/tmp/jgb-hotupdate')/package['file']
        raw = archive_path.read_bytes()
        assert sha(raw) == package['sha256']
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            assert archive.testzip() is None
            resource = archive.read(change['physical'])
        parsed = table(resource)
        rows = {int(r[0]):dict(zip(parsed[0], r)) for r in parsed[1:]}
        changes = [] if latest is None else [dict(cortege_type=t, before=latest[t], after=r)
                                             for t, r in rows.items() if latest[t] != r]
        report['versions'].append(dict(version=change['version'], package=package['file'],
                                        package_sha256=sha(raw), physical=change['physical'],
                                        resource_sha256=sha(resource), rows=len(rows), changes=changes))
        latest = rows
    official = (evidence/'official_csv'/name).read_bytes()
    runtime_path = ROOT/'analysis/configs/immortal_hotupdate'/name
    assert runtime_path.read_bytes() == official
    assert reborn.CORTS == latest
    with (ROOT/'analysis/configs'/name).open(encoding='utf-8-sig', newline='') as source:
        baseline = {int(r['cortege_type']):r for r in csv.DictReader(source)}
    assert len(baseline) == 14 and len(latest) == 25
    assert all(latest[t] == r for t, r in baseline.items())
    report['added'] = [r for t, r in latest.items() if t not in baseline]
    assert len(report['added']) == 11
    assert len(fate_rebuild.ACTIVE) == 15 and fate_rebuild.ACTIVE <= latest.keys()
    assert fate_rebuild.ACTIVE & (latest.keys()-baseline.keys()) == {5013}
    files = collect_files()
    relative = runtime_path.relative_to(ROOT).as_posix()
    assert files[relative] == runtime_path
    report.update(runtime_table=relative, extracted_utf8_sha256=sha(official),
                  runtime_count=len(reborn.CORTS), fate_count=len(fate_rebuild.ACTIVE),
                  missing_fate_prerequisites=sorted(fate_rebuild.ACTIVE-latest.keys()),
                  payload_input_includes_table=True)
    apk_path = ROOT/'build/金箍棒3.87离线正式版v107.apk'
    with zipfile.ZipFile(apk_path) as apk, zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as program:
        version, mapping = index(program.read('client/release_w/index.txt'))
        overlay = 'client/release_w/'+mapping[logical]
        raw = program.read(overlay) if overlay in program.namelist() else apk.read('assets/release_/'+mapping[logical])
        parsed = table(raw)
        assert {int(r[0]):dict(zip(parsed[0], r)) for r in parsed[1:]} == latest
        report['existing_apk_client'] = dict(path=apk_path.relative_to(ROOT).as_posix(),
                                             version=version, roster_count=len(parsed)-1,
                                             resource_sha256=sha(raw))
    out = ROOT/'analysis/evidence/reborn_hotupdate_20261031'
    out.mkdir(parents=True, exist_ok=True)
    (out/'audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
