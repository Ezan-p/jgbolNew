"""Record original Taixu Lua/CSV evidence and the explicitly inferred policy."""
import csv
import hashlib
import io
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from luajit_static import parse,decode
from network_redirect import activity_undergo as u
index=dict(line.split('====')[:2] for line in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
encodings={r['logical']:r['encoding'] for r in json.loads((ROOT/'analysis/evidence/config_inventory.json').read_text())}
inputs=[];contracts={}
for name in ['undergoOrdealUI','undergoMapUI','undergoSubLevelUI','undergoLineupUI','arenaUI']:
    logical='lua/ui/'+name+'.lua';raw=(ROOT/'jgbol3.87/assets/release_'/index[logical]).read_bytes()
    c=parse(raw);names={}
    for p in c['protos']:
        for x,y in zip(p['code'],p['code'][1:]):
            op,a,b,c1,d=decode(x);op2,a2,b2,c2,d2=decode(y)
            if op=='FNEW' and op2=='GSET':names[p['kgc'][d]['id']]=p['kgc'][d2]
    contracts[name]=[dict(function=names.get(p['id'],'nested'+str(p['id'])),line=p['line'],last_line=p['last_line'],
                         numbers=p['numbers'],strings=[k for k in p['kgc'] if isinstance(k,str)]) for p in c['protos'] if p['line']]
    inputs.append(dict(logical=logical,sha256=hashlib.sha256(raw).hexdigest()))
for relative in ['undergo_ordeal/map_config.csv','undergo_ordeal/tollgate_config.csv','undergo_ordeal/npc_list.csv',
                 'undergo_ordeal/map_name.csv','undergo_ordeal/tollgate_name.csv','newbie_content18.csv',
                 'cross_server/manual.csv','all_rank_prize.csv']:
    logical='csv_config/'+relative;raw=(ROOT/'jgbol3.87/assets/release_'/index[logical]).read_bytes()
    assert list(csv.reader(io.StringIO(raw.decode(encodings[logical]))))==list(csv.reader((ROOT/'analysis/configs'/relative).open(encoding='utf-8-sig')))
    inputs.append(dict(logical=logical,sha256=hashlib.sha256(raw).hexdigest(),csv_values_match=True))
report=dict(client='3.87',official_server_available=False,inputs=inputs,contracts=contracts,local_rules=u.rules(),
    classification={'A':['mode1=挑战,mode2=历劫','cortege_list=神仙ID→阵位','原版81关及守卫与修炼',
       '挑战每日10次/2体力，历劫0体力/每神仙4次','72小时退关/每日当前小关重置',
       '血战七组、冲榜、练习、三段血战、血量优先排名','原包50级入口与all_rank_prize.csv原始档位'],
      'B':['按用户要求血战每次胜利100仙晶，榜奖为元宝、圣母蟠桃及分档仙晶','历劫首战开始计时、历史通关日奖保留','按本地NPC库补足血战分组、数值与赛程推进',
           '每周一北京时间零点强制刷新未完成赛程，最终奖励不再记录声望']})
out=ROOT/'analysis/evidence/taixu';out.mkdir(parents=True,exist_ok=True)
(out/'official_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Verified',len(inputs),'original inputs and',len(u.GATES),'gates')
