"""Read-only audit of real code using disposable SQLite accounts, never player saves.

Run with .runtime/venv/bin/python analysis/tools/probe_remaining_achievement_branches.py.
The fixed scenario time is 2026-10-27 12:00 UTC+8; only the evidence JSON persists.
This checks settlement and achievement deltas, not original-client interaction.
"""
import hashlib
import json
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode
from network_redirect import achievements, formation, summon

ZONE = timezone(timedelta(hours=8))
NOW = int(datetime(2026, 10, 27, 12, tzinfo=ZONE).timestamp())
OUTPUT = ROOT / 'analysis/evidence/server_integration/achievement_branch_probes_2026-10-27.json'


def run():
    probes = []
    with tempfile.TemporaryDirectory(prefix='achievement-branch-audit-') as temp:
        with patch('network_redirect.backend.time.time', return_value=NOW):
            backend = Backend(Path(temp), 18770, lambda *args, **kwargs: None)
            try:
                serial = 10000

                def request(mid, **fields):
                    nonlocal serial
                    serial += 1
                    packets = backend.respond(encode(mid, dict(serial_num=serial, **fields)),
                                              {'authenticated': True})
                    decoded = [decode(packet) for packet in packets]
                    assert decoded[-1][0] == 1106 and decoded[-1][2]['req_serial_num'] == serial
                    events = [dict(message_id=m, event_id=d['id'], data=login_fields(d['data']))
                              for m, _, d in decoded if m in (2998, 1301)]
                    assert not any(event['event_id'] == 55 for event in events), events
                    return dict(request=dict(message_id=mid, serial_num=serial, **fields),
                                response_message_ids=[m for m, _, _ in decoded], events=events)

                def progress(role, ident):
                    return next(row for row in achievements.rows(role) if row['id'] == ident)

                role = backend.profile()
                role.update(level=60, gold_coin=100000, silver_coin=100000)
                tid = 5005
                assert not any(c['type'] == tid for c in role['corteges'])
                need = formation.COMPOSE[int(formation.BASES[tid]['quality'])]
                role.setdefault('souls', {})[str(tid)] = need
                backend.save(role)
                before = backend.profile()
                exchange = request(1083, type_id=tid)
                after = backend.profile()
                assert after['souls'][str(tid)] == 0 and any(c['type'] == tid for c in after['corteges'])
                probes.append(dict(name='soul_compose_achievement_119', **exchange,
                    before=dict(souls=before['souls'][str(tid)], owns=False, achievement=progress(before, 119)),
                    after=dict(souls=after['souls'][str(tid)], owns=True, achievement=progress(after, 119)),
                    achievement_unchanged=progress(before, 119) == progress(after, 119)))

                setup = [request(1301, id=1, data=summon.lua(dict(union_name='审计临时仙盟'))),
                         request(1301, id=43, data=summon.lua(dict(flag=1)))]
                before = backend.profile()
                treasure = request(1301, id=43, data=summon.lua(dict(flag=2)))
                after = backend.profile()
                assert after['guild']['instances']['search'] == before['guild']['instances']['search'] + 1
                assert after['guild']['instances']['points'] == before['guild']['instances']['points'] + 10
                probes.append(dict(name='guild_treasure_achievement_139', setup=setup, **treasure,
                    before=dict(search=before['guild']['instances']['search'],
                                points=before['guild']['instances']['points'], achievement=progress(before, 139)),
                    after=dict(search=after['guild']['instances']['search'],
                               points=after['guild']['instances']['points'], achievement=progress(after, 139)),
                    achievement_unchanged=progress(before, 139) == progress(after, 139)))
            finally:
                backend.close()
    paths = [
        'network_redirect/backend.py', 'network_redirect/formation.py',
        'network_redirect/achievements.py', 'network_redirect/guild_instances.py',
        'analysis/evidence/lua_named/lua/ui/allLineupUI.lua.txt',
        'analysis/evidence/lua_named/lua/ui/formationUI.lua.txt',
        'analysis/configs/achievements_config.csv',
        'analysis/tools/probe_remaining_achievement_branches.py',
    ]
    result = dict(audited_at=datetime.now(ZONE).isoformat(), scenario_time=NOW,
                  timezone='Asia/Shanghai',
                  scope='Temporary SQLite Backend.respond probes; no real saves, sockets or emulator',
                  probes=probes,
                  source_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths})
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    return result


if __name__ == '__main__':
    result = run()
    print(json.dumps(dict(output=str(OUTPUT.relative_to(ROOT)), probes=[
        {k: p[k] for k in ('name', 'before', 'after', 'achievement_unchanged')}
        for p in result['probes']]), ensure_ascii=False, indent=2))
