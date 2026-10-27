local ms=assert(package.loaded.ms)
local function up(fn,key)
 for i=1,80 do local n,v=debug.getupvalue(fn,i);if not n then break end;if n==key then return v end end
 error('missing upvalue '..key)
end
local factory=up(ms.d_packageUI.ensureFilter,'getPackageCellsDataSource')
local draw=up(factory,'createCellOnPackage')
local screen=up(factory,'scrSize')
local size=CCSizeMake(screen.width*0.7,screen.height*0.21)
local root=CCNode:create();root:retain()
local renderer
local sent=0;local oldsend=ms.d_u.main_server_send_msg
ms.d_u.main_server_send_msg=function() sent=sent+1;error('unexpected network call') end
local out={screen={width=screen.width,height=screen.height},row={width=size.width,height=size.height},sample_count=12}
local ok,err=xpcall(function()
 for i,tid in ipairs({1152,1156}) do
  local node=CCNode:create();root:addChild(node);node:setPosition(0,(2-i)*size.height)
  local item={id=900000+tid,type_id=tid,attach_type=5,count=12,level=1,csvInfo=ms.d_packageUI.g_itemAttrTable[tid]}
  draw(node,6,item,'v2/packageUI/xinxilan.png',size)
 end
 renderer=CCRenderTexture:create(math.ceil(size.width),math.ceil(size.height*2))
 renderer:retain();renderer:beginWithClear(0.10,0.07,0.04,1)
 root:visit();renderer:endToLua()
 local path='/sdcard/gold_cards_native_rows.png'
 out.saved=renderer:saveToFile('/sdcard/gold_cards_native_rows.png')
 out.path=path
end,debug.traceback)
ms.d_u.main_server_send_msg=oldsend
root:removeAllChildrenWithCleanup(true);root:release()
if renderer then renderer:release() end
out.ok=ok;out.error=err;out.sent=sent;out.restored=ms.d_u.main_server_send_msg==oldsend
return table.tostring(out)
