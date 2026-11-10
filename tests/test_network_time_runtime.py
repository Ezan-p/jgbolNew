"""Production startup enables the service, while fixtures use no external I/O."""
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from offline_android import backend
from offline_android.pack_payload import ROOT
from tests.test_game_clock import Source, NOW
from tests.test_trusted_game_clock import Service


class RuntimeNetworkClockTests(unittest.TestCase):
    def test_default_startup_enables_network_before_player_clock_is_opened(self):
        source=Source();source.wall_seconds=NOW+86400
        service=Service(source);service.set(NOW)
        with tempfile.TemporaryDirectory() as tmp:
            with patch('network_redirect.network_time.TimeService',return_value=service) as factory:
                try:
                    status=backend.start(tmp, ROOT, port=0)
                    self.assertTrue(status['ready'])
                    factory.assert_called_once()
                    self.assertIn(True,service.requests)
                    with sqlite3.connect(Path(tmp)/'save/clock.sqlite3') as db:
                        state=json.loads(db.execute('SELECT data FROM clock').fetchone()[0])
                    self.assertEqual(state['policy_version'],3)
                    self.assertEqual(state['game'],NOW)
                    self.assertFalse(state.get('quarantined',False))
                finally:backend.stop()

    def test_startup_offline_does_not_invent_reboot_gap(self):
        source=Source();service=Service(source);service.set(NOW)
        with tempfile.TemporaryDirectory() as tmp:
            try:
                backend.start(tmp,ROOT,port=0,network_time=service)
                backend.stop()
                source.boot_id='boot-b';source.seconds=10;source.wall_seconds+=86400
                service.observation=None
                backend.start(tmp,ROOT,port=0,network_time=service)
                with sqlite3.connect(Path(tmp)/'save/clock.sqlite3') as db:
                    state=json.loads(db.execute('SELECT data FROM clock').fetchone()[0])
                self.assertEqual(state['game'],NOW)
                self.assertEqual(state['status'],'network_required_after_restart')
            finally:backend.stop()
