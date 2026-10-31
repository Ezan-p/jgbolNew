"""Verify scoped 1263 tables, shipped client compatibility, packaging and regressions.

Uses existing local original evidence and a temporary payload; never opens saves
or modifies/replaces the released APK. Run with .runtime/venv/bin/python.
"""
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT/'tests'), str(ROOT/'analysis/tools')]
from test_immortal_hotupdate import TABLES
from network_redirect import formation as f, summon, activity_home as home
from offline_android.pack_payload import build_payload
from audit_hotupdate_gap import index

OUT = ROOT/'analysis/evidence/immortal_hotupdate_implementation_20261031'
SUITES = ['test_immortal_hotupdate', 'test_growth_values', 'test_formation',
          'test_level_culture', 'test_expbooks', 'test_reborn', 'test_journey',
          'test_activity_home', 'test_activity', 'test_cortege_recycle']


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    audit = json.loads((ROOT/'analysis/evidence/hotupdate_gap_20261031/audit.json').read_text())
    evidence = {r['logical']: r for r in audit['csv']}
    tables = []
    apk_path = ROOT/'build/金箍棒3.87离线正式版v107.apk'
    with zipfile.ZipFile(apk_path) as apk, zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as program:
        version, mapping = index(program.read('client/release_w/index.txt'))
        assert version == 1263
        for name in TABLES:
            logical = 'csv_config/'+name
            raw = (ROOT/'analysis/configs/immortal_hotupdate'/name).read_bytes()
            assert sha(raw) == evidence[logical]['original_sha256'], name
            physical = mapping[logical]
            path = 'client/release_w/'+physical
            client = program.read(path) if path in program.namelist() else apk.read('assets/release_/'+physical)
            assert client == raw, name
            tables.append(dict(name=name, sha256=sha(raw), original_match=True,
                               shipped_client_match=True, rows=len(summon.rows(name))))
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp)/'backend.zip'
        manifest = build_payload(target)
        with zipfile.ZipFile(target) as z:
            for name in TABLES:
                path='analysis/configs/immortal_hotupdate/'+name
                assert z.read(path) == (ROOT/path).read_bytes()
            for name in ('summon','formation','journey','activity_home'):
                path=f'network_redirect/{name}.py'
                assert z.read(path) == (ROOT/path).read_bytes()
    from lupa.lua51 import LuaRuntime
    vm = LuaRuntime(unpack_returned_tuples=True)
    vm.execute('assert(loadstring(...))', summon.client_source(summon.load_rules()))
    checks = list(vm.execute((ROOT/'tests/expbook_client_regression.lua').read_text(),
                            (ROOT/'network_redirect/expbook_client.lua').read_text()).values())
    (OUT/'lua_validation.json').write_text(json.dumps(
        dict(passed=True, native_cocos=False, checks=checks), ensure_ascii=False, indent=2)+'\n')
    with (OUT/'tests.log').open('w') as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromNames(SUITES))
    report = dict(date='2026-10-31', passed=result.wasSuccessful(), tables=tables,
                  tests=result.testsRun, failures=len(result.failures), errors=len(result.errors), suites=SUITES,
                  payload_verified=True, temporary_payload_bundle_id=manifest['bundle_id'],
                  client_resource_version=version, released_apk_sha256=sha(apk_path.read_bytes()),
                  lua51_compile=True, expbook_adapter_checks=checks, native_ui_playthrough=False,
                  limits=dict(ascension=max(f.EVOLVE_COST), recycle=max(f.DEVOLVE),
                              experience=f.EXPERIENCE_CAPS, buildings={k:max(v) for k,v in home.BUILD.items()}),
                  caveat='A validates original client tables and contracts, not original server transactions. Existing v107 APK backend is unchanged.')
    (OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(passed=report['passed'], tests=report['tests'], failures=report['failures'],
                         errors=report['errors'], original_tables=len(tables),
                         lua_checks=len(checks), report=str(OUT/'validation.json')),ensure_ascii=False))
    if not result.wasSuccessful():
        print((OUT/'tests.log').read_text()[-6000:])
        raise SystemExit(1)


if __name__ == '__main__':
    main()
