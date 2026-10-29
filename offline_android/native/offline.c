/* ARM32 adapter for the frozen JGBOL 3.87 native engine.
 * No Frida, ADB, root, downloaded scripts, or external helper process.
 * Compiled without a host/NDK sysroot: declarations below are Android ARM EABI.
 */
typedef unsigned int u32;
typedef unsigned short u16;
typedef unsigned char u8;
typedef unsigned int size_t;
typedef int ssize_t;
typedef void lua_State;
typedef struct { const char *filename; void *base; const char *symbol; void *address; } Dl_info;
extern void *dlopen(const char *, int);
extern void *dlsym(void *, const char *);
extern int dladdr(void *, Dl_info *);
extern void *mmap(void *, size_t, int, int, int, int);
extern int mprotect(void *, size_t, int);
extern int cacheflush(int, int, int);
extern int open(const char *, int, ...);
extern int close(int);
extern ssize_t read(int, void *, size_t);
extern void *malloc(size_t);
extern void free(void *);
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern int memcmp(const void *, const void *, size_t);
extern size_t strlen(const char *);
extern int strcmp(const char *, const char *);
extern int snprintf(char *, size_t, const char *, ...);
extern int __android_log_print(int, const char *, const char *, ...);
extern int getpeername(int, void *, u32 *);
extern int getsockopt(int, int, int, void *, u32 *);
extern int connect(int, const void *, u32);
extern void *gethostbyname(const char *);
extern int getaddrinfo(const char *, const char *, const void *, void **);
struct timespec32 { int sec; int nsec; };
extern int clock_gettime(int, struct timespec32 *);

#define LOG(...) __android_log_print(4, "JGBOffline", __VA_ARGS__)
#define ERR(...) __android_log_print(6, "JGBOffline", __VA_ARGS__)
#define PORT 18770
#define MAX_PATCH (4 * 1024 * 1024)
static char ca_path[4096];
static char *patch_source;
static u32 patch_size;
static int installed, evaluating, lua_ready, lua_failed;
static u32 previous_ms;
static int (*lua_gettop_)(lua_State *);
static void (*lua_settop_)(lua_State *, int);
static void (*lua_getfield_)(lua_State *, int, const char *);
static int (*lua_type_)(lua_State *, int);
static int (*luaL_loadbuffer_)(lua_State *, const char *, u32, const char *);
static int (*lua_pcall_original)(lua_State *, int, int, int);
static const char *(*lua_tolstring_)(lua_State *, int, u32 *);
static int (*curl_setopt_)(void *, int, ...);
static int (*curl_perform_original)(void *);
static int (*curl_add_original)(void *, void *);
static void *(*ssl_new_original)(void *);
static int (*ssl_ca_)(void *, const char *, const char *);
static int (*curl_multi_perform_)(void *, int *);
static int (*curl_getinfo_)(void *, int, ...);

static void throw_error(void *env, const char *message) {
    void **jni = *(void ***)env;
    void *klass = ((void *(*)(void *, const char *))jni[6])(env, "java/lang/RuntimeException");
    ((int (*)(void *, void *, const char *))jni[14])(env, klass, message);
    ERR("native_install_failed: %s", message);
}

static int local_name(const char *name) {
    return !name || !strcmp(name, "localhost") || !strcmp(name, "::1") ||
        !strcmp(name, "::ffff:127.0.0.1") ||
        (name[0] == '1' && name[1] == '2' && name[2] == '7' && name[3] == '.');
}

static void *offline_gethostbyname(const char *name) {
    return gethostbyname(local_name(name) ? name : "127.0.0.1");
}

static int offline_getaddrinfo(const char *name, const char *service, const void *hints, void **result) {
    const int *h = (const int *)hints;
    /* Preserve AI_NUMERICHOST probing; replacing a name there changes semantics. */
    if (!local_name(name) && !(h && (h[0] & 4)))
        name = h && h[1] == 10 ? "::ffff:127.0.0.1" : "127.0.0.1";
    return getaddrinfo(name, service, hints, result);
}

static int offline_connect(int fd, const void *address, u32 length) {
    if (!address || length < 16) return connect(fd, address, length);
    const u8 *input = (const u8 *)address;
    u16 family = *(const u16 *)input;
    if ((family != 2 && family != 10) || (family == 10 && length < 28))
        return connect(fd, address, length);
    int type = 0; u32 size = sizeof(type);
    if (getsockopt(fd, 1, 3, &type, &size) || type != 1)
        return connect(fd, address, length);
    u8 output[28];
    memset(output, 0, sizeof(output));
    *(u16 *)output = family;
    output[2] = PORT >> 8; output[3] = PORT & 255;
    if (family == 2) { output[4] = 127; output[7] = 1; }
    else { output[18] = 255; output[19] = 255; output[20] = 127; output[23] = 1; }
    return connect(fd, output, family == 2 ? 16 : 28);
}

/* This is the same state transition as network_redirect/offline.js. */
static int fixed_get_socket_fd(u8 *self) {
    int *fd_field = (int *)(self + 0x81a8), *status = (int *)(self + 0x18c);
    if (*fd_field > 0) return *fd_field;
    if (*status == 1) return 0;
    int active = 0, code = 0;
    for (int i = 0; i < 8; ++i) {
        code = curl_multi_perform_(*(void **)(self + 0x194), &active);
        if (code != -1) break;
    }
    if (code > 0) { *(int *)(self + 8) = 100; *status = 1; return 0; }
    int fd = -1;
    if (curl_getinfo_(*(void **)(self + 0x190), 0x20001d, &fd)) return 0;
    u8 peer[128]; u32 length = sizeof(peer);
    if (fd < 0 || getpeername(fd, peer, &length)) return 0;
    *fd_field = fd; *status = 3;
    LOG("local_socket_connected fd=%d", fd);
    return fd;
}

static int offline_perform(void *easy) {
    if (easy) curl_setopt_(easy, 10065, ca_path);
    return curl_perform_original(easy);
}
static int offline_add(void *multi, void *easy) {
    if (easy) curl_setopt_(easy, 10065, ca_path);
    return curl_add_original(multi, easy);
}
static void *offline_ssl_new(void *context) {
    ssl_ca_(context, ca_path, (const char *)0);
    return ssl_new_original(context);
}

static int client_patches_current(lua_State *state) {
    int top = lua_gettop_(state), current = 0;
    lua_getfield_(state, -10002, "package"); /* LUA_GLOBALSINDEX, LuaJIT 2.0 */
    if (lua_type_(state, -1) == 5) {
        lua_getfield_(state, -1, "loaded");
        if (lua_type_(state, -1) == 5) {
            lua_getfield_(state, -1, "ui.summonUI");
            if (lua_type_(state, -1) == 5) {
                lua_getfield_(state, -1, "_localGoldRestore");
                current = lua_type_(state, -1) == 6;
            }
        }
    }
    lua_settop_(state, top);
    return current;
}

static int offline_pcall(lua_State *state, int nargs, int nresults, int errfunc) {
    struct timespec32 now;
    clock_gettime(1, &now);
    u32 ms = (u32)now.sec * 1000 + (u32)now.nsec / 1000000;
    if (!evaluating && !lua_failed && (u32)(ms - previous_ms) >= 250) {
        previous_ms = ms;
        if (lua_ready && client_patches_current(state))
            return lua_pcall_original(state, nargs, nresults, errfunc);
        /* The original client unloads modules when returning to the login UI.
         * Reinstall the unchanged idempotent patches after that normal reload. */
        if (lua_ready) LOG("offline_lua_reload: client modules changed");
        lua_ready = 0;
        int top = lua_gettop_(state);
        evaluating = 1;
        int result = luaL_loadbuffer_(state, patch_source, patch_size, "@offline-summon-gold");
        if (!result) result = lua_pcall_original(state, 0, 1, 0);
        const char *value = lua_tolstring_(state, -1, (u32 *)0);
        if (result) {
            lua_failed = 1;
            ERR("offline_lua_error: %s", value ? value : "unknown Lua error");
        } else if (value && !strcmp(value, "ready")) {
            lua_ready = 1;
            LOG("offline_lua_ready: frozen client patches installed");
        }
        lua_settop_(state, top);
        evaluating = 0;
    }
    return lua_pcall_original(state, nargs, nresults, errfunc);
}

static void branch(u8 *destination, void *target, int thumb) {
    /* All sites are 4-byte aligned. LDR pc preserves all registers and flags. */
    *(u32 *)destination = thumb ? 0xf000f8df : 0xe51ff004;
    *(u32 *)(destination + 4) = (u32)target;
}

static void *hook(void *entry, void *replacement, const u8 expected[8], int trampoline) {
    u32 raw = (u32)entry, thumb = raw & 1;
    u8 *code = (u8 *)(raw & ~1u);
    if (((u32)code & 3) || memcmp(code, expected, 8)) return (void *)0;
    u8 *copy = (u8 *)1;
    if (trampoline) {
        copy = mmap((void *)0, 4096, 3, 0x22, -1, 0);
        if (copy == (void *)-1) return (void *)0;
        /* The verified first eight bytes contain no PC-relative instructions. */
        memcpy(copy, code, 8);
        branch(copy + 8, (void *)((u32)(code + 8) | thumb), thumb);
        cacheflush((int)copy, (int)(copy + 16), 0);
        if (mprotect(copy, 4096, 5)) return (void *)0;
    }
    u8 *page = (u8 *)((u32)code & ~4095u);
    if (mprotect(page, 4096, 7)) return (void *)0;
    branch(code, replacement, thumb);
    cacheflush((int)code, (int)(code + 8), 0);
    if (mprotect(page, 4096, 5)) return (void *)0;
    return trampoline ? (void *)((u32)copy | thumb) : (void *)1;
}

static int got(u8 *base, u32 offset, void *replacement) {
    void **slot = (void **)(base + offset);
    if (mprotect((void *)((u32)slot & ~4095u), 4096, 3)) return 0;
    *slot = replacement;
    return 1;
}

__attribute__((visibility("default")))
void Java_com_jgbol_offline_NativeBridge_install(void *env, void *klass, void *root_string, void *ca_string) {
    (void)klass;
    if (installed) return;
    void **jni = *(void ***)env;
    const char *(*get_utf)(void *, void *, void *) = (void *)jni[169];
    void (*release_utf)(void *, void *, const char *) = (void *)jni[170];
    const char *root = get_utf(env, root_string, (void *)0);
    const char *ca = get_utf(env, ca_string, (void *)0);
    char path[4096];
    int path_len = snprintf(path, sizeof(path), "%s/offline_client.lua", root);
    int ca_len = snprintf(ca_path, sizeof(ca_path), "%s", ca);
    release_utf(env, root_string, root); release_utf(env, ca_string, ca);
    if (path_len >= (int)sizeof(path) || ca_len >= (int)sizeof(ca_path)) {
        throw_error(env, "Offline resource path is too long"); return;
    }
    int ca_fd = open(ca_path, 0);
    if (ca_fd < 0) { throw_error(env, "Bundled offline CA is missing"); return; }
    close(ca_fd);
    int fd = open(path, 0);
    if (fd < 0) { throw_error(env, "Bundled Lua patches are missing"); return; }
    /* Guard the early VM startup; the unmodified 44-patch body follows it. */
    const char *guard = "if not package or not package.loaded or type(package.loaded.ms)~='table' then return 'pending' end\n";
    patch_source = malloc(MAX_PATCH + 1);
    if (!patch_source) { close(fd); throw_error(env, "Cannot allocate bundled Lua patches"); return; }
    patch_size = strlen(guard);
    memcpy(patch_source, guard, patch_size);
    int count;
    while ((count = read(fd, patch_source + patch_size, MAX_PATCH - patch_size)) > 0) patch_size += count;
    close(fd);
    if (count < 0 || patch_size >= MAX_PATCH) { throw_error(env, "Cannot read bundled Lua patches"); return; }
    patch_source[patch_size] = 0;
    void *game = dlopen("libxiyoujilua.so", 2);
    if (!game) { throw_error(env, "Cannot open 32-bit game engine"); return; }
    void *pcall = dlsym(game, "lua_pcall");
    Dl_info info;
    if (!pcall || !dladdr(pcall, &info) || (u32)pcall - (u32)info.base != 0x1d4450) {
        throw_error(env, "Unsupported game engine ABI"); return;
    }
    u8 *base = info.base;
#define RESOLVE(variable, name) variable = (void *)dlsym(game, name); if (!variable) { throw_error(env, "Missing engine symbol: " name); return; }
    RESOLVE(lua_gettop_, "lua_gettop");
    RESOLVE(lua_settop_, "lua_settop");
    RESOLVE(lua_getfield_, "lua_getfield");
    RESOLVE(lua_type_, "lua_type");
    RESOLVE(luaL_loadbuffer_, "luaL_loadbuffer");
    RESOLVE(lua_tolstring_, "lua_tolstring");
    RESOLVE(curl_setopt_, "curl_easy_setopt");
    RESOLVE(curl_multi_perform_, "curl_multi_perform");
    RESOLVE(curl_getinfo_, "curl_easy_getinfo");
    RESOLVE(ssl_ca_, "SSL_CTX_load_verify_locations");
    static const u8 arm_pcall[] = {0x38,0x40,0x2d,0xe9,0x08,0x40,0x90,0xe5};
    static const u8 thumb_perform[] = {0x70,0xb5,0x04,0x1c,0x2b,0x20,0x00,0x2c};
    static const u8 thumb_add_ssl[] = {0xf0,0xb5,0x57,0x46,0x4e,0x46,0x45,0x46};
    static const u8 thumb_socket[] = {0xf0,0xb5,0x47,0x46,0x80,0xb4,0x51,0x4b};
    /* Verify every site before changing any executable memory. */
    if (memcmp(base+0x1d4450, arm_pcall, 8) || memcmp(base+0x2ce9f8, thumb_perform, 8) ||
        memcmp(base+0x2d1de0, thumb_add_ssl, 8) || memcmp(base+0x360e64, thumb_add_ssl, 8) ||
        memcmp(base+0x105350, thumb_socket, 8)) {
        throw_error(env, "Game engine does not match the frozen 3.87 baseline"); return;
    }
    curl_perform_original = hook(base+0x2ce9f9, offline_perform, thumb_perform, 1);
    curl_add_original = hook(base+0x2d1de1, offline_add, thumb_add_ssl, 1);
    ssl_new_original = hook(base+0x360e65, offline_ssl_new, thumb_add_ssl, 1);
    lua_pcall_original = hook(pcall, offline_pcall, arm_pcall, 1);
    if (!curl_perform_original || !curl_add_original || !ssl_new_original || !lua_pcall_original ||
        !hook(base+0x105351, fixed_get_socket_fd, thumb_socket, 0) ||
        !got(base, 0x48b8e4, offline_gethostbyname) ||
        !got(base, 0x48b93c, offline_connect) ||
        !got(base, 0x48bda8, offline_getaddrinfo)) {
        throw_error(env, "Cannot install built-in offline engine adapter"); return;
    }
    installed = 1;
    LOG("offline_native_ready: loopback 18770, TLS CA, socket fix, Lua thread adapter");
}
