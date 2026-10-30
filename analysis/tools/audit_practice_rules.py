"""Export the auditable offline curve; only base/growth/skill data is original."""
import csv
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity_practice as practice, formation, journey
rules=practice.load_rules()
activity_rules=json.loads((ROOT/'server_config/activity_rules.json').read_text())
out=ROOT/'analysis/evidence/practice';out.mkdir(parents=True,exist_ok=True)
rows=[]
for index in range(max(formation.LEVELS)-4):
    _, enemies=journey.fighters({'corteges':[]},practice.encounter(index,rules))
    enemy=enemies[0]
    rows.append(dict(stage=index+1,unlock_level=index+5,enemy_type=enemy['type'],enemy_name=practice.NAMES[enemy['type']],
                     enemy_level=enemy['level'],hp=enemy['hp'],attack=enemy['gongji'],defense=enemy['fangyu'],magic=enemy['magic'],
                     skill_type=enemy['skills'][0][0],skill_level=enemy['skills'][0][1],
                     **{f'reward_{stat}': practice.reward_amount(index,stat,activity_rules) for stat in practice.FIELDS}))
with (out/'stage_schedule.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
(out/'rules_audit.json').write_text(json.dumps(dict(revision=rules['revision'],stage_count=len(rows),
    original_sources=['analysis/configs/cortege/cortege_base_0.csv:5001','analysis/configs/cortege/cortege_name_0.csv:5001',
    'analysis/evidence/lua_named/lua/ui/practiceUI.lua.txt:51-291','analysis/evidence/lua_named/lua/event_mgr.lua.txt:1406-1420'],
    inferred=rules['provenance']['inferred'],reward_base=activity_rules['train_increase'],
    reward_formula='train_increase[stat] * (rule_index + 1)',
    native_protocol=dict(request=1026,fight_type=4,des_type=1,des_id=0,des_value=0,
    lineup=1028,replay=1027,reward_event=5,end_event=44)),ensure_ascii=False,indent=2)+'\n')
print(f'Exported {len(rows)} stages; original stats, inferred stage curve and rewards')
