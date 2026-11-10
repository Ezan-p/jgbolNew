"""Real Lua 5.1 execution of display clock sync, pause and module reload."""
from pathlib import Path
import unittest
try:
    from lupa.lua51 import LuaRuntime
except ImportError:
    LuaRuntime = None
from network_redirect import summon


@unittest.skipIf(LuaRuntime is None, 'requires lupa.lua51')
class ClientClockTests(unittest.TestCase):
    def setUp(self):
        self.lua = LuaRuntime()
        self.source = Path('network_redirect/game_clock_client.lua').read_text()
        self.lua.execute('''
         seconds=100;wall=1000;requests=0;beats=0;lifecalls=0
         realTime=os.time
         os.time=function(fields) if fields then return realTime(fields) end;return wall end
         _jgbolContinuousTime=function()return seconds,nanos end
         t={g_self={server_time=1000}}
         t.setTime=function(value) t.g_self.server_time=value;t.g_self.time_interval=wall-value end
         t.getTime=function()return wall-(t.g_self.time_interval or 0)end
         oldSet=t.setTime;oldGet=t.getTime
         event={g_msg_fun={},g_has_inside_game=true}
         event.msg_keep_alive_2999=function(head,data)beats=beats+1;return 'beat-result'end
         event.event_client_info_20=function(head,data)lifecalls=lifecalls+1;return 'life-result'end
         event.g_msg_fun[2999]=event.msg_keep_alive_2999
         event.g_msg_fun[20]=event.event_client_info_20
         package.loaded.ms={d_time=t,d_event_mgr=event,d_net={g_self={delay_time=7},sendHeartBeat=function()requests=requests+1;sentDelay=package.loaded.ms.d_net.g_self.delay_time end}}
        ''')
        self.assertEqual(self.lua.execute(self.source), 'ready')

    def test_display_uses_elapsed_and_ignores_forward_backward_wall_changes(self):
        self.lua.execute('''
         t.setTime(5000);seconds=110;wall=99999999;assert(t.getTime()==5010)
         wall=1;seconds=111;assert(t.getTime()==5011)
         assert(t.g_self.server_time==5000)
        ''')

    def test_heartbeat_resyncs_time_and_preserves_native_callback(self):
        self.lua.execute('''
         seconds=120
         assert(event.g_msg_fun[2999]({}, {time=3000})=='beat-result')
         assert(beats==1 and t.getTime()==3000 and t.g_self.server_time==3000)
         seconds=121;assert(t.getTime()==3001)
        ''')

    def test_native_integer_pair_preserves_subsecond_anchor(self):
        self.lua.execute('''
         seconds=100;nanos=900000000;t.setTime(5000)
         seconds=101;nanos=100000000;assert(t.getTime()==5000)
         nanos=900000000;assert(t.getTime()==5001)
        ''')

    def test_resume_freezes_until_heartbeat_and_requests_sync(self):
        self.lua.execute('''
         seconds=105;assert(event.g_msg_fun[20]({}, {type=201})=='life-result')
         seconds=28905;wall=999999
         assert(t.getTime()==1005)
         event.g_msg_fun[20]({}, {type=202})
         assert(requests==1 and lifecalls==2 and t.getTime()==1005)
         assert(sentDelay==2147483646 and package.loaded.ms.d_net.g_self.delay_time==7)
         event.g_msg_fun[2999]({}, {time=29805})
         assert(t.getTime()==29805)
         seconds=28906;assert(t.getTime()==29806)
         event.g_has_inside_game=false
         event.g_msg_fun[20]({}, {type=202});assert(requests==1)
        ''')

    def test_frozen_vm_elapsed_uses_server_decision_after_resume(self):
        self.lua.execute('''
         event.g_msg_fun[20]({}, {type=201});wall=wall+28800
         event.g_msg_fun[20]({}, {type=202});assert(t.getTime()==1000)
         event.g_msg_fun[2999]({}, {time=1000});assert(t.getTime()==1000)
         seconds=101;assert(t.getTime()==1001)
        ''')

    def test_missing_or_reset_source_never_uses_wall_fallback(self):
        self.lua.execute('''
         seconds=105;assert(t.getTime()==1005)
         seconds=nil;wall=99999999;assert(t.getTime()==1005)
         seconds=1;assert(t.getTime()==1005)
         t.setTime(2000);seconds=2;assert(t.getTime()==2001)
        ''')

    def test_idempotency_restore_and_reload(self):
        self.lua.execute('wrapped=t.getTime;beat=event.g_msg_fun[2999]')
        self.assertEqual(self.lua.execute(self.source), 'ready')
        self.lua.execute('assert(t.getTime==wrapped and event.g_msg_fun[2999]==beat)')
        self.lua.execute('t._localGameClockRestore();assert(t.getTime==oldGet and t.setTime==oldSet)')
        self.assertEqual(self.lua.execute(self.source), 'ready')
        self.lua.execute('''
         previous=t
         t={g_self={server_time=8000},setTime=oldSet,getTime=oldGet}
         package.loaded.ms.d_time=t
         assert(previous._localGameClockCurrent()=='pending')
        ''')
        self.assertEqual(self.lua.execute(self.source), 'ready')
        self.lua.execute('assert(t.getTime()==8000)')

    def test_resume_collects_async_result_once_and_cancels_stale_callback(self):
        self.lua.execute("""
         local ms=package.loaded.ms
         ms.d_u={delay_node=function(seconds,fn) assert(seconds==6);callback=fn end}
         event.g_msg_fun[20]({}, {type=202})
         assert(requests==1 and sentDelay==2147483646)
         callback();assert(requests==2 and sentDelay==7)
         event.g_msg_fun[20]({}, {type=202});assert(requests==3)
         local stale=callback
         event.g_msg_fun[20]({}, {type=201});stale();assert(requests==3)
         event.g_msg_fun[20]({}, {type=202});assert(requests==4)
         t._localGameClockRestore();callback();assert(requests==4)
        """)

    def test_beijing_labels_ignore_device_timezone(self):
        import os
        import time
        from unittest.mock import patch
        try:
            for zone in ('UTC', 'Asia/Shanghai', 'America/Los_Angeles'):
                with self.subTest(zone=zone), patch.dict(os.environ, {'TZ': zone}):
                    time.tzset()
                    self.lua.execute("""
                     t.setTime(1794153600)
                     assert(t.getHour()==0 and t.getMin()==0)
                     assert(t.getWeekIndex()=='1' and not t.is_weekend())
                     assert(t.getWeekIndex(1794153599)=='7')
                     assert(os.date('%Y-%m-%d %H:%M',t.getShowTime())=='2026-11-09 00:00')
                    """)
        finally:
            time.tzset()

    def test_generated_payload_contains_clock_and_compiles(self):
        source = summon.client_source(summon.load_rules())
        self.assertIn(self.source, source)
        self.lua.globals().source = source
        self.lua.execute('assert(loadstring(source))')
