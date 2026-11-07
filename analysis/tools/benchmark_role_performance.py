"""Synthetic request benchmark; isolated SQLite, never opens a player's save.

Run from the repository root:
PYTHONPATH=.:tests .runtime/venv/bin/python analysis/tools/benchmark_role_performance.py after
The setup and seven-sample timing match before.json in the accompanying evidence.
"""
import json
import statistics
import sys
import time

from tests.test_activity import ActivityCase
from network_redirect import formation, summon, journey
from network_redirect.request_timing import current


def main(label):
    case = ActivityCase()
    case.setUp()
    try:
        role = case.b.profile()
        for _ in range(59):
            role['corteges'].append(summon.companion(role, 5004))
        for _ in range(1200):
            role['attachments'].append(dict(id=formation.new_id(role), type_id=2001,
                count=1, attach_type=5, level=1, equip_order=0, equip_pos=0))
        role['benchmark_history'] = [{'id': n, 'events': list(range(30))} for n in range(2000)]
        formation.prepare(role, case.b.formation_rules)
        case.b.save(role)
        case.ok(case.req(1353, id=1, data='{}'))
        times = []
        for _ in range(7):
            metrics = {}
            token = current.set(metrics)
            try:
                start = time.perf_counter()
                case.ok(case.req(1353, id=1, data='{}'))
                times.append((time.perf_counter() - start) * 1000)
            finally:
                current.reset(token)
        map_times = []
        for _ in range(7):
            start = time.perf_counter()
            journey.snapshots(role)
            map_times.append((time.perf_counter() - start) * 1000)
        print(json.dumps(dict(label=label, role_bytes=len(json.dumps(role)),
            companions=len(role['corteges']), attachments=len(role['attachments']),
            query_median_ms=statistics.median(times), query_samples_ms=times,
            maps_median_ms=statistics.median(map_times), metrics=metrics), indent=2))
    finally:
        case.doCleanups()


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'current')
