'use strict';
// REDIRECT_CONFIG is prepended by the Python controller. Android/Bionic ABI only.
const libc = Process.getModuleByName('libc.so');
const address = name => libc.findExportByName(name);
const installed = [];
const callbacks = [];
const local4 = Memory.allocUtf8String('127.0.0.1');
const local6 = Memory.allocUtf8String('::ffff:127.0.0.1');
const gettype = new NativeFunction(address('getsockopt'), 'int',
    ['int', 'int', 'int', 'pointer', 'pointer']);
function event(kind, fields) { send(Object.assign({kind: kind, pid: Process.id}, fields)); }
function localName(name) {
    return name === 'localhost' || name === '::1' || /^127\./.test(name) ||
        name === '::ffff:127.0.0.1';
}
function resolver(name, familyArg, hintsArg) {
    const ptr = address(name);
    if (!ptr) return;
    callbacks.push(Interceptor.attach(ptr, {
        onEnter(args) {
            if (args[0].isNull()) return;
            const original = args[0].readCString();
            if (!original || localName(original)) return;
            let family = familyArg === null ? 0 : args[familyArg].toInt32();
            if (hintsArg !== null && !args[hintsArg].isNull()) {
                // Android's InetAddress first probes whether the input is numeric.
                // Returning success for a hostname here breaks its parsing checks.
                if (args[hintsArg].readS32() & 4) return; // AI_NUMERICHOST
                family = args[hintsArg].add(4).readS32();
            }
            // Replace only the name, preserving service, flags, hints and allocator ownership.
            args[0] = family === 10 ? local6 : local4;
            this.original = original;
            this.target = family === 10 ? '::ffff:127.0.0.1' : '127.0.0.1';
        },
        onLeave(result) {
            if (this.original) event('dns_redirect', {
                api: name, host: this.original, target: this.target,
                result: name.indexOf('gethostbyname') === 0 ? !result.isNull() : result.toInt32()
            });
        }
    }));
    installed.push(name);
}
resolver('getaddrinfo', null, 2);
resolver('android_getaddrinfofornet', null, 2);
resolver('gethostbyname', null, null);
resolver('gethostbyname2', 1, null);

callbacks.push(Interceptor.attach(address('connect'), {
    onEnter(args) {
        const original = args[1], length = args[2].toInt32();
        if (original.isNull() || length < 16) return;
        const family = original.readU16();
        if (family !== 2 && family !== 10) return; // Keep AF_UNIX/netd/Frida IPC intact.
        if (family === 10 && length < 28) return;
        const type = Memory.alloc(4), size = Memory.alloc(4);
        size.writeU32(4);
        if (gettype(args[0].toInt32(), 1, 3, type, size) !== 0 || type.readS32() !== 1) return;
        const port = original.add(2).readU8() * 256 + original.add(3).readU8();
        const bytes = new Uint8Array(original.add(family === 2 ? 4 : 8).readByteArray(family === 2 ? 4 : 16));
        const host = family === 2 ? Array.from(bytes).join('.') :
            Array.from(bytes).map(x => x.toString(16).padStart(2, '0')).join('');
        const loopback = family === 2 ? bytes[0] === 127 :
            (bytes.slice(0, 15).every(x => x === 0) && bytes[15] === 1) ||
            (bytes.slice(0, 10).every(x => x === 0) && bytes[10] === 255 && bytes[11] === 255 && bytes[12] === 127);
        // Avoid redirect loops and leave the instrumentation transport alone.
        if (loopback && (port === REDIRECT_CONFIG.port || port === 27042 || port === 27043)) return;
        // Copy rather than corrupting the caller's sockaddr (it may be reused).
        this.copy = Memory.alloc(family === 2 ? 16 : 28);
        this.copy.writeByteArray(new Uint8Array(family === 2 ? 16 : 28));
        this.copy.writeU16(family);
        this.copy.add(2).writeU8(REDIRECT_CONFIG.port >> 8);
        this.copy.add(3).writeU8(REDIRECT_CONFIG.port & 255);
        this.copy.add(family === 2 ? 4 : 8).writeByteArray(family === 2 ?
            [127, 0, 0, 1] : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 127, 0, 0, 1]);
        args[1] = this.copy;
        args[2] = ptr(family === 2 ? 16 : 28);
        this.info = {fd: args[0].toInt32(), family: family, original_host: host,
            original_port: port, target: '127.0.0.1:' + REDIRECT_CONFIG.port};
    },
    onLeave(result) {
        if (this.info) event('connect_redirect', Object.assign(this.info, {
            result: result.toInt32(), errno: result.toInt32() === -1 ? this.errno : 0
        }));
    }
}));
installed.push('connect');
Interceptor.flush();
rpc.exports.status = () => ({installed: installed, pid: Process.id, port: REDIRECT_CONFIG.port});
event('hook_ready', {installed: installed, port: REDIRECT_CONFIG.port});
