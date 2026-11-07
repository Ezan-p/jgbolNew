"""Read the installed QA client's activity list; never inject replacement patches."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import threading

import frida

ROOT=Path(__file__).resolve().parents[2]
EVIDENCE=ROOT/'analysis/evidence/v110/activity-entry-fix-20261106'
ADB=[str(ROOT/'.runtime/sdk/platform-tools/adb'),'-s','emulator-5572']
PACKAGE='com.sygame.jingubang.p360'
LUA=r'''
local ms=package.loaded.ms
if not ms or not ms.d_funUI or not ms.d_funUI.getFunList then return 'pending:modules' end
local rows={}
local ok,err=pcall(function() for _,row in ipairs(ms.d_funUI.getFunList()) do rows[#rows+1]=row.id end end)
if not ok then return 'pending:list:'..tostring(err) end
table.sort(rows)
local fun,ys=ms.d_funUI,ms.d_twoYearsCelebrateUI
local entry=fun._localActivityEntryCurrent and fun._localActivityEntryCurrent() or 'missing'
local yuanshi=ys and ys._localYuanshiCurrent and ys._localYuanshiCurrent() or 'missing'
local c=ms.d_data and ms.d_data.g_new_config and ms.d_data.g_new_config[24]
c=c and c.yuanshi_info
return 'ids='..table.concat(rows,',')..';entry='..entry..';yuanshi='..yuanshi..
 ';canJoin='..tostring(ys and ys.canJoin and ys.canJoin())..';permanent='..tostring(c and c.permanent)
'''
JS=r'''
const m=Process.getModuleByName('libxiyoujilua.so');
const fn=(n,r,a)=>new NativeFunction(m.getExportByName(n),r,a);
const top=fn('lua_gettop','int',['pointer']),set=fn('lua_settop','void',['pointer','int']);
const load=fn('luaL_loadbuffer','int',['pointer','pointer','uint','pointer']);
const call=fn('lua_pcall','int',['pointer','int','int','int']);
const str=fn('lua_tolstring','pointer',['pointer','int','pointer']);
let busy=false,done=false,last=0;
const hook=Interceptor.attach(m.getExportByName('lua_pcall'),{onEnter(args){
 if(busy||done||Date.now()-last<1000)return;busy=true;last=Date.now();
 const L=args[0],old=top(L);
 try {
  const code=SOURCE;
  let status=load(L,Memory.allocUtf8String(code),unescape(encodeURIComponent(code)).length,Memory.allocUtf8String('@read-only-activity-inspector'));
  if(!status)status=call(L,0,1,0);
  const p=str(L,-1,ptr(0)),result=p.isNull()?'':p.readUtf8String();
  if(status || !result.startsWith('pending:')) {done=true;send({status:status,result:result});}
 } catch(e) {done=true;send({error:String(e)});}
 finally {set(L,old);busy=false;}
}});
'''


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name',choices=['first-login','reopen','relogin'])
    args=parser.parse_args()
    assert subprocess.check_output(ADB+['emu','avd','name']).decode().splitlines()[0]=='standalone32'
    device=frida.get_device('emulator-5572',timeout=10)
    processes=subprocess.check_output(ADB+['shell','ps']).decode().splitlines()
    pid=next(int(line.split()[1]) for line in processes if line.split()[-1]==PACKAGE)
    session=device.attach(pid)
    event=threading.Event(); messages=[]
    script=session.create_script(JS.replace('SOURCE',json.dumps(LUA)))
    def receive(message,data):messages.append(message);event.set()
    script.on('message',receive)
    try:
        script.load()
        assert event.wait(50),'No loaded Lua activity list observed within 50 seconds'
    finally:
        script.unload();session.detach()
    payload=messages[-1].get('payload',{})
    assert payload.get('status')==0,messages
    fields=dict(field.split('=',1) for field in payload['result'].split(';'))
    ids=[int(n) for n in fields['ids'].split(',') if n]
    report=dict(passed=46 in ids and 40 not in ids and 48 not in ids and fields['entry']==fields['yuanshi']=='ready',
        apk_sha256=json.loads((EVIDENCE/'build-validation.json').read_text())['apk_sha256'],
        activity_ids=ids,entry_patch=fields['entry'],yuanshi_patch=fields['yuanshi'],
        yuanshi_can_join=fields['canJoin']=='true',permanent=fields['permanent']=='true',
        scope=args.name,read_only_probe=True,replacement_lua_injected=False,
        physical_device=False)
    (EVIDENCE/(args.name+'-activities.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    assert report['passed'] and report['yuanshi_can_join'] and report['permanent']


if __name__=='__main__':main()
