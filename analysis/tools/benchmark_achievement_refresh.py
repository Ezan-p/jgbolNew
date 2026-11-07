"""Isolate request-local achievement reuse; both paths use the static map index.

Run: PYTHONPATH=.:tests .runtime/venv/bin/python analysis/tools/benchmark_achievement_refresh.py
Creates synthetic dictionaries only; no player save or database is opened.
"""
import copy
import json
import statistics
from time import perf_counter

from network_redirect import achievements, journey, summon
from network_redirect.request_timing import current, request_cache

NOW = 1792814400


def main():
    role = dict(role_id=1, summon={}, corteges=[], attachments=[], activity={},
                journey=dict(gates={f'{kind}:{gid}': dict(pass_star=3, day_count=0, flush_count=0)
                                   for kind, gates in journey.GATES.items() for gid in gates}))
    for _ in range(60):
        role['corteges'].append(summon.companion(role, 5004))
    for _ in range(1200):
        role['attachments'].append(dict(id=summon.next_id(role), attach_type=5,
                                       type_id=2001, level=1, count=1))
    achievements.refresh(role, NOW)
    expected = copy.deepcopy(role)
    def twice():
        achievements.refresh(role, NOW)
        achievements.refresh(role, NOW)
    variants = dict(uncached=twice, request_cached=request_cache(twice))
    samples = {name: [] for name in variants}
    last_metrics = {}
    for run in variants.values():
        run()
    for trial in range(15):
        order = list(variants) if trial % 2 == 0 else list(reversed(variants))
        for name in order:
            metrics = {}
            token = current.set(metrics)
            try:
                start = perf_counter()
                variants[name]()
                samples[name].append((perf_counter() - start) * 1000)
            finally:
                current.reset(token)
            last_metrics[name] = metrics
            assert role == expected, 'refresh changed an already refreshed fixture'
    print(json.dumps(dict(scope='two refresh calls; both paths use the new static map index',
        companions=len(role['corteges']), attachments=len(role['attachments']),
        gates=len(role['journey']['gates']), trials=15,
        median_ms={name: statistics.median(values) for name, values in samples.items()},
        samples_ms=samples, last_metrics=last_metrics), indent=2))


if __name__ == '__main__':
    main()
