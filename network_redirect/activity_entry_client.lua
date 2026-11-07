-- Use the shipped East Sea Treasure frame animation for these event entries.
-- funUI.createFunCell reads hasCCBI and attaches ui001.ccbi itself.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_funUI
 if not ui or not ui.funConfig or not ui.funID or type(ui.getFunList)~='function'
     or not ui.funID.dream or not ui.funID.saveMonkey then return 'pending' end
 -- A module can be re-executed in the same table. Do not mistake its old
 -- restore marker for the current list callback.
 if ui._localActivityEntryCurrent and ui._localActivityEntryCurrent()~='ready' then
  ui._localActivityEntryRestore()
 end
 if not ui._localActivityEntryRestore then
  local oldList=ui.getFunList
  local names={'tower','springCard','springActivityMoney','mooncake','rice','destiny'}
  local saved={}
  for _,name in ipairs(names) do
   local config=ui.funConfig[ui.funID[name]]
   if config then
    saved[#saved+1]={config=config,hasCCBI=config.hasCCBI}
    config.hasCCBI=true
   end
  end
  -- Hide dream (仙梦居) and saveMonkey (十万猴急) in the shared entry list.
  -- Reindex after filtering so selection and table cells stay aligned.
  ui.getFunList=function(...)
   local visible={}
   for _,row in ipairs(oldList(...)) do
    if row.id~=ui.funID.dream and row.id~=ui.funID.saveMonkey then
     row.index=#visible+1
     visible[#visible+1]=row
    end
   end
   return visible
  end
  local installedList=ui.getFunList
  local installedConfig,installedIDs=ui.funConfig,ui.funID
  ui._localActivityEntryCurrent=function()
   if package.loaded.ms==ms and ms.d_funUI==ui and ui.getFunList==installedList
       and ui.funConfig==installedConfig and ui.funID==installedIDs then return 'ready' end
   return 'pending'
  end
  ui._localActivityEntryRestore=function()
   if ui.getFunList==installedList then ui.getFunList=oldList end
   for _,entry in ipairs(saved) do entry.config.hasCCBI=entry.hasCCBI end
   ui._localActivityEntryRestore=nil
   ui._localActivityEntryCurrent=nil
  end
 end
end
