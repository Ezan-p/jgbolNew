"""Native portrait and market callbacks with isolated state and intercepted sends."""
import json
from pathlib import Path
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis/tools')]
from network_redirect import market, summon
from network_redirect.backend import Backend, login_fields
from android_emulator.config import load_config
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR


def main():
    import frida
    with tempfile.TemporaryDirectory() as tmp:
        b = Backend(Path(tmp), 18770, lambda *a, **k: None)
        goods = market.catalog(b.profile(), int(time.time()), b.market_rules)
        b.close()
    source = r'''
local ms=assert(package.loaded.ms)
local ui,shop,sales=ms.d_runeUI,ms.d_shopUI,ms.d_salesUI
local function snapshot(t) local r={};for k,v in pairs(t) do r[k]=v end;return r end
local function restore(t,r)
 for k in pairs(t) do if r[k]==nil then t[k]=nil end end
 for k,v in pairs(r) do t[k]=v end
end
local u0,s0,a0=snapshot(ui),snapshot(shop),snapshot(sales)
local saved={player=ms.d_mainUI.g_playerInfo,config=ms.d_data.g_new_config,
 send=ms.d_u.main_server_send_msg,menu=ms.d_u.createMenu,
 confirm=ms.d_quitUI.createYesNoByStyle,info=ms.d_info.show,
 needGold=ms.d_summonUI.needGold,hz=ms.d_hz.gethz}
local parent=CCNode:create();parent:retain()
local checks={};local sent={};local change,freePrompt
local function check(ok,name) assert(ok,name);checks[#checks+1]=name end
local function up(fn,key)
 for i=1,40 do local n,v=debug.getupvalue(fn,i);if not n then break end;if n==key then return v end end
end
local ok,err=xpcall(function()
 ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
 ms.d_data.g_new_config=ms.d_c.table_copy(saved.config)
 ui.g_self=ms.d_c.table_copy(u0.g_self)
 shop.g_self=ms.d_c.table_copy(s0.g_self)
 sales.g_self=ms.d_c.table_copy(a0.g_self)
 local player=ms.d_mainUI.g_playerInfo
 player.head_type=101;player.gold_coin=0;player.strength_item_count=0
 ms.d_u.main_server_send_msg=function(mid,data) sent[#sent+1]={mid=mid,data=data} end
 ms.d_info.show=function() end
 ms.d_summonUI.needGold=function() end
 ms.d_u.createMenu=function(style,...)
  if style[2] and style[2].npic=='v2/namingUI/change1.png' then change=style[2].call_back end
  return saved.menu(style,...)
 end
 ms.d_quitUI.createYesNoByStyle=function(layer,style,yes)
  freePrompt=style.string;yes()
 end
 assert(loadstring(__PROFILE__))()
 ms.d_data.g_new_config.local_profile={head_free_available=true}
 ui.showChangeUserHead(parent,10,9811,true);ui.g_head_type=102
 assert(change)()
 check(freePrompt and freePrompt:find('免费',1,true),'native_free_confirmation')
 check(#sent==1 and sent[1].mid==1069 and sent[1].data.flag==0
  and sent[1].data.head_type==102,'zero_gold_free_change_sends_request')
 parent:removeAllChildrenWithCleanup(true)
 ms.d_data.g_new_config.local_profile={head_free_available=false}
 ui.showChangeUserHead(parent,10,9812,true);ui.g_head_type=102
 local yes=assert(up(change,'changeUserHeadYes'))
 yes();check(#sent==1,'used_free_chance_enforces_paid_balance')
 player.gold_coin=200;yes()
 check(#sent==2 and sent[2].mid==1069 and sent[2].data.flag==1,'paid_change_sends_paid_flag')
 if shop._localMarketBunRestore then shop._localMarketBunRestore() end
 assert(loadstring(__MARKET__))()
 shop.loadGoods(__GOODS__)
 local bun
 for _,g in ipairs(shop.g_self.Goods[1]) do if g.buyInfo.type_id==1022 then bun=g end end
 check(bun and bun.csvInfo and bun.buyInfo.count==1 and bun.buyInfo.origin_price==20
  and bun.buyInfo.buy_price==5 and bun.buyInfo.buy_limit_times==10,'native_catalog_discount_bun')
 player.gold_coin=5;shop.buyShopItem(bun,1)
 check(#sent==3 and sent[3].mid==1057 and sent[3].data.index==24 and sent[3].data.count==1
  and sent[3].data.page_id==1,'bun_buy_independent_of_quick_use_counter')
 check(player.strength_item_count==0,'quick_use_counter_unchanged')
 bun.buyInfo.buy_limit_times=0;shop.buyShopItem(bun,1)
 check(#sent==3,'sold_out_bun_cannot_send')
 bun.buyInfo.buy_limit_times=10;player.gold_coin=4;shop.buyShopItem(bun,1)
 check(#sent==3,'bun_buy_checks_five_gold_balance')
 local regular
 for _,g in ipairs(shop.g_self.Goods[2]) do if g.buyInfo.type_id==1022 then regular=g end end
 check(regular and regular.buyInfo.index==25 and regular.buyInfo.buy_price==20
  and regular.buyInfo.count==1 and regular.buyInfo.is_day_limit==0,'native_regular_bun_catalog')
 player.gold_coin=60;shop.buyShopItem(regular,2,3)
 check(#sent==4 and sent[4].mid==1057 and sent[4].data.index==25
  and sent[4].data.page_id==2 and sent[4].data.count==3,'regular_buns_batch_request')
 player.gold_coin=59;shop.buyShopItem(regular,2,3)
 check(#sent==4,'regular_buns_batch_checks_total_price')
 check(player.strength_item_count==0,'regular_buns_do_not_use_quick_use_quota')
end,debug.traceback)
parent:removeAllChildrenWithCleanup(true);parent:release()
restore(ui,u0);restore(shop,s0);restore(sales,a0)
ms.d_mainUI.g_playerInfo=saved.player;ms.d_data.g_new_config=saved.config
ms.d_u.main_server_send_msg=saved.send;ms.d_u.createMenu=saved.menu
ms.d_quitUI.createYesNoByStyle=saved.confirm;ms.d_info.show=saved.info
ms.d_summonUI.needGold=saved.needGold;ms.d_hz.gethz=saved.hz
return table.tostring({passed=ok,error=not ok and tostring(err) or nil,
 checks=checks,live_account_resources_changed=false,restored=true})
'''.replace('__PROFILE__', summon.lua((ROOT / 'network_redirect/profile_client.lua').read_text()))
    source = source.replace('__MARKET__', summon.lua((ROOT / 'network_redirect/market_client.lua').read_text()))
    source = source.replace('__GOODS__', summon.lua(goods))
    config = load_config(ROOT / 'game.json')
    pid = next(p for p, n in processes(config).items() if n == config['package'])
    session = frida.get_device(config['serial'], timeout=10).attach(pid)
    script = session.create_script(LUA_EVALUATOR)
    try:
        script.load()
        result = script.exports_sync.evaluate(source)
        assert result.get('status') == 0, result
        report = login_fields(result['result'])
    finally:
        script.unload()
        session.detach()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    (ROOT / 'analysis/evidence/profile_market_client_validation.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    assert report['passed'], report


if __name__ == '__main__':
    main()
