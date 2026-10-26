-- Original 3.87 betting dialogs mix old globals with the new page's locals.
-- Repair only that bridge; keep the native dialog, selection and send handlers.
do
 local ms=package.loaded.ms
 if not (ms and ms.d_guildFightUI and ms.d_crossRealm) then return 'pending' end
 if ms and debug and debug.getupvalue and debug.setupvalue then
  for _,name in ipairs({'d_guildFightUI','d_crossRealm'}) do
   local ui=ms[name]
   if ui and ui.showAgainstDetail and not ui._localGuildRestore then
    for i=1,100 do
     local key,native=debug.getupvalue(ui.showAgainstDetail,i)
     if not key then break end
     if key=='showBetLayer' and type(native)=='function' then
      local env=getfenv(native)
      local oldData,oldParent=rawget(env,'dataTable'),rawget(env,'parent')
      local bridges={}
      local function show(parent,choices)
       parent=parent or ms.d_xianmengUI.getXianMengMainLayer()
       local state={}
       for k,v in pairs(rawget(env,'dataTable') or {}) do state[k]=v end
       state.main_layer=parent
       state.getWorldPos=ms.d_data.getWorldPos
       state.getCDStr=ms.d_u.getCDStr
       env.dataTable=state
       for n=1,100 do
        local field,value=debug.getupvalue(native,n)
        if not field then break end
        if field=='dataTable' and type(value)=='table' then
         if not bridges[value] then bridges[value]={value.getWorldPos,value.getCDStr} end
         value.getWorldPos=ms.d_data.getWorldPos;value.getCDStr=ms.d_u.getCDStr
        end
       end
       local previous=rawget(env,'parent');env.parent=parent
       local ok,result=pcall(native,parent,choices or (env.betInfo and env.betInfo.teams))
       env.parent=previous
       if not ok then error(result) end
       return result
      end
      debug.setupvalue(ui.showAgainstDetail,i,show)
      ui._localGuildRestore=function()
       debug.setupvalue(ui.showAgainstDetail,i,native)
       for value,old in pairs(bridges) do value.getWorldPos=old[1];value.getCDStr=old[2] end
       env.dataTable=oldData;env.parent=oldParent;ui._localGuildRestore=nil
      end
      break
     end
    end
   end
  end
 end
end
