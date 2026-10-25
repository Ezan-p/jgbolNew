"""Password accounts and isolated protocol sessions for the local game."""
import hashlib
import hmac
import json
import re
import secrets
import sqlite3
import time

from .backend import Backend, login_fields
from .protocol import decode, encode


class Accounts:
    def __init__(self, directory, port, emit):
        self.directory, self.port, self.emit = directory, port, emit
        self.base = Backend(directory, port, emit)
        self.db = self.base.db
        self.db.execute('CREATE TABLE IF NOT EXISTS accounts (name TEXT PRIMARY KEY, salt BLOB NOT NULL, digest BLOB NOT NULL)')
        self.db.execute('CREATE TABLE IF NOT EXISTS remembered_logins (digest TEXT PRIMARY KEY, name TEXT NOT NULL, expires REAL NOT NULL)')
        self.db.commit()
        self.summon_rules = self.base.summon_rules
        self.csrf = secrets.token_urlsafe(32)
        self.sessions = {}
        self.pending = {}
        self.backends = {}
        self.attempts = []
        self.token = ''  # No automatic/shared credential is exposed to the client.

    def authenticate(self, data, remembered=''):
        action = data.get('action')
        remembered = remembered if isinstance(remembered, str) else ''
        cookie_digest = hashlib.sha256(remembered.encode()).hexdigest()
        if action == 'forget':
            with self.db:
                self.db.execute('DELETE FROM remembered_logins WHERE digest=?', (cookie_digest,))
            self.sessions.clear()
            self.pending.clear()
            return {'ok': True, 'remember_token': ''}
        if action == 'resume':
            row = self.db.execute(
                'SELECT name FROM remembered_logins WHERE digest=? AND expires>?',
                (cookie_digest, time.time())).fetchone()
            if not row or not self.db.execute('SELECT 1 FROM accounts WHERE name=?', (row[0],)).fetchone():
                raise ValueError('请登录本地账号')
            return self.start_session(row[0])

        now = time.monotonic()
        self.attempts = [t for t in self.attempts if now - t < 60]
        if len(self.attempts) >= 12:
            raise ValueError('操作过于频繁，请一分钟后再试')
        self.attempts.append(now)
        name, password = data.get('username', ''), data.get('password', '')
        if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9_]{3,24}', name):
            raise ValueError('账号须为 3–24 位字母、数字或下划线')
        name = name.lower()
        if not isinstance(password, str) or not 8 <= len(password) <= 128:
            raise ValueError('密码须为 8–128 个字符')
        action = data.get('action')
        if action not in ('login', 'register'):
            raise ValueError('不支持的操作')
        row = self.db.execute('SELECT salt,digest FROM accounts WHERE name=?', (name,)).fetchone()
        if action == 'register':
            if password != data.get('confirm'):
                raise ValueError('两次输入的密码不一致')
            if row:
                raise ValueError('该账号已注册')
            salt = secrets.token_bytes(16)
            digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 600000)
            with self.db:
                self.db.execute('INSERT INTO accounts VALUES (?,?,?)', (name, salt, digest))
                if data.get('inherit') is True:
                    claimed = self.db.execute("SELECT value FROM settings WHERE key='legacy_claimed'").fetchone()
                    if claimed:
                        raise ValueError('旧存档已绑定其他账号，请取消继承选项')
                    legacy = self.db.execute("SELECT data FROM roles WHERE account='local-player'").fetchone()
                    if not legacy:
                        raise ValueError('没有可继承的旧存档，请取消继承选项')
                    role = json.loads(legacy[0])
                    for key in ('register_account', 'pf_account', 'mobile_account'):
                        role[key] = name
                    self.db.execute('INSERT INTO roles VALUES (?,?)', (name, json.dumps(role, ensure_ascii=False)))
                    self.db.execute('INSERT INTO settings VALUES (?,?)', ('legacy_claimed', name))
        else:
            salt = row[0] if row else bytes(16)
            digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 600000)
            if not row or not hmac.compare_digest(digest, row[1]):
                raise ValueError('账号或密码错误')
        remembered_token = ''
        with self.db:
            self.db.execute('DELETE FROM remembered_logins WHERE digest=? OR name=? OR expires<=?',
                            (cookie_digest, name, time.time()))
            if data.get('remember') is True:
                remembered_token = secrets.token_urlsafe(32)
                self.db.execute('INSERT INTO remembered_logins VALUES (?,?,?)',
                                (hashlib.sha256(remembered_token.encode()).hexdigest(), name,
                                 time.time() + 30 * 86400))
        result = self.start_session(name)
        result['remember_token'] = remembered_token
        return result

    def start_session(self, name):
        now = time.monotonic()
        # Only one game is on screen. Invalidate old sockets, tickets and reconnect
        # secrets before handing the native client a different identity.
        for backend in self.backends.values():
            backend.tickets.clear()
            backend.random_key = secrets.randbelow(0x7ffffffe) + 1
        self.sessions.clear()
        self.pending.clear()
        token = secrets.token_urlsafe(32)
        if name not in self.backends:
            self.backends[name] = Backend(self.directory, self.port, self.emit, account=name)
        backend = self.backends[name]
        backend.token = token
        self.sessions[token] = (backend, now + 12 * 3600)
        return {'ok': True, 'token': token, 'username': name}

    def respond(self, packet, state):
        mid, _, data = decode(packet)
        self.sessions = {k: v for k, v in self.sessions.items() if v[1] > time.monotonic()}
        if mid == 3001:
            token = login_fields(data['data']).get('access_token')
            session = self.sessions.get(token) if isinstance(token, str) else None
            if not session:
                return [encode(3002, dict(auth_key=1, seed=0, server_port=0, account='', server_ip=''))]
            backend = session[0]
            replies = backend.respond(packet, {})
            ticket = decode(replies[0])[2]['auth_key']
            self.pending = {k: v for k, v in self.pending.items() if v[1] > time.monotonic()}
            self.pending[ticket] = (backend, time.monotonic() + 60)
            return replies
        if mid == 1001:
            entry = self.pending.pop(data['auth_key'], None)
            if not entry or entry[1] <= time.monotonic():
                return [encode(1002, {'result': 1})]
            state.clear()
            state['backend'] = entry[0]
            state['token'] = entry[0].token
        elif mid == 1016:
            backend = self.backends.get(data['account'])
            if not backend or backend.token not in self.sessions:
                return [encode(2996, {'ret': 1})]
            state.clear()
            state['backend'], state['token'] = backend, backend.token
        backend = state.get('backend')
        if not backend or state.get('token') not in self.sessions:
            raise ValueError('登录已失效，请重新登录')
        return backend.respond(packet, state)

    def close(self):
        for backend in self.backends.values():
            backend.close()
        self.base.close()
