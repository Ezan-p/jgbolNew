"""Generate isolated responses for real 3.87 sale UI; never mutate the live save."""
import sys
import tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon
from network_redirect.backend import Backend
from network_redirect.protocol import encode, decode

lines = [r'''local ms=assert(package.loaded.ms);local ui=ms.d_packageUI
local saved={player=ms.d_mainUI.g_playerInfo,corts=ms.d_lineupUI.g_characterInfo,items=ui.g_packageItemsInfo,
 send=ms.d_u.main_server_send_msg,report=ms.MS_report_error,tableMenu=ms.d_tableView.createTableViewMenu,
 menu=ms.d_u.createMenu,calc=ms.d_guildPartyUI.getCalc,style=ms.d_u.createByStyle,info=ms.d_info.show}
local cases={};local errors='';local sent={};local saleButtons={};local confirm;local calc;local preview;local tip
item_sale_fixture_results={};item_sale_fixture_finished=false
local function step(name,fn) cases[#cases+1]={name=name,run=fn} end
ms.MS_report_error=function(e) errors=errors..'\n'..tostring(e) end
ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
ms.d_tableView.createTableViewMenu=function(style,...)
 for _,b in ipairs(style.menuItems or {}) do if b.npic=='v2/batchBuyUI/sale1.png' then saleButtons[#saleButtons+1]=b.tapHandler end end
 return saved.tableMenu(style,...)
end
ms.d_u.createMenu=function(style,...)
 for _,b in ipairs(style) do if b.npic=='v2/batchBuyUI/ensure1.png' then confirm=b.call_back end end
 return saved.menu(style,...)
end
ms.d_guildPartyUI.getCalc=function(...) calc=saved.calc(...);return calc end
ms.d_u.createByStyle=function(style,...) if style.string and tostring(style.string):find(ms.d_hz.gethz('saleHint'),1,true) then preview=tostring(style.string) end;return saved.style(style,...) end
ms.d_info.show=function(s,...) tip=tostring(s);return saved.info(s,...) end
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
local function apply(mid,d)
 if mid==1032 then ms.d_event_mgr.msg_modify_attr_1032(nil,d,nil)
 elseif mid==1034 then ms.d_lineupUI.getDateFormServer(d)
 elseif mid==1035 then ui.getDateFormServer(d)
 elseif mid==2998 and (d.id==153 or d.id==55) then ms.d_event_mgr.msg_common_event_2998(nil,d,nil) end
end
local function item(tid) for _,i in ipairs(ui.g_packageItemsInfo) do if i.type_id==tid then return i end end end
local function press(delta)
 local function walk(n)
  local children=n:getChildren();if not children then return false end
  for j=0,children:count()-1 do
   local c=tolua.cast(children:objectAtIndex(j),'CCNode')
   if c:getTag()==delta then tolua.cast(c,'CCMenuItem'):activate();return true end
   if walk(c) then return true end
  end
  return false
 end
 assert(walk(calc),'missing calculator button '..delta)
end
local function refresh() saleButtons={};ui.showPackage(ui.packageTagDef.props) end
''']
with tempfile.TemporaryDirectory() as tmp:
    b = Backend(Path(tmp), 18770, lambda *a, **kw: None)
    role = b.profile(); role.update(level=60, silver_coin=123000)
    summon.add_item(role, 7010, 23); summon.add_item(role, 1001, 9)
    b.save(role)
    lines.append('ms.d_mainUI.g_playerInfo.silver_coin=123000')
    for packet in b.inventory(role):
        mid, _, data = decode(packet)
        lines.append('apply(%d,%s)' % (mid, summon.lua(data)))
    lines.append(r'''
step('original_price_table',function()
 ms.d_data.getEquipPiecePrice();local n=0;for t,p in pairs(ms.d_data.g_ep_price) do n=n+1;assert(p==1000) end;assert(n==28)
end)
step('main_page',function() ms.d_mainUI.show() end)
step('bag_page',function() ui.show() end)
step('props_page',function() refresh() end)
step('bag_sale_entry_and_non_sale_item',function() assert(#saleButtons==1,'expected one sell button, got '..#saleButtons) end)
step('default_quantity_and_price',function() saleButtons[1]();assert(confirm and calc);assert(preview:find('1000',1,true)) end)
step('minus_one_lower_bound',function() press(-1);assert(preview:find('1000',1,true)) end)
step('plus_one',function() press(1);assert(preview:find('2000',1,true)) end)
step('plus_ten',function() press(10);assert(preview:find('12000',1,true)) end)
step('minus_ten',function() press(-10);assert(preview:find('2000',1,true)) end)
step('upper_bound',function() press(10);press(10);press(10);assert(preview:find('23000',1,true)) end)
step('cancel_does_not_send',function() local n=#sent;confirm(1);assert(#sent==n);assert(item(7010).count==23) end)
step('confirm_original_1088_partial',function()
 saleButtons[1]();press(1);confirm(2);local s=sent[#sent];assert(s.mid==1088)
 local d=assert(loadstring('return '..s.data.data))();assert(d.item_list[7010]==2)
end)
''')
    def response(name, count, check):
        packets = b.respond(encode(1088, dict(serial_num=1000+count, data=summon.lua(dict(item_list={7010: count})))), {'authenticated': True})
        lines.append('step(%s,function()' % summon.lua(name))
        for packet in packets:
            mid, _, data = decode(packet)
            assert not (mid == 2998 and data['id'] == 55), data
            if mid in (1032, 1034, 1035) or mid == 2998 and data['id'] == 153:
                lines.append('apply(%d,%s)' % (mid, summon.lua(data)))
        lines.append(check+' end)')
    response('partial_sale_callback_and_balance', 2, "assert(item(7010).count==21);assert(ms.d_mainUI.g_playerInfo.silver_coin==125000);assert(tip:find('2000',1,true))")
    lines.append(r'''step('partial_refresh',function() refresh() end)
step('confirm_original_1088_all',function()
 saleButtons[1]();press(10);press(10);confirm(2);local s=sent[#sent];assert(s.mid==1088)
 local d=assert(loadstring('return '..s.data.data))();assert(d.item_list[7010]==21)
end)''')
    response('full_sale_callback_removes_row', 21, "assert(not item(7010));assert(ms.d_mainUI.g_playerInfo.silver_coin==146000);assert(tip:find('21000',1,true));assert(item(1001).count==9)")
    lines.append(r'''step('full_refresh',function() refresh() end)
step('full_refresh_no_sale_button',function() assert(#saleButtons==0) end)
step('close_bag',function() ms.d_mainUI.show() end)
step('reopen_bag',function() ui.show() end)
step('reopen_props',function() refresh() end)
step('reopen_without_sold_item',function() assert(#saleButtons==0) end)''')
    b.close()
lines.append(r'''
local function restore()
 ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report
 ms.d_tableView.createTableViewMenu=saved.tableMenu;ms.d_u.createMenu=saved.menu
 ms.d_guildPartyUI.getCalc=saved.calc;ms.d_u.createByStyle=saved.style;ms.d_info.show=saved.info
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_lineupUI.g_characterInfo=saved.corts;ui.g_packageItemsInfo=saved.items
 ui.g_isPackageSorted=false;ui.sortItems();ms.d_lineupUI.sortcharacterInfo();ms.d_mainUI.show()
 item_sale_fixture_finished=true
end
local scheduler=CCDirector:sharedDirector():getScheduler();local index=0;local handle
handle=scheduler:scheduleScriptFunc(function()
 if index>0 then item_sale_fixture_results[index]={name=cases[index].name,errors=errors} end
 index=index+1
 if index>#cases then scheduler:unscheduleScriptEntry(handle);restore();return end
 errors='';local ok,e=xpcall(cases[index].run,debug.traceback);if not ok then errors=errors..'\n'..tostring(e) end
end,2,false)
return 'scheduled '..#cases..' item sale cases'
''')
(ROOT/'.runtime/item-sale-fixture.lua').write_text('\n'.join(lines))
print('Built original-client sale fixture')
