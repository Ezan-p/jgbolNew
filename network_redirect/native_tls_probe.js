// Uses the game bundled libcurl with peer and hostname verification enabled.
rpc.exports.nativetlsprobe = function () {
    const m = Process.getModuleByName('libxiyoujilua.so');
    const fn = (name, ret, args) => new NativeFunction(m.getExportByName(name), ret, args);
    const init = fn('curl_easy_init', 'pointer', []);
    const option = fn('curl_easy_setopt', 'int', ['pointer', 'int', 'pointer']);
    const perform = fn('curl_easy_perform', 'int', ['pointer']);
    const info = fn('curl_easy_getinfo', 'int', ['pointer', 'int', 'pointer']);
    const cleanup = fn('curl_easy_cleanup', 'void', ['pointer']);
    let bytes = 0;
    const sink = new NativeCallback((data, size, count, user) => { bytes += size * count; return size * count; }, 'uint', ['pointer', 'uint', 'uint', 'pointer']);
    const h = init();
    try {
        option(h, 10002, Memory.allocUtf8String('https://jgbol-local.invalid/__redirect_health'));
        option(h, 64, ptr(1)); // Verify peer chain.
        option(h, 81, ptr(2)); // Verify hostname.
        option(h, 13, ptr(8));
        option(h, 20011, sink);
        const result = perform(h);
        const out = Memory.alloc(4); out.writeS32(0);
        info(h, 0x200002, out);
        return {curl_result: result, http_status: out.readS32(), response_bytes: bytes};
    } finally { cleanup(h); }
};
