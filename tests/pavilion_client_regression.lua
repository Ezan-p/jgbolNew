-- Exercise native-shaped captured timers without a live account or Cocos.
local now=1000
local labels,callbacks,sent={},{},{}
local ms={d_time={},d_u={},d_data={},d_csv={},d_smithUI={},d_commonLayerUI={}}
local ui={g_self={config={begin_time=1000,end_time=1000+14*86400}},g_csv={},g_data={},g_destinyUI={}}
ms.d_destinyUI=ui;package.loaded.ms=ms
ms.d_time.getTime=function() return now end
ms.d_time.getRestTime=function(deadline) return deadline>now and 'native time' or nil end
ms.d_u.createByStyles=function(style) labels[#labels+1]=style.string end
ms.d_u.delay=function(layer,seconds,fn) callbacks[#callbacks+1]=fn end
ms.d_data.callback_update_config=function() end
ms.d_csv.open2=function() end
ms.d_smithUI.getItemInfoByType=function() return {count=0} end
ui.onGetResult=function() end
ui.updateActivityStatus=function(c) ui.g_self.config=c end
ui.canJoin=function() return false end
ui.sendRequest=function(flag) sent[#sent+1]=flag end
ui.closeBuyItemLayer=function() ui.g_destinyUI.buy_layer=nil end
ui.showMyMoney=function() end
ui.showPageDeatail=function() end
ui.showRechargePage=function() end
local function nativeTimer()
 local capturedEnd=ui.g_self.config.end_time
 local function tick()
  local text=ms.d_time.getRestTime(capturedEnd)
  assert(text,'native timer closed permanent activity')
  ms.d_u.createByStyles({type='label',string='活动剩余：'..text,fontsize=26})
  ms.d_u.delay({},1,tick)
 end
 tick()
end
ui.show=nativeTimer;ui.showGift=nativeTimer
local rest,delay,create=ms.d_time.getRestTime,ms.d_u.delay,ms.d_u.createByStyles
-- INSTALL_PATCH
ui.show()
assert(labels[#labels]=='刷新剩余：14天00:00:00')
assert(ms.d_time.getRestTime==rest and ms.d_u.delay==delay and ms.d_u.createByStyles==create)
assert(ui.canJoin(),'entry closed at inclusive start boundary')
now=now+1;callbacks[#callbacks]()
assert(labels[#labels]=='刷新剩余：13天23:59:59')
ui.showGift();assert(labels[#labels]=='刷新剩余：13天23:59:59')
now=ui.g_self.config.end_time
callbacks[#callbacks]()
assert(labels[#labels]=='刷新剩余：0天00:00:00')
assert(ui.canJoin(),'permanent entry closed at rollover')
assert(#sent==1 and sent[1]==1,'zero must request fresh data')
ui.sendRequest(2);ui.sendRequest(3)
assert(#sent==1,'stale purchase or claim escaped query throttle')
now=now+3;ui.sendRequest(2);assert(#sent==2 and sent[2]==1)
local oldTick=callbacks[#callbacks]
ui.g_destinyUI.buy_layer={}
local data={begin_time=1000+14*86400,end_time=1000+28*86400,exchange_info={},charge_info={}}
ms.d_data.callback_update_config({local_pavilion={data=data,status=data}})
assert(ui.g_destinyUI.buy_layer==nil,'old purchase dialog survived rollover')
oldTick()
assert(labels[#labels]=='刷新剩余：13天23:59:57','captured timer still uses old deadline')
ui.sendRequest(2);assert(sent[#sent]==2,'fresh purchase remains blocked')
ui.showGift=function() error('render failure') end -- restore must still recover original.
ui._localPavilionRestore()
assert(ui.show==nativeTimer and ui.showGift==nativeTimer and not ui._localPavilionRestore)
assert(ms.d_time.getRestTime==rest and ms.d_u.delay==delay and ms.d_u.createByStyles==create)
return 'fortnight countdown, zero refresh, stale actions, captured timer, dialog reset and restoration passed'
