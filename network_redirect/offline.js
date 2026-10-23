// Explicit local mode: inject a local CA, and a local account at the SDK bridge.
if (REDIRECT_CONFIG.offline) {
    let offlineReady = false;
    rpc.exports.offlinestatus = () => offlineReady && socketFixInstalled && curlCAInstalled;
    Java.perform(function () {
        try {
            const FileInputStream = Java.use('java.io.FileInputStream');
            const CertificateFactory = Java.use('java.security.cert.CertificateFactory');
            const KeyStore = Java.use('java.security.KeyStore');
            const TrustManagerFactory = Java.use('javax.net.ssl.TrustManagerFactory');
            const SSLContext = Java.use('javax.net.ssl.SSLContext');
            const HTTPS = Java.use('javax.net.ssl.HttpsURLConnection');
            const originalFactory = HTTPS.getDefaultSSLSocketFactory();
            rpc.exports.offlinecleanup = async () => {
                const restored = await cleanupSummonClient();
                await new Promise(resolve => Java.perform(function () {
                    HTTPS.setDefaultSSLSocketFactory(originalFactory);
                    resolve(true);
                }));
                return restored;
            };
            const input = FileInputStream.$new(REDIRECT_CONFIG.caPath);
            const ca = CertificateFactory.getInstance('X.509').generateCertificate(input);
            input.close();
            const store = KeyStore.getInstance(KeyStore.getDefaultType());
            store.load(null, null);
            store.setCertificateEntry('jgbol-local', ca);
            const factory = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
            factory.init.overload('java.security.KeyStore').call(factory, store);
            const trust = factory.getTrustManagers();
            const init = SSLContext.init.overload('[Ljavax.net.ssl.KeyManager;', '[Ljavax.net.ssl.TrustManager;', 'java.security.SecureRandom');
            init.implementation = function (keys, managers, random) {
                return init.call(this, keys, trust, random);
            };
            const context = SSLContext.getInstance('TLS');
            context.init(null, trust, null);
            Java.use('javax.net.ssl.HttpsURLConnection').setDefaultSSLSocketFactory(context.getSocketFactory());
            event('local_ca_ready', {layer: 'java'});

            const API = Java.use('com.syyx.sdkproxy.ThirdPartyAPI');
            const Callback = Java.use('com.syyx.sdkproxy.ThirdPartyCallback');
            const localLogin = function () {
                Java.scheduleOnMainThread(function () {
                    try {
                        API.mAccessToken.value = REDIRECT_CONFIG.sdkToken;
                        API.m_map.value.put('access_token', Java.use('java.lang.String').$new(REDIRECT_CONFIG.sdkToken));
                        Java.cast(API.m_sEventCallback.value, Callback).onEvent(1, 0);
                        event('local_sdk_login', {message: '本地测试账号已通过 SDK 桥接回调'});
                    } catch (e) { event('offline_error', {message: String(e)}); }
                });
            };
            API.login.implementation = localLogin;
            API.switchAccount.implementation = localLogin;
            offlineReady = true;
            event('local_sdk_ready', {message: '360 登录桥接已切换为本地测试账号'});
            rpc.exports.tlsprobe = function () {
                return new Promise(function (resolve, reject) {
                    Java.perform(function () {
                        try {
                            const URL = Java.use('java.net.URL');
                            const connection = Java.cast(URL.$new('https://jgbol-local.invalid/__redirect_health').openConnection(), Java.use('javax.net.ssl.HttpsURLConnection'));
                            connection.setConnectTimeout(5000);
                            connection.setReadTimeout(5000);
                            const code = connection.getResponseCode();
                            const cipher = connection.getCipherSuite();
                            connection.disconnect();
                            resolve({status: code, cipher: String(cipher)});
                        } catch (e) { reject(new Error(String(e))); }
                    });
                });
            };
        } catch (e) { event('offline_error', {message: String(e)}); }
    });
    const configuredSSL = new Set();
    let socketFixInstalled = false;
    let curlCAInstalled = false;
    const caPath = Memory.allocUtf8String(REDIRECT_CONFIG.caPath);
    const installNativeCA = function () {
        for (const m of Process.enumerateModules()) {
            if (m.name !== 'libxiyoujilua.so' && m.name !== 'libssl.so') continue;
            if (m.name === 'libxiyoujilua.so' && !curlCAInstalled) {
                const setopt = new NativeFunction(m.getExportByName('curl_easy_setopt'), 'int', ['pointer', 'int', 'pointer']);
                // libcurl loads its CA file before SSL_new; configure both entry paths.
                for (const [name, handleIndex] of [['curl_easy_perform', 0], ['curl_multi_add_handle', 1]]) {
                    Interceptor.attach(m.getExportByName(name), {onEnter(args) {
                        setopt(args[handleIndex], 10065, caPath); // CURLOPT_CAINFO
                    }});
                }
                curlCAInstalled = true;
            }
            if (m.name === 'libxiyoujilua.so' && !socketFixInstalled) {
                const symbol = m.enumerateExports().find(e => e.name.indexOf('11getSocketFdEv') !== -1);
                if (!symbol || Process.pointerSize !== 4 ||
                    !symbol.address.and(ptr('0xfffffffe')).equals(m.base.add(0x105350))) {
                    event('offline_error', {message: 'CurlSocket ABI 与已验证的 3.87 样本不符'});
                    return;
                }
                const perform = new NativeFunction(m.getExportByName('curl_multi_perform'), 'int', ['pointer', 'pointer']);
                const getinfo = new NativeFunction(m.getExportByName('curl_easy_getinfo'), 'int', ['pointer', 'int', 'pointer']);
                const peername = new NativeFunction(address('getpeername'), 'int', ['int', 'pointer', 'pointer']);
                const fixedGetFd = new NativeCallback(function (self) {
                    const fdField = self.add(0x81a8), status = self.add(0x18c);
                    if (fdField.readS32() > 0) return fdField.readS32();
                    if (status.readS32() === 1) return 0;
                    const active = Memory.alloc(4);
                    let code;
                    for (let i = 0; i < 8; ++i) {
                        code = perform(self.add(0x194).readPointer(), active);
                        if (code !== -1) break; // CURLM_CALL_MULTI_PERFORM
                    }
                    if (code > 0) { self.add(8).writeS32(100); status.writeS32(1); return 0; }
                    const out = Memory.alloc(4);
                    out.writeS32(-1);
                    if (getinfo(self.add(0x190).readPointer(), 0x20001d, out) !== 0) return 0;
                    const fd = out.readS32(), peer = Memory.alloc(128), length = Memory.alloc(4);
                    length.writeU32(128);
                    // No fd yet is a normal asynchronous connect state, not a failure.
                    if (fd < 0 || peername(fd, peer, length) !== 0) return 0;
                    fdField.writeS32(fd);
                    status.writeS32(3);
                    event('local_socket_connected', {fd: fd});
                    return fd;
                }, 'int', ['pointer']);
                callbacks.push(fixedGetFd);
                Interceptor.replace(symbol.address, fixedGetFd);
                socketFixInstalled = true;
                event('local_socket_fix_ready', {message: '修正旧 CurlSocket 将异步连接未就绪误判为失败的问题'});
            }
            const sslNew = m.findExportByName('SSL_new');
            const load = m.findExportByName('SSL_CTX_load_verify_locations');
            if (!sslNew || !load || configuredSSL.has(sslNew.toString())) continue;
            configuredSSL.add(sslNew.toString());
            const addCA = new NativeFunction(load, 'int', ['pointer', 'pointer', 'pointer']);
            Interceptor.attach(sslNew, {onEnter(args) {
                const result = addCA(args[0], caPath, ptr(0));
                event('local_ca_ready', {layer: 'native', module: m.name, result: result});
            }});
        }
    };
    installNativeCA();
    setInterval(installNativeCA, 500);
}
