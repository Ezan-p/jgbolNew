"""Real Lua 5.1 resource scheduling with deterministic native cache stand-ins."""
import copy
import json
import re
import unittest
from pathlib import Path

from network_redirect import resource_preload, summon
from tests.test_request_wait import LuaRuntime

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'network_redirect/resource_preload_client.lua'
FIXTURE = r'''
cpu=0; jobCost=0; loads={}; calls={}; reads={}; tasks={}; textures={}; logs={}; nextTimer=0
freeMemory=80; showCount=0; loginCount=0; clearCount=0; sendCount=0
print=function(s) logs[#logs+1]=s end
os.clock=function() return cpu end
function cost(name) loads[#loads+1]=name;cpu=cpu+jobCost end
scheduler={scheduleScriptFunc=function(self,fn,interval,paused)
 assert(interval>0 and not paused);nextTimer=nextTimer+1;tasks[nextTimer]=fn;return nextTimer end,
 unscheduleScriptEntry=function(self,id) tasks[id]=nil end}
CCDirector={sharedDirector=function() return {getScheduler=function() return scheduler end} end}
cache={textureForKey=function(self,path) return textures[path] end,
 addImage=function(self,path)
  cost(path)
  if path==failTexture then return nil end
  local texture={refs=1,getPixelsWide=function() return actualWidth or 64 end,
   getPixelsHigh=function() return actualHeight or 64 end,
   retain=function(self) self.refs=self.refs+1 end,
   release=function(self) self.refs=self.refs-1;assert(self.refs>=0) end}
  textures[path]=texture;return texture
 end,
 removeAllTextures=function(self) for name,texture in pairs(textures) do
  texture:release();textures[name]=nil end end,
 removeUnusedTextures=function(self) for name,texture in pairs(textures) do
  if texture.refs==1 then texture:release();textures[name]=nil end end end}
CCTextureCache={sharedTextureCache=function() return cache end}
main_server={get_free_mem_rate=function() return freeMemory end,
 send_msg=function() sendCount=sendCount+1;error('prewarm must not send gameplay') end}
function makeModules()
 local main={g_currentBoard=0,boardID={none=0},g_isNeedGuide=false}
 local login={g_currentSence=1,senceID={login=1,mainUI=2}}
 local u={g_sys_busy=false,g_is_waiting_1106=false,
  removeAllCache=function() clearCount=clearCount+1;cache:removeAllTextures();return 'cleared' end}
 main.show=function(...)
  showCount=showCount+1;atShow=#loads;showArgs={n=select('#',...),...}
  main.g_mainUI={main_scene={}};login.g_currentSence=2
  return 'shown',nil,7
 end
 login.show=function() loginCount=loginCount+1;login.g_currentSence=1;main.g_mainUI=nil;return 'login' end
 local ms={d_mainUI=main,d_loginUI=login,d_u=u,d_guideUI={},d_data={},d_packageUI={},d_lineupUI={}}
 for _,jobs in ipairs({PLAN.core,PLAN.warm}) do for _,job in ipairs(jobs) do
  if job.kind=='config' then
   local module,key=ms[job.module],job.getter
   module[key]=function()
    calls[key]=(calls[key] or 0)+1
    if module[job.cache_fields[1]] then return module[job.cache_fields[1]] end
    cost(key);reads[key]=(reads[key] or 0)+1
    for _,field in ipairs(job.cache_fields) do module[field]={ready=true} end
    if key==failGetter then error('partial parse') end
    return module[job.cache_fields[1]]
   end
  end
 end end
 package.loaded.ms=ms
 return ms
end
ms=makeModules()
function step(dt)
 local batch={};for id,fn in pairs(tasks) do batch[id]=fn end
 for id,fn in pairs(batch) do if tasks[id] then fn(dt or PLAN.warm_interval_seconds) end end
end
function finish() for n=1,2000 do if next(tasks)==nil then return end;step() end;error('timer leaked') end
'''


def small_plan():
    plan = resource_preload.load_plan()
    configs = [j for j in plan['core'] if j['kind'] == 'config']
    textures = [j for j in plan['core'] if j['kind'] == 'texture']
    plan['core'] = [configs[0], textures[0], textures[1]]
    plan['warm'] = [configs[1], textures[2], textures[3]]
    return plan


@unittest.skipIf(LuaRuntime is None, 'requires lupa.lua51')
class ResourcePreloadClientTests(unittest.TestCase):
    def runtime(self, plan=None):
        lua = LuaRuntime()
        lua.execute('PLAN=' + summon.lua(plan or small_plan()))
        lua.execute(FIXTURE)
        return lua

    def install(self, lua):
        lua.execute(SOURCE.read_text().replace('__RESOURCE_PRELOAD_PLAN__', 'PLAN'))

    def test_core_before_main_and_warm_after_idle_delay(self):
        lua = self.runtime()
        self.install(lua)
        lua.execute('''assert(#loads==0)
        local a,b,c=ms.d_mainUI.show('a',nil,'b')
        assert(a=='shown' and b==nil and c==7 and showArgs.n==3 and showArgs[3]=='b')
        assert(atShow==#PLAN.core and _localResourcePreload.phase=='warm')
        for n=1,10 do step() end;assert(#loads==#PLAN.core)
        finish();assert(#loads==#PLAN.core+#PLAN.warm and next(tasks)==nil)
        assert(_localResourcePreload.phase=='done' and sendCount==0)''')

    def test_startup_runs_one_task_per_tick_and_native_getter_hits_cache(self):
        lua = self.runtime()
        self.install(lua)
        lua.execute('''step();assert(#loads==1);step();assert(#loads==2)
        step();assert(#loads==3);step();assert(#loads==3)
        local job=PLAN.core[1];ms[job.module][job.getter]()
        assert(reads[job.getter]==1 and calls[job.getter]==2)
        ms.d_mainUI.show();finish();assert(sendCount==0)''')

    def test_core_slice_has_work_and_time_limits_and_keeps_remaining_jobs(self):
        plan = small_plan()
        plan['startup_slice_seconds'] = .1
        plan['startup_max_jobs'] = 1
        lua = self.runtime(plan)
        self.install(lua)
        lua.execute('ms.d_mainUI.show();assert(atShow==1);finish();assert(#loads==6)')
        plan['startup_max_jobs'] = 32
        lua = self.runtime(plan)
        self.install(lua)
        lua.execute('jobCost=.2;ms.d_mainUI.show();assert(atShow==1);jobCost=0;finish();assert(#loads==6)')

    def test_busy_board_battle_and_guide_pause_without_bursts(self):
        for flag, reset in [('ms.d_u.g_sys_busy=true','ms.d_u.g_sys_busy=false'),
                            ('ms.d_u.g_is_waiting_1106=true','ms.d_u.g_is_waiting_1106=false'),
                            ('ms.d_mainUI.g_currentBoard=9','ms.d_mainUI.g_currentBoard=0'),
                            ('ms.d_loginUI.g_currentSence=3','ms.d_loginUI.g_currentSence=2'),
                            ('ms.d_mainUI.g_isNeedGuide=true','ms.d_mainUI.g_isNeedGuide=false'),
                            ('ms.d_guideUI.g_isPlayingMoving=true','ms.d_guideUI.g_isPlayingMoving=false')]:
            with self.subTest(flag=flag):
                lua = self.runtime()
                self.install(lua)
                lua.execute('ms.d_mainUI.show();'+flag+';for n=1,30 do step() end;assert(#loads==3);'+reset+';finish();assert(#loads==6)')

    def test_long_frame_and_slow_resource_cooldown(self):
        lua = self.runtime()
        self.install(lua)
        lua.execute('''ms.d_mainUI.show();for n=1,18 do step() end
        local before=#loads;step(5);assert(#loads==before)
        step();step();assert(#loads==before)
        for n=1,5 do step() end
        jobCost=.02;local old=#loads;step();step();assert(#loads<=old+1)
        jobCost=0;finish()''')

    def test_pins_survive_unused_cleanup_and_explicit_cleanup_releases_them(self):
        lua = self.runtime()
        self.install(lua)
        lua.execute('''ms.d_mainUI.show();finish()
        held={};for path,t in pairs(textures) do held[#held+1]=t;assert(t.refs==2) end
        cache:removeUnusedTextures();assert(next(textures)~=nil)
        assert(ms.d_u.removeAllCache()=='cleared');assert(clearCount==1)
        assert(next(textures)==nil and _localResourcePreload.retained_bytes==0)
        for _,t in ipairs(held) do assert(t.refs==0) end
        ms.d_mainUI.show();step();assert(next(textures)==nil)''')

    def test_pressure_during_warmup_releases_pins_and_skips_remaining_images(self):
        lua = self.runtime()
        self.install(lua)
        lua.execute('''ms.d_mainUI.show();assert(_localResourcePreload.retained_bytes>0)
        freeMemory=20;step();assert(_localResourcePreload.retained_bytes==0)
        cache:removeUnusedTextures();assert(next(textures)==nil)
        finish();assert(reads[PLAN.warm[1].getter]==1)
        assert(_localResourcePreload.skipped==2 and sendCount==0)''')

    def test_retained_budget_and_existing_cache_avoid_duplicate_decodes(self):
        plan = small_plan()
        plan['retained_texture_bytes'] = plan['core'][1]['estimated_bytes']
        lua = self.runtime(plan)
        self.install(lua)
        lua.execute('''cache:addImage(PLAN.core[2].path);local before=#loads
        ms.d_mainUI.show();finish();assert(#loads==before+2)
        assert(_localResourcePreload.retained_bytes<=PLAN.retained_texture_bytes)''')

    def test_one_broken_job_restores_partial_cache_and_other_jobs_continue(self):
        lua = self.runtime()
        self.install(lua)
        lua.execute('''failGetter=PLAN.core[1].getter;failTexture=PLAN.core[2].path
        ms.d_mainUI.show();finish();assert(showCount==1 and _localResourcePreload.failed==2)
        local job=PLAN.core[1]
        for _,key in ipairs(job.cache_fields) do assert(ms[job.module][key]==nil) end
        failGetter=nil;ms[job.module][job.getter]();assert(reads[job.getter]==2)
        assert(_localResourcePreload.phase=='done')''')

    def test_reinstall_logout_and_restore_do_not_leak_callbacks_or_retains(self):
        lua = self.runtime()
        lua.execute('nativeShow=ms.d_mainUI.show;nativeLogin=ms.d_loginUI.show;nativeClear=ms.d_u.removeAllCache')
        self.install(lua)
        lua.execute('wrapped=ms.d_mainUI.show;ms.d_mainUI.show();finish();held={};for _,t in pairs(textures) do held[#held+1]=t end')
        self.install(lua)
        lua.execute('''assert(wrapped==ms.d_mainUI.show and next(tasks)==nil)
        assert(ms.d_loginUI.show()=='login');for _,t in ipairs(held) do assert(t.refs==1) end
        ms.d_mainUI.show();finish();assert(sendCount==0)
        _localResourcePreload.restore();assert(next(tasks)==nil and _localResourcePreload==nil)
        assert(ms.d_mainUI.show==nativeShow and ms.d_loginUI.show==nativeLogin and ms.d_u.removeAllCache==nativeClear)
        for _,t in pairs(textures) do assert(t.refs==1) end''')

    def test_reloaded_modules_and_replaced_show_are_rebound(self):
        for replacement in ('ms=makeModules()', 'ms.d_mainUI.show=function() showCount=showCount+1 end'):
            with self.subTest(replacement=replacement):
                lua = self.runtime()
                self.install(lua)
                lua.execute('oldState=_localResourcePreload;step();'+replacement)
                self.install(lua)
                lua.execute('assert(oldState.phase=="restored" and _localResourcePreload.current());_localResourcePreload.restore();assert(next(tasks)==nil)')

    def test_expired_login_session_can_warm_when_main_finally_opens(self):
        lua = self.runtime()
        self.install(lua)
        lua.execute('''step(PLAN.max_warm_seconds+1);assert(next(tasks)==nil)
        ms.d_mainUI.show();finish();assert(_localResourcePreload.phase=='done')''')

    def test_missing_native_api_or_scheduler_failure_does_not_block_other_patches(self):
        for setup in ('CCDirector=nil', 'scheduler.scheduleScriptFunc=function() error("unavailable") end',
                      'ms.d_mainUI=nil'):
            with self.subTest(setup=setup):
                lua = self.runtime()
                lua.execute(setup)
                self.install(lua)
                lua.execute('remainingPatchInstalled=true')
                self.assertTrue(lua.globals().remainingPatchInstalled)

    def test_full_plan_runs_before_and_after_main_without_sends(self):
        lua = self.runtime(resource_preload.load_plan())
        self.install(lua)
        lua.execute('''ms.d_mainUI.show();finish()
        assert(_localResourcePreload.failed==0 and sendCount==0)
        assert(_localResourcePreload.retained_bytes<=PLAN.retained_texture_bytes)
        assert(_localResourcePreload.phase=='done')''')

    def test_full_patch_chain_compiles_and_installs_preloader_before_pending_features(self):
        lua = self.runtime()
        result = lua.execute(summon.client_source(summon.load_rules()))
        self.assertIsNotNone(lua.globals()._localResourcePreload)
        self.assertTrue(lua.eval('_localResourcePreload.current()'))
        # Other adapters may still await their real native UI modules.
        self.assertIsInstance(result, (str, type(None)))


class ResourcePreloadPlanTests(unittest.TestCase):
    def test_manifest_matches_packaged_images_and_lazy_getters(self):
        inventory = {row['logical']: row for row in json.loads((ROOT/'analysis/evidence/resource_inventory.json').read_text())}
        scripts = json.loads((ROOT/'analysis/evidence/script_inventory.json').read_text())
        modules = dict(d_mainUI='ui/mainUI', d_packageUI='ui/packageUI', d_data='data', d_lineupUI='ui/lineupUI')
        plan = resource_preload.load_plan()
        for job in plan['core'] + plan['warm']:
            with self.subTest(job=job):
                if job['kind'] == 'texture':
                    resource = ROOT/'jgbol3.87/assets/release_'/inventory[job['path']]['physical']
                    self.assertTrue(resource.is_file())
                else:
                    module = modules[job['module']]
                    script = next(row for row in scripts if row['logical']==f'lua/{module}.lua')
                    proto = next(key for key, name in script['functions'].items() if name==job['getter'])
                    body = (ROOT/f'analysis/evidence/lua_named/lua/{module}.lua.txt').read_text().split('FUNCTION '+proto+' ')[1].split('\nFUNCTION ')[0]
                    self.assertIn('params=0', body.splitlines()[0])
                    self.assertNotIn('send_msg', body)
                    self.assertEqual(job['cache_fields'], sorted(set(re.findall(r"GSET.*'(g_[^']+)'", body))))
        self.assertLessEqual(sum(j.get('estimated_bytes',0) for j in plan['core']+plan['warm']), plan['retained_texture_bytes'])

    def test_shared_payload_and_desktop_cleanup_include_preloader(self):
        self.assertIn('resource_preload_client.lua', (ROOT/'network_redirect/summon.py').read_text())
        cleanup = (ROOT/'network_redirect/summon_client.js').read_text()
        self.assertIn("preload.restore()", cleanup)
        from offline_android.pack_payload import collect_files
        files = collect_files()
        for name in ('network_redirect/resource_preload.py',
                     'network_redirect/resource_preload_client.lua',
                     'server_config/resource_preload.json'):
            self.assertEqual(files[name], ROOT / name)
