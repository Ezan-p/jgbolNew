"""Test-edition-only fixed starter; imported only by the repackaged v106 payload.

No user database is used as an input. Never reseed an existing role.
"""
from collections import Counter

ACCOUNT = 'v106_fixed_test'
SEED_REVISION = 1


def material_plan():
    from network_redirect import formation as f, reborn as r
    stock = Counter()
    # Nine rebirths, using the first allowed essence for choice-based veins.
    for row in r.VEINS.values():
        entries = [tuple(map(int, p.split('|'))) for p in row['consume_list'].split('/')]
        fixed = int(row['fixed_count(fix>0|unfix=0)'])
        if fixed:
            stock[entries[0][1]] += fixed
        else:
            for _, tid, _, count in entries:
                stock[tid] += count
    for row in r.LAYERS.values():
        for part in row['consum_list'].split('/'):
            _, tid, _, count = map(int, part.split('|'))
            stock[tid] += count
    # Include realm four to make the requested ninth rebirth reachable.
    for realm in r.load_rules()['realms']:
        stock[realm['material']] += realm['cost']
    cfg = f.load_rules()['equipment_advance']
    for advance in range(cfg['max_advance_level']):
        for star in range(1, cfg['max_star_level'] + 1):
            stock[1310] += int(f.STAR_COST[5, star][advance].split('|')[0])
        for part in f.ADVANCE_COST[5, advance + 1]['wuqi_cost'].split('/'):
            tid, count = map(int, part.split('|'))
            stock[tid] += count
    # Also cover weapon rebirth and all casting levels, beyond requested advance.
    for text in [list(r.EQUIP[1].values())[1]] + [
            list(row.values())[2] for (kind, level), row in r.CAST.items() if kind == 1 and level > 1]:
        for part in text.split('/'):
            _, tid, _, count = map(int, part.split('|'))
            stock[tid] += count
    # Highest scripture; enough XP for level 1->200 and every rebirth reset.
    book = max(f.EXPERIENCE_BOOKS, key=lambda tid: int(f.ITEMS[tid]['experience_plus']))
    experience = sum(f.EXPERIENCE[5, lv] for lv in range(1, 200))
    experience += sum(sum(f.EXPERIENCE[5, lv] for lv in range(int(row['reset_level']), 200))
                      for row in r.LAYERS.values())
    worth = int(f.ITEMS[book]['experience_plus'])
    stock[book] += (experience + worth - 1) // worth + len(r.LAYERS) + 1
    return stock


def build_role(backend, now):
    from network_redirect import formation as f, summon, immortal, guild
    role = backend.profile()
    role.update(role_name='测试行者', level=99, cur_exp=0, vip_level=10,
                charge_gold=backend.vip_rules['thresholds'][10], gold_coin=10000,
                silver_coin=sum(int(f.EQUIP_COST[n]['star5_money']) for n in range(1, 198)),
                guide_progress=0x7fffffff, reborn_layer=0, corteges=[], attachments=[],
                test_seed_revision=SEED_REVISION)
    role.setdefault('summon', {})
    yuanshi = summon.companion(role, 5046)
    yuanshi.update(order=1)
    role['corteges'].append(yuanshi)
    # Three off-lineup helpers satisfy original realm gates, without rule edits.
    for tid in (5045, 5025, 5022):
        helper = summon.companion(role, tid)
        helper.update(level=200, reborn_layer=8, reborn_vein_level=0)
        role['corteges'].append(helper)
    role['souls'] = {'5046': sum(f.EVOLVE_COST[n] for q, n in f.EVOLVE_POINTS if q == 5)}

    def item(kind, tid, level=1, **fields):
        value = dict(id=f.new_id(role), attach_type=kind, type_id=tid,
                     count=0 if kind == 6 else 1, level=level, **fields)
        role['attachments'].append(value)
        return value

    # Three five-star equipment pieces plus the actual four-star fate talisman.
    for tid, pos in ((2044, 1), (3003, 2), (4003, 3)):
        item(5, tid, equip_order=1, equip_pos=pos)
    item(5, 4013)
    item(6, 42, equip_order=1, equip_pos=2)
    # One max-level donor guarantees each of the nine spell upgrades.
    for _ in range(9):
        item(6, 25, level=10)
    for tid in (42, 46):
        item(6, tid)
    for tid, count in sorted(material_plan().items()):
        summon.add_item(role, tid, count)
    # Keep one of every essence after using the reserved rebirth materials.
    for tid in sorted(immortal.ESSENCES):
        summon.add_item(role, tid, 1)
    guild.prepare(role, now, backend.guild_rules)
    g = guild.new_union(2, '测试仙盟', backend.guild_rules)
    g.update(level=5, popularity=4 * backend.guild_rules['level_popularity'])
    g['members'][str(int(role['role_id']))] = dict(
        id=int(role['role_id']), name=role['role_name'], rank=1, level=99,
        contrib=0, totalcontrib=0, head_type=1, jointime=now, lastlogin=now,
        online=True, toporder=0, logout_time=0, combat_power=0)
    role['guild']['unions'] = {'2': g}
    role['guild']['next_id'] = 3
    role.update(union_id=2, union_name=g['name'], union_rank=1)
    guild.prepare(role, now, backend.guild_rules)
    backend.save(role, gameplay=False)
    return backend.profile()


def initialize(backend, now):
    import tempfile
    from pathlib import Path
    from network_redirect.backend import Backend
    if backend.db.execute('SELECT 1 FROM roles WHERE account=?', (ACCOUNT,)).fetchone():
        return False
    # Generate away from the durable database; publish the complete seed once.
    directory = Path(backend.db.execute('PRAGMA database_list').fetchone()[2]).parent
    with tempfile.TemporaryDirectory(prefix='seed-', dir=directory) as tmp:
        scratch = Backend(Path(tmp), backend.port, lambda *a, **k: None, account=ACCOUNT)
        try:
            role = build_role(scratch, now)
        finally:
            scratch.close()
    backend.save(role, gameplay=False)
    return True


def fixed_accounts_class():
    import time
    from network_redirect.accounts import Accounts
    from network_redirect.backend import Backend

    class FixedAccounts(Accounts):
        def __init__(self, directory, port, emit):
            super().__init__(directory, port, emit)
            fixed = Backend(directory, port, emit, account=ACCOUNT)
            initialize(fixed, int(time.time()))
            self.backends[ACCOUNT] = fixed

        def authenticate(self, data, remembered=''):
            return self.start_session(ACCOUNT)

    return FixedAccounts
