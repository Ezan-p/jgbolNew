import asyncio
import json
from pathlib import Path
import ssl
import struct
import tempfile
import unittest

from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode, fields
from network_redirect.server import LandingServer, HEALTH
from network_redirect.tls import LocalTLS


class ProtocolTests(unittest.TestCase):
    def test_known_wire_bytes(self):
        self.assertEqual(encode(1002, {'result': 0}), bytes.fromhex('ea030b0000000000000000'))
        packet = encode(3001, {'id': 68, 'data': 'abc'})
        self.assertEqual(packet, struct.pack('<HIIB', 3001, 15, 0, 68) + b'abc\0')
        self.assertEqual(decode(packet)[2], {'id': 68, 'data': 'abc'})

    def test_double_role_id_and_all_fields(self):
        packet = encode(1017, {'role_id': 123.0, 'role_name': '本地行者', 'level': 1})
        self.assertEqual(packet[18:26], struct.pack('<d', 123.0))
        data = decode(packet)[2]
        self.assertEqual(len(data), 307)
        self.assertEqual(data['role_name'], '本地行者')

    def test_invalid_packets_rejected(self):
        good = encode(1002, {'result': 0})
        for packet in (b'', good[:-1], good + b'\0', struct.pack('<HII', 3001, 12, 0) + b'Da'):
            with self.assertRaises(ValueError):
                decode(packet)
        with self.assertRaises(ValueError):
            encode(1001, {'account': 'a' * 33})

    def test_ticket_replay_and_persistence(self):
        with tempfile.TemporaryDirectory() as directory:
            backend = Backend(Path(directory), 18770, lambda *a, **k: None)
            response = backend.respond(encode(3001, {'id': 68, 'data': '{access_token="' + backend.token + '"}'}), {})[0]
            ticket = decode(response)[2]
            login = encode(1001, {k: ticket[k] for k in ('auth_key', 'seed', 'account')})
            state = {}
            replies = backend.respond(login, state)
            self.assertEqual([decode(r)[0] for r in replies[:5]], [1002, 2998, 1017, 1034, 1035])
            self.assertIn(1046, [decode(r)[0] for r in replies])
            self.assertTrue(state['authenticated'])
            self.assertEqual(decode(backend.respond(login, {})[0])[2]['result'], 1)
            token = backend.token
            role = backend.profile()
            role['role_name'] = '测试存档'
            backend.save(role)
            backend.close()
            backend = Backend(Path(directory), 18770, lambda *a, **k: None)
            self.assertEqual(backend.token, token)
            self.assertEqual(backend.profile()['role_name'], '测试存档')
            self.assertEqual(backend.profile()['corteges'][0]['type'], 5004)
            with self.assertRaises(ValueError):
                backend.respond(encode(1018, {}), {})
            backend.close()

    def test_literal_credentials_only(self):
        self.assertEqual(login_fields('{loss_plus=-10, result=1}'), {'loss_plus': -10, 'result': 1})
        self.assertEqual(login_fields('{loss_plus=-os.execute("false")}'), {})
        self.assertEqual(login_fields('{["access_token"]="local-test"}')['access_token'], 'local-test')
        for value in ('{access_token=os.getenv("HOME")}', '{access_token="a",access_token="b"}',
                      '{note="access_token=\\"local-test\\""}; do_something()'):
            self.assertEqual(login_fields(value), {})

    def test_auth_reconnect_queries_and_expired_ticket(self):
        with tempfile.TemporaryDirectory() as directory:
            backend = Backend(Path(directory), 18770, lambda *a, **k: None)
            try:
                bad = backend.respond(encode(3001, {'id': 68, 'data': '{access_token="wrong"}'}), {})
                self.assertEqual(decode(bad[0])[2]['server_port'], 0)
                request = encode(3001, {'id': 68, 'data': '{access_token="' + backend.token + '"}'})
                ticket = decode(backend.respond(request, {})[0])[2]
                backend.tickets[ticket['auth_key']] = (ticket['seed'], 0)
                login = encode(1001, {k: ticket[k] for k in ('auth_key', 'seed', 'account')})
                self.assertEqual(decode(backend.respond(login, {})[0])[2]['result'], 1)
                state = {}
                reconnect = encode(1016, dict(account='local-player', random_key=backend.random_key))
                replies = backend.respond(reconnect, state)
                self.assertTrue(state['authenticated'])
                self.assertEqual([decode(r)[0] for r in replies[:5]], [2996, 2998, 1017, 1034, 1035])
                self.assertTrue(decode(replies[2])[2]['reconnect'])
                self.assertEqual(decode(replies[2])[2]['cortege_count'], 2)
                self.assertEqual(decode(replies[3])[2]['cortege_count'], 1)
                next_server_serial = 200001
                for mid, values, ids in [(1018, {'serial_num': 123}, [1020, 1023, 1032, 1106]),
                                         (1094, {'serial_num': 124, 'flag': 1}, [1095, 1106]),
                                         (1033, {'serial_num': 125, 'flag': 3}, [1034, 1035, 1046, 2998, 1106])]:
                    replies = [decode(r) for r in backend.respond(encode(mid, values), state)]
                    self.assertEqual([r[0] for r in replies], ids)
                    self.assertEqual([r[2]['serial_num'] for r in replies],
                                     list(range(next_server_serial, next_server_serial + len(ids))))
                    self.assertEqual(replies[-1][2]['req_serial_num'], values['serial_num'])
                    next_server_serial += len(ids)
                    if mid == 1033:
                        self.assertTrue(replies[1][2]['first_send'])
                        self.assertEqual(replies[1][2]['attach_list'][0]['type_id'], 209)
                        self.assertEqual(replies[-2][2]['id'], 1)
                        self.assertEqual(login_fields(replies[-2][2]['data']), {'flag': 3})
                heartbeat = backend.respond(encode(2999, {}), state)
                self.assertEqual(decode(heartbeat[0])[2]['random_key'], backend.random_key)
            finally:
                backend.close()

    def test_bootstrap_initializes_formation_and_innate_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            backend = Backend(Path(directory), 18770, lambda *a, **k: None)
            try:
                replies = [decode(r) for r in backend.bootstrap()]
                self.assertEqual([r[0] for r in replies[:4]], [2998, 1017, 1034, 1035])
                self.assertEqual(replies[0][2]['id'], 80)
                config = login_fields(replies[0][2]['data'])
                self.assertIs(config['config_end'], True)
                # Enabled Bagua must provide complete original-client config.
                self.assertIs(config[14]['is_open'], True)
                self.assertIsInstance(config[14]['cheer_level_limit'], dict)
                self.assertEqual(len(config[10]['cheap_item_list']), 7)
                self.assertEqual(len(config[10]['rich_item_list']), 8)
                self.assertEqual(config[10]['limit_item_list'], {})
                self.assertEqual(len(config[10]['panic_buy_list']['activity_data']['sale_item']), 2)
                self.assertEqual(replies[1][2]['cortege_count'], 2)
                self.assertEqual(replies[2][2]['cortege_count'], 1)
                self.assertEqual(replies[2][2]['cortege_list'][0]['order'], 1)
                self.assertTrue(replies[3][2]['first_send'])
                self.assertEqual(replies[3][2]['attach_count'], 1)
                self.assertEqual(replies[3][2]['attach_list'][0]['type_id'], 209)
                self.assertEqual(replies[3][2]['attach_list'][0]['protogenic'], 1)
            finally:
                backend.close()

    def test_existing_save_gains_formation_slots_without_replacing_progress(self):
        with tempfile.TemporaryDirectory() as directory:
            backend = Backend(Path(directory), 18770, lambda *a, **k: None)
            legacy = dict(role_name='已有角色', level=1, gold_coin=37, silver_coin=4200,
                          corteges=[dict(id=42.0, type=5004, order=1, level=3)],
                          attachments=[dict(id=91.0, type_id=1001, count=7)],
                          local_note='保留存档中的额外字段')
            backend.save(legacy)
            backend.close()
            backend = Backend(Path(directory), 18770, lambda *a, **k: None)
            try:
                migrated = backend.profile()
                for key in ('role_name', 'level', 'gold_coin', 'silver_coin', 'local_note'):
                    self.assertEqual(migrated[key], legacy[key])
                self.assertEqual(migrated['attachments'][0], legacy['attachments'][0])
                self.assertEqual(migrated['corteges'][0]['id'], 42.0)
                self.assertEqual(migrated['corteges'][0]['level'], 3)
                self.assertEqual(migrated['cortege_count'], 2)
                self.assertEqual(migrated['attachments'][1]['type_id'], 209)
                stored = json.loads(backend.db.execute(
                    'SELECT data FROM roles WHERE account=?', ('local-player',)).fetchone()[0])
                self.assertEqual(stored, migrated)
                self.assertEqual(backend.profile(), migrated)
            finally:
                backend.close()

    def test_serial_zero_queries_do_not_consume_server_sequence_or_send_done(self):
        with tempfile.TemporaryDirectory() as directory:
            backend = Backend(Path(directory), 18770, lambda *a, **k: None)
            try:
                state = {'authenticated': True}
                for mid, values, ids in [(1018, {}, [1020, 1023, 1032]),
                                         (1094, {'flag': 1}, [1095]),
                                         (1033, {'flag': 3}, [1034, 1035, 1046, 2998])]:
                    replies = [decode(r) for r in backend.respond(encode(mid, values), state)]
                    self.assertEqual([r[0] for r in replies], ids)
                    self.assertTrue(all(r[2]['serial_num'] == 0 for r in replies))
                numbered = backend.respond(encode(1018, {'serial_num': 1}), state)
                self.assertEqual(decode(numbered[0])[2]['serial_num'], 200001)
            finally:
                backend.close()

    def test_missing_response_replay_preserves_bytes_and_sequence_after_reconnect(self):
        with tempfile.TemporaryDirectory() as directory:
            backend = Backend(Path(directory), 18770, lambda *a, **k: None)
            try:
                original = backend.respond(encode(1033, {'serial_num': 31, 'flag': 3}),
                                           {'authenticated': True})
                state = {}
                backend.respond(encode(1016, dict(account='local-player', random_key=backend.random_key)),
                                state)
                # If the first numbered response was lost, the client still
                # reports zero and needs the whole original response batch.
                self.assertEqual(backend.respond(encode(1105, {'req_serial_num': 0}), state),
                                 original)
                replay = backend.respond(encode(1105, {'req_serial_num': 200001}), state)
                self.assertEqual(replay, original[1:])
                self.assertEqual(backend.respond(encode(1105, {'req_serial_num': 200000}), state),
                                 original)
                following = backend.respond(encode(1094, {'serial_num': 32}), state)
                self.assertEqual([decode(r)[2]['serial_num'] for r in following], [200006, 200007])
                self.assertEqual(decode(following[-1])[2]['req_serial_num'], 32)
            finally:
                backend.close()

    def test_empty_replay_completes_reconnect_wait_without_a_client_request(self):
        with tempfile.TemporaryDirectory() as directory:
            backend = Backend(Path(directory), 18770, lambda *a, **k: None)
            try:
                state = {'authenticated': True}
                first = backend.respond(encode(1105, {'req_serial_num': 0}), state)
                self.assertEqual([decode(r) for r in first],
                                 [(1106, 0, dict(serial_num=200001, req_serial_num=0))])
                caught_up = backend.respond(encode(1105, {'req_serial_num': 200001}), state)
                self.assertEqual([decode(r) for r in caught_up],
                                 [(1106, 0, dict(serial_num=200002, req_serial_num=0))])
                replay = backend.respond(encode(1105, {'req_serial_num': 200000}), state)
                self.assertEqual(replay, first + caught_up)
            finally:
                backend.close()

    def test_struct_array_wire_and_bounds(self):
        data = dict(serial_num=7, first_send=True, tollgate_count=1,
                    tollgate_list=[dict(tollgate_type=1, map_id=1, tollgate_id=101)])
        packet = encode(1020, data)
        self.assertEqual(packet, struct.pack('<HIII?BBB IHHB', 1020, 27, 0, 7, True, 1, 1, 1, 101, 0, 0, 0))
        self.assertEqual(decode(packet)[2]['tollgate_list'][0]['tollgate_id'], 101)
        with self.assertRaises(ValueError):
            encode(1020, dict(data, tollgate_count=0))
        truncated = bytearray(packet[:-1])
        struct.pack_into('<I', truncated, 2, len(truncated))
        with self.assertRaises(ValueError):
            decode(bytes(truncated))

    def test_inventory_array_accepts_lowercase_byte_count_and_rejects_truncation(self):
        self.assertEqual(dict(fields(1035))['attach_count'], 'b')
        empty = dict(serial_num=17, first_send=True, attach_count=0, attach_list=[])
        self.assertEqual(encode(1035, empty), struct.pack('<HIII?B', 1035, 16, 0, 17, True, 0))
        self.assertEqual(decode(encode(1035, empty))[2], empty)

        items = [dict(id=51.0, attach_type=1, type_id=1001, count=3, level=1),
                 dict(id=52.0, attach_type=2, type_id=209, count=1, owner_id=42.0)]
        data = dict(empty, attach_count=2, attach_list=items)
        packet = encode(1035, data)
        decoded = decode(packet)[2]
        self.assertEqual(decoded['attach_count'], 2)
        for actual, expected in zip(decoded['attach_list'], items):
            for key, value in expected.items():
                self.assertEqual(actual[key], value)
        with self.assertRaisesRegex(ValueError, 'Array count mismatch'):
            encode(1035, dict(data, attach_count=1))
        truncated = bytearray(packet[:-1])
        struct.pack_into('<I', truncated, 2, len(truncated))
        with self.assertRaisesRegex(ValueError, 'Truncated field'):
            decode(bytes(truncated))


class TLSAndWireTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        path = Path(self.temp.name)
        self.events = []
        emit = lambda kind, **row: self.events.append(dict(kind=kind, **row))
        self.tls = LocalTLS(path / 'tls')
        self.backend = Backend(path / 'data', 18770, emit)
        self.server = LandingServer(0, b'cached-list', emit, backend=self.backend, tls=self.tls)
        await self.server.start()
        self.port = self.server.server.sockets[0].getsockname()[1]

    async def asyncTearDown(self):
        await self.server.close()
        self.backend.close()
        self.temp.cleanup()

    async def test_verified_tls_with_dynamic_sni(self):
        context = ssl.create_default_context(cafile=str(self.tls.ca))
        reader, writer = await asyncio.open_connection('127.0.0.1', self.port, ssl=context,
                                                      server_hostname='sdk.example.invalid')
        writer.write(b'GET /__redirect_health HTTP/1.1\r\nHost: sdk.example.invalid\r\n\r\n')
        await writer.drain()
        response = await reader.read()
        self.assertIn(HEALTH, response)
        self.assertTrue(any(e['kind'] == 'tls_established' for e in self.events))
        writer.close()
        await writer.wait_closed()

    async def test_untrusted_certificate_rejected(self):
        with self.assertRaises(ssl.SSLCertVerificationError):
            await asyncio.open_connection('127.0.0.1', self.port, ssl=ssl.create_default_context(),
                                          server_hostname='sdk.example.invalid')

    async def test_large_tls_response(self):
        self.server.server_list = b'x' * 59531
        context = ssl.create_default_context(cafile=str(self.tls.ca))
        reader, writer = await asyncio.open_connection('127.0.0.1', self.port, ssl=context,
                                                      server_hostname='list.example.invalid')
        writer.write(b'GET /update/jgb/p360_na/server_list.txt HTTP/1.1\r\nHost: list.example.invalid\r\n\r\n')
        await writer.drain()
        response = await reader.read()
        self.assertEqual(response.split(b'\r\n\r\n', 1)[1], self.server.server_list)
        writer.close()
        await writer.wait_closed()

    async def test_unsupported_support_endpoint_is_json_error(self):
        reader, writer = await asyncio.open_connection('127.0.0.1', self.port)
        writer.write(b'GET /find_problem HTTP/1.1\r\nHost: jgbkf.syyx.com\r\n\r\n')
        await writer.drain()
        response = await reader.read()
        self.assertTrue(response.startswith(b'HTTP/1.1 501'))
        body = json.loads(response.split(b'\r\n\r\n', 1)[1])
        self.assertEqual(body['ok'], 0)
        self.assertEqual(body['data'], [])
        writer.close()
        await writer.wait_closed()

    async def test_fragmented_binary_ls_response(self):
        reader, writer = await asyncio.open_connection('127.0.0.1', self.port)
        packet = encode(3001, {'id': 68, 'data': '{access_token="' + self.backend.token + '"}'})
        for part in (packet[:3], packet[3:10], packet[10:]):
            writer.write(part)
            await writer.drain()
            await asyncio.sleep(.01)
        header = await asyncio.wait_for(reader.readexactly(10), 3)
        size = struct.unpack_from('<I', header, 2)[0]
        response = header + await reader.readexactly(size - 10)
        self.assertEqual(decode(response)[0], 3002)
        self.assertEqual(decode(response)[2]['server_ip'], '127.0.0.1')
        writer.close()
        await writer.wait_closed()
