import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


class RequestRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.addCleanup(self.b.close)
        self.state = {'authenticated': True}
        self.request = encode(1353, dict(serial_num=81, id=4, data='{index=1}'))

    def test_same_id_after_reconnect_reuses_response_without_running_again(self):
        with patch.object(self.b, '_respond', return_value=[encode(1106, dict(req_serial_num=81))]) as run:
            first = self.b.respond(self.request, self.state)
            self.assertEqual(self.b.respond(self.request, {'authenticated': True}), first)
            reconnected = encode(1353, dict(serial_num=81, id=4, data='{index=1}'), connection_id=77)
            self.assertEqual(self.b.respond(reconnected, {'authenticated': True}), first)
            self.assertEqual(run.call_count, 1)

    def test_changed_payload_and_evicted_receipt_never_repeat_execution(self):
        with patch.object(self.b, '_respond', return_value=[encode(1106, dict(req_serial_num=81))]) as run:
            self.b.respond(self.request, self.state)
            conflict = encode(1353, dict(serial_num=81, id=4, data='{index=2}'))
            replies = self.b.respond(conflict, self.state)
            self.assertEqual(decode(replies[-1])[2]['req_serial_num'], 81)
            self.assertEqual(decode(replies[0])[0], 2998)
            self.b.request_receipts.clear()
            self.b.respond(self.request, self.state)
            self.assertEqual(run.call_count, 1)

    def test_exception_after_commit_is_not_charged_twice_and_has_wait_exit(self):
        role = self.b.profile()
        role['gold_coin'] = 100
        self.b.save(role)
        def charge_then_fail(packet, state):
            role = self.b.profile()
            role['gold_coin'] -= 10
            self.b.save(role)
            raise RuntimeError('response serialization failed')
        with patch.object(self.b, '_respond', side_effect=charge_then_fail) as run:
            result = self.b.respond(self.request, self.state)
            self.assertEqual(decode(result[-1])[2]['req_serial_num'], 81)
            self.assertEqual(self.b.respond(self.request, self.state), result)
            self.assertEqual(run.call_count, 1)
        self.assertEqual(self.b.profile()['gold_coin'], 90)

    def test_expired_response_history_resets_sequence_and_sends_snapshot(self):
        self.b.server_serial = 201000
        self.b.last_request_serial = 81
        snapshot = encode(1032, dict(id=1, unit_type=1, attr_count=0, attr_list=[]))
        with patch.object(self.b, 'bootstrap', return_value=[snapshot]) as boot:
            replies = self.b.respond(encode(1105, dict(req_serial_num=200001)), self.state)
        mid, _, data = decode(replies[0])
        self.assertEqual((mid, data['serial_num'], data['id']), (2998, 0, 80))
        reset = login_fields(data['data'])['local_request_reset']
        self.assertEqual(reset['server_serial'], 201000)
        self.assertEqual(reset['next_request_serial'], 82)
        self.assertEqual(replies[1:], [snapshot])
        boot.assert_called_once_with(reconnect=True)

    def test_actual_reconnect_keeps_request_receipts(self):
        request = encode(1094, dict(serial_num=81))
        original = self.b.respond(request, self.state)
        with patch.object(self.b, 'bootstrap', return_value=[]):
            state = {}
            self.b.respond(encode(1016, dict(account=self.b.account, random_key=self.b.random_key)), state)
        self.assertTrue(state['authenticated'])
        self.assertEqual(self.b.respond(request, state), original)
