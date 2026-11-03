local source=...
local received
local notices={}
local popups={}
local sent={}
CCDirector={sharedDirector=function() return {getRunningScene=function() return {} end} end}
local native=function(data) received=data end
local closeNative=function() return 'closed' end
local ui={getDateFormServer=native,closeRewardsPage=closeNative}
ui.get_promotion_time_bit=function(index) return math.floor((ui.g_rankInfo.promote_time or 0)/2^(index-2))%2 end
ui.get_promotion_prize_bit=function(index) return math.floor((ui.g_rankInfo.promote_prize or 0)/2^(index-2))%2 end
local ms={d_rankUI=ui,d_fightrecordUI={},d_fightUI={},
 d_commonLayerUI={showPrizeResLayer=function(parent,prizes) popups[#popups+1]=prizes end},
 d_msg_def={gscl_msg_id={msg_exchange_top_score=1203}},
 d_u={main_server_send_msg=function(mid,data) assert(mid==1203);sent[#sent+1]=data.exchange_type end},
 d_info={show=function(text) notices[#notices+1]=text end},
 d_data={callback_update_config=function() end},d_hz={gethz=function(key) return key end}}
package.loaded.ms=ms
assert(loadstring(source))()
assert(loadstring(source))()
ms.d_data.callback_update_config({local_rank={cortege_layers={[930001]=499,[930002]=299},score=0}})
ui.getDateFormServer({show_list={{id=930001,cortege_layer=255},{id=930002,cortege_layer=255},{id=930500,cortege_layer=0}}})
assert(received.show_list[1].cortege_layer==499)
assert(received.show_list[2].cortege_layer==299)
assert(received.show_list[3].cortege_layer==0)
-- Every board replaces the mapping; displaced opponents keep their identity.
ms.d_data.callback_update_config({local_rank={cortege_layers={[930003]=449},score=1}})
ui.getDateFormServer({show_list={{id=930003,cortege_layer=255},{id=930001,cortege_layer=42}}})
assert(received.show_list[1].cortege_layer==449 and received.show_list[2].cortege_layer==42)
assert(#notices==0)
ms.d_data.callback_update_config({local_rank_reset_notice=true})
assert(#notices==1 and notices[1]=='玩法更新，排名重置')
ms.d_data.callback_update_config({local_rank={score=2}})
assert(#notices==1)
ms.d_data.callback_update_config({local_rank_promotion_reset_notice=true})
assert(#notices==2 and notices[2]=='玩法更新，晋升奖励进度重置')
ms.d_data.callback_update_config({local_rank={promote_time=0,promote_prize=0}})
assert(#notices==2)
-- Ten rows map display positions to stable claim IDs, including the three new tiers.
local rows=ms.d_data.g_topScoreExchangeTable
local expected={{500,100,4},{400,200,11},{300,300,12},{200,500,13},{100,800,5},
 {50,1000,6},{30,1500,7},{20,2000,8},{10,5000,9},{1,10000,10}}
assert(#rows==12)
ui.g_rankInfo={promote_time=0,promote_prize=0}
for i,t in ipairs(expected) do
 local index=i+2;local row=rows[index]
 assert(row.promoteOrder==t[1] and row.count==t[2] and row.exchangeIndex==t[3])
 assert(row.object_type==11 and row.sub_type==1)
 ui.g_rankInfo.promote_time=2^(t[3]-2);ui.g_rankInfo.promote_prize=0
 assert(ui.get_promotion_time_bit(index)==1)
 ui.chargeButtonCallBack(index);assert(sent[#sent]==t[3])
 local count=#sent;ui.g_rankInfo.promote_prize=2^(t[3]-2)
 ui.chargeButtonCallBack(index);assert(#sent==count)
end
-- Bonus presentation follows the five-card page, with no duplicate popup on replay/retry.
local prizes={{object_type=5,attach_type=1152,attach_count=2,attach_level=1}}
local payload={local_rank_battle_bonus={fight_id=123,prizes=prizes}}
ms.d_data.callback_update_config(payload)
assert(#popups==0)
assert(ui.closeRewardsPage()=='closed' and #popups==1 and popups[1]==prizes)
ms.d_data.callback_update_config(payload);ui.closeRewardsPage();assert(#popups==1)
ms.d_data.callback_update_config({local_rank_battle_bonus={fight_id=124,prizes=prizes}})
ms.d_data.callback_update_config({local_rank_battle_bonus={fight_id=125,prizes={}}})
ui.closeRewardsPage();assert(#popups==1)
ms.d_data.callback_update_config({local_rank_battle_bonus={fight_id=126,prizes=prizes}})
ui.closeRewardsPage();assert(#popups==2)
ui._localRankRestore()
assert(ui.getDateFormServer==native and ui.closeRewardsPage==closeNative)
return 'rank 500 ascension, reset, ten promotions and bonus display regression passed'
