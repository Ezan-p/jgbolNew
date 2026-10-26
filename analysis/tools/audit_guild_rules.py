"""Re-extract original 3.87 guild contracts, without changing client assets."""
import ast
import hashlib
import json
import plistlib
from pathlib import Path
from luajit_static import parse, listing
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'analysis/evidence/guild'
MODULES = ['ui/'+n for n in ('xianmengUI','worldTreeUI','guildStoreUI','guildPartyUI','guildFightUI','secretAreaUI','petHomeUI','pethuntUI','escortUI','crossRealm','newChatUI')] + ['common/common_def','event_mgr','data']

def main():
    OUT.mkdir(exist_ok=True)
    index = dict(line.split('====')[:2] for line in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    inputs=[]
    for module in MODULES:
        logical='lua/'+module+'.lua'; path=ROOT/'jgbol3.87/assets/release_'/index[logical]
        chunk=parse(path.read_bytes()); text='\n'.join('NUMERIC proto%d %r'%(p['id'],p['numbers']) for p in chunk['protos'])+'\n'+listing(chunk)
        (OUT/(module.replace('/','_')+'.txt')).write_text(text)
        inputs.append(dict(logical=logical,physical=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    enums={}; lines=(OUT/'common_common_def.txt').read_text().splitlines()
    for i,line in enumerate(lines[:-1]):
        if 'TDUP' in line and "{'kind': 'table'" in line and 'GSET' in lines[i+1]:
            name=lines[i+1].split("'")[-2]
            if name.startswith(('union_','tree_','feast_','west_')) or name=='common_event_type':
                enums[name]=ast.literal_eval(line[line.index("{'kind'"):])['value']
    (OUT/'enums.json').write_text(json.dumps(enums,ensure_ascii=False,indent=2)+'\n')
    strings={}
    for logical in ('v2/String.plist','v2/String2.plist'):
        if logical not in index:continue
        path=ROOT/'jgbol3.87/assets/release_'/index[logical]
        strings.update({k:v for k,v in plistlib.loads(path.read_bytes()).items() if any(x in str(k).lower() for x in ('union','guild','tree','feast','xianmeng','pethunt','pethome','escort','west_','party_'))})
    (OUT/'strings.json').write_text(json.dumps(strings,ensure_ascii=False,indent=2)+'\n')
    (OUT/'audit.json').write_text(json.dumps(dict(client='3.87',official_server_available=False,inputs=inputs,request=1301,notification=82,config_section=8),ensure_ascii=False,indent=2)+'\n')
    names=('role_ranking','union_consume','union_fight','take_merge_gift','update_union_wander','update_union_catch')
    references={name:[] for name in names};count=0
    for logical,physical in index.items():
        if not logical.startswith('lua/') or not logical.endswith('.lua'):continue
        raw=(ROOT/'jgbol3.87/assets/release_'/physical).read_bytes();count+=1
        for name in names:
            if name.encode() in raw:references[name].append(logical)
    reserved=dict(scanned_lua_modules=count,string_references=references,
        conclusions={'10':'Only role_ranking enum found; no confirmed native request.',
                     '17':'Only union_consume enum found; no confirmed native request.',
                     '49':'xianmengUI L3324/L3579 handle replies; guildFightUI L632 uses fight_type 14 via 1026, not 1301/id49.',
                     '77':'Only take_merge_gift enum found; no native merge claim entry confirmed.',
                     '93':'Wander broadcast handler; no confirmed client request.',
                     '94':'petHomeUI proto26 L798-803 sends this request; proto2 L244 opens history.'},
        limitation='String inventory plus manual inspection of guild UI instructions; not proof of unavailable official server behavior.')
    (OUT/'current_reserved_protocol_audit.json').write_text(json.dumps(reserved,ensure_ascii=False,indent=2)+'\n')
    print('Audited',len(inputs),'original guild modules')
if __name__=='__main__': main()
