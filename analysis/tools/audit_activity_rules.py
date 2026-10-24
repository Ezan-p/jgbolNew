"""Rebuild activity contracts from unmodified 3.87 LuaJIT and CSV assets."""
import csv
import hashlib
import io
import json
import re
from pathlib import Path
from luajit_static import parse, listing, decode
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'analysis/evidence'
MODULES = '''commonLayerUI packageUI treasureMapUI monthCardUI expbookUI petUI activityUI funUI eatBunUI loginGameUI qiFuUI cortegeRecycleUI practiceUI rankUI crossDoomUI endlessFightUI worldBossUI cortCallUI shilianUI undergoOrdealUI undergoMapUI undergoSubLevelUI undergoLineupUI checkLineupUI fightUI yaoshendianUI tongtiantaUI homeUI abyssUI landUI springCardUI springActivityMoneyUI lanternRiddleUI chargePresentUI fishRushUI friendsUI mondayUI richmanUI ricePuddingUI moonCakeUI checkinUI goldRushUI soulHuntUI destinyUI snowmanUI dreamUI alchemyUI summerUI answerUI omenUI kickUI towerUI guessUI saveMonkeyUI turntableUI'''.split()
TABLES = '''cards_letter cards_tip item_name animal_base animal_control animal_name animal_growup animal_upgrade animal_train_config animal_exprience item_base prey_map_config prey_charm_convert prey_open_grid prey_week_rank prey_open_charm pray_spirit_config cortege_quality luhsing_form_rate top_score top_score_exchange rank_prize duty_topprize_config convert_output gold_rush_config reward_over_time zongzi_formula compose_monthcake babel_tower_floor_prize hunt_ball_config hunt_soul_config hunt_day_prize hunt_week_prize dream_prize_config'''.split()

def main():
    index = dict(line.split('====')[:2] for line in (OUT/'resource_index.decoded.txt').read_text().splitlines())
    encodings = {r['logical']: r['encoding'] for r in json.loads((OUT/'config_inventory.json').read_text())}
    inputs, contracts, enums = [], {}, {}
    for module in ['ui/'+m for m in MODULES] + ['common/common_def','event_mgr','data','skill/skill_mgr','skill/skillExt']:
        name='lua/'+module+'.lua'; path=ROOT/'jgbol3.87/assets/release_'/index[name]
        chunk=parse(path.read_bytes()); names={}
        for p in chunk['protos']:
            for i, ins in enumerate(p['code'][:-1]):
                op,a,b,c,d=decode(ins); op2,a2,b2,c2,d2=decode(p['code'][i+1])
                if op=='FNEW' and op2=='GSET': names[p['kgc'][d]['id']]=p['kgc'][d2]
                if module=='common/common_def' and op=='TDUP' and op2=='GSET':
                    enums[p['kgc'][d2]]=p['kgc'][d]['value']
        contracts[module]=[dict(function=names.get(p['id'],'nested'+str(p['id'])),line=p['line'],last_line=p['last_line'],
            numbers=p['numbers'],strings=[s for s in p['kgc'] if isinstance(s,str)]) for p in chunk['protos']]
        inputs.append(dict(logical=name,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    names=[next(k for k in index if k.startswith('csv_config/') and Path(k).stem==n) for n in TABLES]
    names += [k for k in index if (k.startswith(('csv_config/undergo_ordeal/','csv_config/hole/')) or Path(k).stem.startswith(('specter_', 'abyss_rule_'))) and k.endswith('.csv')]
    for name in names:
        path=ROOT/'jgbol3.87/assets/release_'/index[name]
        extracted=ROOT/'analysis/configs'/name.removeprefix('csv_config/')
        assert list(csv.reader(io.StringIO(path.read_bytes().decode(encodings[name]))))==list(csv.reader(io.StringIO(extracted.read_text(encoding='utf-8-sig')))),name
        inputs.append(dict(logical=name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),csv_values_match=True))
    report=dict(client='3.87',official_server_available=False,inputs=inputs,contracts=contracts,
                classification={'A':'原客户端协议、回调及 CSV','B':'缺失服务端配置及结算推测'})
    (OUT/'activity_official_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (OUT/'activity_enums.json').write_text(json.dumps(enums,ensure_ascii=False,indent=2)+'\n')
    print('Verified',len(inputs),'original inputs;',len(enums),'literal enum tables')
if __name__=='__main__':main()
