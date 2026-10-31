"""Reproducible catalogue audit and isolated Lua 5.1 wire/adapter verification."""
import copy
import hashlib
import json
from pathlib import Path
import sys
from lupa.lua51 import LuaRuntime
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import achievements as a, summon
from network_redirect.protocol import decode
from offline_android.pack_payload import collect_files

def main():
    official=ROOT/'analysis/evidence/hotupdate_gap_20261031/official_csv/achievements_config.csv'
    assert a.CATALOG_PATH.read_bytes()==official.read_bytes()
    role=dict(role_id=1)
    a.finalize(role)
    def packets(r,**kw):
        return [dict(mid=m,data=d) for m,_,d in map(decode,a.packets(r,**kw))]
    initial=packets(role)
    other=packets(dict(role,role_id=200))
    before=copy.deepcopy(role);a.add(role,590);a.finalize(role)
    delta=packets(role,new=1,previous=before)
    vm=LuaRuntime()
    data=vm.eval(summon.lua(dict(initial=initial,other=other,delta=delta)))
    checks=list(vm.execute((ROOT/'tests/achievement_hotupdate_client_regression.lua').read_text(),a.client_patch(),data).values())
    vm.execute('assert(loadstring(...))',summon.client_source(summon.load_rules()))
    files=collect_files()
    for p in ('analysis/configs/achievement_hotupdate/achievements_config.csv','network_redirect/achievements_client.lua'):
        assert p in files
    report=dict(passed=True,checks=checks,catalogue_count=len(a.CATALOG),open_count=len(a.OPEN),
        sha256=hashlib.sha256(official.read_bytes()).hexdigest(),official_byte_match=True,
        full_client_lua51_compile=True,payload_resources_present=True,
        native_cocos=False,live_save_modified=False,apk_rebuilt=False)
    (ROOT/'analysis/evidence/achievement_hotupdate/client_and_catalogue.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
