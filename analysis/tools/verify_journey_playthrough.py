"""All 664 gates: real combat, sweep, rewards, replay and restart in disposable storage."""
import copy
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import journey, npc_players
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


def main():
    now = 1792987200
    serial = 100000
    trace = []
    session = dict(authenticated=True)
    key = max(npc_players.catalog(), key=lambda k: npc_players.catalog()[k]['profile']['role_combat_power'])
    with tempfile.TemporaryDirectory() as tmp, patch('network_redirect.backend.time.time', return_value=now) as clock:
        backend = Backend(Path(tmp), 18770, lambda *a, **k: None)
        role = backend.profile()
        identity = role['role_id']
        role.update(copy.deepcopy(npc_players.get(key)['role']))
        role.update(role_id=identity, role_name='旅途全关卡验证', strength=10000, gold_coin=100000, silver_coin=1000000)
        role.pop('journey', None)
        journey.prepare(role, now, backend.journey_rules)
        backend.save(role)

        def request(mid, accepted=True, **args):
            nonlocal serial
            serial += 1
            before = backend.profile()
            packet = encode(mid, dict(serial_num=serial, **args))
            replies = backend.respond(packet, session)
            decoded = list(map(decode, replies))
            events = [(d['id'], login_fields(d['data'])) for code, _, d in decoded if code == 2998]
            errors = [data for event, data in events if event == 55]
            assert bool(errors) != accepted, (mid, args, errors)
            assert decoded[-1][0] == 1106 and decoded[-1][2]['req_serial_num'] == serial
            after = backend.profile()
            if not accepted:
                assert after == before
            if mid != 1018:
                assert backend.respond(packet, session) == replies
                assert backend.profile() == after
            return decoded, events

        request(1018, flag=1)
        request(1026, False, fight_type=20, des_type=1, des_id=101)
        request(1026, False, fight_type=1, des_type=1, des_id=6710)
        for mapid in journey.MAPS[1]:
            for kind in (1, 2):
                gates = [gid for gid, cfg in journey.GATES[kind].items() if int(cfg['map_id']) == mapid]
                for gid in gates:
                    cfg = journey.GATES[kind][gid]
                    before = backend.profile()
                    decoded, _ = request(1026, fight_type=1 if kind == 1 else 20, des_type=1, des_id=gid)
                    result = next(d for code, _, d in decoded if code == 1027)
                    assert result['final_result'] == 3, (kind, gid, result['final_result'])
                    assert result['fight_result'] and all(len(a['damage_list']) == 8 for a in result['fight_result'])
                    assert backend.profile()['strength'] == before['strength'] - int(cfg['strenth_consume'])
                    assert journey.progress(backend.profile(), kind, gid)['pass_star'] == 3
                    settled = backend.profile()
                    request(2998, id=3, data='{}')
                    assert backend.profile() == settled
                    _, events = request(1061, tollgate_type=kind, tollgate_id=gid, sweep_count=1)
                    sweeps = next(data for event, data in events if event == 63)
                    assert len(sweeps) == 1 and sweeps[1]['silver_coin'] == int(cfg['money'])
                    assert backend.profile()['strength'] == settled['strength'] - int(cfg['strenth_consume'])
                    request(1061, False, tollgate_type=kind, tollgate_id=gid, sweep_count=1)
                    trace.append(dict(kind=kind, gate=gid, result=result['final_result'], actions=result['fight_round'], sweep=True))
                    now += 1800
                    clock.return_value = now
            request(1201, flag=3, id=mapid)
            request(1201, False, flag=3, id=mapid)
            if mapid % 10 == 0:
                print(f'passed {mapid}/67 chapters; {len(trace)}/664 fights and sweeps', flush=True)
            if mapid == 34:
                before = backend.profile()
                backend.close()
                backend = Backend(Path(tmp), 18770, lambda *a, **k: None)
                assert backend.profile() == before
                request(1018, flag=2)
        request(1018, flag=1)
        role = backend.profile()
        assert len(role['journey']['claimed_maps']) == 67
        assert len(trace) == 664
        backend.close()
    report = dict(date='2026-10-26', passed=True, temporary_database=True, live_account_changed=False,
                  real_combat=True, army=key, seeded_strength=10000, seeded_gold=100000, seeded_silver=1000000,
                  stat_boosts=False, seeded_progress=False, normal_gates=597, elite_gates=67,
                  sweeps=664, chapter_rewards=67, restart_at_chapter=34,
                  replayed_every_mutation=True, cooldown_rejections=664, requests=serial-100000,
                  simulated_seconds=664*1800, balance_claim=False, steps=trace)
    path = ROOT / 'analysis/evidence/journey_playthrough.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'steps'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
