import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import threading
import unittest
from unittest.mock import patch

from observability.cli import main
from observability.collector import LogcatCollector, PackageFilter, package_processes, processes
from observability.events import SessionWriter, matches, parse_logcat, redact, render, replay_paths

PACKAGE = 'com.sygame.jingubang.p360'
HEADER = 'USER PID PPID VSIZE RSS WCHAN PC NAME\n'
PS = HEADER + f'u0_a55 2976 684 1375072 147612 epoll 0 S {PACKAGE}\n' + \
     f'u0_a55 2995 684 1239960 27976 epoll 0 S {PACKAGE}:QLocal\n' + \
     f'u0_a55 3000 684 1239960 27976 epoll 0 S {PACKAGE}.other\n'


class ObserverTests(unittest.TestCase):
    def test_threadtime_keeps_multiline_prefix_and_chinese(self):
        event = parse_logcat('10-23 21:49:13.599  2976  2989 D cocos2d-x debug info: 更新完成: ok\r\n')
        self.assertEqual((event['pid'], event['tid'], event['source']), (2976, 2989, 'engine'))
        self.assertEqual(event['message'], '更新完成: ok')
        self.assertEqual(parse_logcat('10-23 21:49:13.599 2976 2989 E Lua: \tat main.lua:9')['message'], '\tat main.lua:9')
        self.assertIsNone(parse_logcat('--------- beginning of main'))

    def test_exact_package_and_child_processes(self):
        self.assertEqual(package_processes(PS, PACKAGE), {2976: PACKAGE, 2995: PACKAGE + ':QLocal'})

    def test_android6_silent_ps_a_failure_falls_back(self):
        with patch('observability.collector.adb', side_effect=[HEADER, PS]) as command:
            self.assertIn(2976, processes({'package': PACKAGE}))
            self.assertEqual(command.call_args.args[1:], ('shell', 'ps'))

    def test_new_android_all_processes_format(self):
        output = f'USER PID PPID VSZ RSS WCHAN ADDR S NAME\nu0_a55 22 1 0 0 x 0 S {PACKAGE}\n'
        self.assertEqual(package_processes(output, PACKAGE), {22: PACKAGE})

    def test_filters_do_not_capture_unrelated_native_crash(self):
        f = PackageFilter(PACKAGE)
        f.pids = {2976: PACKAGE}
        def row(message, pid=678, tag='DEBUG'):
            return dict(pid=pid, tid=678, tag=tag, message=message, source='android')
        self.assertFalse(f.accepts(row('arbitrary device log'), 1))
        self.assertTrue(f.accepts(row(f'pid: 2976 >>> {PACKAGE} <<<'), 1))
        self.assertTrue(f.accepts(row('backtrace: #00 pc 123'), 2))
        self.assertFalse(f.accepts(row('>>> another.app <<<'), 3))
        self.assertFalse(f.accepts(row('backtrace: #00 pc 456'), 4))
        self.assertTrue(f.accepts(row('hello', 2976), 4))
        f.pids = {4000: PACKAGE}
        self.assertFalse(f.accepts(row('PID reused', 2976), 5))

    def test_native_crash_block_expires(self):
        f = PackageFilter(PACKAGE)
        row = dict(pid=678, tid=1, tag='DEBUG', message=f'>>> {PACKAGE} <<<')
        self.assertTrue(f.accepts(row, 1))
        self.assertFalse(f.accepts(dict(row, message='unrelated'), 12))

    def test_sensitive_values_redacted_in_fields_and_messages(self):
        value = dict(access_token='secret1', nested=['auth_key=secret2', 'password="space secret"',
                     '{"token":"secret3"}', "access_token='secret 4'", 'Authorization: Bearer secret5'])
        text = json.dumps(redact(value))
        self.assertNotIn('secret', text)
        self.assertIn('REDACTED', text)
        self.assertEqual(redact({'pids': {2976: PACKAGE}})['pids']['2976'], PACKAGE)

    def test_console_filter_does_not_drop_saved_events(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()) as out:
            writer = SessionWriter(directory, {}, level='E')
            writer.emit(dict(source='lua', level='D', message='token=secret'))
            writer.emit(dict(source='engine', level='E', message='failure\n\x1b[31m'))
            writer.close()
            rows = [json.loads(x) for x in (writer.directory / 'events.jsonl').read_text().splitlines()]
            self.assertEqual(len(rows), 2)
            self.assertNotIn('secret', (writer.directory / 'console.log').read_text())
            self.assertNotIn('REDACTED', out.getvalue())
            self.assertIn('failure\\n\\u001b', out.getvalue())

    def test_rotation_replay_order_and_thread_safe_sequence(self):
        with tempfile.TemporaryDirectory() as directory:
            writer = SessionWriter(directory, {}, max_bytes=1500, backups=3, console=False)
            threads = [threading.Thread(target=lambda: [writer.emit(dict(message='x' * 30))
                                                       for _ in range(20)]) for _ in range(3)]
            for t in threads: t.start()
            for t in threads: t.join()
            writer.close()
            paths = replay_paths(writer.directory)
            self.assertLessEqual(len(paths), 4)
            rows = [json.loads(line) for p in paths for line in p.read_text().splitlines()]
            sequence = [r['sequence'] for r in rows]
            self.assertEqual(sequence, sorted(set(sequence)))
            self.assertEqual(sequence[-1], 60)
            self.assertEqual(json.loads((writer.directory / 'summary.json').read_text())['events'], 60)

    def test_replay_is_offline_and_reports_corruption(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / 'events.jsonl'
            p.write_text('{"message":"ok", "level":"E", "source":"lua"}\nbroken\n')
            with contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(io.StringIO()) as err:
                self.assertEqual(main(['replay', str(p), '--level', 'E']), 1)
            self.assertIn('ok', out.getvalue())
            self.assertIn('跳过损坏记录', err.getvalue())

    def test_new_pid_logs_are_buffered_then_attributed(self):
        with tempfile.TemporaryDirectory() as directory:
            writer = SessionWriter(directory, {}, console=False)
            collector = LogcatCollector({'package': PACKAGE}, writer)
            collector.last_poll = float('inf')
            collector.rows.put('10-23 21:49:13.599 4000 4001 D cocos2d-x: early log\n')
            collector.pump()
            self.assertEqual(writer.sequence, 0)
            collector.filter.pids = {4000: PACKAGE}
            collector.pump()
            self.assertEqual(writer.sequence, 1)
            writer.close()

    def test_logcat_disconnect_fails_instead_of_hanging(self):
        with tempfile.TemporaryDirectory() as directory:
            writer = SessionWriter(directory, {}, console=False)
            collector = LogcatCollector({'package': PACKAGE}, writer)
            collector.last_poll = float('inf')
            collector.done.set()
            class Process:
                def wait(self, timeout): return 1
            collector.proc = Process()
            with self.assertRaisesRegex(RuntimeError, 'logcat'):
                collector.pump()
            writer.close()

    def test_filters_and_terminal_escape(self):
        event = dict(source='lua', level='E', message='Lua Error\n\x1b[2J')
        self.assertTrue(matches(event, 'W', ['lua'], 'ERROR'))
        self.assertFalse(matches(event, 'W', ['engine']))
        self.assertNotIn('\x1b', render(event))


if __name__ == '__main__':
    unittest.main()
