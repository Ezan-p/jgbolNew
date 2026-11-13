"""Donation response updates visible client state without adding rewards twice."""
import unittest
from pathlib import Path

try:
    from lupa.lua51 import LuaRuntime
except ImportError:
    LuaRuntime = None


@unittest.skipIf(LuaRuntime is None, 'requires lupa.lua51')
class GuildDonationClientTests(unittest.TestCase):
    def test_donation_balances_feedback_cached_members_and_replay(self):
        lua = LuaRuntime()
        lua.execute('''
            local tipsInfo={contrib=20,totalcontrib=120}
            local selfInfo={id=1,contrib=20,totalcontrib=120}
            local memberList={selfInfo,{id=2,contrib=50,totalcontrib=90}}
            calls=0;messages={}
            ms={d_worldTreeUI={},d_xianmengUI={},d_guildFightUI={},d_crossRealm={},
                d_mainUI={g_playerInfo={role_id=1,union_contrib=120,cur_union_contrib=20}},
                d_info={show=function(s) messages[#messages+1]=s end}}
            ms.d_xianmengUI.getServerResponse=function() return tipsInfo,selfInfo,memberList end
            native=function(data) calls=calls+1;tree=data;return 'refreshed' end
            ms.d_worldTreeUI.donateGoldSuccess=native
            package.loaded.ms=ms
        ''')
        source = Path('network_redirect/guild_client.lua').read_text()
        lua.execute(source)
        lua.execute('wrapped=ms.d_worldTreeUI.donateGoldSuccess')
        lua.execute(source)
        lua.execute('''
            assert(wrapped==ms.d_worldTreeUI.donateGoldSuccess)
            local response={contribution_gain=70,union_contrib=190,cur_union_contrib=90,
                            union_money=1070,donate_count=7}
            -- Model the normal 1032-before-1301 packet order.
            ms.d_mainUI.g_playerInfo.union_contrib=190
            ms.d_mainUI.g_playerInfo.cur_union_contrib=90
            for i=1,2 do
                assert(wrapped(response)=='refreshed')
                assert(ms.d_mainUI.g_playerInfo.union_contrib==190)
                assert(ms.d_mainUI.g_playerInfo.cur_union_contrib==90)
            end
            local tips,own,members=ms.d_xianmengUI.getServerResponse()
            assert(tips.contrib==90 and tips.totalcontrib==190)
            assert(own.contrib==90 and own.totalcontrib==190)
            assert(members[2].contrib==50 and members[2].totalcontrib==90)
            assert(calls==2 and tree.union_money==1070 and tree.donate_count==7)
            assert(messages[1]=='捐赠成功，获得贡献度：70')
            -- The donation reply also repairs an old client-side balance.
            ms.d_mainUI.g_playerInfo.union_contrib=120
            ms.d_mainUI.g_playerInfo.cur_union_contrib=20
            wrapped(response)
            assert(ms.d_mainUI.g_playerInfo.union_contrib==190)
            assert(ms.d_mainUI.g_playerInfo.cur_union_contrib==90)
            -- Older servers lack contribution fields: preserve their behavior.
            wrapped({union_money=1080,donate_count=8})
            assert(calls==4 and #messages==3)
            assert(ms.d_mainUI.g_playerInfo.cur_union_contrib==90)
            ms.d_worldTreeUI._localGuildDonationRestore()
            assert(ms.d_worldTreeUI.donateGoldSuccess==native)
        ''')
