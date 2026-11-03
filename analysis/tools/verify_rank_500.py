"""Exercise all 500 rank opponents through production wire requests in a temporary DB."""
import copy
import json
import random
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity, activity_rank as rank, journey, npc_players
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode

NOW = 1793707200
OUT = ROOT / 'analysis/evidence/rank/rank_500_validation.json'


def main():
    rows = []
    with tempfile.TemporaryDirectory() as tmp, patch('network_redirect.backend.time.time', return_value=NOW):
        b = Backend(Path(tmp), 18770, lambda *a, **k: None)
        try:
            base = b.profile(); base.update(level=60, energy=100)
            activity.prepare(base, NOW, b.activity_rules)
            assert base['activity']['rank_order'] == 501
            for order, (ident, npc) in enumerate(rank.catalog().items(), 1):
                role = copy.deepcopy(base)
                role['activity'].update(rank_order=order+1, rank_origin_order=order+1, rank_slots={}, rank_count=0,
                                        rank_version=2, rank_day_best=order+1, rank_records=[])
                b.save(role); before = b.profile()
                state = dict(authenticated=True)
                # Both scene inspection and permanent profile use the exact fighting snapshot.
                for k, target in enumerate((ident, npc['role']['role_id'])):
                    inspection = b.respond(encode(1039, dict(serial_num=200000+order*10+k, des_type=2 if k==0 else 1, des_id=target)), state)
                    data = next(login_fields(d['data']) for m, _, d in map(decode, inspection) if m==2998 and d['id']==11)
                    assert data['role_combat_power'] == npc['role']['role_combat_power']
                    assert all(len(p) <= 32768 for p in inspection)
                request = encode(1026, dict(serial_num=200000+order*10+2, fight_type=2, des_type=2, des_value=order, des_id=ident))
                with patch('network_redirect.combat.secrets.randbelow', side_effect=random.Random(83+order).randrange):
                    packets = b.respond(request, state)
                decoded = [decode(p) for p in packets]
                assert not any(m==2998 and d['id']==55 for m, _, d in decoded), (order, decoded)
                assert any(m==1027 for m, _, _ in decoded), order
                after = b.profile(); record = after['activity']['rank_records'][-1]
                assert after['energy'] == before['energy']-1 and after['activity']['rank_count'] == 1
                assert b.respond(request, state) == packets and b.profile() == after
                b.close(); b = Backend(Path(tmp), 18770, lambda *a, **k: None)
                assert b.profile() == after
                replay = b.respond(encode(1244, dict(serial_num=200000+order*10+3, fight_type=2)), dict(authenticated=True))
                assert not any(m==2998 and d['id']==55 for m, _, d in map(decode, replay))
                assert b.profile() == after
                assert all(len(p) <= 32768 for p in packets + replay)
                rows.append(dict(order=order, npc_id=npc['npc_id'], power=npc['role']['role_combat_power'],
                                 result=record['fight_result_msg']['final_result'], stop_reason=record['stop_reason'],
                                 largest_packet=max(map(len, packets+replay))))
                if order % 25 == 0:
                    print(f'backend challenge/inspection/retry/restart/replay: {order}/500', flush=True)
        finally:
            b.close()
    # Comparable full-loadout fights exercise high-tier fate/essence chains, not just one-hit wins.
    stress = []
    for order in range(1, 101):
        npc = rank.catalog()[930000+order]
        for seed in (17, 83):
            role = copy.deepcopy(npc['role'])
            role['activity'] = dict(rank_order=501, rank_origin_order=501, rank_slots={}, fight_id=0,
                                    rank_day_best=501, rank_records=[])
            with patch('network_redirect.combat.secrets.randbelow', side_effect=random.Random(seed).randrange):
                _, record = rank.simulate(role, order, NOW, journey.load_rules())
            packets = rank.replay_packets(record)
            assert record['stop_reason'] in ('elimination', 'round_limit')
            assert all(len(p) <= 32768 for p in packets)
            stress.append(dict(order=order, seed=seed, result=record['fight_result_msg']['final_result'],
                               stop_reason=record['stop_reason'], largest_packet=max(map(len, packets))))
        if order % 10 == 0:
            print(f'extreme full-loadout mirror stress: {order}/100 (two seeds)', flush=True)
    from analysis.tools import build_npc_extreme
    original = json.loads((ROOT/'analysis/npc_design/extreme/catalog.json').read_text())['npcs']
    regressions = build_npc_extreme.battles(original)
    assert len(regressions) == 152 and all(not row['error'] for row in regressions)
    data = dict(date='2026-11-03', backend_challenges=len(rows), full_loadout_battles=len(stress),
                original_extreme_regressions=len(regressions), native_client_playback_tested=False,
                rows=rows, stress=stress, original_regressions=regressions)
    OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    print(f'PASS: {len(rows)} backend challenges, {len(stress)} full-loadout fights, {len(regressions)} original regressions', flush=True)


if __name__ == '__main__':
    main()
