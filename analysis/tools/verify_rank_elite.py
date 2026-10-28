"""Real combat/replay checks for rank elites; never touches player saves."""
import copy
import json
import random
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity_rank as rank, journey
from analysis.tools import build_npc_catalog as design


def main():
    current = rank.catalog()
    original_rules = dict(rank.rules(), elite_npcs=[])
    with patch.object(rank, 'rules', return_value=original_rules):
        original = rank.catalog.__wrapped__()
    rows = []
    for target in range(1, 6):
        opponents = [(f'elite_{i}', current[930000+i]['role']) for i in range(1, 6) if i != target]
        opponents += [('previous_same_rank', original[930000+target]['role'])]
        for label, opponent in opponents:
            for seed in (17, 83):
                role = copy.deepcopy(opponent)
                role['activity'] = dict(rank_order=100, rank_origin_order=100, rank_slots={},
                                        fight_id=0, rank_day_best=100, rank_records=[])
                rng = random.Random(seed)
                with patch('network_redirect.combat.secrets.randbelow', side_effect=rng.randrange):
                    _, replay = rank.simulate(role, target, design.NOW, journey.load_rules())
                packets = rank.replay_packets(replay)
                assert all(len(p) <= 32768 for p in packets)
                # A normal 30-round HP settlement is supported by the current engine.
                assert replay['stop_reason'] in ('elimination', 'round_limit'), (target, label, seed, replay['stop_reason'])
                rows.append(dict(target=target, opponent=label, seed=seed,
                                 result=replay['fight_result_msg']['final_result'],
                                 stop_reason=replay['stop_reason'], packet_count=len(packets),
                                 largest_packet=max(map(len, packets))))
    out = ROOT / 'analysis/evidence/rank/elite_validation.json'
    out.write_text(design.json_text(dict(battles=len(rows),
        elimination=sum(r['stop_reason']=='elimination' for r in rows),
        round_limit=sum(r['stop_reason']=='round_limit' for r in rows), rows=rows)))
    print(f'{len(rows)} real battles completed; every replay packet fits the protocol')


if __name__ == '__main__':
    main()
