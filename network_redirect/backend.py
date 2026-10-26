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
from . import role_profile, achievements
from . import summon, formation, market, immortal, journey, activity, reborn, reborn_stars, daily, guild, vip, xianling, welfare, cheer, monument, equipment


# The client initializes these sections together in data.set_g_new_config.
# Every enabled feature supplies the field types consumed by its original UI.
CLIENT_CONFIG = '''{
    [4]=__PARTY_CONFIG__,
    [5]={},
    [7]={achievement=true,collector=true,Bulletin=true,message=true,setting=true,service=true,relogin=true},
    [10]=__MARKET_CONFIG__,
    [11]=__STONE_CONFIG__,
    [14]=__CHEER_CONFIG__,
    [15]=__IMMORTAL_CONFIG__,
    [24]={vip_shop=__XIANLING_HINT__,buff_data={buff_type=0}},
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
    def __init__(self, directory, port, emit, account="local-player"):
        self.account = account
        self.achievement_rules = achievements.load_rules()
        self.achievement_context = None
        self.achievement_pending = []
        self.profile_rules = role_profile.load_rules()
        self.profile_replies = {}
        self.last_profile_serial = 0
        self.monument_rules = monument.load_rules()
        self.monument_replies = {}
        self.last_monument_serial = 0
        self.welfare_rules = welfare.load_rules()
        self.welfare_replies = {}
        self.last_welfare_serial = 0
        self.xianling_rules = xianling.load_rules()
        self.vip_rules = vip.load_rules()
        self.vip_replies = {}
        self.last_vip_serial = 0
        self.guild_rules = guild.load_rules()
        self.guild_replies = {}
        self.last_guild_serial = 0
        self.daily_rules = daily.load_rules()
        self.daily_replies = {}
        self.last_daily_serial = 0
        self.reborn_rules = reborn.load_rules()
        self.reborn_replies = {}
        self.last_reborn_serial = 0
        self.summon_rules = summon.load_rules()
        self.formation_rules = formation.load_rules()
        self.cheer_rules = cheer.load_rules()
        self.market_rules = market.load_rules()
        self.immortal_rules = immortal.load_rules()
        self.journey_rules = journey.load_rules()
        self.activity_rules = activity.load_rules()
        self.activity_replies = {}
        self.last_activity_serial = 0
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
        # This instance owns one account, including response replay across reconnects.
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
        self.journey_replies = {}
        self.last_journey_serial = 0

    def close(self):
        self.db.close()

    def profile(self, account=None):
        account = self.account if account is None else account
        row = self.db.execute('SELECT data FROM roles WHERE account=?', (account,)).fetchone()
        if row:
            role = json.loads(row[0])
            original_role = copy.deepcopy(role)
            # Migrate existing bootstrap saves without replacing the user's role.
            changed = False
            if 'cortege_count' not in role:
                role['cortege_count'] = FORMATION_SLOTS[role['level']]
                changed = True
            if 'attachments' not in role:
                role['attachments'] = []
                changed = True
            role_profile.prepare(role, self.profile_rules)
            cheer.prepare(role, self.cheer_rules)
            changed = formation.prepare(role, self.formation_rules) or changed
            changed = immortal.prepare(role, self.immortal_rules) or changed
            changed = reborn.prepare(role, self.reborn_rules) or changed
            if 'journey' not in role:
                changed = journey.prepare(role, int(time.time()), self.journey_rules) or changed
            formation.recalculate(role, self.formation_rules)
            achievements.refresh(role, int(time.time()))
            if changed or role != original_role:
                self.save(role, account)
            return role
        # Explicit local bootstrap defaults; these are not recovered official server values.
        role = dict(area_id=1, role_id=1.0, role_name='本地行者', level=1,
                    register_account=account, pf_account=account, mobile_account=account,
                    next_exp=100, silver_coin=1000, gold_coin=0, strength=60, energy=10,
                    head_type=1, guide_progress=0x7fffffff, cortege_count=FORMATION_SLOTS[1],
                    attachments=[])
        formation.prepare(role, self.formation_rules)
        journey.prepare(role, int(time.time()), self.journey_rules)
        self.save(role, account)
        return role

    def save(self, role, account=None):
        account = self.account if account is None else account
        role_profile.prepare(role, self.profile_rules)
        cheer.prepare(role, self.cheer_rules)
        vip.prepare(role, self.vip_rules)
        reborn.prepare(role, self.reborn_rules)
        immortal.prepare(role, self.immortal_rules)
        formation.recalculate(role, self.formation_rules)
        stored = self.db.execute('SELECT data FROM roles WHERE account=?', (account,)).fetchone()
        before_achievements = json.loads(stored[0]) if stored else None
        context = self.achievement_context if account == self.account else None
        mid, req = context or (0, {})
        achievements.track(role, before_achievements, mid, req, int(time.time()))
        updates = achievements.packets(role, new=1, previous=before_achievements) if context and before_achievements else []
        self.db.execute('INSERT OR REPLACE INTO roles VALUES (?,?)',
                        (account, json.dumps(role, ensure_ascii=False)))
        self.db.commit()
        self.achievement_pending.extend(updates)

    def snapshot(self):
        role = self.profile()
        now = int(time.time())
        journey.prepare(role, now, self.journey_rules)
        summon.prepare(role, now, self.summon_rules)
        activity.prepare(role, now, self.activity_rules)
        daily.prepare(role, now, self.daily_rules)
        guild.prepare(role, now, self.guild_rules)
        xianling.prepare(role, now)
        welfare.prepare(role, now, self.welfare_rules)
        monument.prepare(role, now, self.monument_rules)
        role.update(summon.remaining(role, now))
        self.save(role)
        return dict(role, server_time=now, random_key=self.random_key)

    def bootstrap(self, reconnect=False):
        # 2998/event 80 feeds data.callback_update_config before mainUI is created.
        # This is a minimal local configuration, not an official configuration dump.
        role = self.profile()
        achievements.login(role, int(time.time()))
        journey.prepare(role, int(time.time()), self.journey_rules)
        activity.prepare(role, int(time.time()), self.activity_rules)
        goods = market.catalog(role, int(time.time()), self.market_rules)
        self.save(role)
        vip.prepare(role, self.vip_rules)
        config = CLIENT_CONFIG.replace('__MARKET_CONFIG__', summon.lua(goods))
        config = config.replace('__STONE_CONFIG__', summon.lua(dict(open_flag=True, min_role_level=equipment.load_rules()['min_role_level'])))
        config = config.replace('__CHEER_CONFIG__', summon.lua(cheer.client_config(self.cheer_rules)))
        config = config.replace('__XIANLING_HINT__', summon.lua(xianling.hint(role,int(time.time()),self.xianling_rules)))
        config = config.replace('config_end=true', '[8]=' + summon.lua(guild.client_config(self.guild_rules)) + ',config_end=true')
        for key, value in daily.client_config(self.daily_rules).items():
            config = config.replace('config_end=true', '[%d]=' % key + summon.lua(value) + ',config_end=true')
        config = config.replace('config_end=true', '[1]=' + summon.lua(vip.client_config(self.vip_rules)) + ',local_vip=' + summon.lua(vip.client_state(role)) + ',config_end=true')
        config = config.replace('__PARTY_CONFIG__', summon.lua(dict(party_top_list={},pay_consume_gold=self.activity_rules['party_fight_gold'])))
        config = config.replace('__IMMORTAL_CONFIG__', summon.lua(immortal.client_config(self.immortal_rules)))
        realm_config = reborn.client_config(self.reborn_rules)
        for realm, values in realm_config.items():
            values['rights']['open_stone_sys'] = realm >= equipment.load_rules()['reborn_min_realm']
        realm_config[self.cheer_rules['skill_realm']]['rights']['open_cheer_skill'] = True
        config = config.replace('config_end=true', '[31]=' + summon.lua(realm_config) + ',[32]={is_open=true,flag=true},config_end=true')
        config = config.replace('config_end=true', '[23]=' + summon.lua(self.formation_rules['equipment_advance']) + ',config_end=true')
        config = config.replace('config_end=true', '[19]=' + summon.lua(monument.client_config(int(time.time()), self.monument_rules)) + ',config_end=true')
        login_snapshot = self.snapshot()
        # Original reverse skill levels use B in 1017 but signed I in 1032.
        # Bootstrap follows this bounded legacy snapshot with full-precision attributes.
        for name in cheer.NAMES[8:]:
            login_snapshot[name + '_skill_level'] = min(255, login_snapshot[name + '_skill_level'])
        replies = [encode(2998, dict(id=80, data=config)),
                encode(1017, dict(login_snapshot, reconnect=reconnect))] + self.inventory()
        role = self.profile()
        replies += self.power_attributes(role)
        replies += cheer.attributes(role)
        from . import equipment_crafting
        replies.append(summon.event(98, equipment_crafting.random_list()))
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
        replies += achievements.packets(role)
        replies.append(daily.hint(role, int(time.time()), self.daily_rules))
        replies.append(welfare.hint(role, int(time.time()), self.welfare_rules))
        replies.append(welfare.mail_snapshot(role, int(time.time()), self.welfare_rules))
        self.save(role)
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
            if mid == 1087:
                events = cheer.settle(role, data, self.cheer_rules)
                achievements.record_events(role, events, int(time.time()), login_fields)
                formation.prepare(role, self.formation_rules)
            else:
                events = formation.settle(role, mid, data, self.formation_rules, login_fields)
                achievements.record_events(role, events, int(time.time()), login_fields)
            immortal.prepare(role, self.immortal_rules)
            attrs = [dict(type=t, value=role.get(k, 0)) for t, k in
                     ((7, 'silver_coin'), (8, 'gold_coin'), (30, 'role_combat_power'), (39, 'max_combat_power'), (71, 'cortege_count'))]
            # Equipment panels keep the selected table throughout repeated
            # upgrades. Preserve it with deltas; full snapshots would detach it.
            snapshots = [] if mid in (1052, 1054, 1073) else self.inventory(role)
            if mid == 1076:
                # Update the selected spell table before the full inventory refresh.
                snapshots.insert(0, encode(1032, dict(id=data['des_id'], unit_type=6, attr_count=1,
                    attr_list=[dict(type=61, value=1)])))
            if mid == 1054:
                old_ids = {i['id'] for i in before['attachments']}
                added = [i for i in role['attachments'] if i['id'] not in old_ids]
                for start in range(0, len(added), 128):
                    chunk = added[start:start + 128]
                    snapshots.append(encode(1035, dict(first_send=False, attach_count=len(chunk), attach_list=chunk)))
            replies = self.companion_deltas(before, role) + self.item_deltas(before, role) + snapshots + summon.soul_snapshots(role) + immortal.handbook(role, self.immortal_rules) + [
                encode(1032, dict(id=role['role_id'], unit_type=1, attr_count=len(attrs), attr_list=attrs))] + cheer.attributes(role) + events
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

    def panel_attributes(self, role):
        fields = ((58, 'combat_power'), (61, 'hp'), (62, 'magic'), (63, 'gongji'), (64, 'fangyu'))
        return [encode(1032, dict(id=c['id'], unit_type=4, attr_count=len(fields),
                    attr_list=[dict(type=n, value=c.get(k, 0)) for n, k in fields]))
                for c in role['corteges']]

    def power_attributes(self, role):
        return [encode(1032, dict(id=role['role_id'], unit_type=1, attr_count=2,
                    attr_list=[dict(type=30, value=role['role_combat_power']),
                               dict(type=39, value=role['max_combat_power'])]))]

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
                  'train_change_value': 57, 'reborn_layer': 224, 'reborn_vein_level': 225, 'reborn_plus_type': 226}
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
        fields = {'level': 103, 'star_level': 117, 'count': 102, 'equip_order': 105, 'equip_pos': 10,
                  'effect_value': 209, 'advance_level': 109, 'star_count': 110,
                  'cur_spirit_count': 111, 'is_lock': 116, 'reborn_bit': 113, 'cast_level': 115,
                  'owner_id': 311, 'ext_awaken_pos': 313, 'prob_compen': 310,
                  'drill_count': 301, 'stone1_level': 302, 'stone2_level': 303,
                  'stone3_level': 304, 'stone4_level': 305}
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
        if self.achievement_pending:
            replies = self.achievement_pending + replies
            self.achievement_pending = []
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
            achievements.record_events(role, [summon.event(23, result)], int(time.time()), login_fields)
            welfare.track(role,1045,data,[],int(time.time()),self.welfare_rules)
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
        mid, _, data = decode(packet)
        self.achievement_context = (mid, data) if state.get('authenticated') else None
        self.achievement_pending = []
        try:
            return self._respond(packet, state)
        finally:
            self.achievement_context = None
            self.achievement_pending = []

    def _respond(self, packet, state):
        mid, connection, data = decode(packet)
        self.emit('game_request', message_id=mid, bytes=len(packet), authenticated=state.get('authenticated', False))
        if mid == 3001:
            token = login_fields(data['data']).get('access_token')
            if data['id'] != 68 or not isinstance(token, str) or not secrets.compare_digest(token.encode(), self.token.encode()):
                self.emit('game_auth_rejected', message='仅接受已验证的本地账号凭据')
                return [encode(3002, dict(auth_key=1, seed=0, server_port=0, account='', server_ip=''))]
            ticket = secrets.randbelow(0x7ffffff0) + 10
            seed = secrets.randbelow(0x7ffffffe) + 1
            self.tickets = {k: v for k, v in self.tickets.items() if v[1] > time.monotonic()}
            if len(self.tickets) >= 256:
                raise ValueError('Too many pending login tickets')
            self.tickets[ticket] = (seed, time.monotonic() + 60)
            return [encode(3002, dict(auth_key=ticket, seed=seed, server_port=self.port,
                                     account=self.account, server_ip='127.0.0.1'))]
        if mid == 1001:
            entry = self.tickets.pop(data['auth_key'], None)
            if (not entry or entry[0] != data['seed'] or entry[1] < time.monotonic()
                    or data['account'] != self.account):
                return [encode(1002, {'result': 1})]
            state['authenticated'] = True
            self.server_serial = 200000
            self.reply_history.clear()
            self.profile_replies.clear()
            self.last_profile_serial = 0
            self.reborn_replies.clear()
            self.last_reborn_serial = 0
            self.monument_replies.clear()
            self.last_monument_serial = 0
            self.welfare_replies.clear()
            self.last_welfare_serial = 0
            self.vip_replies.clear()
            self.last_vip_serial = 0
            self.guild_replies.clear()
            self.last_guild_serial = 0
            self.daily_replies.clear()
            self.last_daily_serial = 0
            self.summon_replies.clear()
            self.last_summon_serial = 0
            self.formation_replies.clear()
            self.last_formation_serial = 0
            self.market_replies.clear()
            self.last_market_serial = 0
            self.immortal_replies.clear()
            self.last_immortal_serial = 0
            self.activity_replies.clear()
            self.last_activity_serial = 0
            self.journey_replies.clear()
            self.last_journey_serial = 0
            state['market_sale_time'] = market.sale_time(int(time.time()), self.market_rules)
            self.emit('game_login_ok', message='本地账号通过 LS→BS 认证')
            return [encode(1002, {'result': 0})] + self.bootstrap()
        if mid == 1016:
            if data['account'] == self.account and data['random_key'] == self.random_key:
                state['authenticated'] = True
                state['market_sale_time'] = market.sale_time(int(time.time()), self.market_rules)
                return [encode(2996, {'ret': 0})] + self.bootstrap(reconnect=True)
            return [encode(2996, {'ret': 1})]
        if not state.get('authenticated'):
            raise ValueError('Business message before login')
        if mid == 2999:
            role = self.profile()
            now = int(time.time())
            previous_month = role.get('xianling', {}).get('month')
            xianling.prepare(role, now)
            previous_day = role.get('daily', {}).get('day')
            journey.prepare(role, now, self.journey_rules)
            daily.prepare(role, now, self.daily_rules)
            self.save(role)
            # Refresh expiring permanent effects without replacing UI-held objects.
            updates = self.panel_attributes(role) + self.journey_attributes(role)
            if previous_month != role['xianling']['month']:
                updates.append(xianling.tip(role,now,self.xianling_rules))
            if previous_day != role['daily']['day']:
                updates.append(daily.hint(role, now, self.daily_rules))
                updates.append(welfare.hint(role, now, self.welfare_rules))
                updates.append(welfare.mail_snapshot(role, now, self.welfare_rules))
                self.save(role)
            return [encode(2999, dict(time=now, random_key=self.random_key, delay_time=0))] + self.number_replies(self.achievement_pending + updates)
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
        if mid == 1067:
            try:
                formation.require(data['flag'] in (0, 1), '成就查询标志无效')
                target_id = data['des_role_id']
                target = self.profile() if target_id in (0, self.profile()['role_id']) else None
                if target is None:
                    matches = [json.loads(raw) for (raw,) in self.db.execute('SELECT data FROM roles')
                               if json.loads(raw).get('role_id') == target_id]
                    formation.require(len(matches) == 1, '目标角色不存在或编号不唯一')
                    target = matches[0]
                    achievements.refresh(target, int(time.time()))
                return self.complete(data['serial_num'], achievements.packets(target))
            except (formation.Rejected, ValueError) as error:
                return self.complete(data['serial_num'], [summon.event(55, dict(op_string=str(error)))])
        if mid in role_profile.HANDLED:
            return self.role_profiles(packet, mid, data)
        if monument.handles(mid, data):
            return self.monuments(packet, mid, data)
        if welfare.handles(mid, data):
            return self.welfares(packet, mid, data)
        if vip.handles(mid, data) or mid == 1336 or mid == 1051 and data['item_type'] == 1249:
            return self.vips(packet, mid, data)
        if mid in guild.HANDLED or mid == 1026 and data['fight_type'] in guild.FIGHTS or mid == 1097 and data['channel'] == 6:
            return self.guilds(packet, mid, data)
        if mid in daily.HANDLED:
            return self.dailies(packet, mid, data)
        if (mid in activity.HANDLED or (mid == 1026 and data['fight_type'] in activity.FIGHTS)
                or (mid == 1244 and data['fight_type'] == 2)
                or (mid == 1051 and data['item_type'] in (1021,1130,1131,1132,1133,1213,1214,1215,1216,1217))
                or (mid == 1059 and data['flag'] == 3)
                or (mid == 1201 and data['flag'] in (1, 2))):
            return self.activities(packet, mid, data)
        if (mid in journey.HANDLED or (mid == 1051 and data['item_type'] in (1022, 1023))
                or (mid == 2998 and data['id'] == 3)):
            return self.journeys(packet, mid, data)
        if mid == 1094:
            return self.complete(data['serial_num'], [encode(1095, dict(first_send=True,
                                     op_type=data['flag'], attention_count=0, attention_list=[]))])
        if mid == 1033:
            # Event 1 opens/refreshes the requested UI after both lists arrive.
            return self.complete(data['serial_num'], self.inventory() + summon.soul_snapshots(self.profile()) + [
                encode(2998, dict(id=1, data='{flag=%d}' % data['flag']))])
        if mid in reborn.HANDLED:
            return self.rebirth(packet, mid, data)
        if mid in immortal.HANDLED and mid != 1074:
            return self.immortals(packet, mid, data)
        if mid == 1087 or mid in formation.HANDLED:
            return self.formation(packet, mid, data)
        if mid == 1042:
            return self.summon(packet, data)
        if mid in (1057, 1241, 1242):
            return self.market(packet, mid, data, state)
        self.emit('game_unimplemented', message_id=mid, message='尚未实现的业务消息；不返回伪成功')
        if data and data.get('serial_num'):
            return self.complete(data['serial_num'], [summon.event(55, {'op_string': '该功能尚未接入本地服务端（%d）' % mid})])
        return []

    def role_profiles(self, packet, mid, data):
        serial = data['serial_num']
        cached = self.profile_replies.get(serial)
        if cached and cached[0] == packet:
            return cached[1]
        if not serial or serial <= self.last_profile_serial:
            return self.complete(serial, [summon.event(55, {'op_string': '角色资料请求已过期，请刷新后重试'})])
        try:
            role = self.profile()
            before = copy.deepcopy(role)
            # Acquire the write lock before checking names to prevent cross-account races.
            self.db.execute('BEGIN IMMEDIATE')
            records = [(account, json.loads(raw)) for account, raw in self.db.execute('SELECT account,data FROM roles')]
            names = [r['role_name'] for account, r in records if account != self.account]
            target = None
            if mid == 1078 and data['flag'] == 2:
                target = next((r for account, r in records if r['role_id'] == data['des_id']), None)
                if target is not None:
                    role_profile.prepare(target, self.profile_rules)
            events = role_profile.settle(role, mid, data, int(time.time()), self.profile_rules, names, target)
            achievements.record_events(role, events, int(time.time()), login_fields)
            formation.recalculate(role, self.formation_rules)
            replies = self.item_deltas(before, role) + [role_profile.attributes(role)]
            replies += self.panel_attributes(role) + self.power_attributes(role) + events
            self.save(role)
            self.emit('game_profile_ok', message_id=mid, rules_revision=self.profile_rules['revision'])
        except (formation.Rejected, ValueError, KeyError, TypeError, OverflowError, struct.error) as error:
            self.db.rollback()
            replies = [summon.event(55, {'op_string': str(error) if isinstance(error, formation.Rejected) else '角色资料数据无效，请刷新后重试'})]
            self.emit('game_profile_rejected', message_id=mid, message=str(error))
        replies = self.complete(serial, replies)
        self.last_profile_serial = serial
        self.profile_replies[serial] = (packet, replies)
        if len(self.profile_replies) > 256:
            del self.profile_replies[next(iter(self.profile_replies))]
        return replies

    def monuments(self, packet, mid, data):
        serial = data['serial_num']
        cached = self.monument_replies.get(serial)
        if cached and cached[0] == packet:
            return cached[1]
        if not serial or serial <= self.last_monument_serial:
            return self.complete(serial, [summon.event(55, {'op_string': '名人山请求已过期，请刷新后重试'})])
        try:
            role = self.profile()
            before = copy.deepcopy(role)
            events = monument.settle(role, mid, data, int(time.time()), self.monument_rules,
                                     self.guild_rules, self.activity_rules, self.journey_rules)
            achievements.record_events(role, events, int(time.time()), login_fields)
            replies = self.item_deltas(before, role) + self.inventory(role) + [monument.attributes(role)] + events
            self.save(role)
            self.emit('game_monument_ok', message_id=mid, rules_revision=self.monument_rules['revision'])
        except (formation.Rejected, ValueError, KeyError, TypeError, OverflowError, struct.error) as error:
            replies = [summon.event(55, {'op_string': str(error) if isinstance(error, formation.Rejected) else '名人山数据无效，请刷新后重试'})]
            self.emit('game_monument_rejected', message_id=mid, message=str(error))
        replies = self.complete(serial, replies)
        self.last_monument_serial = serial
        self.monument_replies[serial] = (packet, replies)
        if len(self.monument_replies) > 256:
            del self.monument_replies[next(iter(self.monument_replies))]
        return replies

    def guilds(self, packet, mid, data):
        serial = data['serial_num']
        cached = self.guild_replies.get(serial)
        if cached and cached[0] == packet:
            return cached[1]
        if not serial or serial <= self.last_guild_serial:
            return self.complete(serial, [summon.event(55, {'op_string': '仙盟请求已过期，请刷新后重试'})])
        try:
            now = int(time.time())
            role = self.profile()
            before = copy.deepcopy(role)
            if mid == 1026:
                from . import guild_combat
                events = guild_combat.fight(role, data, now, self.guild_rules, self.journey_rules)
            elif mid == 1097:
                events = guild.chat(role, data['chat_msg'], now, self.guild_rules)
            else:
                events = guild.settle(role, data, now, self.guild_rules, login_fields, self.daily_rules)
                achievements.record_events(role, events, int(time.time()), login_fields)
            gs, current_guild = guild.prepare(role, now, self.guild_rules)
            events += [summon.event(82,n) for n in gs.pop('pending_notices',[])]
            if mid == 1301 and current_guild and data['id'] in guild.MANAGEMENT:
                current_guild['events'].append(role['role_name'] + '：' + guild.OP_LABELS.get(data['id'], '仙盟管理操作') + '（' + str(now) + '）')
                current_guild['events'] = current_guild['events'][-100:]
            guild.offline.audit(before,role,now,data.get('id',data.get('fight_type',23)),self.guild_rules)
            attrs = [dict(type=t, value=role.get(k, 0)) for t, k in ((141,'union_join_count'),(143,'union_apply_count'),(7, 'silver_coin'), (8, 'gold_coin'),
                (101, 'strength'), (102, 'energy'), (144, 'union_id'), (145, 'union_rank'), (146, 'union_contrib'), (148, 'cur_union_contrib'), (147, 'union_store_flush_time'), (151, 'last_feast_grab_time'), (152, 'last_feast_grab_count'), (153, 'last_rece_award_time'), (154, 'train_tree_rate'), (155, 'contrib_plus_rate'), (156, 'last_west_book_time'), (157, 'west_book_count'), (158, 'last_stop_book_time'), (159, 'stop_book_count'))]
            replies = self.item_deltas(before, role) + self.inventory(role) + [
                encode(1032, dict(id=role['role_id'], unit_type=1, attr_count=len(attrs), attr_list=attrs)),
                daily.hint(role, now, self.daily_rules)] + events
            self.save(role)
            self.emit('game_guild_ok', operation=data.get('id', data.get('fight_type')), rules_revision=self.guild_rules['revision'])
        except (formation.Rejected, ValueError, KeyError, TypeError, OverflowError, struct.error) as error:
            replies = [summon.event(55, {'op_string': str(error) if isinstance(error, formation.Rejected) else '仙盟数据无效，请刷新后重试'})]
            self.emit('game_guild_rejected', operation=data.get('id', data.get('fight_type')), message=str(error))
        replies = self.complete(serial, replies)
        self.last_guild_serial = serial
        self.guild_replies[serial] = (packet, replies)
        if len(self.guild_replies) > 256:
            del self.guild_replies[next(iter(self.guild_replies))]
        return replies

    def welfares(self, packet, mid, data):
        serial = data['serial_num']
        if mid == 1102:
            # Original getMoreSysMail sends serial 0: this is a read, not a
            # serialized reward mutation. Do not consume the claim watermark.
            try:
                now = int(time.time())
                role = self.profile()
                state = welfare.prepare(role, now, self.welfare_rules)
                replies = welfare.mail_request(role, mid, data, now, self.welfare_rules, state)
                self.emit('game_mail_read', mail_id=data['mail_id'])
            except (formation.Rejected, ValueError, KeyError, TypeError, OverflowError, struct.error) as error:
                replies = [summon.event(55, {'op_string': str(error) if isinstance(error, formation.Rejected) else '邮件数据无效'})]
            return self.complete(serial, replies) if serial else self.number_replies(replies)
        cached = self.welfare_replies.get(serial)
        if cached and cached[0] == packet:
            return cached[1]
        if not serial or serial <= self.last_welfare_serial:
            return self.complete(serial, [summon.event(55, {'op_string': '福利请求已过期，请刷新后重试'})])
        try:
            now = int(time.time())
            role = self.profile()
            before = copy.deepcopy(role)
            events = welfare.settle(role, mid, data, now, self.welfare_rules, login_fields)
            achievements.record_events(role, events, int(time.time()), login_fields)
            replies = self.item_deltas(before, role) + self.inventory(role) + summon.soul_snapshots(role) + [
                welfare_attributes(role), vip.attrs(role), summon.event(80,dict(local_vip=vip.client_state(role)))] + events + [welfare.hint(role, now, self.welfare_rules),welfare.mail_snapshot(role,now,self.welfare_rules)]
            self.save(role)
            self.emit('game_welfare_ok', message_id=mid, rules_revision=self.welfare_rules['revision'])
        except (formation.Rejected, ValueError, KeyError, TypeError, OverflowError, struct.error) as error:
            replies = [summon.event(55, {'op_string': str(error) if isinstance(error, formation.Rejected) else '福利数据无效，请刷新后重试'})]
            self.emit('game_welfare_rejected', message_id=mid, message=str(error))
        replies = self.complete(serial, replies)
        self.last_welfare_serial = serial
        self.welfare_replies[serial] = (packet, replies)
        if len(self.welfare_replies) > 256:
            del self.welfare_replies[next(iter(self.welfare_replies))]
        return replies

    def vips(self, packet, mid, data):
        serial = data['serial_num']
        cached = self.vip_replies.get(serial)
        if cached and cached[0] == packet:
            return cached[1]
        if not serial or serial <= self.last_vip_serial:
            return self.complete(serial, [summon.event(55, {'op_string': 'VIP请求已过期，请刷新后重试'})])
        try:
            now = int(time.time())
            role = self.profile()
            before = copy.deepcopy(role)
            if mid == 1336 or mid == 1051 and data['item_type'] == 1249:
                events = xianling.settle(role, mid, data, now, self.xianling_rules)
                achievements.record_events(role, events, int(time.time()), login_fields)
            else:
                events = vip.settle(role, mid, data, now, self.vip_rules, login_fields)
                achievements.record_events(role, events, int(time.time()), login_fields)
            charged = role.get('charge_gold',0)-before.get('charge_gold',0)
            if charged > 0:
                xianling.record_charge(role, charged, now)
                welfare.record_charge(role, charged, now, self.welfare_rules)
            journey.prepare(role, now, self.journey_rules)
            activity.prepare(role, now, self.activity_rules)
            formation.prepare(role, self.formation_rules)
            replies = self.companion_deltas(before, role) + self.item_deltas(before, role) + self.inventory(role) + self.power_attributes(role) + [vip.attrs(role),
                summon.event(80, dict(local_vip=vip.client_state(role)))] + events
            if mid in (1336,1111):
                replies.append(xianling.tip(role,now,self.xianling_rules))
                if mid == 1111:
                    replies = [welfare.hint(role,now,self.welfare_rules), welfare_attributes(role)] + replies
            self.save(role)
            self.emit('game_vip_ok', message_id=mid, rules_revision=self.vip_rules['revision'])
        except (formation.Rejected, ValueError, KeyError, TypeError, OverflowError, struct.error) as error:
            replies = [summon.event(55, {'op_string': str(error) if isinstance(error, formation.Rejected) else 'VIP数据无效，请刷新后重试'})]
            self.emit('game_vip_rejected', message_id=mid, message=str(error))
        replies = self.complete(serial, replies)
        self.last_vip_serial = serial
        self.vip_replies[serial] = (packet, replies)
        if len(self.vip_replies) > 256:
            del self.vip_replies[next(iter(self.vip_replies))]
        return replies

    def dailies(self, packet, mid, data):
        serial = data['serial_num']
        cached = self.daily_replies.get(serial)
        if cached and cached[0] == packet:
            return cached[1]
        if not serial or serial <= self.last_daily_serial:
            return self.complete(serial, [summon.event(55, {'op_string': '日常请求已过期，请刷新后重试'})])
        try:
            now = int(time.time())
            role = self.profile()
            before = copy.deepcopy(role)
            events = daily.settle(role, mid, data, now, self.daily_rules, login_fields)
            achievements.record_events(role, events, int(time.time()), login_fields)
            attrs = [dict(type=t, value=role[k]) for t, k in ((7, 'silver_coin'), (8, 'gold_coin'))]
            replies = self.item_deltas(before, role) + self.inventory(role) + [
                encode(1032, dict(id=role['role_id'], unit_type=1, attr_count=len(attrs), attr_list=attrs)),
                daily.hint(role, now, self.daily_rules)] + events
            self.save(role)
            self.emit('game_daily_ok', message_id=mid, rules_revision=self.daily_rules['revision'])
        except (formation.Rejected, ValueError, KeyError, TypeError, OverflowError, struct.error) as error:
            replies = [summon.event(55, {'op_string': str(error) if isinstance(error, formation.Rejected) else '日常数据无效，请刷新后重试'})]
            self.emit('game_daily_rejected', message_id=mid, message=str(error))
        replies = self.complete(serial, replies)
        self.last_daily_serial = serial
        self.daily_replies[serial] = (packet, replies)
        if len(self.daily_replies) > 256:
            del self.daily_replies[next(iter(self.daily_replies))]
        return replies

    def rebirth(self, packet, mid, data):
        serial = data['serial_num']
        cached = self.reborn_replies.get(serial)
        if cached and cached[0] == packet:
            return cached[1]
        if not serial or serial <= self.last_reborn_serial:
            return self.complete(serial, [summon.event(55, {'op_string': '转生请求已过期，请刷新后重试'})])
        try:
            role = self.profile()
            before = copy.deepcopy(role)
            events = (reborn.settle(role, data, self.reborn_rules, login_fields) if mid == 1328 else
                      reborn_stars.settle(role, mid, data, self.reborn_rules, login_fields))
            achievements.record_events(role, events, int(time.time()), login_fields)
            welfare.track(role,mid,data,events,int(time.time()),self.welfare_rules)
            events = daily.track(role, before, mid, data, events, int(time.time()), self.daily_rules, login_fields) + events
            reborn.prepare(role, self.reborn_rules)
            formation.recalculate(role, self.formation_rules)
            attrs = [dict(type=t, value=role.get(k, 0)) for t, k in
                     ((7, 'silver_coin'), (8, 'gold_coin'), (30, 'role_combat_power'), (39, 'max_combat_power'),
                      (580, 'reborn_layer'), (581, 'maxlayer_reborn_count'))]
            replies = self.companion_deltas(before, role) + self.item_deltas(before, role)
            old_skills = {x['id']: x for x in before['attachments'] if x['attach_type'] == 6}
            for item in role['attachments']:
                old = old_skills.get(item['id'])
                if old and old.get('awaken', 0) != item.get('awaken', 0):
                    replies.append(encode(1032, dict(id=item['id'], unit_type=6, attr_count=1,
                                   attr_list=[dict(type=65, value=item.get('awaken', 0))])))
            # Preserve selected objects during repeated rebirth/upgrade callbacks.
            if mid in (1332, 1337, 1338, 1339, 1341, 1342):
                replies += self.inventory(role)
            replies += [encode(1032, dict(id=role['role_id'], unit_type=1,
                         attr_count=len(attrs), attr_list=attrs))] + events
            self.save(role)
            self.emit('game_reborn_ok', message_id=mid)
        except (formation.Rejected, ValueError, KeyError, TypeError, OverflowError, struct.error) as error:
            replies = [summon.event(55, {'op_string': str(error) if isinstance(error, formation.Rejected) else '转生数据无效，请刷新后重试'})]
            self.emit('game_reborn_rejected', message_id=mid, message=str(error))
        replies = self.complete(serial, replies)
        self.last_reborn_serial = serial
        self.reborn_replies[serial] = (packet, replies)
        if len(self.reborn_replies) > 256:
            del self.reborn_replies[next(iter(self.reborn_replies))]
        return replies

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
                achievements.record_events(role, events, int(time.time()), login_fields)
                formation.recalculate(role, self.formation_rules)
                attrs = [dict(type=t, value=role.get(k, 0)) for t, k in
                         ((7, 'silver_coin'), (8, 'gold_coin'), (30, 'role_combat_power'), (39, 'max_combat_power'))]
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

    def journey_attributes(self, role):
        fields = {3: 'level', 5: 'cur_exp', 6: 'next_exp', 7: 'silver_coin', 8: 'gold_coin',
                  30: 'role_combat_power', 39: 'max_combat_power', 71: 'cortege_count', 101: 'strength', 102: 'energy',
                  64: 'tollgate_flush_limit', 65: 'tollgate_flush_count', 66: 'tollgate_flush_time',
                  91: 'sweep_flush_limit', 92: 'sweep_flush_count', 93: 'last_sweep_time',
                  511: 'elite_tollgate_flush_count', 512: 'elite_tollgate_flush_time',
                  513: 'elite_fight_count', 514: 'elite_fight_time',
                  55: 'strength_item_count', 56: 'strength_item_time',
                  57: 'energy_item_count', 58: 'energy_item_time',
                  59: 'strength_item_limit', 60: 'energy_item_limit'}
        attrs = [dict(type=t, value=int(role.get(k, 0))) for t, k in fields.items()]
        return [encode(1032, dict(id=role['role_id'], unit_type=1, attr_count=len(attrs), attr_list=attrs))]

    def journeys(self, packet, mid, data):
        serial = data['serial_num']
        now = int(time.time())
        if mid == 1018:
            role = self.profile()
            journey.prepare(role, now, self.journey_rules)
            self.save(role)
            return self.complete(serial, journey.snapshots(role))
        cached = self.journey_replies.get(serial)
        if cached and cached[0] == packet:
            return cached[1]
        if not serial or serial <= self.last_journey_serial:
            return self.complete(serial, [summon.event(55, {'op_string': '旅途请求已过期，请刷新后重试'})])
        try:
            role = self.profile()
            journey.prepare(role, now, self.journey_rules)
            before = copy.deepcopy(role)
            events = journey.settle(role, mid, data, now, self.journey_rules, self.formation_rules, self.activity_rules)
            achievements.record_events(role, events, int(time.time()), login_fields)
            welfare.track(role,mid,data,events,now,self.welfare_rules)
            hints = daily.track(role, before, mid, data, events, now, self.daily_rules, login_fields)
            # Keep the sweep result first and the battle-start callback last.
            events = events + hints if mid == 1061 else hints + events
            formation.prepare(role, self.formation_rules)
            immortal.prepare(role, self.immortal_rules)
            # Keep existing companion tables alive for the battle-end experience UI.
            # Refresh inventory before event 44 starts the original replay.
            replies = []
            if mid not in (1018, 2998):
                replies = (self.companion_deltas(before, role) + self.item_deltas(before, role)
                           + self.inventory(role) + summon.soul_snapshots(role)
                           + journey.updates(role, before))
            replies += self.journey_attributes(role) + events
            self.save(role)
            self.emit('game_journey_ok', message_id=mid, rules_revision=self.journey_rules['revision'])
        except (formation.Rejected, ValueError, KeyError, TypeError, OverflowError, struct.error) as error:
            replies = [summon.event(55, {'op_string': str(error) if isinstance(error, formation.Rejected) else '旅途数据无效，请刷新后重试'})]
            self.emit('game_journey_rejected', message_id=mid, message=str(error))
        replies = self.complete(serial, replies)
        self.last_journey_serial = serial
        self.journey_replies[serial] = (packet, replies)
        if len(self.journey_replies) > 256:
            del self.journey_replies[next(iter(self.journey_replies))]
        return replies

    def activities(self, packet, mid, data):
        serial = data['serial_num']
        now = int(time.time())
        # [A] abyssUI sends query_tips without a request serial. This is the
        # only activity poll exempted from mutation-request replay validation.
        poll = mid == 1329 and data.get('id') == 15 and serial == 0
        cached = self.activity_replies.get(serial) if not poll else None
        if cached and cached[0] == packet:
            return cached[1]
        if not poll and (not serial or serial <= self.last_activity_serial):
            return self.complete(serial, [summon.event(55, {'op_string': '活动请求已过期，请刷新后重试'})])
        try:
            role = self.profile()
            before = copy.deepcopy(role)
            events = activity.settle(role, mid, data, now, self.activity_rules,
                                     self.journey_rules, self.formation_rules, login_fields)
            achievements.record_events(role, events, int(time.time()), login_fields)
            welfare.track(role,mid,data,events,int(time.time()),self.welfare_rules)
            events = daily.track(role, before, mid, data, events, now, self.daily_rules, login_fields) + events
            formation.prepare(role, self.formation_rules)
            immortal.prepare(role, self.immortal_rules)
            attrs = activity.attributes(role) + self.power_attributes(role)
            replies = (self.companion_deltas(before, role) + self.item_deltas(before, role)
                       + self.inventory(role) + summon.soul_snapshots(role)
                       + immortal.handbook(role, self.immortal_rules) + attrs + events)
            if poll:
                replies = events
            self.save(role)
            self.emit('game_activity_ok', message_id=mid, rules_revision=self.activity_rules['revision'])
        except (formation.Rejected, ValueError, KeyError, TypeError, OverflowError, struct.error) as error:
            replies = [summon.event(55, {'op_string': str(error) if isinstance(error, formation.Rejected) else '活动数据无效，请刷新后重试'})]
            self.emit('game_activity_rejected', message_id=mid, message=str(error))
        if poll:
            return self.number_replies(replies)
        replies = self.complete(serial, replies)
        self.last_activity_serial = serial
        self.activity_replies[serial] = (packet, replies)
        if len(self.activity_replies) > 256:
            del self.activity_replies[next(iter(self.activity_replies))]
        return replies


def welfare_attributes(role):
    pairs=((7,'silver_coin'),(8,'gold_coin'),(53,'first_charge'),(23,'first_charge_gift'),(16,'take_charge_gift_time'),(34,'buy_growup'))
    return encode(1032,dict(id=role['role_id'],unit_type=1,attr_count=len(pairs),attr_list=[dict(type=t,value=role.get(k,0)) for t,k in pairs]))
