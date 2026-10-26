"""Hash original resources and reproduce the A/B classification for 捕魂达人."""
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity_hunt as h
from analysis.tools.luajit_static import parse,listing


def main():
    index=dict(line.split('====')[:2] for line in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    out=ROOT/'analysis/evidence/hunt';out.mkdir(parents=True,exist_ok=True)
    sources=[]
    for name in ['csv_config/'+n for n in ('hunt_ball_config.csv','hunt_soul_config.csv','hunt_day_prize.csv','hunt_week_prize.csv','newbie_content6.csv','title_config.csv','item_name.csv','item_base.csv')]+['lua/ui/soulHuntUI.lua','lua/ui/activityUI.lua','v2/soulHuntUI/ground.png']:
        path=ROOT/'jgbol3.87/assets/release_'/index[name];raw=path.read_bytes()
        row=dict(logical=name,path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(raw).hexdigest())
        if name.startswith('csv_config/'):
            try: original=raw.decode('utf-8-sig')
            except UnicodeDecodeError: original=raw.decode('gb18030')
            row['extracted_identical']=original==(ROOT/'analysis/configs'/name.split('/')[-1]).read_bytes().decode('utf-8-sig')
            assert row['extracted_identical'],name
        if name.endswith('soulHuntUI.lua'):
            (out/'soulHuntUI.asm').write_text(listing(parse(raw)))
        sources.append(row)
    report=dict(sources=sources,official_server_available=False,balls=h.BALLS,souls=h.SOULS,
        day_prizes=h.PRIZES['day'],week_prizes=h.PRIZES['week'],
        A=['activityUI L1520-1521: level20, activity36; L254 hunt_data',
           'soulHuntUI L523-529: flag2 count=ball index=rounded angle; L765-769 angle30..150',
           'soulHuntUI L82 cannon Below=-20; L317 raw pixel coordinate transform',
           'soulHuntUI L99-111/604-680: server move_path and per-segment soul_list; extra_soul',
           'newbie_content6: daily400 max1000; shop06:00; day00:00 mail top10; Monday00:00 last-week top20 claim',
           'item1036 grants100 soul; item1037 five-realm five-star souls; titles130..133 last1w'],
        B=['always-open local schedule; UTC+8;100 shots and3 map refreshes daily',
           'contour approximated from original alpha-mask silhouette;30px radius;right edge absorbing trap',
           'each colour independently adds rand_count with rand_weight/100 probability;positions uniform rejection sampling',
           'combo floor(base*min(100,10*(captured-1))/100);clear respawns board automatically',
           '10 soul per energy;200 soul shop reset;six configurable goods;one equal-weight item per box',
           '29 NPC identities from project catalog;400..2400 daily deterministic scores;independent account leaderboard',
           'historical board retains best observed period;ties by role_id;no score for cards or spending',
           'lazy settlement on login/activity;missed unclaimed weekly rewards become permanent mail;no inactive-day awards'],
        inferred_config=h.load_rules())
    (out/'official_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Verified 8 original CSV files, 2 Lua resources and original ground image')


if __name__=='__main__':main()
