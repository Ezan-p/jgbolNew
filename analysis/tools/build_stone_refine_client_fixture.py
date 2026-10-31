"""Build an isolated native UI/send fixture; intercept requests and restore live state."""
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import summon, formation
from network_redirect.backend import Backend
from network_redirect.protocol import decode


def main():
    with tempfile.TemporaryDirectory() as tmp:
        backend = Backend(Path(tmp), 18790, lambda *a, **k: None)
        role = backend.profile()
        role.update(level=99, reborn_layer=4)
        cases = []
        for kind in (1, 2, 3):
            for level in (12, 13):
                stone = dict(id=formation.new_id(role), attach_type=5, type_id=1089+kind,
                             count=1, level=level, owner_id=0, equip_order=0, equip_pos=0)
                role['attachments'].append(stone)
                cases.append(dict(id=stone['id'], kind=kind, level=level))
                for _ in range(2):
                    role['attachments'].append(dict(stone, id=formation.new_id(role)))
        summon.add_item(role, 1369, 100)
        backend.save(role)
        packets = [decode(p) for p in backend.inventory(backend.profile())]
        backend.close()
    source = (ROOT/'network_redirect/equipment_client.lua').read_text()
    lua = r'''
local ms=assert(package.loaded.ms)
local ui=ms.d_stoneCastUI
local saved={player=ms.d_mainUI.g_playerInfo,items=ms.d_packageUI.g_packageItemsInfo,
 corts=ms.d_lineupUI.g_characterInfo,send=ms.d_u.main_server_send_msg,info=ms.d_info.show,
 menu=ms.d_u.createMenu,style=ms.d_u.createByStyle,rights=ms.d_roleRebornUI.g_reborn_condition,
 cast=ui.g_stoneCastUI,self=ui.g_self,press=ui.pressCast,restore=ui._localStoneRefineRestore}
local results={};local sent,labels,button,close
local function restore()
 if close then pcall(close) end
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_packageUI.g_packageItemsInfo=saved.items
 ms.d_lineupUI.g_characterInfo=saved.corts;ms.d_roleRebornUI.g_reborn_condition=saved.rights
 ms.d_u.main_server_send_msg=saved.send;ms.d_info.show=saved.info
 ms.d_u.createMenu=saved.menu;ms.d_u.createByStyle=saved.style
 ui.g_stoneCastUI=saved.cast;ui.g_self=saved.self;ui.pressCast=saved.press;ui._localStoneRefineRestore=saved.restore
 ms.d_packageUI.g_isPackageSorted=false;ms.d_packageUI.sortItems();ms.d_lineupUI.sortcharacterInfo()
 ms.d_mainUI.show()
end
local ok,err=xpcall(function()
 ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
 ms.d_mainUI.g_playerInfo.level=99;ms.d_mainUI.g_playerInfo.reborn_layer=4
 ms.d_roleRebornUI.g_reborn_condition=ms.d_c.table_copy(saved.rights)
 ms.d_roleRebornUI.g_reborn_condition[4].rights.open_stone_sys=true
 ui.g_stoneCastUI={};ui.g_self=ms.d_c.table_copy(saved.self)
 ms.d_u.main_server_send_msg=function(mid,data) sent={mid=mid,data=data} end
 ms.d_info.show=function(text) results[#results+1]='info:'..tostring(text) end
 ms.d_u.createByStyle=function(spec,...) if spec.string then labels[tostring(spec.string)]=true end;return saved.style(spec,...) end
 ms.d_u.createMenu=function(spec,...)
  for _,entry in ipairs(spec) do
   if entry.npic=='v2/stoneCastUI/tilian.png' then button=entry.call_back end
   if entry.npic=='v2/introUI/close1.png' then close=entry.call_back end
  end
  return saved.menu(spec,...)
 end
 labels={}
 __INVENTORY__
 __ADAPTER__
 local cases=__CASES__
 for _,case in ipairs(cases) do
  sent=nil;labels={};button=nil;close=nil
  local stone
  for _,item in ipairs(ms.d_packageUI.g_packageItemsInfo) do if item.id==case.id then stone=item end end
  assert(stone,'missing temporary stone')
  ui.pressCast(ms.d_mainUI.g_mainUI.main_layer,stone,1000)
  assert(button,'no refine button for '..case.kind..'/'..case.level)
  local old=case.level==12 and (case.kind==3 and '120.0%' or '100.0%') or (case.kind==3 and '240.0%' or '200.0%')
  local new=case.level==12 and (case.kind==3 and '240.0%' or '200.0%') or (case.kind==3 and '600.0%' or '500.0%')
  assert(labels[old] and labels[new],'wrong preview '..old..'/'..new)
  button()
  assert(sent and sent.mid==1054 and sent.data.flag==5 and sent.data.des_id==case.id,'wrong native request')
  assert(sent.data.src_count==0 and #sent.data.src_list==0 and sent.data.stone_pos==0 and sent.data.equip_order==0,'wrong native request fields')
  results[#results+1]='PASS '..case.kind..':'..case.level..'->'..(case.level+1)..' preview and native button request'
  assert(close);close();close=nil
 end
end,debug.traceback)
restore()
assert(ok,err)
return table.concat(results,'\n')..'\nRESTORED'
'''
    inventory = []
    for mid, _, data in packets:
        target = 'ms.d_packageUI' if mid == 1035 else 'ms.d_lineupUI'
        if mid in (1034, 1035):
            inventory.append(target + '.getDateFormServer(' + summon.lua(data) + ')')
    lua = lua.replace('__INVENTORY__', '\n'.join(inventory)).replace('__ADAPTER__', source).replace('__CASES__', summon.lua(cases))
    (ROOT/'.runtime/stone-refine-native-fixture.lua').write_text(lua)
    print('Generated six native preview/send cases; no requests leave the fixture.')


if __name__ == '__main__':
    main()
