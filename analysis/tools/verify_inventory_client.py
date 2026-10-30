"""Check native inventory ordering and bag use with captured sends, no account writes."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT/'analysis/tools')]
from android_emulator.config import load_config
from observability.collector import processes
from network_redirect.backend import login_fields
from network_redirect import summon
from verify_guild_client import LUA_EVALUATOR

HARNESS = r'''
local source=__SOURCE__
local ms=assert(package.loaded.ms)
local bag=assert(ms.d_packageUI)
assert(not bag._localInventoryRestore,'run before applying the inventory patch')
local saved={sort=bag.sortProps,groups=bag.g_reorgItemsInfo,props=bag.g_propsTable,
 last=bag.g_lastRequestUsedItem,send=ms.d_u.main_server_send_msg,picker=ms.d_data.createBatchUse}
local report={passed=false,checks={},live_before={}}
local function check(name,fn)
 fn();report.checks[#report.checks+1]=name
end
local function rows(ids)
 local result={}
 for _,id in ipairs(ids) do result[#result+1]={attach_type=5,type_id=id,id=900000+id,count=16,
  csvInfo=assert(bag.g_itemAttrTable[id])} end
 return result
end
local function build(items)
 bag.g_reorgItemsInfo={[5]={[6]=items}}
 bag.getAllProps()
 return bag.g_propsTable
end
local function bagOrder(items)
 local ids={}
 for _,i in ipairs(items) do if i.type_id>=1304 and i.type_id<=1307 then ids[#ids+1]=i.type_id end end
 return table.concat(ids,',')
end
local ok,err=xpcall(function()
 for n,i in ipairs(saved.props or {}) do
  if i.type_id>=1304 and i.type_id<=1307 then
   report.live_before[#report.live_before+1]={type_id=i.type_id,count=i.count,position=n}
  end
 end
 local input=rows({1304,1305,1306,1307,1041,1042,1043,1044,1034})
 check('reproduce_original_misplaced_1307',function()
  assert(bagOrder(build(input))=='1307,1304,1305,1306')
 end)
 assert(loadstring(source))()
 local comparator=bag.sortProps
 check('four_bags_consecutive_in_native_list',function()
  local result=build(input)
  local first
  for n,i in ipairs(result) do if i.type_id==1304 then first=n end end
  assert(first)
  for n=0,3 do assert(result[first+n].type_id==1304+n) end
 end)
 check('other_items_keep_native_relative_order',function()
  local others=rows({1044,1041,1034,1043,1042})
  table.sort(others,saved.sort)
  local index=1
  for _,i in ipairs(bag.g_propsTable) do
   if i.type_id<1304 or i.type_id>1307 then assert(i.type_id==others[index].type_id);index=index+1 end
  end
  assert(index==#others+1)
 end)
 check('missing_bags_not_created_and_rebuild_stable',function()
  for _=1,3 do local result=build(rows({1307,1304}));assert(#result==2 and bagOrder(result)=='1304,1307') end
  assert(#build({})==0)
 end)
 check('metadata_untouched_and_patch_idempotent',function()
  assert(bag.g_itemAttrTable[1307].sortOrder==100)
  assert(loadstring(source))();assert(bag.sortProps==comparator)
 end)
 local sent={}
 ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
 ms.d_data.createBatchUse=function(parent,range,callback)
  assert(range.min==1 and range.max==15);callback(15)
 end
 bag.g_lastRequestUsedItem={}
 for tid=1304,1307 do
  check('native_bag_'..tid..'_single_and_batch',function()
   local item=rows({tid})[1]
   build({item})
   for _,count in ipairs({1,16}) do
    item.count=count;sent={};bag.requestUseItem(item)
    assert(#sent==1 and sent[1].mid==1051)
    local req=sent[1].data
    assert(req.item_type==tid and req.item_id==item.id and req.item_count==(count==1 and 1 or 15))
   end
  end)
 end
 check('restore_and_reinstall',function()
  bag._localInventoryRestore();assert(bag.sortProps==saved.sort)
  assert(loadstring(source))();assert(bag.sortProps~=saved.sort)
 end)
 report.passed=true
end,debug.traceback)
if bag._localInventoryRestore then bag._localInventoryRestore() end
bag.sortProps=saved.sort;bag.g_reorgItemsInfo=saved.groups;bag.g_propsTable=saved.props
bag.g_lastRequestUsedItem=saved.last;ms.d_u.main_server_send_msg=saved.send;ms.d_data.createBatchUse=saved.picker
report.restored=bag.sortProps==saved.sort and bag.g_propsTable==saved.props
if not ok then report.error=tostring(err) end
return table.tostring(report)
'''


def main():
    import frida
    cfg = load_config(ROOT/'game.json')
    pid = next(p for p, n in processes(cfg).items() if n == cfg['package'])
    session = frida.get_device(cfg['serial'], timeout=10).attach(pid)
    evaluator = LUA_EVALUATOR.replace('pending={code,resolve};',
        "const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
    script = session.create_script(evaluator)
    try:
        script.load()
        source = (ROOT/'network_redirect/inventory_client.lua').read_text()
        result = script.exports_sync.evaluate(HARNESS.replace('__SOURCE__', summon.lua(source)))
        if result.get('status') != 0:
            raise RuntimeError(result)
        report = login_fields(result['result'])
        report.update(native_cocos=True, live_account_resources_changed=False)
        path = ROOT/'analysis/evidence/item_rewards/inventory_order_20261030.json'
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if not report['passed'] or not report['restored']:
            raise SystemExit(1)
    finally:
        script.unload()
        session.detach()


if __name__ == '__main__':
    main()
