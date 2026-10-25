"""Reproduce pet client evidence, including numeric constants omitted by listings."""
import hashlib
import json
from pathlib import Path
from luajit_static import parse, listing
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'analysis/evidence'
index={p[0]:p[1] for line in (E/'resource_index.decoded.txt').read_text().splitlines() if len(p:=line.split('===='))==3}
names=['lua/ui/petUI.lua','lua/data.lua','lua/event_mgr.lua','lua/ui/actNoticeUI.lua']+['csv_config/'+n+'.csv' for n in ('animal_base','animal_control','animal_exprience','animal_growup','animal_pet_exp','animal_train_config','animal_upgrade')]
inputs=[]
for n in names:
 p=ROOT/'jgbol3.87/assets/release_'/index[n]
 inputs.append(dict(logical=n,physical=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
c=parse((ROOT/'jgbol3.87/assets/release_'/index[names[0]]).read_bytes())
ids=[1,3,21,22,28,30,31,34,35,39,40,46,48,49,51,52,54,55,61,65,68,74,75]
(E/'pet_official_bytecode.txt').write_text('\n'.join('NUMERIC CONSTANTS proto%d: %s\n'%(i,c['protos'][i]['numbers'])+listing(dict(source=c['source'],root=i,protos=[c['protos'][i]])) for i in ids))
(E/'pet_official_audit.json').write_text(json.dumps(dict(inputs=inputs,request=1330,response_event=174,operations={1:'eat',2:'compose',3:'select',4:'enter',5:'train',6:'star'},fusion_numeric_constants=c['protos'][65]['numbers'],official_server_available=False),ensure_ascii=False,indent=2)+'\n')
print('pet evidence generated')
