"""Verify all seven gold promotions and native claim panels with disposable saves."""
import json
import runpy
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/tools')]
from android_emulator.config import load_config,device_environment
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR
from network_redirect import activity,activity_rank as rank,summon
from network_redirect.backend import Backend
from network_redirect.protocol import encode,decode
NOW=1792933200


def packets():
    with tempfile.TemporaryDirectory() as tmp,patch('network_redirect.backend.time.time',return_value=NOW):
        b=Backend(Path(tmp),18770,lambda *a,**k:None)
        try:
            r=b.profile();r.update(level=60,gold_coin=10000)
            activity.prepare(r,NOW,b.activity_rules);r['activity'].update(rank_reached_order=1,rank_promotions=[])
            b.save(r)
            result={'initial':[dict(mid=decode(p)[0],data=decode(p)[2]) for p in (rank.client_state(r),rank.board(r))],'claims':[]}
            for i in range(4,11):
                response=b.respond(encode(1203,dict(serial_num=200000+i,exchange_type=i)),{'authenticated':True})
                decoded=[decode(p) for p in response]
                assert not any(m==2998 and d['id']==55 for m,_,d in decoded)
                assert not any(m==1022 for m,_,d in decoded)
                result['claims'].append([dict(mid=m,data=d) for m,_,d in decoded if m==1032 or m==2998 and d['id'] in (80,36)])
            return result
        finally:b.close()


def main():
    import frida
    runpy.run_path(str(ROOT/'analysis/tools/build_rank_client_fixture.py'))
    payload=packets();config=load_config(ROOT/'game.json')
    pid=next(p for p,n in processes(config).items() if n==config['package'])
    session=frida.get_device(config['serial'],timeout=10).attach(pid)
    evaluator=LUA_EVALUATOR.replace('pending={code,resolve};',"const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
    script=session.create_script(evaluator);report=dict(native_cocos=True,live_save_modified=False)
    output=ROOT/'analysis/evidence/rank'
    def check(code):
        result=script.exports_sync.evaluate(code)
        if result.get('status')!=0:raise RuntimeError(result)
        return result['result']
    def shot(name):
        time.sleep(.5)
        data=subprocess.run([str(config['adb_path']),'-s',config['serial'],'exec-out','screencap','-p'],env=device_environment(config),capture_output=True,timeout=15,check=True)
        (output/name).write_bytes(data.stdout)
    try:
        script.load();check("if rankClaimPreview then pcall(rankClaimPreview.restore);rankClaimPreview=nil end;if rank_fixture_restore then rank_fixture_restore() end;return 'clean'");check((ROOT/'.runtime/rank-fixture.lua').read_text())
        check('rankClaimData='+summon.lua(payload))
        report['render']=check('''local ms=package.loaded.ms;local ui=ms.d_rankUI
ui.g_rankUI=nil;ui.g_isInRankPage=false;ui.g_isInChangePage=false
function rankClaimApply(rows)
 for _,v in ipairs(rows) do
  if v.mid==1022 then ui.getDateFormServer(v.data)
  elseif v.mid==1032 then ms.d_event_mgr.msg_modify_attr_1032(nil,v.data,nil)
  elseif v.mid==2998 then ms.d_event_mgr.msg_common_event_2998(nil,v.data,nil) end
 end
 assert(rank_fixture_errors=='',rank_fixture_errors)
end
rankClaimApply(rankClaimData.initial);ms.d_activityUI.show();ui.showRankUI();ui.goToCreditsChargePage()
local amounts={50,100,200,300,400,1000,2000}
for index=3,9 do
 local node;for _,v in pairs(ui.g_chargeNode) do if v:getTag()==index then node=v end end
 local text=tolua.cast(assert(node):getChildren():objectAtIndex(3),'CCLabelTTF'):getString()
 assert(text:find('元宝: '..amounts[index-2],1,true),text);assert(not text:find('蟠桃',1,true),text)
 assert(ui.g_label_info[index].btn:isVisible() and ui.g_label_info[index].btn:isEnabled())
end
local root=CCLayer:create();root:retain();CCDirector:sharedDirector():getRunningScene():addChild(root,9999)
local native=ms.d_commonLayerUI.showPrizeResLayer;local send=ms.d_u.main_server_send_msg
rankClaimPreview={root=root,count=0,sends=0,restore=function()
 ms.d_commonLayerUI.showPrizeResLayer=native;ms.d_u.main_server_send_msg=send
 root:removeFromParentAndCleanup(true);root:release();rankClaimPreview=nil;rankClaimData=nil;rankClaimApply=nil;rankClaimStep=nil
end}
ms.d_u.main_server_send_msg=function(mid,data)
 assert(mid==1203);rankClaimPreview.sends=rankClaimPreview.sends+1;rankClaimPreview.request=data.exchange_type
end
ms.d_commonLayerUI.showPrizeResLayer=function(parent,list,...)
 rankClaimPreview.count=rankClaimPreview.count+1;rankClaimPreview.prizes=list
 return native(root,list,...)
end
function rankClaimStep(index)
 root:removeAllChildrenWithCleanup(true)
 local scene=CCDirector:sharedDirector():getRunningScene()
 if root:getParent()~=scene then root:removeFromParentAndCleanup(true);scene:addChild(root,9999) end
 local page=ui.g_rankUI.credits_layer;local before=rankClaimPreview.sends;local popups=rankClaimPreview.count
 ui.g_label_info[index].btn:activate();assert(rankClaimPreview.sends==before+1 and rankClaimPreview.request==index+1)
 rankClaimApply(rankClaimData.claims[index-2])
 assert(rankClaimPreview.count==popups+1 and root:getChildrenCount()>0)
 local p=rankClaimPreview.prizes[1];assert(p.object_type==11 and p.attach_count==amounts[index-2])
 assert(ui.g_isInChangePage and ui.g_rankUI.credits_layer==page and page:isVisible())
 local label=ui.g_label_info[index];assert(not label.btn:isVisible() and not label.btn:isEnabled())
 assert(label.btn2:isVisible() and not label.btn2:isEnabled())
 assert(label.claimed_background:isVisible() and label.claimed_text:isVisible() and label.claimed_text:getString()=='已领取')
 assert(not label.numlabel:isVisible() and not label.countBkg:isVisible())
 ui.chargeButtonCallBack(index);label.btn:activate();label.btn2:activate()
 assert(rankClaimPreview.sends==before+1,'duplicate claim sent')
 assert(rank_fixture_errors=='',rank_fixture_errors)
 return 'gold '..amounts[index-2]..': panel shown, disabled button says 已领取, page preserved'
end
local layer=ui.g_rankUI.credits_cells_layer
for _,v in pairs(ui.g_chargeNode) do if v:getTag()==5 then layer.container:setPositionY(layer.scrollView:getContentSize().height-v:getPositionY()-v:getContentSize().height*.5) end end
return 'all seven native rows show gold names and enabled claim buttons'
''')
        shot('peach_exchange_gold_claim_before.png')
        report['claims']=[check('return rankClaimStep('+str(i)+')') for i in range(3,10)]
        shot('peach_exchange_gold_claim_panel.png')
        report['reopen']=check('''local ui=package.loaded.ms.d_rankUI
rankClaimPreview.root:removeAllChildrenWithCleanup(true)
ui.destroyCreditsLayer();ui.createCreditsChargePage()
for i=3,9 do local row=ui.g_label_info[i];assert(not row.btn:isEnabled() and row.btn2:isVisible() and not row.btn2:isEnabled());assert(row.claimed_text:isVisible() and row.claimed_text:getString()=='已领取') end
local layer=ui.g_rankUI.credits_cells_layer
for _,v in pairs(ui.g_chargeNode) do if v:getTag()==5 then layer.container:setPositionY(layer.scrollView:getContentSize().height-v:getPositionY()-v:getContentSize().height*.5) end end
return 'all seven remain disabled and show 已领取 after reopening'
''')
        shot('peach_exchange_gold_claim_after.png');report['passed']=True
    finally:
        try:report['restore']=check("if rankClaimPreview then rankClaimPreview.restore() end;if rank_fixture_restore then return rank_fixture_restore() end;return 'restored'")
        finally:script.unload();session.detach()
        (output/'peach_exchange_gold_claim_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
