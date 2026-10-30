-- Offline edition identity on the original start / server-selection scene.
-- Runs before gameplay's ms module is loaded; never writes saves.
do
 local ui=package.loaded['update.updateUI']
 if type(ui)=='table' and type(ui.create)=='function' and not ui._localBrandingRestore then
  local tag=918106
  local originalCreate=ui.create
  local function refresh()
   local scene=ui.g_self and ui.g_self.main_scene
   if not scene or scene:getChildByTag(tag) then return end
   local update=package.loaded['update.update_ms']
   local panel=CCLayer:create()
   panel:setTouchEnabled(false)
   -- Match the native version labels, including their style helper's scaling.
   local function label(text,y)
    local node=update.d_u.createByStyle({type='label',string=text,
     font='arial',fontsize=22,x=0.98,y=y,anchor={1,0.5},color={255,255,202}})
    panel:addChild(node)
   end
   label('离线版·非商业·仅供学习',0.80)
   label('v106',0.75)
   label('开发者@Ezan',0.70)
   scene:addChild(panel,20000,tag)
  end
  ui.create=function(...)
   local result=originalCreate(...)
   refresh()
   return result
  end
  ui._localBrandingRefresh=refresh
  ui._localBrandingRestore=function()
   local scene=ui.g_self and ui.g_self.main_scene
   if scene and scene==CCDirector:sharedDirector():getRunningScene() then scene:removeChildByTag(tag,true) end
   ui.create=originalCreate
   ui._localBrandingRefresh=nil
   ui._localBrandingRestore=nil
  end
  if ui.g_self and ui.g_self.main_scene==CCDirector:sharedDirector():getRunningScene() then refresh() end
 end
end
