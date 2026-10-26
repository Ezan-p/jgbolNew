"""Reproducible local original evidence and 60-floor NPC schedule (no network)."""
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT))
from network_redirect import activity_babel_npc as npc, npc_players
paths=['analysis/evidence/lua_named/lua/ui/tongtiantaUI.lua.txt',
       'analysis/configs/babel_tower_floor_prize.csv','analysis/configs/item_name.csv',
       'jgbol3.87/assets/release_/08b0428edce64d19f304d30c3829ec87.data',
       'analysis/npc_design/players/catalog.json','server_config/activity_rules.json']
report=dict(date='2026-10-26',official_server_available=False,classification={
    'A':['36级入口；1353/event203；1028/1027/44战报，类型200',
         '周一0点重置进度、发周榜奖励；钥匙和道具保留',
         '每日0点恢复生命；仙力每半小时恢复；仙露无仙力上限限制',
         '仙露20016—20019恢复10/25/80/200点',
         '同层按到达时间排名；榜奖界面显示通天币',
         '恢复生命200元宝；传送20元宝；商店刷新200通天币',
         '金银铜箱与钥匙对应；石块耗锤、篝火耗道符',
         '原包12档1—60层道具池；商店limit是总限购，客户端扣my_exchange'],
    'B':['5×8固定布局与3×3探索视野；60层封顶依据已恢复奖励表',
         '本层守塔者必须击败；终层楼梯结算一次并变为空地',
         '初始生命/仙力100；半小时恢复1；生命损失公式',
         'NPC阵容按固定目标战力选择，保留资料库属性和技能',
         '掉落等概率按CSV条目抽取；每箱/守卫/终点50通天币',
         '六格商品、价格、限购、每日一次刷新；刷新补货而不换商品',
         '30名NPC确定性周进度；周奖2000/1500/1000/500/200通天币',
         '结算上次参与周，系统永久邮件领取，不补造未参与周奖励',
         '手动reset仅回到一层，不刷新已领取内容；允许传送本周已达任意层']},
    files=[dict(path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in paths],schedule=[])
for floor in range(1,61):
    row=dict(floor=floor,enemies={})
    for kind in (20012,20011,20010,20015,20014,20013,9):
        key=npc.choose(floor,kind); p=npc_players.catalog()[key]['profile']
        row['enemies'][str(kind)]=dict(npc_id=key,name=p['role_name'],level=p['level'],power=p['role_combat_power'])
    report['schedule'].append(row)
out=ROOT/'analysis/evidence/babel'; out.mkdir(parents=True,exist_ok=True)
(out/'official_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Recorded original evidence and 420 guard selections.')
