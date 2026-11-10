"""Exercise the packaged test runtime and its default network-clock entry point."""
import http.client
import io
import json
import re
from pathlib import Path
import sqlite3
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
import zipfile

ROOT=Path(__file__).resolve().parents[2]
PROGRAM=ROOT/'.runtime/v110-test-refresh-20261110/program'
EVIDENCE=ROOT/'analysis/evidence/v110-test-refresh-20261110'
APK=ROOT/'.runtime/v110-test-refresh-20261110/金箍棒ol测试版-v110-20261110整合更新.apk'
sys.path[:0]=[str(PROGRAM),str(ROOT/'tests'),str(ROOT)]
from offline_android import backend
from network_redirect import game_clock,network_time
from tests.test_game_clock import Source
from tests.test_trusted_game_clock import Service


class RuntimeTests(unittest.TestCase):
    def test_default_network_service_and_fixed_account_share_trusted_clock(self):
        source=Source();source.wall_seconds=int(time.time())
        service=Service(source);service.set(source.wall())
        with tempfile.TemporaryDirectory() as tmp:
            with patch('network_redirect.network_time.TimeService',return_value=service) as factory:
                try:
                    status=backend.start(tmp,PROGRAM,port=0)
                    self.assertTrue(status['ready']);factory.assert_called_once()
                    self.assertIn(True,service.requests)
                    dbpath=Path(tmp)/'test-save-v106/game.sqlite3'
                    self.assertEqual(Path(status['database']).resolve(),dbpath.resolve())
                    self.assertFalse((Path(tmp)/'save').exists())
                    with sqlite3.connect(dbpath) as db:
                        role=json.loads(db.execute("SELECT data FROM roles WHERE account='v106_fixed_test'").fetchone()[0])
                    self.assertEqual(role['test_supply_revision'],108)
                    self.assertEqual(role['test_v110_abyss_maps_500_v1']['total'],500)
                    with sqlite3.connect(dbpath.with_name('clock.sqlite3')) as db:
                        state=json.loads(db.execute('SELECT data FROM clock').fetchone()[0])
                    self.assertEqual(state['policy_version'],3)
                    self.assertEqual(state['status'],'network_synchronized')
                    conn=http.client.HTTPConnection('127.0.0.1',status['port'],timeout=10)
                    conn.request('GET','/local-login');response=conn.getresponse()
                    self.assertEqual(response.status,200)
                    page=response.read().decode();self.assertIn('测试',page)
                    conn.close()
                    csrf=re.search(r"setRequestHeader\('X-Local-CSRF','([^']+)'\)",page)[1]
                    conn=http.client.HTTPConnection('127.0.0.1',status['port'],timeout=10)
                    conn.request('POST','/local-auth',json.dumps({'action':'resume'}),
                        {'Content-Type':'application/json','X-Local-CSRF':csrf})
                    response=conn.getresponse();self.assertEqual(response.status,200)
                    authenticated=json.loads(response.read());self.assertTrue(authenticated['ok'])
                    self.assertTrue(authenticated['token']);conn.close()
                finally:backend.stop()
                try:
                    status=backend.start(tmp,PROGRAM,port=0,network_time=service)
                    with sqlite3.connect(status['database']) as db:
                        after=json.loads(db.execute("SELECT data FROM roles WHERE account='v106_fixed_test'").fetchone()[0])
                    for key in ('attachments','corteges','gold_coin','silver_coin','test_supply_revision','test_v110_abyss_maps_500_v1'):
                        self.assertEqual(role[key],after[key],key)
                finally:backend.stop()

    def test_offline_restart_waits_for_verification_without_wall_credit(self):
        source=Source();source.wall_seconds=int(time.time())
        service=Service(source);service.set(source.wall())
        with tempfile.TemporaryDirectory() as tmp:
            try:
                backend.start(tmp,PROGRAM,port=0,network_time=service)
                backend.stop()
                with sqlite3.connect(Path(tmp)/'test-save-v106/clock.sqlite3') as db:
                    before=json.loads(db.execute('SELECT data FROM clock').fetchone()[0])
                source.boot_id='new-boot';source.seconds=10;source.wall_seconds+=86400
                service.observation=None
                backend.start(tmp,PROGRAM,port=0,network_time=service)
                with sqlite3.connect(Path(tmp)/'test-save-v106/clock.sqlite3') as db:
                    after=json.loads(db.execute('SELECT data FROM clock').fetchone()[0])
                self.assertEqual(after['game'],before['game'])
                self.assertEqual(after['status'],'network_required_after_restart')
            finally:backend.stop()

if __name__=='__main__':
    import hashlib
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(RuntimeTests))
    for name,module in list(sys.modules.items()):
        if name.startswith(('network_redirect.','offline_android.')) and getattr(module,'__file__',None):
            assert Path(module.__file__).resolve().is_relative_to(PROGRAM.resolve()),name
    report=dict(passed=result.wasSuccessful(),tests=result.testsRun,errors=len(result.errors),failures=len(result.failures),skipped=len(result.skipped),apk_sha256=hashlib.sha256(APK.read_bytes()).hexdigest())
    (EVIDENCE/'runtime-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())
