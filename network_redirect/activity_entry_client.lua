-- Use the shipped East Sea Treasure frame animation for these event entries.
-- funUI.createFunCell reads hasCCBI and attaches ui001.ccbi itself.
do
 local ms=package.loaded.ms
 local ui=ms and ms.d_funUI
 if not ui or not ui.funConfig or not ui.funID or not ui.getFunList then return 'pending' end
 if not ui._localActivityEntryRestore then
  local oldList=ui.getFunList
  local names={'tower','springCard','springActivityMoney','mooncake','rice','destiny'}
  local saved={}
  for _,name in ipairs(names) do
   if not ui.funConfig[ui.funID[name]] then return 'pending' end
  end
  for _,name in ipairs(names) do
   local config=ui.funConfig[ui.funID[name]]
   saved[#saved+1]={config=config,hasCCBI=config.hasCCBI}
   config.hasCCBI=true
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
  ui._localActivityEntryRestore=function()
   ui.getFunList=oldList
   for _,entry in ipairs(saved) do entry.config.hasCCBI=entry.hasCCBI end
   ui._localActivityEntryRestore=nil
  end
 end
end
