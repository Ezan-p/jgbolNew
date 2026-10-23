"""Local-only account and LS/BS bootstrap. Never contacts a channel service."""
from collections import deque
import copy
import csv
import json
import os
from pathlib import Path
import secrets
import sqlite3
import struct
import time

from .protocol import encode, decode
from . import summon, formation, market, immortal


# The client initializes these sections together in data.set_g_new_config.
# Explicitly disable unavailable local features rather than leaving their UI
# state uninitialized (notably cheerSquadUI.canJoin's Lv/isOpen fields).
CLIENT_CONFIG = '''{
    [4]={party_top_list={},pay_consume_gold=0},
    [5]={},
    [10]=__MARKET_CONFIG__,
    [11]={open_flag=false,min_role_level=60},
    [14]={cost_item_count={},cost_gold_count={},is_open=false,cheer_level_limit={},
          is_open_ni=false,open_cheer_item={}},
    [15]=__IMMORTAL_CONFIG__,
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
        self.summon_rules = summon.load_rules()
        self.formation_rules = formation.load_rules()
        self.market_rules = market.load_rules()
        self.immortal_rules = immortal.load_rules()
        self.summon_status = summon.rule_status()
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
        self.summon_replies = {}
        self.last_summon_serial = 0
        self.formation_replies = {}
        self.last_formation_serial = 0
        self.market_replies = {}
        self.last_market_serial = 0
        self.immortal_replies = {}
        self.last_immortal_serial = 0

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
            changed = formation.prepare(role, self.formation_rules) or changed
            changed = immortal.prepare(role, self.immortal_rules) or changed
            formation.recalculate(role, self.formation_rules)
            if changed:
                self.save(role, account)
            return role
        # Explicit local bootstrap defaults; these are not recovered official server values.
        role = dict(area_id=1, role_id=1.0, role_name='本地行者', level=1,
                    register_account=account, pf_account=account, mobile_account=account,
                    next_exp=100, silver_coin=1000, gold_coin=0, strength=60, energy=10,
                    head_type=1, guide_progress=0x7fffffff, cortege_count=FORMATION_SLOTS[1],
                    attachments=[])
        formation.prepare(role, self.formation_rules)
        self.save(role, account)
        return role

    def save(self, role, account='local-player'):
        immortal.prepare(role, self.immortal_rules)
        formation.recalculate(role, self.formation_rules)
        self.db.execute('INSERT OR REPLACE INTO roles VALUES (?,?)',
                        (account, json.dumps(role, ensure_ascii=False)))
        self.db.commit()

    def snapshot(self):
        role = self.profile()
        now = int(time.time())
        summon.prepare(role, now, self.summon_rules)
        role.update(summon.remaining(role, now))
        self.save(role)
        return dict(role, server_time=now, random_key=self.random_key)

    def bootstrap(self, reconnect=False):
        # 2998/event 80 feeds data.callback_update_config before mainUI is created.
        # This is a minimal local configuration, not an official configuration dump.
        role = self.profile()
        goods = market.catalog(role, int(time.time()), self.market_rules)
        self.save(role)
        config = CLIENT_CONFIG.replace('__MARKET_CONFIG__', summon.lua(goods))
        config = config.replace('__IMMORTAL_CONFIG__', summon.lua(immortal.client_config(self.immortal_rules)))
        config = config.replace('config_end=true', '[23]=' + summon.lua(self.formation_rules['equipment_advance']) + ',config_end=true')
        replies = [encode(2998, dict(id=80, data=config)),
                encode(1017, dict(self.snapshot(), reconnect=reconnect))] + self.inventory()
        role = self.profile()
        replies += summon.soul_snapshots(role)
        replies += immortal.handbook(role, self.immortal_rules)
        replies.append(summon.event(158, immortal.collection_snapshot(role)))
        if any(role['collection_bonuses'].values()):
            attrs = [dict(type=t, value=role['collection_bonuses'][k]) for t, k in
                     ((87, 'hp'), (88, 'gongji'), (89, 'fangyu'), (90, 'magic'))]
            replies.append(encode(1032, dict(id=role['role_id'], unit_type=1,
                                             attr_count=len(attrs), attr_list=attrs)))
        if 'news' in role.get('summon', {}):
            replies.append(summon.news_snapshot(role, self.summon_rules))
        if role.get('summon', {}).get('last_result'):
            replies.append(summon.event(79, role['summon']['last_result']))
        return replies

    def roster(self, serial=0, role=None):
        role = self.profile() if role is None else role
        return encode(1034, dict(serial_num=serial, first_send=True,
                                cortege_count=len(role['corteges']), cortege_list=role['corteges']))

    def inventory(self, role=None):
        """The byte count is a per-packet limit, not a 255-object account cap."""
        role = self.profile() if role is None else role
        replies = []
        for mid, key, count, field in ((1034, 'corteges', 'cortege_count', 'cortege_list'),
                                        (1035, 'attachments', 'attach_count', 'attach_list')):
            rows = role[key]
            for start in range(0, max(1, len(rows)), 128):
                chunk = rows[start:start + 128]
                replies.append(encode(mid, dict(first_send=start == 0, **{count: len(chunk), field: chunk})))
        return replies

    def formation(self, packet, mid, data):
        serial = data['serial_num']
        cached = self.formation_replies.get(serial)
        if cached and cached[0] == packet:
            return cached[1]
        if not serial or serial <= self.last_formation_serial:
            return self.complete(serial, [summon.event(55, {'op_string': '阵容请求已过期，请刷新后重试'})])
        try:
            role = self.profile()
            before = copy.deepcopy(role)
            events = formation.settle(role, mid, data, self.formation_rules, login_fields)
            immortal.prepare(role, self.immortal_rules)
            attrs = [dict(type=t, value=role.get(k, 0)) for t, k in
                     ((7, 'silver_coin'), (8, 'gold_coin'), (30, 'role_combat_power'), (71, 'cortege_count'))]
            # Equipment panels keep the selected table throughout repeated
            # upgrades. Preserve it with deltas; full snapshots would detach it.
            snapshots = [] if mid in (1052, 1073) else self.inventory(role)
            replies = self.companion_deltas(before, role) + self.item_deltas(before, role) + snapshots + summon.soul_snapshots(role) + immortal.handbook(role, self.immortal_rules) + [
                encode(1032, dict(id=role['role_id'], unit_type=1, attr_count=len(attrs), attr_list=attrs))] + events
            self.save(role)
            self.emit('game_formation_ok', message_id=mid, rules_revision=self.formation_rules['revision'])
        except (formation.Rejected, ValueError, KeyError, TypeError, OverflowError, struct.error) as error:
            replies = [summon.event(55, {'op_string': str(error) if isinstance(error, formation.Rejected) else '阵容数据无效，请刷新后重试'})]
            self.emit('game_formation_rejected', message_id=mid, message=str(error))
        replies = self.complete(serial, replies)
        self.last_formation_serial = serial
        self.formation_replies[serial] = (packet, replies)
        if len(self.formation_replies) > 256:
            del self.formation_replies[next(iter(self.formation_replies))]
        return replies

    def companion_deltas(self, before, after):
        # [A] lineupUI.updateCharacterInfo mutates existing objects. Training UI
        # retains those references and reads culture_point before re-fetching.
        # Send deltas before replacing list snapshots, preserving that contract.
        fields = {'level': 3, 'cur_exp': 5, 'next_exp': 6, 'cheer_order': 50,
                  'order': 52, 'combat_power': 58, 'hp': 61, 'magic': 62,
                  'gongji': 63, 'fangyu': 64, 'evolve_level': 75,
                  'hp_plus': 86, 'magic_plus': 87, 'gongji_plus': 88,
                  'fangyu_plus': 89, 'culture_point': 90,
                  'train_increase_field': 55, 'train_decrease_field': 56,
                  'train_change_value': 57}
        old = {c['id']: c for c in before['corteges']}
        packets = []
        for c in after['corteges']:
            if c['id'] not in old:
                continue
            # 1032 values are signed int32; fractional/large experience is
            # delivered by the following 1034 double-precision snapshot.
            attrs = [dict(type=t, value=int(c.get(k, 0))) for k, t in fields.items()
                     if c.get(k, 0) != old[c['id']].get(k, 0)
                     and c.get(k, 0) == int(c.get(k, 0))
                     and -2147483648 <= c.get(k, 0) <= 2147483647]
            if attrs:
                packets.append(encode(1032, dict(id=c['id'], unit_type=4,
                                                attr_count=len(attrs), attr_list=attrs)))
        return packets

    def attachments(self, serial=0, role=None):
        items = (self.profile() if role is None else role).get('attachments', [])
        return encode(1035, dict(serial_num=serial, first_send=True,
                                attach_count=len(items), attach_list=items))

    def item_deltas(self, before, after):
        fields = {'level': 103, 'count': 102, 'equip_order': 105, 'equip_pos': 10,
                  'effect_value': 209, 'advance_level': 109, 'star_count': 110,
                  'cur_spirit_count': 111, 'is_lock': 116}
        old = {i['id']: i for i in before['attachments']}
        packets = []
        for item in after['attachments']:
            if item['id'] not in old or item['attach_type'] != 5:
                continue
            attrs = [dict(type=t, value=int(item.get(k, 0))) for k, t in fields.items()
                     if item.get(k, 0) != old[item['id']].get(k, 0)
                     and 0 <= item.get(k, 0) <= 2147483647]
            if attrs:
                packets.append(encode(1032, dict(id=item['id'], unit_type=5,
                                                attr_count=len(attrs), attr_list=attrs)))
        remaining = {i['id'] for i in after['attachments']}
        for item in before['attachments']:
            if item['attach_type'] == 5 and item['id'] not in remaining:
                packets.append(encode(1032, dict(id=item['id'], unit_type=5, attr_count=1,
                                                attr_list=[dict(type=102, value=0)])))
        return packets

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

    def summon(self, packet, data):
        serial = data['serial_num']
        cached = self.summon_replies.get(serial)
        if cached and cached[0] == packet:
            return cached[1]
        if not serial or serial <= self.last_summon_serial:
            return self.complete(serial, [summon.event(55, {'op_string': '召唤请求已过期，请重新操作'})])
        try:
            role = self.profile()
            result = summon.settle(role, data, int(time.time()), self.summon_rules)
            formation.prepare(role, self.formation_rules)
            immortal.prepare(role, self.immortal_rules)
            # Encode every business response before committing any resources.
            replies = self.inventory(role) + summon.soul_snapshots(role) + immortal.handbook(role, self.immortal_rules) + [
                       encode(1032, dict(id=role['role_id'], unit_type=1, attr_count=1,
                                        attr_list=[dict(type=8, value=role['gold_coin'])])),
                       summon.news_snapshot(role, self.summon_rules), summon.event(23, result)]
            self.save(role)
            self.emit('game_summon_ok', grade=data['pick_grade'], payment=data['pick_type'],
                      count=data['ten_pick'] or 1, rules_revision=self.summon_rules['revision'],
                      rule_mode='inferred', roster_count=len(role['corteges']))
        except summon.SummonRejected as error:
            replies = [summon.event(55, {'op_string': str(error)})]
            self.emit('game_summon_rejected', message=str(error))
        replies = self.complete(serial, replies)
        self.last_summon_serial = serial
        self.summon_replies[serial] = (packet, replies)
        if len(self.summon_replies) > 256:
            del self.summon_replies[next(iter(self.summon_replies))]
        return replies

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
            self.summon_replies.clear()
            self.last_summon_serial = 0
            self.formation_replies.clear()
            self.last_formation_serial = 0
            self.market_replies.clear()
            self.last_market_serial = 0
            self.immortal_replies.clear()
            self.last_immortal_serial = 0
            state['market_sale_time'] = market.sale_time(int(time.time()), self.market_rules)
            self.emit('game_login_ok', message='本地账号通过 LS→BS 认证')
            return [encode(1002, {'result': 0})] + self.bootstrap()
        if mid == 1016:
            if data['account'] == 'local-player' and data['random_key'] == self.random_key:
                state['authenticated'] = True
                state['market_sale_time'] = market.sale_time(int(time.time()), self.market_rules)
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
            return self.complete(data['serial_num'], self.inventory() + summon.soul_snapshots(self.profile()) + [
                encode(2998, dict(id=1, data='{flag=%d}' % data['flag']))])
        if mid in immortal.HANDLED:
            return self.immortals(packet, mid, data)
        if mid in formation.HANDLED:
            return self.formation(packet, mid, data)
        if mid == 1042:
            return self.summon(packet, data)
        if mid in (1057, 1241, 1242):
            return self.market(packet, mid, data, state)
        self.emit('game_unimplemented', message_id=mid, message='尚未实现的业务消息；不返回伪成功')
        if data and data.get('serial_num'):
            return self.complete(data['serial_num'], [summon.event(55, {'op_string': '该功能尚未接入本地服务端（%d）' % mid})])
        return []

    def market(self, packet, mid, data, state):
        now = int(time.time())
        serial = data.get('serial_num', 0)
        if mid != 1242:
            cached = self.market_replies.get(serial)
            if cached and cached[0] == packet:
                return cached[1]
            if not serial or serial <= self.last_market_serial:
                return self.complete(serial, [summon.event(55, {'op_string': '集市请求已过期，请刷新后重试'})])
        role = self.profile()
        if mid == 1242:
            snapshot = market.panic_snapshot(role, now, self.market_rules)
            self.save(role)
            state['market_sale_time'] = snapshot['activity_data']['sale_time']
            # The original query has no request serial and does not wait for 1106.
            return self.number_replies([summon.event(138, snapshot)])
        try:
            if mid == 1057 and data['first_send'] == 1:
                goods = market.catalog(role, now, self.market_rules)
                replies = [summon.event(24, dict(goods, first_send=1))]
                state['market_sale_time'] = goods['panic_buy_list']['activity_data']['sale_time']
            else:
                before = copy.deepcopy(role)
                if mid == 1057:
                    if data['first_send'] != 0:
                        raise market.Rejected(2)
                    result = market.buy(role, data, now, self.market_rules)
                else:
                    result = market.panic_buy(role, data, now, self.market_rules,
                                              state.get('market_sale_time'))
                replies = self.item_deltas(before, role) + self.inventory(role) + [
                    encode(1032, dict(id=role['role_id'], unit_type=1, attr_count=2,
                        attr_list=[dict(type=7, value=role['silver_coin']), dict(type=8, value=role['gold_coin'])])),
                    summon.event(24 if mid == 1057 else 139, result)]
            # All resources and limits commit together, after wire validation.
            self.save(role)
            self.emit('game_market_ok', message_id=mid, rules_revision=self.market_rules['revision'])
        except market.Rejected as error:
            if mid == 1057:
                result = dict(first_send=0, result=error.result)
            else:
                result = dict(market.panic_snapshot(self.profile(), now, self.market_rules), result=error.result)
            replies = [summon.event(24 if mid == 1057 else 139, result)]
            self.emit('game_market_rejected', message_id=mid, result=error.result)
        except (ValueError, KeyError, TypeError, OverflowError, struct.error) as error:
            replies = [summon.event(55, {'op_string': '集市数据无效，请刷新后重试'})]
            self.emit('game_market_rejected', message_id=mid, message=str(error))
        replies = self.complete(serial, replies)
        self.last_market_serial = serial
        self.market_replies[serial] = (packet, replies)
        if len(self.market_replies) > 256:
            del self.market_replies[next(iter(self.market_replies))]
        return replies

    def immortals(self, packet, mid, data):
        serial = data['serial_num']
        cached = self.immortal_replies.get(serial)
        if cached and cached[0] == packet:
            return cached[1]
        if not serial or serial <= self.last_immortal_serial:
            return self.complete(serial, [summon.event(55, {'op_string': '神仙请求已过期，请刷新后重试'})])
        try:
            role = self.profile()
            if mid == 1048:
                formation.require(data['flag'] == 0, '图鉴查询参数无效')
                replies = immortal.handbook(role, self.immortal_rules) + [summon.event(25, {})]
            elif mid == 1305:
                replies = [summon.event(158, immortal.collection_snapshot(role))]
            else:
                before = copy.deepcopy(role)
                events = immortal.settle(role, mid, data, self.immortal_rules, login_fields)
                formation.recalculate(role, self.formation_rules)
                attrs = [dict(type=t, value=role.get(k, 0)) for t, k in
                         ((7, 'silver_coin'), (8, 'gold_coin'), (30, 'role_combat_power'))]
                attrs += [dict(type=t, value=role['collection_bonuses'][k]) for t, k in
                          ((87, 'hp'), (88, 'gongji'), (89, 'fangyu'), (90, 'magic'))]
                replies = (self.companion_deltas(before, role) + self.item_deltas(before, role)
                           + self.inventory(role) + summon.soul_snapshots(role)
                           + immortal.handbook(role, self.immortal_rules)
                           + [encode(1032, dict(id=role['role_id'], unit_type=1,
                                               attr_count=len(attrs), attr_list=attrs))] + events)
            self.save(role)
            self.emit('game_immortal_ok', message_id=mid, rules_revision=self.immortal_rules['revision'])
        except (formation.Rejected, ValueError, KeyError, TypeError, OverflowError, struct.error) as error:
            replies = [summon.event(55, {'op_string': str(error) if isinstance(error, formation.Rejected) else '神仙数据无效，请刷新后重试'})]
            self.emit('game_immortal_rejected', message_id=mid, message=str(error))
        replies = self.complete(serial, replies)
        self.last_immortal_serial = serial
        self.immortal_replies[serial] = (packet, replies)
        if len(self.immortal_replies) > 256:
            del self.immortal_replies[next(iter(self.immortal_replies))]
        return replies
