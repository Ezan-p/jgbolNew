// Opt-in live test: independent sockets in the instrumented process.
rpc.exports.probe = function () {
    const fn = (name, result, args) => new NativeFunction(address(name), result, args);
    const resolve = fn('getaddrinfo', 'int', ['pointer', 'pointer', 'pointer', 'pointer']);
    const free = fn('freeaddrinfo', 'void', ['pointer']);
    const socket = fn('socket', 'int', ['int', 'int', 'int']);
    const connect = fn('connect', 'int', ['int', 'pointer', 'int']);
    const sendData = fn('send', 'int', ['int', 'pointer', 'int', 'int']);
    const recvData = fn('recv', 'int', ['int', 'pointer', 'int', 'int']);
    const close = fn('close', 'int', ['int']);
    const setopt = fn('setsockopt', 'int', ['int', 'int', 'int', 'pointer', 'int']);
    const output = Memory.alloc(Process.pointerSize);
    output.writePointer(ptr(0));
    const hints = Memory.alloc(48);
    hints.writeByteArray(new Uint8Array(48));
    hints.add(4).writeS32(2);
    hints.add(8).writeS32(1);
    const dns = resolve(Memory.allocUtf8String('jgbol-redirect-probe.invalid'),
        Memory.allocUtf8String('80'), hints, output);
    let resolved = null;
    if (dns === 0) {
        const ai = output.readPointer();
        // Bionic's addrinfo places ai_canonname before ai_addr (unlike glibc).
        const sa = ai.add(Process.pointerSize === 4 ? 24 : 32).readPointer();
        resolved = Array.from(new Uint8Array(sa.add(4).readByteArray(4))).join('.');
        free(ai);
    }
    function request(family) {
        const fd = socket(family, 1, 0);
        if (fd < 0) return {socket: fd};
        try {
            const tv = Memory.alloc(Process.pointerSize * 2);
            tv.writeByteArray(new Uint8Array(Process.pointerSize * 2));
            if (Process.pointerSize === 4) tv.writeS32(3); else tv.writeS64(3);
            setopt(fd, 1, 20, tv, Process.pointerSize * 2);
            setopt(fd, 1, 21, tv, Process.pointerSize * 2);
            const sa = Memory.alloc(28);
            sa.writeByteArray(new Uint8Array(28));
            sa.writeU16(family);
            sa.add(3).writeU8(80);
            if (family === 2) sa.add(4).writeByteArray([192, 0, 2, 123]);
            else sa.add(8).writeByteArray([32, 1, 13, 184, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]);
            const rc = connect(fd, sa, family === 2 ? 16 : 28);
            if (rc !== 0) return {connect: rc};
            const request = 'GET /__redirect_health HTTP/1.0\r\nHost: jgbol-redirect-probe.invalid\r\n\r\n';
            sendData(fd, Memory.allocUtf8String(request), request.length, 0);
            const buffer = Memory.alloc(2048);
            let response = '';
            for (;;) {
                const count = recvData(fd, buffer, 2048, 0);
                if (count <= 0) break;
                response += buffer.readUtf8String(count);
            }
            return {connect: rc, ok: response.indexOf('JGBOL_LOCAL_REDIRECT_OK') !== -1,
                caller_port_unchanged: sa.add(2).readU8() === 0 && sa.add(3).readU8() === 80};
        } finally { close(fd); }
    }
    return {dns: dns, resolved: resolved, ipv4: request(2), ipv6: request(10)};
};
