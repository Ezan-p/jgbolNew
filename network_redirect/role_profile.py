"""3.87 profile wire contracts [A], configurable missing server policies [B]."""
import csv
import io
import copy
import secrets
import json
import re
import time
from pathlib import Path
from . import formation as f, summon
from .protocol import encode

ROOT = Path(__file__).resolve().parents[1]
HANDLED = {1031, 1069, 1070, 1078, 1307}
HEADS = {101, 102, 103, 104, 201, 202, 203, 204}
# Bare CR occurs inside original unquoted descriptions; LF separates records.
RUNES = {int(r['id']): r for r in csv.DictReader(io.StringIO(
    (ROOT / 'analysis/configs/rune.csv').read_bytes().decode('utf-8-sig').replace('\r', '')))}
TITLES = {int(r['title_id']): r for r in summon.rows('title_config.csv')}


def load_rules(path=ROOT / 'server_config/profile_rules.json'):
    r = json.loads(path.read_text())
    f.require(r['mode'] == 'inferred', '角色配置模式无效')
    for key in ('rename_count', 'name_min', 'name_max', 'head_gold', 'ling_open_level'):
        f.require(type(r[key]) is int and r[key] > 0, '角色配置数值无效')
    f.require(r['name_min'] <= r['name_max'] <= 7 and r['rename_item'] in f.ITEMS, '改名配置无效')
    f.require(r['initial_head'] == 1 and r['initial_genius'] in RUNES, '角色初始配置无效')
    for key in ('genius_single_percent', 'genius_all_percent'):
        f.require(type(r[key]) is int and 0 <= r[key] <= 100, '天赋增益配置无效')
    f.require(type(r['ling_is_open']) is bool and isinstance(r['blocked_names'], list), '角色开关无效')
    f.require(isinstance(r['simulated_title_results'], dict), '模拟称号成绩无效')
    for k, v in r['simulated_title_results'].items():
        f.require(k in ('imperial_rank', 'duty_rank', 'prey_layer', 'prey_rank', 'hunt_rank', 'single_rank')
                  and type(v) is int and v >= 0, '模拟称号成绩无效')
    return r


def grant_title(role, tid, now):
    """Trusted server award, never a client-selected entitlement. Repeat within a period is idempotent."""
    row = TITLES[tid]
    titles = role.setdefault('profile_titles', {})
    if int(row['category(1permanent|2tmp)']) == 1:
        titles.setdefault(str(tid), dict(id=tid, begintime=now, endtime=0))
    else:
        seconds = {'h': 3600, 'w': 7 * 86400, 'm': 30 * 86400}[row['time_unit']] * int(row['keeptime'])
        # [B] Fixed UTC+8 award periods; re-query cannot extend the lease.
        start = (now + 28800) // seconds * seconds - 28800
        titles[str(tid)] = dict(id=tid, begintime=max(0, start), endtime=start + seconds)


def prepare(role, rules=None, now=None):
    rules = rules or load_rules()
    now = int(time.time()) if now is None else now
    if role.get('head_type') not in HEADS:
        role['head_type'] = rules['initial_head']
    role.setdefault('profile_head_changed', role['head_type'] in HEADS)
    if role.get('cur_genius_type') not in RUNES:
        role['cur_genius_type'] = rules['initial_genius']
    titles = role.setdefault('profile_titles', {})
    # Preserve a previously awarded legacy equipped title.
    tid = role.get('title_id', 0)
    if tid in TITLES and str(tid) not in titles:
        titles[str(tid)] = dict(id=tid, begintime=role.get('title_begintime', now), endtime=role.get('title_endtime', 0))
    groups = [
        (range(1, 6), (36, 45, 60, 70, 80), role.get('level', 1)),
        (range(6, 10), (1, 2, 3, 4), role.get('reborn_layer', 0)),
        (range(10, 14), (1, 3, 6, 9), max((c.get('reborn_layer', 0) for c in role.get('corteges', [])), default=0)),
        (range(20, 25), (200000, 500000, 1000000, 1500000, 2500000), role.get('max_combat_power', 0)),
        (range(30, 35), (10, 25, 40, 50, 60), max((c.get('evolve_level', 0) for c in role.get('corteges', [])), default=0)),
        (range(40, 45), (12, 24, 36, 54, 72), role.get('activity', {}).get('abyss', {}).get('boss', 1) - 1),
    ]
    for ids, limits, value in groups:
        for tid, minimum in zip(ids, limits):
            if value >= minimum:
                grant_title(role, tid, now)
    results = dict(rules['simulated_title_results'], **role.get('profile_title_results', {}))
    # Existing local leaderboards are authoritative when present.
    results.setdefault('top_rank', role.get('top_order', 0))
    results.setdefault('single_rank', role.get('single_rank', 0))
    rank = results.get('imperial_rank', 0)
    if 0 < rank <= 100:
        grant_title(role, 50, now)
        if rank <= 3:
            grant_title(role, 54 - rank, now)
    for metric, base in (('top_rank', 100), ('duty_rank', 110), ('prey_rank', 125), ('hunt_rank', 130), ('single_rank', 140)):
        rank = results.get(metric, 0)
        if 0 < rank <= 10:
            grant_title(role, base + (3 if rank == 1 else 2 if rank <= 3 else 1 if rank <= 6 else 0), now)
    for tid, minimum in zip(range(120, 125), (32, 40, 48, 55, 60)):
        if results.get('prey_layer', 0) >= minimum:
            grant_title(role, tid, now)
    tid = role.setdefault('title_id', 0)
    active = titles.get(str(tid))
    if not active or not available(active, now):
        role.update(title_id=0, title_begintime=0, title_endtime=0)
    else:
        role.update(title_begintime=active['begintime'], title_endtime=active['endtime'])


def available(title, now):
    row = TITLES.get(title['id'])
    return bool(row and title['begintime'] <= now and
                (title['endtime'] > now or title['endtime'] == 0 and int(row['category(1permanent|2tmp)']) == 1))


def titles_packet(role):
    # Include expired records: native UI keeps ownership and computes expiry itself.
    titles = sorted(role['profile_titles'].values(), key=lambda t: t['id'])
    return encode(1077, dict(new=0, wear_id=role['title_id'], role_id=role['role_id'], title_count=len(titles), titles=titles))


def attributes(role):
    fields = ((8, 'gold_coin'), (29, 'head_type'), (86, 'cur_genius_type'))
    return encode(1032, dict(id=role['role_id'], unit_type=1, attr_count=len(fields),
        attr_list=[dict(type=i, value=role[k]) for i, k in fields]))


def result(event, code, **data):
    return [summon.event(event, dict(result=code, **data))]


def settle(role, mid, req, now, rules, names=(), target=None):
    prepare(role, rules, now)
    if mid == 1307:
        f.require(req['flag'] in (1, 2), '资料查询标志无效')
        return [titles_packet(role), summon.event(159, dict(role_info=dict(
            union_name=role.get('union_name', ''), ling_is_open=rules['ling_is_open'],
            ling_open_level=rules['ling_open_level'])))]
    if mid == 1031:
        name = req['new_name']
        if len(name) < rules['name_min']:
            return result(12, 4)
        if len(name) > rules['name_max']:
            return result(12, 5)
        if not re.fullmatch(r'[\u3400-\u4dbf\u4e00-\u9fff]+', name) or any(word and word in name for word in rules['blocked_names']):
            return result(12, 3)
        if name == role['role_name']:
            return result(12, 6)
        if name in names:
            return result(12, 2)
        count = sum(i['count'] for i in role['attachments'] if i['attach_type'] == 5 and i['type_id'] == rules['rename_item'] and not i.get('is_lock'))
        if count < rules['rename_count']:
            return result(12, 7)
        f.debit_item(role, rules['rename_item'], rules['rename_count'])
        role['role_name'] = name
        return result(12, 1, new_name=name)
    if mid == 1069:
        head, flag = req['head_type'], req['flag']
        if head not in HEADS or flag not in (0, 1):
            return result(99, 6)
        if head == role['head_type'] and role['profile_head_changed']:
            return result(99, 6)
        if flag == 0:
            if role['profile_head_changed']:
                return result(99, 6)
        else:
            if head // 100 != role['head_type'] // 100:
                return result(99, 6)
            if role['gold_coin'] < rules['head_gold']:
                return result(99, 8)
            f.debit_money(role, 'gold_coin', rules['head_gold'])
        role.update(head_type=head, profile_head_changed=True)
        return result(99, 1)
    if mid == 1070:
        tid = req['type_id']
        if tid not in RUNES or tid == role['cur_genius_type']:
            return result(109, 3)
        if role['level'] < int(RUNES[tid]['open_level']):
            return result(109, 2)
        role['cur_genius_type'] = tid
        return result(109, 1)
    if mid == 1078:
        flag, tid = req['flag'], req['des_id']
        f.require(flag in (1, 2, 3), '称号操作无效')
        if flag == 3:
            f.require(tid == int(tid), '称号编号无效')
            tid = int(tid)
            f.require(tid == 0 or str(tid) in role['profile_titles'] and available(role['profile_titles'][str(tid)], now), '称号尚未获得或已经到期')
            role['title_id'] = tid
            active = role['profile_titles'].get(str(tid), {})
            role.update(title_begintime=active.get('begintime', 0), title_endtime=active.get('endtime', 0))
        elif flag == 2:
            f.require(target is not None, '目标角色不存在')
            return [titles_packet(target)]
        return [summon.event(175, dict(wear_id=role['title_id']))] if flag == 3 else [titles_packet(role)]
    raise f.Rejected('未知角色资料操作')


def talent_units(role, units, probability, rules=None):
    """[A] Rune target/stat and map probability; [B] percentage and pre-battle timing."""
    units = copy.deepcopy(units)
    tid = role.get('cur_genius_type', 0)
    row = RUNES.get(tid)
    if not row or role.get('level', 0) < int(row['open_level']) or secrets.randbelow(100) >= max(0, min(100, probability)):
        return units, dict(use_genius=False, use_order=0)
    targets = [u for u in units[0] if u['hp'] > 0]
    if not targets:
        return units, dict(use_genius=False, use_order=0)
    rules = rules or load_rules()
    single = tid % 2 == 1
    if single:
        targets = [targets[secrets.randbelow(len(targets))]]
    percent = rules['genius_single_percent' if single else 'genius_all_percent']
    stat = {'1': 'gongji', '2': 'hp', '3': 'fangyu'}[row['eff']]
    for unit in targets:
        gain = unit[stat] * percent // 100
        unit[stat] += gain
        if stat == 'hp':
            unit['max_hp'] += gain
    return units, dict(use_genius=True, use_order=targets[0]['order'] if single else 0)
