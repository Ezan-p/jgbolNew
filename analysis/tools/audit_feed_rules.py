"""Record shipped eatBun UI evidence separately from local missing rules."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    out = ROOT/'analysis/evidence/feed';out.mkdir(exist_ok=True)
    index = dict(line.split('====')[:2] for line in
                 (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    inputs = []
    for name in ('lua/ui/eatBunUI.lua', 'lua/ui/activityUI.lua',
                 'v2/eatBunUI/info1.png', 'v2/eatBunUI/info2.png',
                 'csv_config/achievement.csv'):
        if name not in index:
            if name.endswith('achievement.csv'):
                # The inventory preserves the exact plural filename.
                name = next(k for k in index if k.startswith('csv_config/') and 'achievement' in k)
            else:
                raise KeyError(name)
        data = (ROOT/'jgbol3.87/assets/release_'/index[name]).read_bytes()
        inputs.append(dict(logical=name, resource=index[name], sha256=hashlib.sha256(data).hexdigest()))
        if name.endswith('.png'):
            (out/Path(name).name).write_bytes(data)
    report = dict(client='3.87', official_server_available=False, inputs=inputs,
        verified=[
            'eatBunUI L135-139: enter only sends query feed_count=0',
            'eatBunUI L268-293 and L339-355: Begin opens barrel with zero clicks and 10 seconds',
            'eatBunUI L423-431: first barrel click starts timer; each valid click increments score',
            'eatBunUI L468-489: ten-second timer, two-second result delay, positive score submitted via 1040',
            'info2.png: 点击木桶开始倒计时，点击速度越快，吃的越多。',
            'info1.png: more buns earn more strength; no numeric reward table in image',
            'activityUI uses 12:00-14:00 and 18:00-20:00; feed result 2/3/4 = success/closed/already claimed',
            'eatBunUI L278 and L596 use truthiness/nil, while L494-511 require numeric 1 / claimed timestamp',
            'achievement 108 = feed once; 445 = enter 快快侠 board'],
        inferred=[
            'six reward tiers: 1/10/20/30/40/50 clicks -> 10/20/30/40/50/60 strength, per user fallback',
            'retain offline maximum 200; client shares cap and tier config with server',
            'per-slot daily claims and best score storage; query returns historical earned best strength',
            'today champion among actual local saves; ties by completion time then role id',
            'achievement 445 on successful settlement into local first place; official award timing unavailable',
            'original 1040 sends only final count; server bounds score and prevents double rewards but cannot prove individual clicks'])
    (out/'official_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Recorded original eatBun UI and image evidence; reward tiers remain inferred')


if __name__ == '__main__':
    main()
