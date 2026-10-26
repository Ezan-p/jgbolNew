"""Compare 渡劫 refresh variety on read-only players snapshots; no account writes."""
import copy
import json
from pathlib import Path
import random
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity, activity_rape as rape, activity_rape_npc as npcs


def sample(level, rules):
    role = copy.deepcopy(npcs.catalog()[f'npc_v2_l{level:02d}_t3_attack']['role'])
    role['activity'] = {}
    rng = random.Random(20261026 + level)
    seen, previous, duplicate_boards, overlaps = set(), set(), 0, []
    pools = [len(npcs.candidates(role, i, rules)) for i in range(3)]
    with patch.object(rape, 'rules', return_value=rules), \
            patch.object(rape, 'roll_forms', return_value=[6, 6, 6]), \
            patch('secrets.choice', side_effect=rng.choice):
        for _ in range(12):
            role['activity']['rape_boards'] = None
            boards = rape.ensure(role, 1792814400, activity.load_rules())
            keys = [t['npc_id'] for b in boards for rows in b['form_list'].values()
                    for t in rows.values()]
            assert len(keys) == 18
            assert all(npcs.catalog()[key]['role']['level'] <= level for key in keys)
            for b in boards:
                for i, target in enumerate(b['form_list']['2'].values()):
                    assert target['npc_id'] in npcs.candidates(role, i, rules)
            duplicate_boards += len(keys) != len(set(keys))
            if previous:
                overlaps.append(len(previous.intersection(keys)))
            previous = set(keys)
            seen.update(keys)
            assert len(role['activity']['rape_recent_npcs']) <= rules['recent_npc_limit']
    return dict(candidate_counts=pools, boards=12, guards_per_board=18,
                unique_players=len(seen), boards_with_duplicates=duplicate_boards,
                adjacent_board_overlap=overlaps,
                history_size=len(role['activity']['rape_recent_npcs']))


def main():
    rules = rape.rules()
    old = dict(rules, match_candidates=24, recent_npc_limit=54)
    stages = [dict(level=level, previous=sample(level, old), current=sample(level, rules))
              for level in (8, 25, 60, 99)]
    report = dict(date='2026-10-26', revision=rules['revision'],
                  mode='fixed_seed_T3_attack_maximum_boards', native_ui_verified=False,
                  eligible_players=len(npcs.catalog()), stages=stages)
    dest = ROOT / 'analysis/evidence/rape/matchmaking_validation.json'
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    for row in stages:
        print(f"Level {row['level']}: {row['previous']['unique_players']} -> "
              f"{row['current']['unique_players']} unique NPCs across 12 boards; "
              f"{row['current']['boards_with_duplicates']} boards with duplicates")


if __name__ == '__main__':
    main()
