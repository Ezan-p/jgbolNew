"""Export the blood-arena allocation and audit 52 weeks without changing saves."""
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity_arena as arena, npc_players


def main():
    day = (date(2026, 11, 9)-date(1970, 1, 1)).days
    catalog = npc_players.catalog()
    tiers = {}
    for tier in (f'E{i}' for i in range(1, 7)):
        entries = [e for e in catalog.values() if e['profile']['tier'] == tier]
        powers = []
        for entry in entries:
            npc = npc_players.get(entry['npc_id'])
            power = npc['role']['role_combat_power']
            assert power == entry['profile']['role_combat_power'], entry['npc_id']
            assert npc_players.resolve(npc['role']['role_id']) == entry['npc_id']
            assert len(npc_players.inspection_data(npc)['cortege_list']) == 8
            powers.append(power)
        tiers[tier] = dict(candidates=len(entries), min_power=min(powers), max_power=max(powers))
    strongest = {}
    actual_powers = {}
    power_differences = {}
    for group, (lo, hi) in enumerate(arena.rules()['arena_groups'], arena.FIRST_GROUP):
        eligible = [e for e in catalog.values() if lo <= e['profile']['level'] <= hi]
        for entry in eligible:
            npc = npc_players.get(entry['npc_id'])
            key = entry['npc_id']
            actual_powers[key] = npc['role']['role_combat_power']
            if actual_powers[key] != entry['profile']['role_combat_power']:
                power_differences[key] = dict(catalog=entry['profile']['role_combat_power'], actual=actual_powers[key])
            assert npc['role']['level'] == entry['profile']['level'], entry['npc_id']
        strongest[group] = [e['npc_id'] for e in sorted(
            eligible, key=lambda e: (actual_powers[e['npc_id']], e['npc_id']), reverse=True)[:15]]
    sample = {}
    seen = set()
    for week in range(52):
        for group, (lo, hi) in enumerate(arena.rules()['arena_groups'], arena.FIRST_GROUP):
            keys = arena.select_roster(group, day+week*7)
            assert len(keys) == len(set(keys)) == 19
            profiles = [catalog[key]['profile'] for key in keys]
            assert all(lo <= p['level'] <= hi for p in profiles)
            assert list(reversed(keys))[:15] == strongest[group]
            assert all(catalog[k]['profile']['tier'].startswith('T') for k in keys[:4])
            seen.update(k for k in keys if catalog[k]['profile']['tier'].startswith('E'))
            assert keys == arena.select_roster(group, day+week*7+6)
            if week == 0:
                sample[group] = [dict(npc_id=key, actual_combat_power=actual_powers[key], **catalog[key]['profile']) for key in reversed(keys)]
    report = dict(sample_week='2026-11-09', revision=arena.rules()['revision'],
                  weeks_checked=52, groups_checked=208, top_power_count=15, extreme_candidates=tiers,
                  distinct_extremes_in_52_weeks=len(seen), sample_rosters=sample,
                  catalog_power_differences=power_differences, native_client_playback_tested=False)
    output = ROOT / 'analysis/evidence/taixu/arena_top15_roster.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('sample_rosters', 'catalog_power_differences')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
