'use strict';

// Lua 5.1 exports in libxiyoujilua.so. No fixed offsets, bytecode patches,
// replacement print(), Lua evaluation, or changes to the logging flag.
const library = 'libxiyoujilua.so';
const listeners = [];
const printFunctions = new Set();
const inspectedStates = new Map();
let installed = false;
let pending = [];
let dropped = 0;

function emit(source, kind, message, fields) {
    if (pending.length >= 1024) { dropped++; return; }
    pending.push(Object.assign({source, kind, message, level: 'I', tag: kind,
        tid: Process.getCurrentThreadId(), device_time: new Date().toISOString()}, fields || {}));
}

function flush() {
    if (dropped) {
        const count = dropped;
        dropped = 0;
        pending.unshift({source: 'observer', kind: 'hook_overflow', tag: 'hook_overflow',
            level: 'W', message: '钩子缓冲溢出，丢弃 ' + count + ' 条', dropped: count});
    }
    while (pending.length) send({type: 'events', events: pending.splice(0, 128)});
}

function text(pointer, limit, exact) {
    if (pointer.isNull()) return '<null>';
    try {
        const maximum = Math.min(limit === undefined ? 4096 : limit, 4096);
        let size = maximum;
        if (!exact) {
            size = 0;
            while (size < maximum && pointer.add(size).readU8() !== 0) size++;
        }
        if (size === 0) return '';
        try { return pointer.readUtf8String(size); }
        catch (_) { return pointer.readCString(size); }
    } catch (_) { return '<unreadable>'; }
}

function install(module) {
    if (installed || module.name !== library) return;
    installed = true;
    const status = {type: 'hook_status', library, installed: [], missing: [], errors: []};
    function address(name) {
        const p = module.findExportByName(name);
        if (!p) status.missing.push(name);
        return p;
    }
    function native(name, ret, args) {
        const p = address(name);
        return p ? new NativeFunction(p, ret, args) : null;
    }
    function attach(name, callbacks) {
        const p = address(name);
        if (!p) return;
        try {
            listeners.push(Interceptor.attach(p, callbacks));
            status.installed.push(name);
        } catch (e) { status.errors.push(name + ': ' + e); }
    }
    const gettop = native('lua_gettop', 'int', ['pointer']);
    const settop = native('lua_settop', 'void', ['pointer', 'int']);
    const type = native('lua_type', 'int', ['pointer', 'int']);
    const tolstring = native('lua_tolstring', 'pointer', ['pointer', 'int', 'pointer']);
    const tonumber = native('lua_tonumber', 'double', ['pointer', 'int']);
    const toboolean = native('lua_toboolean', 'int', ['pointer', 'int']);
    const pushstring = native('lua_pushstring', 'void', ['pointer', 'pointer']);
    const rawget = native('lua_rawget', 'void', ['pointer', 'int']);
    const tocfunction = native('lua_tocfunction', 'pointer', ['pointer', 'int']);
    const checkstack = native('lua_checkstack', 'int', ['pointer', 'int']);
    const printName = Memory.allocUtf8String('print');

    function value(L, index) {
        const t = type(L, index);
        // Never run tostring/metamethods or convert numbers with lua_tolstring:
        // conversion could mutate the live stack and change game behavior.
        if (t === 4) {
            const size = Memory.alloc(Process.pointerSize);
            const str = tolstring(L, index, size);
            const count = Process.pointerSize === 4 ? size.readU32() : size.readU64().toNumber();
            return text(str, count, true);
        }
        if (t === 3 && tonumber) return String(tonumber(L, index));
        if (t === 1 && toboolean) return toboolean(L, index) ? 'true' : 'false';
        if (t === 0) return 'nil';
        return '<' + ({2: 'lightuserdata', 5: 'table', 6: 'function', 7: 'userdata', 8: 'thread'}[t] || 'value') + '>';
    }
    function error(L, kind, code, chunk) {
        if (!type || !tolstring) return;
        try {
            emit('lua', kind, value(L, -1), {level: 'E', status: code, chunk: chunk || null});
        } catch (e) { emit('observer', 'hook_error', String(e), {level: 'W'}); }
    }
    function inspectPrint(L) {
        if (![gettop, settop, type, tolstring, pushstring, rawget, tocfunction, checkstack].every(Boolean)) return;
        const key = L.toString();
        const clock = Date.now();
        if (clock - (inspectedStates.get(key) || 0) < 1000) return;
        // Bound bookkeeping for transient states; lua_close also removes them.
        if (inspectedStates.size > 128) inspectedStates.clear();
        inspectedStates.set(key, clock);
        const top = gettop(L);
        try {
            if (!checkstack(L, 1)) return;
            pushstring(L, printName);
            rawget(L, -10002); // LUA_GLOBALSINDEX in Lua 5.1; bypass __index.
            const fn = tocfunction(L, -1);
            if (fn.isNull() || printFunctions.has(fn.toString())) return;
            listeners.push(Interceptor.attach(fn, {
                onEnter(args) {
                    try {
                        const state = args[0];
                        const count = gettop(state);
                        const parts = [];
                        for (let i = 1; i <= Math.min(count, 32); i++) parts.push(value(state, i));
                        if (count > 32) parts.push('<truncated arguments>');
                        emit('lua', 'lua_print', parts.join('\t'), {level: 'D', state: state.toString()});
                    } catch (e) { emit('observer', 'hook_error', String(e), {level: 'W'}); }
                }
            }));
            printFunctions.add(fn.toString());
            emit('observer', 'print_hook_ready', '已挂接当前全局 print 的 C 函数', {address: fn.toString()});
        } catch (e) { emit('observer', 'hook_error', String(e), {level: 'W'}); }
        finally { settop(L, top); }
    }

    attach('lua_pcall', {
        onEnter(args) { this.L = args[0]; inspectPrint(this.L); },
        onLeave(result) { if (result.toInt32() !== 0) error(this.L, 'lua_pcall_error', result.toInt32()); }
    });
    attach('luaL_openlibs', {
        onEnter(args) { this.L = args[0]; },
        onLeave() { inspectPrint(this.L); }
    });
    attach('luaL_loadbuffer', {
        onEnter(args) {
            this.L = args[0];
            this.chunk = text(args[3], 512);
            emit('lua', 'lua_load', this.chunk, {chunk: this.chunk, bytes: args[2].toUInt32()});
        },
        onLeave(result) { if (result.toInt32() !== 0) error(this.L, 'lua_load_error', result.toInt32(), this.chunk); }
    });
    attach('luaL_loadfile', {
        onEnter(args) {
            this.L = args[0]; this.chunk = text(args[1], 512);
            emit('lua', 'lua_loadfile', this.chunk, {chunk: this.chunk});
        },
        onLeave(result) { if (result.toInt32() !== 0) error(this.L, 'lua_load_error', result.toInt32(), this.chunk); }
    });
    // lua_resume reports coroutine failures; LUA_YIELD (1) is not an error.
    attach('lua_resume', {
        onEnter(args) { this.L = args[0]; },
        onLeave(result) { if (result.toInt32() > 1) error(this.L, 'lua_coroutine_error', result.toInt32()); }
    });
    attach('lua_close', {
        onEnter(args) { inspectedStates.delete(args[0].toString()); }
    });
    send(status);
}

let observer = null;
let poll = null;
if (typeof Process.attachModuleObserver === 'function') {
    observer = Process.attachModuleObserver({onAdded(module) { install(module); }});
} else {
    // Compatibility with older Frida builds that may be needed on Android 6.
    const check = () => { const m = Process.findModuleByName(library); if (m) install(m); };
    check();
    poll = setInterval(check, 250);
    send({type: 'hook_status', message: '使用模块轮询；可能遗漏库加载后最早的事件'});
}
setInterval(flush, 100);
rpc.exports = {flush() { flush(); return {installed}; }};
send({type: 'hook_status', message: installed ? '脚本就绪' : '等待 ' + library});
