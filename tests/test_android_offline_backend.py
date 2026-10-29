"""Android payload closure and real loopback/login/save restart integration."""
import ast
import hashlib
import http.client
import json
from pathlib import Path
import re
import socket
import sqlite3
import ssl
import subprocess
import sys
import tempfile
import unittest
import zipfile

from offline_android import backend
from offline_android.pack_payload import ROOT, build_payload, collect_files, verify_payload
from network_redirect.protocol import HEADER, decode, encode


class PayloadTests(unittest.TestCase):
    def test_all_runtime_imports_resources_and_original_rules_are_included(self):
        files = collect_files()
        self.assertEqual(sum(name.endswith('.csv') and name.startswith('analysis/configs/')
                             for name in files), len(list((ROOT / 'analysis/configs').rglob('*.csv'))))
        self.assertEqual(sum(name.startswith('server_config/') for name in files),
                         len(list((ROOT / 'server_config').glob('*.json'))))
        self.assertIn('network_redirect/system_mail.py', files)
        for name, path in files.items():
            self.assertNotIn('.runtime/', name)
            self.assertNotIn('game.sqlite3', name)
            if not name.startswith('network_redirect/') or path.suffix != '.py':
                continue
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.ImportFrom) and node.level == 1:
                    modules = [node.module] if node.module else [alias.name for alias in node.names]
                    for module in modules:
                        self.assertIn('network_redirect/' + module.split('.')[0] + '.py', files)
        catalog = json.loads((ROOT / 'analysis/npc_design/players/catalog.json').read_text())
        for entry in catalog['players']:
            self.assertIn(entry['source_file'], files)

    def test_packed_program_boots_in_isolation_and_has_no_player_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / 'payload.zip'
            manifest = build_payload(archive)
            program = root / 'files/program' / manifest['bundle_id']
            with zipfile.ZipFile(archive) as source:
                source.extractall(program)
            self.assertEqual(verify_payload(program)['bundle_id'], manifest['bundle_id'])
            script = '''
import pathlib, sys
sys.path.insert(0, sys.argv[1])
from offline_android.backend import start, stop
from network_redirect import npc_players
state = start(sys.argv[2], sys.argv[1], 0)
assert state['ready']
assert 'luaparser.ast' in sys.modules
assert not list(pathlib.Path(sys.argv[2], 'cache').iterdir())
assert len(npc_players.catalog()) > 1700
assert npc_players.get(next(iter(npc_players.catalog()))) is not None
import network_redirect.system_mail
stop()
assert pathlib.Path(sys.argv[2], 'save/game.sqlite3').is_file()
'''
            result = subprocess.run([sys.executable, '-I', '-c', script, str(program), str(root / 'files')],
                                    cwd=tmp, capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(list(program.rglob('*.sqlite3')))
            self.assertFalse(list(program.rglob('*.pyc')))


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.files = Path(self.tmp.name)
        self.state = backend.start(self.files, ROOT, port=0)
        self.port = self.state['port']

    def tearDown(self):
        backend.stop()
        self.tmp.cleanup()

    def request(self, path, payload=None, csrf='', cookie='', tls=False):
        if tls:
            context = ssl.create_default_context(cafile=str(ROOT / 'offline_android/tls/ca.pem'))
            connection = http.client.HTTPSConnection('127.0.0.1', self.port, context=context, timeout=10)
        else:
            connection = http.client.HTTPConnection('127.0.0.1', self.port, timeout=10)
        body = json.dumps(payload) if payload is not None else None
        headers = {'X-Local-CSRF': csrf, 'Cookie': cookie}
        connection.request('POST' if payload is not None else 'GET', path, body, headers)
        response = connection.getresponse()
        result = response.status, dict(response.getheaders()), response.read()
        connection.close()
        return result

    def csrf(self):
        page = self.request('/local-login')[2].decode()
        return re.search(r"setRequestHeader\('X-Local-CSRF','([^']+)'\)", page)[1]

    def packet(self, connection):
        def exact(size):
            result = b''
            while len(result) < size:
                data = connection.recv(size - len(result))
                if not data:
                    raise EOFError('game connection closed')
                result += data
            return result
        head = exact(HEADER.size)
        return decode(head + exact(HEADER.unpack(head)[1] - HEADER.size))

    def test_http_tls_loopback_and_transport_only_server_list_rewrite(self):
        for tls in (False, True):
            status, _, body = self.request('/__redirect_health', tls=tls)
            self.assertEqual(status, 200)
            self.assertIn(b'JGBOL_LOCAL_REDIRECT_OK', body)
        from fetch_server_list import parse_server_list
        baseline = parse_server_list((ROOT / 'analysis/server_lists/server_list.raw.txt').read_bytes())
        actual = parse_server_list(self.request('/update/jgb/p360_a/server_list.txt')[2])
        self.assertEqual(actual[0], baseline[0])
        self.assertEqual(actual[2], baseline[2])
        for before, after in zip(baseline[1], actual[1]):
            self.assertEqual(after, dict(before, ip='127.0.0.1', port=self.port))
        self.assertEqual(self.state['database'], str((self.files / 'save/game.sqlite3').resolve()))
        with sqlite3.connect(self.files / 'save/game.sqlite3') as db:
            self.assertEqual(db.execute('SELECT count(*) FROM roles').fetchone()[0], 0)
            self.assertEqual(db.execute('SELECT count(*) FROM accounts').fetchone()[0], 0)
        self.assertTrue(backend.start(self.files, ROOT)['ready'])

    def test_real_login_and_account_save_survive_service_restart(self):
        csrf = self.csrf()
        result = self.request('/local-auth', dict(action='register', username='android_player',
                              password='android-pass-123', confirm='android-pass-123', remember=True), csrf)
        payload = json.loads(result[2])
        self.assertTrue(payload['ok'])
        cookie = result[1]['Set-Cookie'].split(';', 1)[0]
        with socket.create_connection(('127.0.0.1', self.port), timeout=15) as connection:
            connection.sendall(encode(3001, dict(id=68, data='{access_token="' + payload['token'] + '"}')))
            _, _, ticket = self.packet(connection)
            self.assertEqual(ticket['server_ip'], '127.0.0.1')
            self.assertEqual(ticket['server_port'], self.port)
            connection.sendall(encode(1001, {key: ticket[key] for key in ('auth_key', 'seed', 'account')}))
            mid, _, login = self.packet(connection)
            self.assertEqual((mid, login['result']), (1002, 0))
            connection.shutdown(socket.SHUT_WR)
            while connection.recv(65536):
                pass
        backend.stop()
        database = self.files / 'save/game.sqlite3'
        with sqlite3.connect(database) as db:
            row = db.execute('SELECT data FROM roles WHERE account=?', ('android_player',)).fetchone()
            self.assertIsNotNone(row)
            original = json.loads(row[0])
            original['gold_coin'] = 4321
            db.execute('UPDATE roles SET data=? WHERE account=?', (json.dumps(original), 'android_player'))
        self.state = backend.start(self.files, ROOT, port=0)
        self.port = self.state['port']
        resumed = json.loads(self.request('/local-auth', {'action': 'resume'}, self.csrf(), cookie)[2])
        self.assertTrue(resumed['ok'])
        backend.stop()
        with sqlite3.connect(database) as db:
            saved = json.loads(db.execute('SELECT data FROM roles WHERE account=?', ('android_player',)).fetchone()[0])
            self.assertEqual(saved['gold_coin'], 4321)

    def test_existing_corrupt_save_is_reported_without_replacement(self):
        backend.stop()
        database = self.files / 'save/game.sqlite3'
        database.write_bytes(b'broken-save-must-not-be-replaced')
        before = hashlib.sha256(database.read_bytes()).hexdigest()
        with self.assertRaisesRegex(RuntimeError, 'not a database'):
            backend.start(self.files, ROOT, port=0)
        self.assertEqual(hashlib.sha256(database.read_bytes()).hexdigest(), before)


if __name__ == '__main__':
    unittest.main()
