"""Exercise timing and wait adapters together with old LuaSocket loaders."""
import unittest
from pathlib import Path

import network_redirect
from tests.test_request_wait import FIXTURE, LuaRuntime


@unittest.skipIf(LuaRuntime is None, 'requires lupa.lua51')
class RequestTimingClientTests(unittest.TestCase):
    def install(self, loader):
        runtime = LuaRuntime()
        runtime.execute(FIXTURE)
        runtime.execute("logs={};print=function(s) logs[#logs+1]=s end\n"
                        "package.loaded.socket=nil;package.preload.socket=function() "
                        + loader + " end")
        source = Path(network_redirect.__file__).with_name('request_timing_client.lua').read_text()
        runtime.execute(source)
        runtime.execute(source)  # Injection retries must not wrap handlers twice.
        runtime.execute(Path(network_redirect.__file__).with_name('request_wait_client.lua').read_text())
        runtime.execute('''request();assert(#sent==1);ack(101)
            assert(ms._localRequestTiming and ms._localRequestWait.state()=='idle')
            assert(not u.g_sys_busy and not u.g_is_waiting_1106)
            assert(u.g_client_req_serial_num==102 and next(tasks)==nil)
            local installs,acks=0,0
            for _,line in ipairs(logs) do
                if string.find(line,'request_timing.*stage=installed') then installs=installs+1 end
                if string.find(line,'request_timing.*stage=ack') then acks=acks+1 end
            end
            assert(installs==1 and acks==1)''')
        return runtime

    def test_legacy_loaders_fall_back_without_aborting_remaining_patches(self):
        for loader in ('return true', 'return false', 'return nil', 'return 1',
                       "return 'socket'", 'return {}', "error('module unavailable')"):
            with self.subTest(loader=loader):
                runtime = self.install(loader)
                self.assertIn('clock=wall_seconds', runtime.globals().logs[1])

    def test_luasocket_gettime_keeps_precise_timing(self):
        runtime = self.install('return {gettime=function() return 123.25 end}')
        self.assertIn('clock=socket_wall', runtime.globals().logs[1])
