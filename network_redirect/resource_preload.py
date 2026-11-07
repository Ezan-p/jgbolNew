"""Bounded client resource plan; ships with both desktop and Android adapters."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / 'server_config/resource_preload.json'


def load_plan(path=PLAN):
    plan = json.loads(Path(path).read_text(encoding='utf-8'))
    if plan.get('version') != 1:
        raise ValueError('Unsupported resource preload plan')
    limits = dict(retained_texture_bytes=(1, 32*1024*1024), startup_slice_seconds=(0.01, 1),
                  startup_max_jobs=(1, 96), warm_interval_seconds=(0.05, 1),
                  warm_delay_seconds=(1, 10), slow_job_seconds=(0.001, 0.05),
                  cooldown_seconds=(0.1, 3), max_warm_seconds=(30, 300))
    for key, (lo, hi) in limits.items():
        if type(plan.get(key)) not in (int, float) or not lo <= plan[key] <= hi:
            raise ValueError('Invalid preload budget: ' + key)
    seen = set()
    for phase in ('core', 'warm'):
        jobs = plan.get(phase)
        if not isinstance(jobs, list) or len(jobs) > 200:
            raise ValueError('Invalid preload task count')
        for job in jobs:
            if job.get('kind') == 'texture':
                path = job.get('path', '')
                size = job.get('estimated_bytes')
                if (not path.startswith('v2/') or not path.endswith('.png') or '..' in path
                        or type(size) is not int or not 0 < size <= 4*1024*1024):
                    raise ValueError('Invalid preload texture')
                key = ('texture', path)
            elif job.get('kind') == 'config':
                if (job.get('module') not in ('d_mainUI', 'd_packageUI', 'd_data', 'd_lineupUI')
                        or not isinstance(job.get('getter'), str) or not job['getter'].startswith('get')
                        or not job.get('cache_fields')
                        or any(not isinstance(k, str) or not k.startswith('g_') for k in job['cache_fields'])):
                    raise ValueError('Invalid preload configuration getter')
                key = ('config', job['module'], job['getter'])
            else:
                raise ValueError('Unknown preload task kind')
            if key in seen:
                raise ValueError('Duplicate preload task')
            seen.add(key)
    return plan
