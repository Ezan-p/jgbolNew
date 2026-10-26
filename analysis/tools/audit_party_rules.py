"""Record reproducible source/config evidence without modifying original assets."""
import hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from network_redirect import activity_party as party
paths=['analysis/evidence/lua_named/lua/ui/worldBossUI.lua.txt',
       'analysis/evidence/lua_named/lua/ui/activityUI.lua.txt',
       'analysis/npc_design/v1/catalog.json','server_config/party_rules.json','server_config/activity_rules.json']
report=dict(official_server_available=False,classification={
    'A':['13级入口','11:00—13:00开放','10次免费、5次付费（worldBossUI 62—63行）','鼓舞价格5×(已购次数+1)','周一00:00、周榜前100名领奖','1049/1201/1202原请求及28/29/30/31/32/141事件','日伤害榜、福星、NPC阵容查看、排行榜点赞'],
    'B':['风伯／太上老君／福星按日期与轮次稳定随机','99名本地NPC及确定性参与模拟','1000万血首领循环刷新','伤害、幸运点公式及奖励数量','每日榜自动入包与未领周奖保留','节日材料轮换掉落']},
    files=[dict(path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in paths],
    npcs=[dict(id=i,npc_id=n['npc_id'],name=n['role']['name'],level=n['role']['level'],power=n['role']['role_combat_power']) for i,n in party.catalog().items()])
(ROOT/'analysis/evidence/party/official_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Recorded original UI evidence and',len(report['npcs']),'NPC identities')
