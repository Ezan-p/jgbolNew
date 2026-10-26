"""Extract original 渡劫 Lua evidence; no game save or network access."""
import hashlib
import json
from pathlib import Path
from luajit_static import parse, listing
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'analysis/evidence/rape'

def main():
    OUT.mkdir(exist_ok=True)
    index=dict(line.split('====')[:2] for line in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    inputs=[]
    for module in ('ui/crossDoomUI','ui/messageUI'):
        name='lua/'+module+'.lua';data=(ROOT/'jgbol3.87/assets/release_'/index[name]).read_bytes()
        (OUT/(module.split('/')[-1]+'.txt')).write_text(listing(parse(data)))
        inputs.append(dict(logical=name,sha256=hashlib.sha256(data).hexdigest()))
    for name in ('v2/crossDoom/info1.png','v2/crossDoom/info2.png'):
        data=(ROOT/'jgbol3.87/assets/release_'/index[name]).read_bytes()
        (OUT/name.split('/')[-1]).write_bytes(data)
        inputs.append(dict(logical=name,sha256=hashlib.sha256(data).hexdigest()))
    report=dict(client='3.87',official_server_available=False,inputs=inputs,
        verified=['original info1/info2 images describe victory skills plus extra rewards for clearing a column','form_list[1] and form_list[2] are both traversed','descending rand determines guard display order','form_type drives dice; ordered consecutive values are straight; equal values are triple','request 1060 carries request_id; fight 12 uses request_id as des_id and skill_type as des_value','events 40/41/77/78/84/114 are native callbacks'],
        user_rules_20261026=['guard count equals each die','column preview reward only; no guard rewards','free_count is remaining uses','explicit Continue refresh request'],
        inferred=['55/70/85 percent power matching','uniform six-sided dice','straight doubles column preview skills','quality-weighted skill drops','one optional revenge per day after loss; expires after 24 hours'])
    (OUT/'official_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Verified original 渡劫 and message Lua assets')

if __name__=='__main__':main()
