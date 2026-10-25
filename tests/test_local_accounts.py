import asyncio
import json
from pathlib import Path
import tempfile
import unittest

from network_redirect.accounts import Accounts
from network_redirect.protocol import encode, decode
from network_redirect.server import LandingServer


class AccountTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.auth = Accounts(Path(self.tmp.name), 18770, lambda *a, **k: None)

    def tearDown(self):
        self.auth.close()
        self.tmp.cleanup()

    def auth_as(self, name, action='register', **kw):
        return self.auth.authenticate(dict(username=name, password='test-pass-123',
                                          confirm='test-pass-123', action=action, **kw))

    def enter(self, token):
        ticket = decode(self.auth.respond(encode(3001, dict(id=68, data='{access_token="'+token+'"}')), {})[0])[2]
        packet = encode(1001, {k: ticket[k] for k in ('auth_key', 'seed', 'account')})
        state = {}
        replies = self.auth.respond(packet, state)
        self.assertEqual(decode(replies[0])[2]['result'], 0)
        self.assertEqual(decode(self.auth.respond(packet, {})[0])[2]['result'], 1)
        return state

    def test_accounts_save_reconnect_switch_and_restart(self):
        a = self.enter(self.auth_as('Alice')['token'])
        backend = a['backend']
        role = backend.profile(); role['gold_coin'] = 4321; backend.save(role)
        reconnect = encode(1016, dict(account='alice', random_key=backend.random_key))
        self.assertEqual(decode(self.auth.respond(reconnect, {})[0])[2]['ret'], 0)
        b = self.enter(self.auth_as('Bob')['token'])
        self.assertEqual(b['backend'].profile()['gold_coin'], 0)
        with self.assertRaises(ValueError):
            self.auth.respond(encode(2999, {}), a)
        self.assertEqual(decode(self.auth.respond(reconnect, {})[0])[2]['ret'], 1)
        self.auth.close()
        self.auth = Accounts(Path(self.tmp.name), 18770, lambda *a, **k: None)
        a = self.enter(self.auth_as('ALICE', 'login')['token'])
        self.assertEqual(a['backend'].profile()['gold_coin'], 4321)
        self.assertNotEqual(a['backend'].random_key, b['backend'].random_key)

    def test_relogin_clears_business_replay_caches(self):
        state = self.enter(self.auth_as('alice')['token'])
        backend = state['backend']
        backend.reborn_replies[100] = ('old', [])
        backend.last_reborn_serial = 100
        state = self.enter(self.auth_as('alice', 'login')['token'])
        self.assertEqual(state['backend'].reborn_replies, {})
        self.assertEqual(state['backend'].last_reborn_serial, 0)

    def test_password_validation_and_hashes(self):
        self.auth_as('alice')
        with self.assertRaisesRegex(ValueError, '已注册'):
            self.auth_as('ALICE')
        for password in ('wrong-pass', 'short'):
            with self.assertRaises(ValueError):
                self.auth.authenticate(dict(action='login', username='alice', password=password))
        with self.assertRaises(ValueError):
            self.auth.authenticate(dict(action='register', username='../evil', password='test-pass-123'))
        raw = (Path(self.tmp.name)/'game.sqlite3').read_bytes()
        self.assertNotIn(b'test-pass-123', raw)
        self.assertEqual(self.auth.db.execute('SELECT count(*) FROM accounts').fetchone()[0], 1)

    def test_expired_tokens_and_tickets(self):
        token = self.auth_as('alice')['token']
        backend, _ = self.auth.sessions[token]
        self.auth.sessions[token] = (backend, 0)
        reply = self.auth.respond(encode(3001, dict(id=68, data='{access_token="'+token+'"}')), {})
        self.assertEqual(decode(reply[0])[2]['server_port'], 0)

    def test_legacy_claim_is_optional_atomic_and_once(self):
        old = self.auth.base.profile(); old['gold_coin'] = 987; self.auth.base.save(old)
        self.auth_as('fresh')
        self.assertEqual(self.auth.backends['fresh'].profile()['gold_coin'], 0)
        self.auth_as('alice', inherit=True)
        self.assertEqual(self.auth.backends['alice'].profile()['gold_coin'], 987)
        self.assertEqual(self.auth.base.profile()['gold_coin'], 987)
        with self.assertRaises(ValueError):
            self.auth_as('bob', inherit=True)
        self.assertIsNone(self.auth.db.execute("SELECT name FROM accounts WHERE name='bob'").fetchone())

    def test_remember_survives_restart_and_expires(self):
        result = self.auth_as('alice', remember=True)
        credential = result['remember_token']
        self.assertNotIn(credential.encode(), (Path(self.tmp.name)/'game.sqlite3').read_bytes())
        state = self.enter(result['token'])
        role = state['backend'].profile(); role['gold_coin'] = 321; state['backend'].save(role)
        self.auth.close()
        self.auth = Accounts(Path(self.tmp.name), 18770, lambda *a, **k: None)
        resumed = self.auth.authenticate({'action': 'resume'}, credential)
        self.assertEqual(self.enter(resumed['token'])['backend'].profile()['gold_coin'], 321)
        with self.auth.db:
            self.auth.db.execute('UPDATE remembered_logins SET expires=0')
        with self.assertRaises(ValueError):
            self.auth.authenticate({'action': 'resume'}, credential)

    def test_forget_and_unchecked_login_revoke_remembered_login(self):
        credential = self.auth_as('alice', remember=True)['remember_token']
        self.auth.authenticate({'action': 'forget'}, credential)
        with self.assertRaises(ValueError):
            self.auth.authenticate({'action': 'resume'}, credential)
        credential = self.auth_as('alice', 'login', remember=True)['remember_token']
        self.auth_as('alice', 'login', remember=False)
        with self.assertRaises(ValueError):
            self.auth.authenticate({'action': 'resume'}, credential)
        self.assertEqual(self.auth.db.execute('SELECT count(*) FROM remembered_logins').fetchone()[0], 0)

    def test_rate_limit(self):
        for i in range(12):
            with self.assertRaises(ValueError):
                self.auth.authenticate({})
        with self.assertRaisesRegex(ValueError, '频繁'):
            self.auth_as('alice')


class AuthHTTPTests(unittest.IsolatedAsyncioTestCase):
    async def test_form_csrf_and_registration(self):
        with tempfile.TemporaryDirectory() as tmp:
            auth = Accounts(Path(tmp), 0, lambda *a, **k: None)
            server = LandingServer(0, b'', lambda *a, **k: None, backend=auth)
            await server.start()
            async def request(path, body=None, csrf='', cookie=''):
                r, w = await asyncio.open_connection('127.0.0.1', server.port)
                raw = json.dumps(body).encode() if body else b''
                method = 'POST' if body else 'GET'
                w.write((f'{method} {path} HTTP/1.1\r\nHost: 127.0.0.1:{server.port}\r\nContent-Length: {len(raw)}\r\nX-Local-CSRF: {csrf}\r\nCookie: {cookie}\r\n\r\n').encode()+raw)
                await w.drain(); response = await r.read(); w.close(); await w.wait_closed()
                return response
            try:
                page = await request('/local-login')
                self.assertIn(auth.csrf.encode(), page)
                payload = dict(action='register', username='alice', password='test-pass-123', confirm='test-pass-123', remember=True)
                self.assertEqual(await request('/local-auth', payload), b'')
                response = await request('/local-auth', payload, auth.csrf)
                result = json.loads(response.split(b'\r\n\r\n')[1])
                self.assertTrue(result['ok'])
                self.assertNotIn('remember_token', result)
                cookie_line = next(line for line in response.split(b'\r\n') if line.startswith(b'Set-Cookie:'))
                self.assertIn(b'HttpOnly', cookie_line)
                cookie = cookie_line.decode().split(': ', 1)[1].split(';', 1)[0]
                resumed = await request('/local-auth', {'action': 'resume'}, auth.csrf, cookie)
                self.assertTrue(json.loads(resumed.split(b'\r\n\r\n')[1])['ok'])
                forgotten = await request('/local-auth', {'action': 'forget'}, auth.csrf, cookie)
                self.assertIn(b'Max-Age=0', forgotten)
                failed = await request('/local-auth', {'action': 'resume'}, auth.csrf, cookie)
                self.assertFalse(json.loads(failed.split(b'\r\n\r\n')[1])['ok'])
                self.assertIn(b'Max-Age=0', failed)
            finally:
                await server.close(); auth.close()
