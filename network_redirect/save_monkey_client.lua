-- Preserve original art, grid preview, two-tap use, effects and reward panels.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_saveMonkeyUI
 local act=ms and ms.d_activityUI
 if not ui or not act or not ui.onGetResult then return 'pending' end
 if not ui._localSaveMonkeyRestore then
  local saved={};local latest;local enabled=__SAVE_MONKEY_ENABLED__
  local function replace(name,fn) saved[name]=ui[name];ui[name]=fn end
  local oldStatus=act.getQiwenStatus
  local oldSend=ms.d_u.main_server_send_msg
  local oldExchange=ms.d_data.g_exchange_table
  local oldLogin=ui.g_newbieLoginConfig
  local function timing(data)
   if not data then return end
   enabled=data.local_enabled
   if ui.g_self and ui.g_self.data and data.score_charge then
    ui.g_self.data.score_charge=data.score_charge
    ui.g_self.data.score_prize_list=data.score_prize_list
   end
   local key=ms.d_common_def.client_config_type.activity_time
   local kind=ms.d_common_def.activity_type.save_monkey_activity
   ms.d_data.g_new_config[key]=ms.d_data.g_new_config[key] or {}
   ms.d_data.g_new_config[key][kind]={data}
  end
  local key=ms.d_common_def.client_config_type.activity_time
  local kind=ms.d_common_def.activity_type.save_monkey_activity
  local originalTimes=ms.d_data.g_new_config[key] and ms.d_data.g_new_config[key][kind]
  act.getQiwenStatus=function(data,...)
   timing(data.local_save_monkey)
   return oldStatus(data,...)
  end
  replace('canJoin',function() return enabled end)
  local function send(op,data)
   data=data or {}
   if op~=1 and op~=4 and op~=6 then
    if not latest or ms.d_time.getTime()>=latest.local_reset_time then
     ms.d_info.show('十万猴急进度已刷新，请重新进入活动')
     return ms.d_u.main_server_send_msg(1346,{id=1,data=table.tostring({})})
    end
    data.local_token=latest.local_token
   end
   return ms.d_u.main_server_send_msg(1346,{id=op,data=table.tostring(data)})
  end
  ms.d_u.main_server_send_msg=function(mid,req,...)
   if mid==1346 and req.id==9 then
    local data=table.loadstring(req.data)
    if not data or not latest or ms.d_time.getTime()>=latest.local_reset_time then
     ms.d_info.show('十万猴急进度已刷新，请重新进入活动');return
    end
    data.local_token=latest.local_token;req.data=table.tostring(data)
   end
   return oldSend(mid,req,...)
  end
  replace('sendMsgEnterGame',function() return send(1) end)
  replace('sendMsgUseItm',function(x,y,kind) return send(2,{item_type=kind,pos_info={x=x,y=y}}) end)
  replace('sendMsgUseEyeItm',function() return send(2,{item_type=1354}) end)
  replace('sendMsgQueryActivityPoint',function() return send(6) end)
  replace('sendMsgQueryPieceShop',function() return send(4) end)
  replace('sendMsgBuyItem',function(index,count) return send(5,{index=index,count=count}) end)
  replace('sendMsgTakeScoreItem',function(id) return send(3,{prize_id=id}) end)
  replace('sendMsgTakePointItem',function(id) return send(7,{prize_id=id}) end)
  local originalResult=ui.onGetResult
  replace('onGetResult',function(data,...)
   latest=data;timing(data.local_activity)
   if data.local_assist then
    local rows={}
    for i,row in pairs(data.local_assist) do
     rows[i]={consume=row.consume,item={},rewardCount={}}
     for _,p in ipairs(row.prizes) do
      rows[i].item[#rows[i].item+1]=p[3]
      rows[i].rewardCount[#rows[i].rewardCount+1]=p
     end
    end
    ms.d_data.g_exchange_table=rows;ui.g_newbieLoginConfig=rows
   end
   -- Claims/shop callbacks do not call setData in the shipped module.
   -- Keep their main-screen counters and recharge statuses authoritative.
   if data.id~=1 and data.id~=2 then ui.setData(data) end
   return originalResult(data,...)
  end)
  replace('getRewardLoginConfig',function()
   if latest and latest.local_assist then return end
   if saved.getRewardLoginConfig then return saved.getRewardLoginConfig() end
  end)
  local originalCheck=ui.checkCanUseBomb
  replace('checkCanUseBomb',function(grid,x,y,kind)
   if kind==1350 and grid[x] and grid[x][y] and grid[x][y].stone_type==3 then return false end
   return originalCheck(grid,x,y,kind)
  end)
  -- Native count helper chooses a single stack and includes locked items.
  replace('getItemCount',function(tid)
   local count=0
   for _,item in pairs(ms.d_packageUI.g_packageItemsInfo or {}) do
    if item.attach_type==5 and item.type_id==tid and (not item.is_lock or item.is_lock==0) and
       (not item.owner_id or item.owner_id==0) and (not item.equip_pos or item.equip_pos==0) then
     count=count+item.count
    end
   end
   return count
  end)
  ui._localSaveMonkeyRestore=function()
   for k,v in pairs(saved) do ui[k]=v end
   act.getQiwenStatus=oldStatus;ms.d_u.main_server_send_msg=oldSend
   ms.d_data.g_exchange_table=oldExchange;ui.g_newbieLoginConfig=oldLogin
   if ms.d_data.g_new_config[key] then ms.d_data.g_new_config[key][kind]=originalTimes end
   ui._localSaveMonkeyRestore=nil
  end
 end
end
