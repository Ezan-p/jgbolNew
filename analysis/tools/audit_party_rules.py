"""Record reproducible source/config evidence without modifying original assets."""
import hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from network_redirect import activity_party as party
paths=['network_redirect/party_client.lua','network_redirect/activity_party.py','network_redirect/activity.py',
       'network_redirect/combat_engine.py','network_redirect/system_mail.py','analysis/evidence/lua_named/lua/ui/worldBossUI.lua.txt',
       'analysis/evidence/lua_named/lua/ui/activityUI.lua.txt',
       'analysis/npc_design/v1/catalog.json','server_config/party_rules.json','server_config/activity_rules.json']
report=dict(daily_npc_count=party.rules()['npc_count'],daily_rewards=party.rules()['daily_rewards'],
    boss_pool=party.rules()['boss_pool'],boss_magic=party.BOSS_MAGIC_CAP,official_server_available=False,classification={
    'A':['13级入口','11:00—13:00开放','10次免费、5次付费（worldBossUI 62—63行）','鼓舞价格5×(已购次数+1)','周一00:00、周榜前100名领奖','1049/1201/1202原请求及28/29/30/31/32/141事件','日伤害榜、福星、NPC阵容查看、排行榜点赞'],
    'B':['风伯／太上老君／福星按日期稳定随机','每日20名NPC及静态随机伤害，仅用于排名','1000万血同一首领循环补满，仅玩家扣血','每10000伤害1蟠桃，单场最多100','每日榜13点结算永久邮件：1—5名100圣母蟠桃，6—10名50圣母蟠桃，11—50名200蟠桃；幸运排行和周奖停用','首领法力2147483647，群攻触发击败全队（含替补）','节日材料独立随机掉落']},
    files=[dict(path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in paths],
    npcs=[dict(id=i,npc_id=n['npc_id'],name=n['role']['name'],level=n['role']['level'],power=n['role']['role_combat_power']) for i,n in party.catalog().items()])
(ROOT/'analysis/evidence/party/official_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Recorded original UI evidence and',len(report['npcs']),'NPC identities')
