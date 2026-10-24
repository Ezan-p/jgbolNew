import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from network_redirect.repair import reset_login, TARGET


class LoginRepairTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.config = dict(runtime_dir=Path(self.temp.name),
                           config_path=Path('/game.json'), serial='emulator-5562', package='game')
        self.state = dict(config='/game.json', serial='emulator-5562', pid=123, port=18770)

    def execute(self, state=None, command=None, mapping='host tcp:18770 tcp:18770'):
        def adb(config, *args, **kwargs):
            if args == ('shell', 'ps'):
                return f'USER PID NAME\nroot 42 {TARGET}\nroot 43 {TARGET}:other\n'
            if args[:2] == ('shell', 'cat'):
                return command if command is not None else TARGET + '\x00-D\x00'
            if args == ('reverse', '--list'):
                return mapping
            return ''
        with patch('network_redirect.repair.read_state', return_value=self.state if state is None else state), \
                patch('network_redirect.repair.owned', return_value=False), \
                patch('network_redirect.repair.adb', side_effect=adb) as mock:
            reset_login(self.config)
        return [call.args[1:] for call in mock.call_args_list]

    def test_reset_only_exact_binary_and_owned_mapping(self):
        calls = self.execute()
        self.assertIn(('shell', 'kill', '-9', '42'), calls)
        self.assertNotIn(('shell', 'kill', '-9', '43'), calls)
        self.assertIn(('reverse', '--remove', 'tcp:18770'), calls)
        self.assertIn(('shell', 'am', 'force-stop', 'game'), calls)
        self.assertFalse(any('pm' in call or 'uninstall' in call for call in calls))

    def test_preserve_mapping_to_other_destination(self):
        calls = self.execute(mapping='host tcp:18770 tcp:19999')
        self.assertFalse(any(call[:2] == ('reverse', '--remove') for call in calls))

    def test_no_state_does_not_remove_mapping(self):
        calls = self.execute(state={})
        self.assertFalse(any(call[0] == 'reverse' for call in calls))

    def test_reject_foreign_state(self):
        with self.assertRaisesRegex(RuntimeError, '不属于当前配置'):
            self.execute(state=dict(self.state, serial='emulator-5554'))

    def test_recheck_pid_before_kill(self):
        with self.assertRaisesRegex(RuntimeError, '身份已变化'):
            self.execute(command='/system/bin/other\x00')

    def test_force_stop_stuck_controller_after_grace_period(self):
        with patch('network_redirect.repair.read_state', return_value=self.state), \
                patch('network_redirect.repair.owned', return_value=True), \
                patch('network_redirect.repair.time.monotonic', side_effect=[0, 13, 14]), \
                patch('network_redirect.repair.os.kill') as kill, \
                patch('network_redirect.repair.adb', return_value='USER PID NAME\n'):
            reset_login(self.config)
        import signal
        self.assertEqual([c.args for c in kill.call_args_list],
                         [(123, signal.SIGTERM), (123, signal.SIGKILL)])
