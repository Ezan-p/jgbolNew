"""Check release provenance and execute v108 regressions from the final test APK."""
import io
import json
from pathlib import Path
import sys
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / '.runtime/v108-test/program'
sys.path[:0] = [str(PROGRAM), str(ROOT), str(ROOT / 'tests')]
from analysis.tools.build_v108_test import APK, BASE, EVIDENCE, digest
from analysis.tools.verify_v108 import SUITES
from offline_android.pack_payload import verify_payload


def main():
    with zipfile.ZipFile(APK) as apk, zipfile.ZipFile(BASE) as base:
        with zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as new, \
                zipfile.ZipFile(io.BytesIO(base.read('assets/offline/program.zip'))) as old:
            assert set(old.namelist()) <= set(new.namelist())
            delta = sorted(n for n in new.namelist() if n not in old.namelist() or new.read(n) != old.read(n))
            assert delta == sorted(['offline_android/backend.py','offline_android/test_edition_seed.py',
                'offline_android/test_edition_v108.py','network_redirect/login.html','payload-manifest.json'])
            for name in new.namelist():
                assert (PROGRAM / name).read_bytes() == new.read(name), name
            assert not any(Path(n).suffix in ('.db', '.sqlite3', '.pyc') for n in new.namelist())
        assert apk.read('assets/offline/runtime.zip') == base.read('assets/offline/runtime.zip')
    verify_payload(PROGRAM)
    from lupa.lua51 import LuaRuntime
    bundle = (PROGRAM / 'offline_client.lua').read_text()
    LuaRuntime().execute('assert(loadstring(...))', bundle)
    assert "label('v108',0.75)" in bundle
    sys.path.insert(0, str(PROGRAM))
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromNames(list(dict.fromkeys(SUITES))))
    loaded = []
    for name, module in list(sys.modules.items()):
        if name.startswith('network_redirect.') and getattr(module, '__file__', None):
            assert Path(module.__file__).resolve().is_relative_to(PROGRAM.resolve()), name
            loaded.append(name)
    report = dict(apk_sha256=digest(APK.read_bytes()), tests=result.testsRun,
        passed=result.wasSuccessful(), failures=len(result.failures), errors=len(result.errors),
        unchanged_official_v108_gameplay=True, changed_program_entries=delta,
        actual_packaged_modules=len(loaded), lua_compiles=True, home_label='v108',
        no_player_database=True)
    (EVIDENCE / 'protocol-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(not result.wasSuccessful())


if __name__ == '__main__':
    main()
