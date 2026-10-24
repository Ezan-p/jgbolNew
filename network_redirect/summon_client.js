// Execute the small offline UI adapter only on the game's Lua thread.
let cleanupSummonClient = async () => true;
if (REDIRECT_CONFIG.offline) {
    let installed = false, ready = false;
    rpc.exports.summonclientstatus = () => ready;
    function installSummonClient() {
        if (installed) return;
        const m = Process.findModuleByName('libxiyoujilua.so');
        if (!m) return;
        installed = true;
        const fn = (name, ret, args) => new NativeFunction(m.getExportByName(name), ret, args);
        const gettop = fn('lua_gettop', 'int', ['pointer']);
        const settop = fn('lua_settop', 'void', ['pointer', 'int']);
        const load = fn('luaL_loadbuffer', 'int', ['pointer', 'pointer', 'uint', 'pointer']);
        const call = fn('lua_pcall', 'int', ['pointer', 'int', 'int', 'int']);
        const str = fn('lua_tolstring', 'pointer', ['pointer', 'int', 'pointer']);
        const chunkName = Memory.allocUtf8String('@offline-summon-gold');
        let executing = false, lastAttempt = 0;
        function evaluate(L, code) {
            const saved = gettop(L);
            executing = true;
            try {
                const source = Memory.allocUtf8String(code);
                let status = load(L, source, unescape(encodeURIComponent(code)).length, chunkName);
                if (!status) status = call(L, 0, 1, 0);
                const value = str(L, -1, ptr(0));
                const result = value.isNull() ? '' : value.readUtf8String();
                if (status) throw new Error(result);
                return result;
            } finally { settop(L, saved); executing = false; }
        }
        let listener = Interceptor.attach(m.getExportByName('lua_pcall'), {onEnter(args) {
            if (executing || Date.now() - lastAttempt < 250) return;
            lastAttempt = Date.now();
            try {
                if (evaluate(args[0], REDIRECT_CONFIG.summonClientSource) !== 'ready') return;
                ready = true;
                listener.detach();
                event('local_summon_ui_ready', {message: '召唤元宝入口已启用，价格与服务端配置同步'});
            } catch (e) {
                listener.detach();
                event('offline_error', {message: '召唤元宝入口初始化失败：' + String(e)});
            }
        }});
        cleanupSummonClient = () => new Promise(resolve => {
            listener.detach();
            if (!ready) { resolve(true); return; }
            let done = false, timer;
            const cleanup = Interceptor.attach(m.getExportByName('lua_pcall'), {onEnter(args) {
                if (executing || done) return;
                done = true;
                try {
                    evaluate(args[0], "local s=package.loaded['ui.summonUI']; if s and s._localGoldRestore then s._localGoldRestore() end; local v=package.loaded['ui.vipUI']; if v and v._localVipRestore then v._localVipRestore() end; local w=package.loaded['ui.actNoticeUI']; if w and w._localWelfareRestore then w._localWelfareRestore() end; return 'restored'");
                    ready = false;
                    resolve(true);
                } catch (e) {
                    event('offline_error', {message: '召唤入口恢复失败：' + String(e)});
                    resolve(false);
                } finally { cleanup.detach(); clearTimeout(timer); }
            }});
            timer = setTimeout(() => {
                if (done) return;
                done = true;
                cleanup.detach();
                event('offline_error', {message: '未等到游戏 Lua 帧，召唤入口将在下次重启游戏时恢复'});
                resolve(false);
            }, 3000);
        });
    }
    installSummonClient();
    const installTimer = setInterval(() => {
        installSummonClient();
        if (installed) clearInterval(installTimer);
    }, 250);
}
