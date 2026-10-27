"""Real OS-random smoke sampling; no account, inventory or database mutations."""
from collections import Counter
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import qiankun_bags as q


def main(samples=100000):
    report = dict(samples_per_bag=samples, random_source='production secrets.randbelow + secrets.choice',
                  live_account_resources_changed=False, bags={})
    for tid, bag in q.load_rules()['bags'].items():
        lookup = {}
        for name, tier in bag['tiers'].items():
            for i, group in enumerate(tier['groups']):
                for kind, target in q.CATALOG[group['pool']]:
                    result = (kind, target, group['count'], 1)
                    assert result not in lookup, 'Outcome must identify a single path in this configuration'
                    lookup[result] = (name, i)
        tiers, groups = Counter(), Counter()
        for _ in range(samples):
            name, index = lookup[tuple(q.draw(bag))]
            tiers[name] += 1; groups[name, index] += 1
        quality = {}
        for name in q.TIERS:
            p = bag['tiers'][name]['weight']/100
            sigma = math.sqrt(samples*p*(1-p))
            quality[name] = dict(count=tiers[name], observed_percent=100*tiers[name]/samples,
                                 expected_percent=100*p, deviation_sigma=(tiers[name]-samples*p)/sigma)
        report['bags'][tid] = dict(name=bag['name'], quality=quality,
            groups=[dict(tier=name, pool=g['pool'], count=g['count'], samples=groups[name,i],
                         expected_samples=samples*bag['tiers'][name]['weight']*g['weight']/10000)
                    for name in q.TIERS for i,g in enumerate(bag['tiers'][name]['groups'])])
    target = ROOT/'analysis/evidence/qiankun_bag_pools/sampling.json'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({tid:b['quality'] for tid,b in report['bags'].items()},ensure_ascii=False))


if __name__ == '__main__':
    main()
