import asyncio
import subprocess
import time
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import start_game
from network_redirect.cli import poll_processes
from network_redirect.server import HEALTH, LandingServer


class ProcessPollingTests(unittest.IsolatedAsyncioTestCase):
    async def test_adb_failures_keep_listener_available_until_recovery(self):
        events = []
        emit = lambda kind, **fields: events.append(kind)
        server = LandingServer(0, b'list', emit)
        await server.start()
        try:
            expected = {123: 'game'}
            failures = [subprocess.TimeoutExpired('adb shell ps -A', 5),
                        subprocess.CalledProcessError(1, 'adb', stderr='device offline'),
                        RuntimeError('ps 未返回进程表'), expected]
            with patch('network_redirect.cli.processes', side_effect=failures):
                task = asyncio.create_task(poll_processes({}, asyncio.Event(), emit, retry_delay=.01))
                reader, writer = await asyncio.open_connection('127.0.0.1', server.port)
                writer.write(b'GET /__redirect_health HTTP/1.1\r\n\r\n')
                await writer.drain()
                self.assertIn(HEALTH, await asyncio.wait_for(reader.read(), 1))
                writer.close()
                await writer.wait_closed()
                self.assertEqual(await asyncio.wait_for(task, 1), expected)
            self.assertIn('process_poll_retry', events)
            self.assertIn('process_poll_recovered', events)
        finally:
            await server.close()

    async def test_stop_interrupts_retry_without_empty_snapshot(self):
        stopped = asyncio.Event()
        def emit(*args, **kwargs):
            stopped.set()
        with patch('network_redirect.cli.processes', side_effect=subprocess.TimeoutExpired('adb', 5)):
            result = await asyncio.wait_for(poll_processes({}, stopped, emit), .5)
        self.assertIsNone(result)

    async def test_duration_still_expires_during_adb_failure(self):
        with patch('network_redirect.cli.processes', side_effect=OSError('ADB unavailable')):
            result = await asyncio.wait_for(poll_processes(
                {}, asyncio.Event(), Mock(), deadline=time.monotonic() + .02), .5)
        self.assertIsNone(result)


class LauncherTests(unittest.TestCase):
    def launch(self, argv, installed='package:game.apk'):
        config = dict(apk=Path(__file__), package='game', python_path=Path('/runtime/python'),
                      config_path=Path('/game.json'), web_port=8768)
        with patch.object(start_game, 'load_config', return_value=config), \
                patch.object(start_game, 'Manager') as manager, \
                patch.object(start_game, 'ready_device'), \
                patch.object(start_game, 'adb', return_value=installed), \
                patch.object(start_game.subprocess, 'run') as run:
            start_game.main(argv)
        return manager.return_value, run

    def test_default_launch_requires_local_login_before_opening_browser(self):
        manager, run = self.launch([])
        manager.launch.assert_not_called()
        manager.install.assert_not_called()
        self.assertEqual(run.call_args_list[0].args[0][-1:], ['stop'])
        self.assertEqual(run.call_args_list[1].args[0][-3:], ['start', '--offline', '--probe'])
        self.assertEqual(run.call_args_list[2].args[0], ['open', 'http://127.0.0.1:8768'])

    def test_client_only_preserves_explicit_raw_client_mode(self):
        manager, run = self.launch(['--client-only'])
        manager.launch.assert_called_once()
        self.assertEqual(run.call_count, 1)

    def test_repair_resets_stale_injection_before_probed_start(self):
        with patch('network_redirect.repair.reset_login') as reset:
            manager, run = self.launch(['--repair'])
        reset.assert_called_once()
        self.assertEqual(run.call_args_list[0].args[0][-3:], ['start', '--offline', '--probe'])

    def test_repair_failure_does_not_launch_or_report_success(self):
        with patch('network_redirect.repair.reset_login', side_effect=RuntimeError('repair failed')):
            with self.assertRaisesRegex(RuntimeError, 'repair failed'):
                self.launch(['--repair'])

    def test_missing_apk_is_installed_before_local_launch(self):
        manager, run = self.launch([], installed='')
        manager.install.assert_called_once()
        self.assertEqual(run.call_args_list[1].args[0][-3:], ['start', '--offline', '--probe'])

    def test_local_service_failure_does_not_report_launch_success(self):
        with patch.object(start_game.subprocess, 'run', side_effect=subprocess.CalledProcessError(1, 'redirect')), \
                patch.object(start_game, 'load_config', return_value=dict(
                    apk=Path(__file__), package='game', python_path=Path('/runtime/python'),
                    config_path=Path('/game.json'), web_port=8768)), \
                patch.object(start_game, 'Manager'), patch.object(start_game, 'ready_device'), \
                patch.object(start_game, 'adb', return_value='package:game.apk'):
            with self.assertRaises(subprocess.CalledProcessError):
                start_game.main([])


if __name__ == '__main__':
    unittest.main()
