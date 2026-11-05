"""Isolated Lua 5.1 adapters with a real encoded backend response; no live account.

Requires lupa.lua51. Does not claim to exercise native Cocos drawing/animations.
"""
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode
from lupa.lua51 import LuaRuntime


def main():
    now=1792814400
    with tempfile.TemporaryDirectory() as temp, patch('network_redirect.game_clock.now',return_value=now):
        b=Backend(Path(temp),18770,lambda *a,**k:None)
        try:
            replies=b.respond(encode(1346,dict(serial_num=90000,id=1,data='{}')),{'authenticated':True})
            fixture=next(login_fields(d['data']) for mid,_,d in map(decode,replies) if mid==2998 and d['id']==197)
        finally: b.close()
    vm=LuaRuntime(unpack_returned_tuples=True)
    source=(ROOT/'network_redirect/save_monkey_client.lua').read_text().replace('__SAVE_MONKEY_ENABLED__','true')
    harness=(ROOT/'tests/save_monkey_client_regression.lua').read_text().replace('-- INSTALL_PATCH',source).replace('-- INSTALL_AGAIN',source)
    vm.execute('FIXTURE='+summon.lua(fixture))
    checks=list(vm.execute(harness).values())
    vm.execute('assert(loadstring(...))',summon.client_source(summon.load_rules()))
    checks.append('full production injection compiles in Lua 5.1')
    report=dict(passed=True,native_cocos=False,live_account_resources_changed=False,checks=checks)
    dest=ROOT/'analysis/evidence/save_monkey/client_validation.json'
    dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
