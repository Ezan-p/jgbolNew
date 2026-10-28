-- The native selector expands every owned scroll into a Lua row. Keep one
-- row per template instead: old saves can contain tens of millions of books.
do
 local ms=package.loaded.ms
 local ui=ms and (ms.d_expbookUI or package.loaded['ui.expbookUI'])
 local bag=ms and ms.d_packageUI
 if not ui or not bag or not ms.d_data or not ms.d_data.createBatchUse then return 'pending' end
 if not ui._localExpbookRestore then
  local originals={}
  local function replace(name,fn)
   originals[name]=ui[name]
   ui[name]=fn
  end
  local function chosen(row)
   if not row.isChosen then return 0 end
   return math.min(row.count or 1,row.selectedCount or 1)
  end
  local function choose(row,count)
   row.selectedCount=count
   row.isChosen=count>0
  end
  local function notice(key)
   ms.d_info.show(ms.d_hz.gethz(key),2)
  end
  local function redraw(index)
   local view=ui.g_expbookUI and ui.g_expbookUI.expTableView
   if view then
    if index then view:updateCellAtIndex(index) else view:reloadData() end
   end
  end
  local function selectionChanged(index)
   redraw(index)
   ui.onSelectedListChanged()
  end
  -- All-select stops before the efficiency penalty, just like the original.
  -- Summing the bounded level curve replaces its loop over individual books.
  local function selectionBudget()
   local state=ui.g_self
   local character=state and state.selectedCortId and ui.getCortegeInfo(state.selectedCortId)
   local curve=character and character.csvInfo and
    ms.d_data.g_characterExpTable[character.csvInfo.quality]
   if not curve then return 0 end
   state.MAXLV=#curve
   local playerLevel=ms.d_mainUI.g_playerInfo.level
   local target=playerLevel>=80 and ui.getMaxLimitLevel() or
    math.floor(playerLevel*state.lvLimit[2].lv)
   target=math.min(target,#curve)
   if character.level>=target then return 0 end
   local budget=-(character.cur_exp or 0)
   for level=character.level,target-1 do budget=budget+(curve[level] or 0) end
   return math.max(0,budget)
  end
  replace('getTotalExp',function()
   local total=0
   for _,row in ipairs(ui.g_self.expbook or {}) do total=total+row.exp*chosen(row) end
   return total
  end)
  replace('cancelSelect',function(index,notify)
   local state=ui.g_self
   if not state or not state.expbook then return end
   if index then
    local row=state.expbook[index]
    if row then choose(row,0) end
   else
    for _,row in ipairs(state.expbook) do choose(row,0) end
    if ui.g_expbookUI then ui.g_expbookUI.isDeselect=false end
    ui.setSelectBtn()
   end
   redraw(index)
   if notify then ui.onSelectedListChanged() end
  end)
  replace('selectAllExpBook',function()
   local state,panel=ui.g_self,ui.g_expbookUI
   if not panel or not panel.allBtn then return end
   if not state.selectedCortId then notice('need_cortege');return end
   if not panel.expTableView then notice('no_expbook');return end
   if panel.isDeselect then ui.cancelSelect(nil,true);return end
   local budget=math.max(0,selectionBudget()-ui.getTotalExp())
   local last
   for index,row in ipairs(state.expbook or {}) do
    local old=chosen(row)
    local count=math.min(row.count-old,math.floor(budget/row.exp))
    if count>0 then
     choose(row,old+count)
     budget=math.max(0,budget-count*row.exp)
     last=index
    end
   end
   selectionChanged()
   if last then panel.expTableView:showIndexAtCenter(last) end
   panel.isDeselect=ui.getTotalExp()>0
   ui.setSelectBtn()
  end)
  replace('filterSelectedList',function()
   local state,panel=ui.g_self,ui.g_expbookUI
   if not state or not state.selectedCortId or not panel or not panel.expTableView then return end
   local budget=selectionBudget()
   for _,row in ipairs(state.expbook or {}) do
    local count=math.min(chosen(row),math.floor(budget/row.exp))
    choose(row,count)
    budget=math.max(0,budget-count*row.exp)
   end
   panel.isDeselect=ui.getTotalExp()>0
   ui.setSelectBtn()
   selectionChanged()
  end)
  replace('sendEatExpbookRequest',function()
   local state=ui.g_self
   if not state or not state.selectedCortId then return end
   local rows,byType={},{}
   for _,row in ipairs(state.expbook or {}) do
    local count=chosen(row)
    if count>0 then
     local request=byType[row.type]
     if not request then
      request={type_id=row.type,count=0}
      byType[row.type]=request
      rows[#rows+1]=request
     end
     request.count=request.count+count
    end
   end
   if #rows==0 then return end
   ms.d_u.main_server_send_msg(ms.d_msg_def.gscl_msg_id.msg_consume_fairy_roll,{
    first_send=true,flag=state.last_select_page,cortege_id=state.selectedCortId,
    roll_count=#rows,roll_list=rows})
  end)
  local nativeCell=ui.createExpBookCell
  replace('createExpBookCell',function(node,row,size)
   nativeCell(node,row,size)
   if not row.count then return end
   -- A separate middle line keeps the native name, level and per-book XP.
   local label=ms.d_u.createByStyle({type='label',font='arial',fontsize=18,
    string='已选 '..chosen(row)..' / '..row.count,color={254,235,192},anchor={0,0.5}})
   label:setPosition(size.width*0.25,size.height*0.5)
   local width=label:getContentSize().width
   if width>size.width*0.52 then label:setScale(size.width*0.52/width) end
   node:addChild(label,2)
  end)
  replace('createExpbookMutilSelectLayer',function()
   local state,panel=ui.g_self,ui.g_expbookUI
   panel.expTableView=nil
   local layer=ms.d_u.clearLayer(panel.page_layer,5,state.tags.exp)
   if not layer then return end
   state.expbook={}
   state.enoughExpbook=false
   panel.isDeselect=false
   ui.setSelectBtn()
   -- Switching pages or receiving a use result clears the old selection.
   -- Refresh the old preview/limit too, so a previously full target does not
   -- leave the new material page unable to accept any selection.
   if state.selectedCortId and ui.getCortegeInfo(state.selectedCortId) then
    selectionBudget()
    ui.onSelectedListChanged()
   end
   local byType={}
   bag.getAllProps()
   local subtypes=ms.d_common_def.item_sub_type
   local wanted=state.last_select_page==1 and subtypes.roll or
    (state.last_select_page==2 and subtypes.exp_pill)
   for _,item in pairs(bag.g_propsTable or {}) do
    local csv=item.csvInfo
    local count=tonumber(item.count) or 0
    if csv and csv.sub_type==wanted and (csv.base_experience_plus or 0)>0 and
      count>0 and count<math.huge and item.is_lock~=true and item.is_lock~=1 then
     count=math.floor(count)
     if count>0 then
      local row=byType[item.type_id]
      if not row then
       row={id=item.id,type=item.type_id,level=csv.show_level,name=csv.name,
        exp=csv.base_experience_plus,count=0,selectedCount=0,isChosen=false}
       byType[item.type_id]=row
       state.expbook[#state.expbook+1]=row
      end
      row.count=row.count+count
     end
    end
   end
   table.sort(state.expbook,function(a,b)
    if a.exp~=b.exp then return a.exp<b.exp end
    return a.type<b.type
   end)
   if #state.expbook==0 then
    local label=ms.d_u.createByStyle({type='label',font='arial',fontsize=30,
     x=0.7,y=0.51,string=ms.d_hz.gethz('no_scroll'..state.last_select_page),color={254,188,39}})
    layer:addChild(label,10)
    return
   end
   local screen=CCDirector:sharedDirector():getVisibleSize()
   local rect={x=screen.width*0.435,y=screen.height*0.185,
    width=screen.width*0.53,height=screen.height*0.57}
   local size=CCSizeMake(rect.width,rect.height*0.3)
   local view=ms.d_tableView.tableView(layer,rect)
   view:startScroll()
   view:setDataSource(ui.createExpBookDataSource(size))
   view:setDelegate({touchCellAtIndex=function(index)
    local row=state.expbook[index]
    if ui.g_self~=state or ui.g_expbookUI~=panel or panel.expTableView~=view or not row then return end
    if chosen(row)>0 then choose(row,0);selectionChanged(index);return end
    if state.enoughExpbook then notice('exp_none');return end
    local target,page,rows=state.selectedCortId,state.last_select_page,state.expbook
    if row.count==1 then choose(row,1);selectionChanged(index);return end
    ms.d_data.createBatchUse(panel.main_layer,{min=1,max=row.count,defaultCount=1},function(count)
     -- A late callback from a closed/rebuilt panel must not edit a new choice.
     if ui.g_self~=state or ui.g_expbookUI~=panel or not panel.main_layer or
       state.selectedCortId~=target or state.last_select_page~=page or
       state.expbook~=rows or rows[index]~=row then return end
     if type(count)~='number' or count~=math.floor(count) or count<1 or count>row.count then return end
     choose(row,count)
     selectionChanged(index)
    end)
   end})
   panel.expTableView=view
  end)
  ui._localExpbookRestore=function()
   for name,original in pairs(originals) do ui[name]=original end
   ui._localExpbookRestore=nil
  end
 end
end
