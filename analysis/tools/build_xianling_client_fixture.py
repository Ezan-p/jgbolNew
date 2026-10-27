"""Original xianling UI replay with disposable backend state, no real purchases."""
import sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from network_redirect import recharge,vip,xianling,summon
from network_redirect.backend import Backend,login_fields
from network_redirect.protocol import encode,decode
root=Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory() as tmp:
 b=Backend(Path(tmp),18790,lambda *a,**k:None);r=b.profile();r['gold_coin']=10000;summon.add_item(r,1140,1000);summon.add_item(r,1249,90);summon.add_item(r,1152,20);summon.add_item(r,1156,100);b.save(r)
 lines=["""local ms=assert(package.loaded.ms)
local x=ms.d_xianlingShopUI
local v=ms.d_vipUI
if v.g_self and v.g_self.main_layer then v.pressClose() end
if v._localVipRestore then v._localVipRestore() end
local saved={player=ms.d_mainUI.g_playerInfo,config=ms.d_data.g_new_config,send=ms.d_u.main_server_send_msg,
 item=ms.d_smithUI.getItemInfoByType,count=ms.d_data.getItemCountByType,shop=x.g_self,box=x.g_boxUI,waiting=ms.d_u.g_is_waiting_1106}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
ms.d_mainUI.g_playerInfo.gold_coin=10000
ms.d_data.g_new_config=ms.d_c.table_copy(saved.config)
x.g_self=ms.d_c.table_copy(saved.shop);x.g_self.main_layer=nil
local scene=CCDirector:sharedDirector():getRunningScene()
local host=CCLayer:create();scene:addChild(host,9999)
local captured
ms.d_u.main_server_send_msg=function(mid,data) captured={mid=mid,data=data} end
ms.d_u.g_is_waiting_1106=false
ms.d_smithUI.getItemInfoByType=function(kind,tid) if kind==5 and tid==1140 then return {count=1000,type_id=1140} end return saved.item(kind,tid) end
ms.d_data.getItemCountByType=function(kind,tid) if kind==5 and tid==1249 then return 90 end return saved.count(kind,tid) end
local results={}
local function check(name,fn) local ok,err=xpcall(fn,debug.traceback);results[#results+1]={name=name,ok=ok,error=not ok and tostring(err) or nil} end
"""]
 lines.append(Path('network_redirect/vip_client.lua').read_text())
 lines.append('ms.d_data.g_new_config.local_recharge='+summon.lua(recharge.client_state(b.profile(),int(__import__('time').time()),recharge.load_rules(),b.welfare_rules)))
 lines.append("check('open_shop',function() x.create(host);assert(captured.mid==1336 and captured.data.flag==4) end)")
 serial=4000
 def req(name,mid=1336,**kw):
  global serial
  serial+=1;packets=b.respond(encode(mid,dict(serial_num=serial,**kw)),dict(authenticated=True))
  lines.append('check('+summon.lua(name)+',function()')
  for p in packets:
   m,_,d=decode(p)
   if m==2998 and d['id']==55 and mid!=1111:raise AssertionError((name,d))
   if m==2998 and d['id']==185:lines.append('x.onGetResult('+summon.lua(login_fields(d['data']))+')')
   if m==2998 and d['id']==21:lines.append('ms.d_commonLayerUI.recvUsedItem('+summon.lua(login_fields(d['data']))+')')
   if m==2995:lines.append('x.updateStatus('+summon.lua(d)+')')
  lines.append('end)')
 req('catalog',flag=4,index=0,count=0)
 lines.append("check('page_two',function() x.g_self.cur_page=2;x.updateExchangeLayer() end)")
 lines.append("check('batch_dialog',function() x.createBatchBuy(x.g_self.config[1]) end)")
 req('exchange',flag=1,index=1,count=2)
 req('daily_buy',flag=3,index=1,count=1)
 req('charge_tracking',1111,event_id=251,data='{item_id=105,large_count=10,small_count=0,order_id="fixture-charge-01"}')
 req('eligible_monthly',flag=4,index=0,count=0)
 for i in range(1,5):
  lines.append("check('preview_%d',function() x.showGiftDetail(%d);x.g_self.main_layer:removeChildByTag(x.g_self.giftDetailTag,true) end)"%(i,i))
  req('monthly_'+str(i),flag=2,index=i,count=1)
 lines.append("check('box_selector',function() x.showBoxUseLayer(host,30) end)")
 item=next(a for a in b.profile()['attachments'] if a['type_id']==1249)
 req('box_reward',1051,item_type=1249,item_id=item['id'],item_count=30,des_type=5,des_id=5001)
 lines.append("""check('close_shop',function() x.closeShop() end)
check('market_recharge',function()
 ms.d_shopUI.recharge()
 local r=ms.d_rechargeUI
 assert(r.g_self.main_layer)
 tolua.cast(r.g_self.menu:getChildByTag(r.g_self.button_tag+1),'CCMenuItem'):activate()
 r._localCardConfirm()
 r.pressClose()
 assert(captured.mid==1111 and captured.data.event_id==251)
 local d=assert(loadstring('return '..captured.data.data))();assert(d.item_id==101 and d.order_id)
end)
check('xianling_recharge',function()
 x.create(host);x.recharge()
 assert(ms.d_rechargeUI.g_self.main_layer);ms.d_rechargeUI.pressClose()
end)
host:removeFromParentAndCleanup(true)
x.g_self=saved.shop;x.g_boxUI=saved.box
ms.d_mainUI.g_playerInfo=saved.player;ms.d_data.g_new_config=saved.config
ms.d_u.main_server_send_msg=saved.send;ms.d_u.g_is_waiting_1106=saved.waiting
ms.d_smithUI.getItemInfoByType=saved.item;ms.d_data.getItemCountByType=saved.count
return table.tostring({results=results,restored=true})
""")
 (root/'analysis/evidence/xianling/client_fixture.lua').write_text('\n'.join(lines));b.close()
