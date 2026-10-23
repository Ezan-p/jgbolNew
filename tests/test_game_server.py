"""Exercise the standalone CLI in separate processes with real local sockets."""
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ('import sys; from pathlib import Path; import game_server; '
             'game_server.SESSION_ROOT = Path(sys.argv[1]); '
             'sys.exit(game_server.main(sys.argv[2:]))')


class GameServerCLITests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='jgbol-server-test-')
        self.addCleanup(self.temporary.cleanup)
        self.sessions = Path(self.temporary.name) / 'sessions'

    def command(self, *args):
        return [sys.executable, '-c', BOOTSTRAP, str(self.sessions), *args]

    def run_cli(self, *args):
        return subprocess.run(self.command(*args), cwd=ROOT, capture_output=True,
                              text=True, timeout=15,
                              env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))

    def start_cli(self, *args):
        process = subprocess.Popen(self.command(*args), cwd=ROOT,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True,
                                   env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))

        def cleanup():
            if process.poll() is None:
                process.terminate()
            try:
                process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate(timeout=5)

        self.addCleanup(cleanup)
        return process

    def free_port(self):
        with socket.socket() as listener:
            listener.bind(('127.0.0.1', 0))
            return listener.getsockname()[1]

    def records(self):
        result = []
        for path in self.sessions.glob('*/events.jsonl'):
            # A concurrent writer may not have finished its final line yet.
            lines = path.read_text(encoding='utf-8').splitlines(keepends=True)
            result.extend(json.loads(line) for line in lines if line.endswith('\n'))
        return result

    def wait_for_event(self, process, kind):
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            matches = [row for row in self.records() if row['kind'] == kind]
            if matches:
                return matches[-1]
            if process.poll() is not None:
                stdout, stderr = process.communicate(timeout=2)
                self.fail(f'CLI exited before {kind}: {process.returncode}\n{stdout}\n{stderr}')
            time.sleep(.02)
        self.fail(f'Timed out waiting for {kind}')

    def test_probe_duration_and_quiet_write_complete_session(self):
        port = self.free_port()
        result = self.run_cli('--port', str(port), '--probe', '--duration', '.05', '--quiet')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(f'http://127.0.0.1:{port}', result.stdout)
        self.assertIn(str(self.sessions), result.stdout)
        self.assertNotIn('HTTP GET', result.stdout)
        events = self.records()
        probes = [row for row in events if row['kind'] == 'probe_result']
        self.assertEqual({row['path'] for row in probes}, {
            '/__redirect_health', '/update/jgb/p360_a/server_list.txt',
            '/update/jgb/p360_na/server_list.txt'})
        self.assertEqual(len(probes), 3)
        self.assertTrue(all(row['ok'] and row['status'] == 200 for row in probes))
        self.assertEqual(events[0]['kind'], 'server_started')
        self.assertEqual(events[-1]['kind'], 'server_stopped')
        self.assertEqual(events[-1]['reason'], 'duration_elapsed')
        directories = list(self.sessions.iterdir())
        self.assertEqual(len(directories), 1)
        summary = json.loads((directories[0] / 'summary.json').read_text())
        self.assertEqual(summary['events'], len(events))
        self.assertTrue((directories[0] / 'session.json').is_file())
        self.assertIn('自检 通过', (directories[0] / 'console.log').read_text())

    def test_sigterm_closes_active_connection_and_releases_port(self):
        port = self.free_port()
        process = self.start_cli('--port', str(port), '--quiet')
        self.wait_for_event(process, 'server_started')
        with socket.create_connection(('127.0.0.1', port), timeout=3) as client:
            client.sendall(b'raw tcp remains connected')
            self.wait_for_event(process, 'tcp_received')
            process.send_signal(signal.SIGTERM)
            stdout, stderr = process.communicate(timeout=10)
            self.assertEqual(process.returncode, 0, stdout + stderr)
            self.assertEqual(client.recv(1), b'')
        events = self.records()
        self.assertEqual(events[-1]['kind'], 'server_stopped')
        self.assertEqual(events[-1]['reason'], 'SIGTERM')
        close = next(row for row in events if row['kind'] == 'local_close')
        self.assertEqual(close['reason'], 'server_shutdown')
        with socket.socket() as replacement:
            replacement.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            replacement.bind(('127.0.0.1', port))
            replacement.listen(1)

    def test_port_conflict_does_not_disturb_existing_listener(self):
        with socket.socket() as existing:
            existing.bind(('127.0.0.1', 0))
            existing.listen(1)
            existing.settimeout(3)
            port = existing.getsockname()[1]
            result = self.run_cli('--port', str(port), '--quiet')
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn('已被占用', result.stderr)
            self.assertIn('--port', result.stderr)
            with socket.create_connection(('127.0.0.1', port), timeout=3) as client:
                accepted, _ = existing.accept()
                with accepted:
                    accepted.sendall(b'still alive')
                self.assertEqual(client.recv(64), b'still alive')
        events = self.records()
        self.assertFalse(any(row['kind'] == 'server_started' for row in events))
        self.assertEqual(events[-1]['reason'], 'startup_failed')

    def test_invalid_arguments_fail_before_creating_session(self):
        for args in [('--port', '0'), ('--port', '65536'), ('--port', 'abc'),
                     ('--duration', '-1'), ('--duration', 'nan'), ('--duration', 'inf')]:
            with self.subTest(args=args):
                result = self.run_cli(*args)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn('error:', result.stderr)
                self.assertFalse(self.sessions.exists())


if __name__ == '__main__':
    unittest.main()
