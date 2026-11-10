"""One-time additive v108 test grant; never imported by the official payload."""
from collections import Counter
from .test_edition_seed import ACCOUNT

REVISION = 108
COMPANIONS = (5046, 5013)  # 元始天尊、六耳猕猴
EQUIPMENT = (2044, 3003)  # 盘古幡、无极道袍
SILVER_WALLET = 2_000_000_000  # Native attribute updates are signed int32.


def refill_silver(role):
    reserve = role.get('test_v108_silver_reserve', 0)
    take = min(reserve, max(0, SILVER_WALLET - role.get('silver_coin', 0)))
    role['silver_coin'] = role.get('silver_coin', 0) + take
    if reserve or 'test_v108_silver_reserve' in role:
        role['test_v108_silver_reserve'] = reserve - take
    return take


def material_plan():
    from network_redirect import formation as f, reborn as r, fate_rebuild as fr
    from network_redirect import activity_home as h, equipment as e, immortal
    items, skills, stones = Counter(), Counter(), Counter()
    silver = 0
    home_gold = 0

    def reborn_cost(text, copies=1):
        for token in text.split('/'):
            kind, tid, level, count = map(int, token.split('|'))
            assert kind == 5 and level == 1
            items[tid] += count * copies

    # Full costs for two companions, in addition to all original v106 stock.
    for row in r.VEINS.values():
        parts = [list(map(int, p.split('|'))) for p in row['consume_list'].split('/')]
        fixed = int(row['fixed_count(fix>0|unfix=0)'])
        if fixed:
            items[parts[0][1]] += fixed * 2
        else:
            reborn_cost(row['consume_list'], 2)
    for row in r.LAYERS.values():
        reborn_cost(row['consum_list'], 2)
    for realm in r.load_rules()['realms']:
        items[realm['material']] += realm['cost']
    book = max(f.EXPERIENCE_BOOKS, key=lambda t: int(f.ITEMS[t]['experience_plus']))
    worth = int(f.ITEMS[book]['experience_plus'])
    # 1->600 plus every rebirth reset; round each feed separately.
    exp_segments = [sum(f.EXPERIENCE[5, lv] for lv in range(1, 600))]
    exp_segments += [sum(f.EXPERIENCE[5, lv] for lv in range(int(row['reset_level']), int(row['min_level'])))
                     for row in r.LAYERS.values()]
    items[book] += 2 * sum((exp + worth - 1) // worth for exp in exp_segments)
    souls = {str(t): sum(f.EVOLVE_COST[lv] for lv in range(1, 500)) for t in COMPANIONS}

    for tid in EQUIPMENT:
        kind = int(f.ITEMS[tid]['main_type'])
        cfg = f.load_rules()['equipment_advance']
        for advance in range(cfg['max_advance_level']):
            for star in range(1, cfg['max_star_level'] + 1):
                items[{1: 1310, 2: 1311, 3: 1312}[kind]] += int(f.STAR_COST[5, star][advance].split('|')[kind - 1])
            for token in f.ADVANCE_COST[5, advance + 1][{1: 'wuqi_cost', 2: 'fangyu_cost', 3: 'fabao_cost'}[kind]].split('/'):
                t, n = map(int, token.split('|'))
                items[t] += n
        reborn_cost(list(r.EQUIP[kind].values())[1])
        for (k, level), row in r.CAST.items():
            if k == kind and level > 1:
                reborn_cost(list(row.values())[2])
        silver += sum(int(f.EQUIP_COST[lv]['star5_money']) for lv in range(1, 198))

    def home_cost(text, copies=1):
        nonlocal silver, home_gold
        for p in h.specs(text):
            typ, tid, count = (p[0], 0, p[1]) if len(p) == 2 else p[:3]
            if typ == 12:
                silver += count * copies
            elif typ == 11:
                home_gold += count * copies
            else:
                assert typ == 5
                items[tid] += count * copies
    for (typ, level), row in h.UPGRADE.items():
        if level in h.BUILD[typ]:
            home_cost(row['cost'])
    for level, row in h.OWNER.items():
        if level > 1:
            home_cost(row['upgrade_list'])
    for level, row in h.GRIDS.items():
        if level > 0:
            home_cost(row['cost'], int(h.BUILD[2][max(h.BUILD[2])]['grid_count']))

    items[1371] += 20 * 2  # Activation, separately from all ten paths.
    for raw in fr.COSTS.values():
        tokens = list(map(int, raw.split('|')))
        chosen = dict(zip(tokens[1::2], tokens[2::2])) if tokens[0] == 3 else {tokens[1]: tokens[-1]}
        dest = skills if tokens[0] == 2 else items
        for tid, count in chosen.items():
            dest[tid] += count * 2
    # These twenty copies remain even after all reserved progression materials.
    for tid in immortal.ESSENCES:
        items[tid] += 20

    items[1093] += 12  # Four holes in each of the three equipment categories.
    items[1369] += 60  # Three six-star upgrades unlock each fourth hole.
    for tid, kind in e.STONES.items():
        stones[tid, 1] += 4
        for old in range(1, 10):
            # Two level-10 donors always exceed the original 100% threshold.
            assert 2 * float(e.STONE_VALUES[kind, 10]['worth']) >= float(e.STONE_VALUES[kind, old]['cost'])
            stones[tid, 10] += 2 * 4
            silver += int(e.STONE_VALUES[kind, old]['silver_cost']) * 4
        for level in range(11, e.STONE_MAX_LEVEL[kind] + 1):
            for token in list(e.STONE_REBORN[kind, level].values())[2].split('/'):
                typ, t, count, lv = map(int, token.split('|'))
                assert typ == 5
                if t in e.STONES:
                    stones[t, lv] += count * 4
                else:
                    assert lv == 1
                    items[t] += count * 4
    return dict(items=items, skills=skills, stones=stones, souls=souls,
                silver=silver, gold=100000, home_gold_cost=home_gold, gear_donors=(2044, 3003, 4003))


def grant(role):
    from network_redirect import summon, formation as f
    if role.get('test_supply_revision', 0) >= REVISION:
        return False
    plan = material_plan()
    for tid in COMPANIONS:
        if not any(c['type'] == tid for c in role['corteges']):
            role['corteges'].append(summon.companion(role, tid))
    for tid in plan['gear_donors']:
        if not any(i['attach_type'] == 5 and i['type_id'] == tid for i in role['attachments']):
            summon.add_item(role, tid, 1)
    for tid in plan['gear_donors']:
        # Same-name sacrifices must be distinct unequipped instances.
        role['attachments'].append(dict(id=f.new_id(role), attach_type=5, type_id=tid, count=1, level=1))
    for tid, count in sorted(plan['items'].items()):
        summon.add_item(role, tid, count)
    for tid, count in sorted(plan['skills'].items()):
        for _ in range(count):
            role['attachments'].append(dict(id=f.new_id(role), attach_type=6, type_id=tid, count=1, level=1))
    for (tid, level), count in sorted(plan['stones'].items()):
        for _ in range(count):
            role['attachments'].append(dict(id=f.new_id(role), attach_type=5, type_id=tid, count=1, level=level))
    for tid, count in plan['souls'].items():
        role.setdefault('souls', {})[tid] = role['souls'].get(tid, 0) + count
    role['gold_coin'] += plan['gold']
    role['test_v108_silver_reserve'] = role.get('test_v108_silver_reserve', 0) + plan['silver']
    refill_silver(role)
    role['test_supply_revision'] = REVISION
    return True


def initialize(backend, now):
    import tempfile
    from pathlib import Path
    from network_redirect.backend import Backend
    from .test_edition_seed import build_role
    exists = backend.db.execute('SELECT 1 FROM roles WHERE account=?', (ACCOUNT,)).fetchone()
    if exists:
        role = backend.profile()
        if not grant(role):
            return False
    else:
        # Build off-database so even an interrupted first launch cannot publish
        # a partial starter or lose the one-time migration marker.
        directory = Path(backend.db.execute('PRAGMA database_list').fetchone()[2]).parent
        with tempfile.TemporaryDirectory(prefix='seed108-', dir=directory) as tmp:
            scratch = Backend(Path(tmp), backend.port, lambda *a, **k: None, account=ACCOUNT,
                              clock=backend.clock)
            try:
                role = build_role(scratch, now)
                grant(role)
            finally:
                scratch.close()
    # Complete the new companion's innate skill and every default field before
    # committing the grant, so the next launch has no deferred seed changes.
    from network_redirect import formation
    formation.prepare(role, backend.formation_rules)
    backend.save(role, gameplay=False)
    return True


def fixed_accounts_class():
    from network_redirect import game_clock
    from network_redirect.accounts import Accounts
    from network_redirect.backend import Backend
    from network_redirect.protocol import encode

    class TestBackend(Backend):
        def save(self, role, account=None, *, gameplay=True):
            refill_silver(role)
            return super().save(role, account, gameplay=gameplay)

        def complete(self, request_serial, replies):
            # Gameplay encodes its original delta before save; send the balance
            # after the finite reserve transfer before acknowledging the request.
            role = self.profile()
            if role.get('test_supply_revision') == REVISION:
                replies = replies + [encode(1032, dict(id=role['role_id'], unit_type=1,
                    attr_count=1, attr_list=[dict(type=7, value=role['silver_coin'])]))]
            return super().complete(request_serial, replies)

    class FixedAccounts(Accounts):
        def __init__(self, directory, port, emit, *, network_time=None):
            super().__init__(directory, port, emit, network_time=network_time)
            fixed = TestBackend(directory, port, emit, account=ACCOUNT, clock=self.base.clock)
            self.backends[ACCOUNT] = fixed
            try:
                with game_clock.scope(fixed.clock) as now:
                    initialize(fixed, now)
            except BaseException:
                self.close()
                raise

        def authenticate(self, data, remembered=''):
            return self.start_session(ACCOUNT)

    return FixedAccounts
