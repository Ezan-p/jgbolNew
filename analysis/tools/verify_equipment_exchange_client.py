"""Isolated native 3.87 menus/labels and real backend exchange replies."""
import json
import copy
from unittest.mock import patch
from pathlib import Path
import subprocess
import sys
import tempfile
import time
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/tools')]
from network_redirect import formation as f, summon, equipment_crafting as c
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode
from android_emulator.config import load_config, device_environment
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR


def fixture():
    with tempfile.TemporaryDirectory() as tmp:
        b=Backend(Path(tmp),18770,lambda *a,**k:None)
        try:
            role=b.profile();role.update(level=99,silver_coin=1000000000)
            role['attachments']=[]
            tid=next(t for t,r in f.ITEMS.items() if r['main_type']=='1' and r['quality']=='4')
            def add(**kw):
                item=dict(id=f.new_id(role),attach_type=5,type_id=tid,level=1,count=1)
                item.update(kw);role['attachments'].append(item);return item['id']
            ids=[add() for _ in range(50)]
            enhanced=add(level=20)
            invalid=[add(is_lock=1),add(advance_level=1),add(equip_order=1,equip_pos=1)]
            b.save(role)
            inventory=[d for m,_,d in map(decode,b.inventory(b.profile())) if m==1035]
            query=dict(c.compose_list(b.profile(),c.load_rules()),show=True)
            forging=copy.deepcopy(b.profile())
            target=query['equip_compose']['appoint'][-1]['material_type']
            cfg=f.ITEMS[target]
            summon.add_item(forging,(1007 if int(cfg['quality'])==5 else 1010)+int(cfg['main_type']),1)
            forged=c.compose(forging,dict(compose_type=2,equip_type=target,equip_quality=int(cfg['quality']),
                material_quality=4,material_count=5,material_list=[dict(id=i) for i in ids[:5]]),c.load_rules())[0][1]
            results=[]
            for n in range(1):
                packet=encode(1053,dict(serial_num=200000+n,compose_type=3,equip_type=6001,equip_quality=4,
                    material_quality=4,material_count=5,material_list=[dict(id=i) for i in ids[n*5:n*5+5]]))
                events=[login_fields(d['data']) for m,_,d in map(decode,b.respond(packet,{'authenticated':True})) if m==2998 and d['id']==6]
                assert len(events)==1;results.append(events[0])
            next_now=query['equip_compose']['weekly_reset_at']
            next_query=dict(c.compose_list(b.profile(),c.load_rules(),next_now),show=True)
            with patch.object(c.time,'time',return_value=next_now):
                packets=b.respond(encode(1053,dict(serial_num=200001,compose_type=3,equip_type=6001,equip_quality=4,
                    material_quality=4,material_count=5,material_list=[dict(id=i) for i in ids[5:10]])),{'authenticated':True})
            next_result=next(login_fields(d['data']) for m,_,d in map(decode,packets) if m==2998 and d['id']==6)
            data=dict(inventory=inventory,query=query,results=results,forged=forged,materials=ids,enhanced=enhanced,
                      invalid=invalid,now=int(time.time()),next_now=next_now,next_query=next_query,next_result=next_result)
            return 'local FIXTURE='+summon.lua(data)+'\n'+(ROOT/'analysis/tools/equipment_exchange_client_harness.lua').read_text().replace('-- INSTALL_PATCH',(ROOT/'network_redirect/equipment_exchange_client.lua').read_text())
        finally:b.close()


def main():
    import frida
    config=load_config(ROOT/'game.json');pid=next(p for p,n in processes(config).items() if n==config['package'])
    session=frida.get_device(config['serial'],timeout=10).attach(pid)
    evaluator=LUA_EVALUATOR.replace('pending={code,resolve};',"const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
    script=session.create_script(evaluator);destination=ROOT/'analysis/evidence/equipment_exchange';destination.mkdir(parents=True,exist_ok=True)
    report=dict(native_cocos=True,live_account_resources_changed=False,network_sends_captured=True,
                animation_completion='20 synchronous weekly callback checks, followed by a real native two-stage reward animation')
    try:
        script.load();raw=script.exports_sync.evaluate(fixture());report['raw']=raw;checks=[]
        if raw.get('status')==0:
            for line in raw['result'].splitlines():
                name,sep,rest=line.partition(':')
                if sep and rest.startswith(('true:','false:')):
                    ok,_,error=rest.partition(':');checks.append(dict(name=name,passed=ok=='true',error=error))
        report['checks']=checks;report['passed']=len(checks)==20 and all(c['passed'] for c in checks)
        if report['passed']:
            script.exports_sync.evaluate('exchangePreview.animate();return "started"')
            stop=time.monotonic()+15
            while time.monotonic()<stop:
                time.sleep(.2)
                raw=script.exports_sync.evaluate('return exchangePreview.animationResult()')
                if raw.get('status')!=0:raise RuntimeError(raw)
                animation=login_fields(raw['result'])
                if animation.get('finished'):break
            report['native_animation']=animation
            report['passed']=bool(animation.get('finished') and animation.get('count')==40 and
                                  animation.get('label')=='本周剩余兑换: 0/1' and '兑换成功' in animation.get('notice','') and not animation.get('errors'))
        if report['passed']:
            time.sleep(.5)
            shot=subprocess.run([str(config['adb_path']),'-s',config['serial'],'exec-out','screencap','-p'],env=device_environment(config),capture_output=True,timeout=15,check=True)
            (destination/'exchange.png').write_bytes(shot.stdout)
            script.exports_sync.evaluate('package.loaded.ms.d_forgeUI.returnBack();return "entry"')
            time.sleep(.3)
            shot=subprocess.run([str(config['adb_path']),'-s',config['serial'],'exec-out','screencap','-p'],env=device_environment(config),capture_output=True,timeout=15,check=True)
            (destination/'entry.png').write_bytes(shot.stdout)
    finally:
        try:report['restored']=script.exports_sync.evaluate('if exchangePreview then exchangePreview.restore();exchangePreview=nil end;return "restored"')==dict(status=0,result='restored')
        finally:script.unload();session.detach()
        (destination/'client_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not report.get('passed') or not report.get('restored'):raise SystemExit(1)


if __name__=='__main__':main()
