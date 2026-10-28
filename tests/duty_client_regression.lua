local source=...
local checks={}
local function check(name,value) assert(value,name);checks[#checks+1]=name end
local sent,changes,normalOpens={},0,0
local position={}
local utility={main_server_send_msg=function(mid,request) sent[#sent+1]={mid=mid,data=request} end,
 createMenu=function(styles) return styles end}
local function change() changes=changes+1;return 'normal-change' end
local guarded={'reloadData','requestChangeChar','requestChangeOrder','requestChangeItem',
 'showChgCharLayer','createChgPos','compareCharPosition'}
for _,name in ipairs(guarded) do position[name]=change end
local menus
position.showOthersInfo=function(info)
 assert(position.g_charPosUI.isReadOnly or not info.duty_preview)
 menus=utility.createMenu({x=0,y=1,
  {npic='v2/charPositionUI/mine1.png'}, {npic='v2/charPositionUI/yours1.png'},
  {npic='details.png'}})
 if info.raise then error('fixture failure') end
 return 'rendered'
end
local duty={showCharPos=function() normalOpens=normalOpens+1 end,initFightType=function() end}
package.loaded.ms={d_endlessFightUI=duty,d_charPositionUI=position,d_u=utility,d_data={},
 d_msg_def={gscl_msg_id={msg_query_lineup_info=1039}}}
local oldShow,oldInfo,oldMenu=duty.showCharPos,position.showOthersInfo,utility.createMenu
assert(loadstring(source))()
duty.showCharPos()
check('main duty button requests fresh server snapshot without opening editor',
 normalOpens==0 and #sent==1 and sent[1].mid==1039 and sent[1].data.flag==51 and
 sent[1].data.des_type==1 and sent[1].data.des_id==0 and sent[1].data.fight_id==0)
position.g_charPosUI={playerInfo={duty_preview=true},isReadOnly=false,usedCharacters={hp=115}}
check('module-local preview is read-only before native rendering',position.showOthersInfo(position.g_charPosUI.playerInfo)=='rendered' and position.g_charPosUI.isReadOnly)
check('comparison buttons cannot open unblessed ordinary cache',#menus==1 and menus[1].npic=='details.png' and menus.x==0 and menus.y==1)
check('shared menu builder restored',utility.createMenu==oldMenu)
for _,name in ipairs(guarded) do position[name]() end
check('all direct mutation and refresh callbacks blocked',changes==0 and position.g_charPosUI.usedCharacters.hp==115)
local wrapped=duty.showCharPos
assert(loadstring(source))()
check('repeated injection is idempotent',duty.showCharPos==wrapped)
local ok=pcall(position.showOthersInfo,{duty_preview=true,raise=true})
check('render errors restore shared UI function',not ok and utility.createMenu==oldMenu)
-- Native loadData replaces g_charPosUI on the next ordinary formation opening.
position.g_charPosUI={playerInfo={},isReadOnly=false,usedCharacters={hp=100}}
position.showOthersInfo(position.g_charPosUI.playerInfo)
for _,name in ipairs(guarded) do check('ordinary '..name..' preserved',position[name]()=='normal-change') end
check('leaving duty restores normal values and menus',#menus==3 and not position.g_charPosUI.isReadOnly and position.g_charPosUI.usedCharacters.hp==100)
duty._localDutyPreviewRestore()
check('all hooks restore cleanly',duty.showCharPos==oldShow and position.showOthersInfo==oldInfo and position.requestChangeChar==change)
check('patch never writes module state into global namespace',_G.g_charPosUI==nil and _G.showOthersInfo==nil)
return table.concat(checks,'\n')
