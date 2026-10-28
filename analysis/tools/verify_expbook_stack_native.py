"""Exercise the native stacked selector on copied client state, without account writes."""
import copy
import json
from pathlib import Path
import sqlite3
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/tools')]
from android_emulator.config import load_config
from observability.collector import processes
from network_redirect import formation, summon
from network_redirect.backend import Backend, login_fields
from verify_guild_client import LUA_EVALUATOR


def expectations():
    with tempfile.TemporaryDirectory() as tmp:
        b=Backend(Path(tmp),18770,lambda *a,**k:None)
        try:
            baseline=b.profile();baseline['level']=99
            result={}
            for name,books in [('mixed',[(1041,2),(1042,1),(1043,1)]),('three',[(1041,3)])]:
                role=copy.deepcopy(baseline);c=role['corteges'][0]
                c.update(type=5046,level=1,cur_exp=0)
                for tid,count in books:summon.add_item(role,tid,count)
                formation.feed(role,dict(flag=1,first_send=True,cortege_id=c['id'],
                    roll_count=len(books),roll_list=[dict(type_id=tid,count=count) for tid,count in books]),b.formation_rules)
                result[name]=dict(level=c['level'],cur_exp=c['cur_exp'])
            return result
        finally:b.close()


def inventory_snapshot():
    with sqlite3.connect('file:'+str(ROOT/'.runtime/offline/game.sqlite3')+'?mode=ro',uri=True) as db:
        return [(account,[(i['id'],i['type_id'],i['count']) for i in json.loads(data)['attachments']])
                for account,data in db.execute('select account,data from roles order by account')]


def main():
    import frida
    cfg=load_config(ROOT/'game.json')
    session=frida.get_device(cfg['serial'],timeout=10).attach(
        next(p for p,n in processes(cfg).items() if n==cfg['package']))
    script=session.create_script(LUA_EVALUATOR)
    source='local ADAPTER_SOURCE='+summon.lua((ROOT/'network_redirect/expbook_client.lua').read_text())+'\n'
    source+='local EXPECTED='+summon.lua(expectations())+'\n'
    source+=(ROOT/'analysis/tools/expbook_stack_native_harness.lua').read_text()
    before=inventory_snapshot()
    try:
        script.load();raw=script.exports_sync.evaluate(source)
        report=login_fields(raw['result']) if raw.get('status')==0 else dict(passed=False,raw=raw)
    finally:script.unload();session.detach()
    report['inventory_preserved']=before==inventory_snapshot()
    report['native_cocos']=True
    report['passed']=bool(report.get('passed') and report.get('restored') and report['inventory_preserved'])
    output=ROOT/'analysis/evidence/expbooks/stack_native_validation_20261028.json'
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not report['passed']:raise SystemExit(1)


if __name__=='__main__':main()
