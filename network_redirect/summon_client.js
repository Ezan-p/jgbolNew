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
                    evaluate(args[0], "local ms=package.loaded.ms; if ms and ms.d_guideUI and ms.d_guideUI._localOpeningRestore then ms.d_guideUI._localOpeningRestore() end; if ms and ms.d_worldBossUI and ms.d_worldBossUI._localPartyRestore then ms.d_worldBossUI._localPartyRestore() end; if ms and ms._localActivityLevelRestore then ms._localActivityLevelRestore() end; if ms and ms.d_packageUI and ms.d_packageUI._localSkillRestore then ms.d_packageUI._localSkillRestore() end; if ms and ms._localStateRefreshRestore then ms._localStateRefreshRestore() end; if ms and ms.d_data and ms.d_data._localSoulRefreshRestore then ms.d_data._localSoulRefreshRestore() end; if ms and ms.d_funUI and ms.d_funUI._localActivityEntryRestore then ms.d_funUI._localActivityEntryRestore() end; local k=package.loaded['ui.rankUI']; if k and k._localRankRestore then k._localRankRestore() end; if ms and ms._localGuildPetRestore then ms._localGuildPetRestore() end; if ms and ms._localGuildAccessRestore then ms._localGuildAccessRestore() end; if ms and ms._localGuildActivitiesRestore then ms._localGuildActivitiesRestore() end; if ms then for _,name in ipairs({'d_guildFightUI','d_crossRealm'}) do local g=ms[name]; if g and g._localGuildRestore then g._localGuildRestore() end end end; local rice=package.loaded['ui.ricePuddingUI']; if rice and rice._localRiceRestore then rice._localRiceRestore() end; local moon=package.loaded['ui.moonCakeUI']; if moon and moon._localMoonRestore then moon._localMoonRestore() end; local caishen=package.loaded['ui.springActivityMoneyUI']; if caishen and caishen._localCaishenRestore then caishen._localCaishenRestore() end; local fish=package.loaded['ui.fishRushUI']; if fish and fish._localFishRestore then fish._localFishRestore() end; local ns=package.loaded['ui.towerUI']; if ns and ns._localNineSkyRestore then ns._localNineSkyRestore() end; local rl=package.loaded['ui.turntableUI']; if rl and rl._localRulaiRestore then rl._localRulaiRestore() end; local ys=package.loaded['ui.twoYearsCelebrateUI']; if ys and ys._localYuanshiRestore then ys._localYuanshiRestore() end; local feed=package.loaded['ui.eatBunUI']; if feed and feed._localFeedRestore then feed._localFeedRestore() end; local tx=package.loaded['ui.arenaUI']; if tx and tx._localTaixuRestore then tx._localTaixuRestore() end; local babel=package.loaded['ui.tongtiantaUI']; if babel and babel._localBabelRestore then babel._localBabelRestore() end; local home=package.loaded['ui.homeUI']; if home and home._localHomeRestore then home._localHomeRestore() end; local q=package.loaded['ui.qiFuUI']; if q and q._localPrayRestore then q._localPrayRestore() end; local pet=package.loaded['ui.petUI']; if pet and pet._localPetRestore then pet._localPetRestore() end; local d=package.loaded['ui.crossDoomUI']; if d and d._localRapeRestore then d._localRapeRestore() end; local realm=package.loaded['ui.roleRebornUI']; if realm and realm._localRealmRestore then realm._localRealmRestore() end; local a=package.loaded['ui.ascensionUI']; if a and a._localRebornRestore then a._localRebornRestore() end; local b=package.loaded['ui.batchSaleUI']; if b and b._localSaleRestore then b._localSaleRestore() end; local f=package.loaded['ui.forgeUI']; if f and f._localCraftingRestore then f._localCraftingRestore() end; local e=package.loaded['ui.stoneUI']; if e and e._localEquipmentRestore then e._localEquipmentRestore() end; local s=package.loaded['ui.summonUI']; if s and s._localGoldRestore then s._localGoldRestore() end; local v=package.loaded['ui.vipUI']; if v and v._localVipRestore then v._localVipRestore() end; local expbook=package.loaded['ui.expbookUI']; if expbook and expbook._localExpbookRestore then expbook._localExpbookRestore() end; local book=package.loaded['ui.tianShuUI']; if book and book._localTianShuRestore then book._localTianShuRestore() end; local m=package.loaded['ui.monumentUI']; if m and m._localMonumentRestore then m._localMonumentRestore() end; local w=package.loaded['ui.actNoticeUI']; if w and w._localPermanentWelfareRestore then w._localPermanentWelfareRestore() end; if w and w._localGrowthRestore then w._localGrowthRestore() end; if w and w._localWelfareRestore then w._localWelfareRestore() end; local trial=package.loaded['ui.shilianUI']; if trial and trial._localTrialRestore then trial._localTrialRestore() end; if ms and ms._localBattleReplayRestore then ms._localBattleReplayRestore() end; local tw=package.loaded['ui.springCardUI']; if tw and tw._localTangwangRestore then tw._localTangwangRestore() end; return 'restored'");
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
