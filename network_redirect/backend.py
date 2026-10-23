"""Local-only account and LS/BS bootstrap. Never contacts a channel service."""
from collections import deque
import csv
import json
import os
from pathlib import Path
import secrets
import sqlite3
import time

from .protocol import encode, decode


# The client initializes these sections together in data.set_g_new_config.
# Explicitly disable unavailable local features rather than leaving their UI
# state uninitialized (notably cheerSquadUI.canJoin's Lv/isOpen fields).
CLIENT_CONFIG = '''{
    [4]={party_top_list={},pay_consume_gold=0},
    [5]={},
    [10]={panic_buy_list={},cheap_item_list={},rich_item_list={},limit_item_list={},
          item_begin_time=0,item_end_time=0,server_time=0},
    [11]={open_flag=false,min_role_level=60},
    [14]={cost_item_count={},cost_gold_count={},is_open=false,cheer_level_limit={},
          is_open_ni=false,open_cheer_item={}},
    [15]={adaptive_visible=false},
    [24]={vip_shop={had_gift=false},buff_data={buff_type=0}},
    config_end=true
}'''
with (Path(__file__).resolve().parents[1] / 'analysis/configs/role_level_config.csv').open() as _levels:
    FORMATION_SLOTS = {int(row['level']): int(row['cortege_count']) for row in csv.DictReader(_levels)}


def login_fields(text):
    # Parse literal Lua data only; never execute a client-provided Lua expression.
    from fetch_server_list import ast, nodes, literal
    try:
        statements = ast.parse('return ' + text).body.body
        if (len(statements) != 1 or not isinstance(statements[0], nodes.Return)
                or len(statements[0].values) != 1 or not isinstance(statements[0].values[0], nodes.Table)):
            return {}
        return literal(statements[0].values[0])
    except Exception:
        return {}


class Backend:
    def __init__(self, directory, port, emit):
        directory.mkdir(parents=True, exist_ok=True)
        self.port, self.emit = port, emit
        self.db = sqlite3.connect(directory / 'game.sqlite3')
        os.chmod(directory / 'game.sqlite3', 0o600)
        self.db.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
        self.db.execute('CREATE TABLE IF NOT EXISTS roles (account TEXT PRIMARY KEY, data TEXT NOT NULL)')
        row = self.db.execute("SELECT value FROM settings WHERE key='sdk_token'").fetchone()
        self.token = row[0] if row else 'local-' + secrets.token_hex(24)
        if not row:
            self.db.execute('INSERT INTO settings VALUES (?, ?)', ('sdk_token', self.token))
            self.db.commit()
        self.tickets = {}
        self.random_key = secrets.randbelow(0x7ffffffe) + 1
        # One local account. Keep response numbering/replay across TCP reconnects.
        self.server_serial = 200000
        self.reply_history = deque(maxlen=256)

    def close(self):
        self.db.close()

    def profile(self, account='local-player'):
        row = self.db.execute('SELECT data FROM roles WHERE account=?', (account,)).fetchone()
        if row:
            role = json.loads(row[0])
            # Migrate existing bootstrap saves without replacing the user's role.
            changed = False
            if 'cortege_count' not in role:
                role['cortege_count'] = FORMATION_SLOTS[role['level']]
                changed = True
            if 'attachments' not in role:
                role['attachments'] = []
                changed = True
            if changed:
                self.save(role, account)
            return role
        # Explicit local bootstrap defaults; these are not recovered official server values.
        role = dict(area_id=1, role_id=1.0, role_name='本地行者', level=1,
                    register_account=account, pf_account=account, mobile_account=account,
                    next_exp=100, silver_coin=1000, gold_coin=0, strength=60, energy=10,
                    head_type=1, guide_progress=0x7fffffff, cortege_count=FORMATION_SLOTS[1],
                    attachments=[])
        self.save(role, account)
        return role

    def save(self, role, account='local-player'):
        self.db.execute('INSERT OR REPLACE INTO roles VALUES (?,?)',
                        (account, json.dumps(role, ensure_ascii=False)))
        self.db.commit()

    def snapshot(self):
        return dict(self.profile(), server_time=int(time.time()), random_key=self.random_key)

    def bootstrap(self, reconnect=False):
        # 2998/event 80 feeds data.callback_update_config before mainUI is created.
        # This is a minimal local configuration, not an official configuration dump.
        config = CLIENT_CONFIG.replace('server_time=0', 'server_time=%d' % int(time.time()))
        return [encode(2998, dict(id=80, data=config)),
                encode(1017, dict(self.snapshot(), reconnect=reconnect)),
                self.roster(), self.attachments()]

    def roster(self, serial=0):
        role = self.profile()
        if 'corteges' not in role:
            # A local starter companion; attributes come from cortege_base_0.csv.
            role['corteges'] = [dict(id=1.0, order=1, type=5004, level=1, next_exp=100,
                                    hp=475, magic=133, gongji=195, fangyu=124,
                                    combat_power=927, equiped_ext_skill_limit=1)]
            self.save(role)
        return encode(1034, dict(serial_num=serial, first_send=True,
                                cortege_count=len(role['corteges']), cortege_list=role['corteges']))

    def attachments(self, serial=0):
        items = self.profile().get('attachments', [])
        return encode(1035, dict(serial_num=serial, first_send=True,
                                attach_count=len(items), attach_list=items))

    def complete(self, request_serial, replies):
        if not request_serial:
            return replies
        # Responses use an independent, contiguous server sequence. Reusing the
        # request number makes packageReturn discard the second packet as a dup.
        replies = replies + [encode(1106, dict(req_serial_num=request_serial))]
        return self.number_replies(replies)

    def number_replies(self, replies):
        numbered = []
        for packet in replies:
            mid, connection, data = decode(packet)
            self.server_serial += 1
            data['serial_num'] = self.server_serial
            packet = encode(mid, data, connection)
            numbered.append(packet)
            self.reply_history.append((self.server_serial, packet))
        return numbered

    def respond(self, packet, state):
        mid, connection, data = decode(packet)
        self.emit('game_request', message_id=mid, bytes=len(packet), authenticated=state.get('authenticated', False))
        if mid == 3001:
            token = login_fields(data['data']).get('access_token')
            if data['id'] != 68 or not isinstance(token, str) or not secrets.compare_digest(token.encode(), self.token.encode()):
                self.emit('game_auth_rejected', message='仅接受本地测试凭据')
                return [encode(3002, dict(auth_key=1, seed=0, server_port=0, account='', server_ip=''))]
            ticket = secrets.randbelow(0x7ffffff0) + 10
            seed = secrets.randbelow(0x7ffffffe) + 1
            self.tickets = {k: v for k, v in self.tickets.items() if v[1] > time.monotonic()}
            if len(self.tickets) >= 256:
                raise ValueError('Too many pending login tickets')
            self.tickets[ticket] = (seed, time.monotonic() + 60)
            return [encode(3002, dict(auth_key=ticket, seed=seed, server_port=self.port,
                                     account='local-player', server_ip='127.0.0.1'))]
        if mid == 1001:
            entry = self.tickets.pop(data['auth_key'], None)
            if (not entry or entry[0] != data['seed'] or entry[1] < time.monotonic()
                    or data['account'] != 'local-player'):
                return [encode(1002, {'result': 1})]
            state['authenticated'] = True
            self.server_serial = 200000
            self.reply_history.clear()
            self.emit('game_login_ok', message='本地账号通过 LS→BS 认证')
            return [encode(1002, {'result': 0})] + self.bootstrap()
        if mid == 1016:
            if data['account'] == 'local-player' and data['random_key'] == self.random_key:
                state['authenticated'] = True
                return [encode(2996, {'ret': 0})] + self.bootstrap(reconnect=True)
            return [encode(2996, {'ret': 1})]
        if not state.get('authenticated'):
            raise ValueError('Business message before login')
        if mid == 2999:
            return [encode(2999, dict(time=int(time.time()), random_key=self.random_key, delay_time=0))]
        if mid == 1105:
            last = data['req_serial_num']
            if last == self.server_serial or (last == 0 and not self.reply_history):
                # Reconnect asks for replay even when nothing was missed. End
                # that wait explicitly; never append another done to a replay.
                return self.number_replies([encode(1106, dict(req_serial_num=0))])
            if self.reply_history and ((last == 0 and self.reply_history[0][0] == 200001)
                    or self.reply_history[0][0] - 1 <= last < self.server_serial):
                return [packet for serial, packet in self.reply_history if serial > last]
            self.emit('game_replay_unavailable', message_id=mid, message='请求不在当前响应缓存范围内')
            return []
        if mid == 1018:
            serial = data['serial_num']
            return self.complete(serial, [encode(1020, dict(first_send=True, tollgate_count=1,
                                     tollgate_list=[dict(tollgate_type=1, map_id=1, tollgate_id=101)])),
                    encode(1023, dict(map_count=1,
                                     map_list=[dict(tollgate_type=1, map_id=1, pass_map=0)]))])
        if mid == 1094:
            return self.complete(data['serial_num'], [encode(1095, dict(first_send=True,
                                     op_type=data['flag'], attention_count=0, attention_list=[]))])
        if mid == 1033:
            # Event 1 opens/refreshes the requested UI after both lists arrive.
            return self.complete(data['serial_num'], [self.roster(), self.attachments(),
                encode(2998, dict(id=1, data='{flag=%d}' % data['flag']))])
        self.emit('game_unimplemented', message_id=mid, message='尚未实现的业务消息；不返回伪成功')
        return []
