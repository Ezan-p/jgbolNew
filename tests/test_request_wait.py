"""Lua 5.1 tests: deterministic scheduler, real installed wrappers."""
import unittest
from pathlib import Path
try:
    from lupa.lua51 import LuaRuntime
except ImportError:
    LuaRuntime = None

FIXTURE = r'''
print=function() end
sent={};notices={};shown=0;stopped=0;tasks={};nextTask=0
scheduler={scheduleScriptFunc=function(self,fn) nextTask=nextTask+1;tasks[nextTask]=fn;return nextTask end,
 unscheduleScriptEntry=function(self,id) tasks[id]=nil end}
CCDirector={sharedDirector=function() return {getScheduler=function() return scheduler end} end}
function advance(dt) local batch={};for id,fn in pairs(tasks) do batch[id]=fn end
 for id,fn in pairs(batch) do if tasks[id] then fn(dt) end end end
u={g_client_req_serial_num=101,g_server_ret_serial_num=200010,g_is_waiting_1106=false}
a={start_wait=function(_,duration,timeout) shown=shown+1;u.g_sys_busy=true end,
 stop_wait=function() stopped=stopped+1;u.g_sys_busy=false end}
main_server={send_msg=function(mid,data)
 if sendError then error('socket failed') end
 local row={mid=mid};for k,v in pairs(data) do row[k]=v end;sent[#sent+1]=row
end}
u.main_server_send_msg=function(mid,data,wait)
 data.serial_num=(wait and wait<=0) and 0 or u.g_client_req_serial_num
 if wait==nil or wait>0 then a.start_wait(nil,10);u.g_is_waiting_1106=true end
 return main_server.send_msg(mid,data)
end
u.tryRetranReq=function() u.main_server_send_msg(1105,{req_serial_num=u.g_server_ret_serial_num}) end
u.packageTimeOut=function() error('native timeout must be intercepted') end
e={g_net_package_list={}}
e.msg_process_done_1106=function(head,data)
 if doneError then error('done failed') end
 u.g_client_req_serial_num=u.g_client_req_serial_num+1
 a.stop_wait(true);u.g_is_waiting_1106=false
 if drainError then e.g_msg_fun[1032]({}, {}) end
end
e.g_msg_fun={[1106]=e.msg_process_done_1106,[1032]=function() error('UI callback failed') end,
 [2996]=function() u.tryRetranReq() end,[1002]=function() end,
 [1017]=function() u.g_is_waiting_1106=false end}
ms={d_u=u,d_alert=a,d_event_mgr=e,d_info={show=function(s) notices[#notices+1]=s end},
 d_data={callback_update_config=function() end}}
package.loaded.ms=ms
function request() u.main_server_send_msg(1353,{id=4,data='{index=1}'}) end
function ack(n) e.g_msg_fun[1106]({}, {req_serial_num=n}) end
'''


@unittest.skipIf(LuaRuntime is None, 'requires lupa.lua51')
class RequestWaitTests(unittest.TestCase):
    def setUp(self):
        self.lua = LuaRuntime()
        self.lua.execute(FIXTURE)
        self.lua.execute(Path('network_redirect/request_wait_client.lua').read_text())

    def test_fast_request_no_spinner_and_immediate_duplicate_guard(self):
        self.lua.execute('''request();request();assert(#sent==1 and u.g_sys_busy)
        advance(0.15);assert(shown==0);ack(101);advance(1)
        assert(shown==0 and not u.g_is_waiting_1106 and not u.g_sys_busy)
        assert(ms._localRequestWait.state()=='idle' and next(tasks)==nil)''')

    def test_delayed_spinner_and_slow_status(self):
        self.lua.execute('''request();advance(0.19);assert(shown==0)
        advance(0.02);assert(shown==1);advance(3);assert(#notices>0)
        ack(101);assert(not u.g_sys_busy)''')

    def test_timeout_replays_first_then_retry_keeps_original_identity(self):
        self.lua.execute('''request();advance(10)
        assert(sent[2].mid==1105 and ms._localRequestWait.state()=='recovering')
        advance(10);assert(ms._localRequestWait.state()=='uncertain' and not u.g_sys_busy)
        u.g_client_req_serial_num=999
        u.main_server_send_msg(1353,{id=4,data='{index=2}'})
        assert(#sent==2)
        request();assert(#sent==3 and sent[3].serial_num==101 and sent[3].data=='{index=1}')
        ack(101);assert(ms._localRequestWait.state()=='idle')''')

    def test_stale_and_zero_ack_never_complete_an_unconfirmed_request(self):
        self.lua.execute('''request();ack(99);assert(ms._localRequestWait.state()=='waiting')
        ack(0);assert(ms._localRequestWait.state()=='uncertain')
        assert(u.g_client_req_serial_num==101);ack(101)
        assert(u.g_client_req_serial_num==102);ack(101);assert(u.g_client_req_serial_num==102)''')

    def test_done_exception_releases_wait_and_advances_only_once(self):
        self.lua.execute('''request();e.g_net_package_list={1,2};doneError=true;ack(101)
        assert(#e.g_net_package_list==0)
        assert(not u.g_is_waiting_1106 and not u.g_sys_busy)
        assert(ms._localRequestWait.state()=='idle' and u.g_client_req_serial_num==102)
        ack(101);assert(u.g_client_req_serial_num==102)''')

    def test_dispatch_exception_during_ack_is_visible_and_does_not_retry(self):
        self.lua.execute('''request();drainError=true;ack(101)
        assert(#notices>0 and #sent==1 and not u.g_sys_busy)
        assert(ms._localRequestWait.state()=='idle')''')

    def test_cache_reset_clears_partial_queue_and_preserves_sequence_floor(self):
        self.lua.execute('''request();e.g_net_package_list={1,2}
        ms.d_data.callback_update_config({local_request_reset={server_serial=200999,next_request_serial=150}})
        assert(#e.g_net_package_list==0 and u.g_server_ret_serial_num==200999)
        assert(u.g_client_req_serial_num==150 and ms._localRequestWait.state()=='idle')
        assert(not u.g_sys_busy and next(tasks)==nil)''')

    def test_reconnect_failure_and_fresh_login_never_auto_resend(self):
        self.lua.execute('''request();e.g_msg_fun[2996]({}, {ret=1})
        assert(ms._localRequestWait.state()=='uncertain' and #sent==1)
        e.g_msg_fun[1002]({}, {result=0});assert(ms._localRequestWait.state()=='idle')
        assert(#sent==1)''')

    def test_reconnect_success_requests_history_without_replacing_pending(self):
        self.lua.execute('''request();e.g_msg_fun[2996]({}, {ret=0})
        assert(sent[2].mid==1105 and ms._localRequestWait.state()=='recovering')
        e.g_msg_fun[1017]({}, {reconnect=true});assert(u.g_is_waiting_1106)
        ack(101);assert(ms._localRequestWait.state()=='idle')''')

    def test_send_exception_keeps_uncertain_intent_and_stops_spinner(self):
        self.lua.execute('''sendError=true;request();advance(1)
        assert(ms._localRequestWait.state()=='uncertain' and not u.g_sys_busy)
        sendError=false;request();assert(sent[1].serial_num==101)''')

    def test_idle_reconnect_ack_drains_queued_updates_without_consuming_sequence(self):
        self.lua.execute("""e.handleSavedPackages=function() drained=true end
        ack(0);assert(drained and u.g_client_req_serial_num==101)
        assert(not u.g_is_waiting_1106 and not u.g_sys_busy)""")

    def test_retry_uses_frozen_payload_even_when_caller_mutates_its_table(self):
        self.lua.execute("""local data={id=4,data='{index=1}'}
        u.main_server_send_msg(1353,data);data.data='{index=999}'
        advance(10);advance(10);request()
        assert(sent[3].serial_num==101 and sent[3].data=='{index=1}')""")

    def test_failed_fresh_login_does_not_report_success_or_auto_retry(self):
        self.lua.execute("""request();e.g_msg_fun[1002]({}, {result=1})
        assert(ms._localRequestWait.state()=='uncertain' and #sent==1 and not u.g_sys_busy)""")
