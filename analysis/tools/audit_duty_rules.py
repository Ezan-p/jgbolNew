"""Verify duty evidence against immutable original 3.87 resources."""
import csv
import hashlib
import io
import json
import plistlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity_duty as duty

index = dict(line.split('====')[:2] for line in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
inputs = []
for name in ('lua/ui/endlessFightUI.lua', 'lua/common/common_def.lua', 'csv_config/duty_topprize_config.csv',
             'csv_config/achievements_config.csv', 'csv_config/title_config.csv'):
    path = ROOT/'jgbol3.87/assets/release_'/index[name]
    inputs.append(dict(logical=name, path=str(path.relative_to(ROOT)), sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
csv_raw = (ROOT/'jgbol3.87/assets/release_'/index['csv_config/duty_topprize_config.csv']).read_bytes().decode('utf-8-sig')
original = list(csv.DictReader(io.StringIO(csv_raw)))
assert original == duty.PRIZES
assert len(original) == 50
enums = json.loads((ROOT/'analysis/evidence/activity_enums.json').read_text())
assert enums['duty_plus_type']['revert_round'] == 4
assert enums['duty_plus_type']['start_yesterday_half_round'] == 5
assert tuple(enums['cortege_property'][k] for k in ('max_hp_rate','max_magic_rate','gongji_rate','fangyu_rate')) == duty.FIELDS
contracts = json.loads((ROOT/'analysis/evidence/activity_official_audit.json').read_text())['contracts']['ui/endlessFightUI']
selected = [x for x in contracts if x['function'] in ('chooseFightType', 'processDataTable', 'setRevertData', 'showRevertPage', 'initBounsType', 'createRankCells', 'createVSIntro')]
assert next(x for x in selected if x['function']=='chooseFightType')['numbers'] == [1]
for g in range(4,9):
    for pos in range(1,51):
        raw = original[pos-1][duty.COLUMNS[g]]
        assert duty.rank_reward(g,pos) == (int(raw.split('|')[2]) if raw else 0)
strings = plistlib.load((ROOT/'jgbol3.87/assets/release_/e926a25accffd37afafb015933e815d4.data').open('rb'))
def select_strings(value):
    result = {}
    if isinstance(value,dict):
        for k,v in value.items():
            if k.startswith('endlessFight') or k in ('initBonusIntroHZ','BonusIntroHZ','sacrificeHZ','continuousRankHZ'):
                result[k] = v
            if isinstance(v,dict): result.update(select_strings(v))
    return result
out = ROOT/'analysis/evidence/duty';out.mkdir(parents=True,exist_ok=True)
(out/'official_audit.json').write_text(json.dumps(dict(client='3.87', official_server_available=False,
    user_authorized_balance='server_config/duty_rules.json', inputs=inputs, contracts=selected,
    strings=select_strings(strings), verified_rank_reward_cells=250,
    original_enums={k:v for k,v in enums.items() if k.startswith('duty_')},
    classifications={
        'A':['12级入口、每日3次','cur_round为已通关数，战斗请求加1','四属性字段174—177','领奖及祭魂状态码','本轮/昨日半程双操作及0/1选项','4—8人分组','榜奖250单元格逐值相同','20/40/60/80/100关成就，原包无30关封顶'],
        'historical_reference':['难度×胜利评级战魂：2013年攻略，与原版三档倍率UI相符；不能视为3.87原服源码'],
        'B_retained':['每3胜3000银币','免费初始祝福10%','半程起点floor(已通关数/2)，至少1'],
        'B_user_authorized':['players库完整NPC阵容，4—8人固定强度曲线、三档80%/100%/125%','每胜一次随机无掉落/10或30元宝/棉布银绸金丝乾坤袋','祭魂5%/10%/15%/20%，费用9/18/27/36，权重50/30/15/5','不足9魂自动继续，有9魂时至少一个可购买选项'],
        'B_local_policy':['真实本地账号排行，星数/关数/账号键排序','最高单次成绩及固定开局分组','跨日自动入包榜奖、按结榜日期授24h称号','跨日保留所有未领奖励','半程仅还原实际快照与已抽选项，不复制跳关奖励']},
    historical_reference='https://jingyan.baidu.com/article/d2b1d10268bad25c7f37d464.html'),ensure_ascii=False,indent=2)+'\n')
print('Verified original inputs, original enums and all 250 rank reward cells')
