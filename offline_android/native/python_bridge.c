/* Small ARM32 JNI host for the unmodified CPython Android distribution.
 * No desktop subprocess, Java/Python bridge framework, or network bootstrap.
 * CPython's stable C ABI declarations avoid requiring a full NDK sysroot.
 */
typedef unsigned int size_t;
typedef unsigned int wchar_t;
typedef void *PyObject;
typedef void *jobject;
typedef jobject jstring;
typedef const void **JNIEnv;
extern int snprintf(char *, size_t, const char *, ...);
extern char *strdup(const char *);
extern void free(void *);
extern void *malloc(size_t);
extern size_t strlen(const char *);
extern int Py_IsInitialized(void);
extern void Py_SetPath(const wchar_t *);
extern void Py_SetProgramName(const wchar_t *);
extern void Py_InitializeEx(int);
extern void *PyEval_SaveThread(void);
extern int PyGILState_Ensure(void);
extern void PyGILState_Release(int);
extern PyObject *PyImport_AddModule(const char *);
extern PyObject *PyModule_GetDict(PyObject *);
extern PyObject *PyUnicode_FromString(const char *);
extern const char *PyUnicode_AsUTF8(PyObject *);
extern int PyDict_SetItemString(PyObject *, const char *, PyObject *);
extern PyObject *PyDict_GetItemString(PyObject *, const char *);
extern int PyRun_SimpleString(const char *);
extern void Py_DecRef(PyObject *);

static volatile int starting;
static void throw_error(JNIEnv *env, const char *message) {
    jobject cls = ((jobject (*)(JNIEnv *, const char *))(*env)[6])(env, "java/lang/RuntimeException");
    ((int (*)(JNIEnv *, jobject, const char *))(*env)[14])(env, cls, message);
}
static void set_string(PyObject *dict, const char *key, const char *value) {
    PyObject *obj = PyUnicode_FromString(value);
    PyDict_SetItemString(dict, key, obj);
    Py_DecRef(obj);
}

__attribute__((visibility("default")))
jstring Java_com_jgbol_offline_PythonBridge_start(
        JNIEnv *env, jobject unused, jstring files, jstring program, jstring python) {
    (void)unused;
    if (__sync_lock_test_and_set(&starting, 1)) {
        throw_error(env, "Python startup is already running");
        return 0;
    }
    const char *(*get_string)(JNIEnv *, jstring, unsigned char *) = (void *)(*env)[169];
    void (*release_string)(JNIEnv *, jstring, const char *) = (void *)(*env)[170];
    const char *files_dir = get_string(env, files, 0);
    const char *program_dir = get_string(env, program, 0);
    const char *python_dir = get_string(env, python, 0);
    int first = !Py_IsInitialized();
    int gil = 0;
    if (first) {
        size_t n = strlen(program_dir) + 2 * strlen(python_dir) + 50;
        char *path = malloc(n);
        wchar_t *wide = malloc(n * sizeof(wchar_t));
        if (!path || !wide) {
            free(path); free(wide);
            release_string(env, files, files_dir);
            release_string(env, program, program_dir);
            release_string(env, python, python_dir);
            __sync_lock_release(&starting);
            throw_error(env, "Insufficient memory to initialize Python");
            return 0;
        }
        snprintf(path, n, "%s/stdlib.zip:%s/modules:%s", python_dir, python_dir, program_dir);
        /* All three paths are Android private app directories (ASCII). */
        size_t i; for (i = 0; path[i]; i++) wide[i] = (unsigned char)path[i];
        wide[i] = 0;
        static const wchar_t name[] = {'j','g','b','o','l','-','o','f','f','l','i','n','e',0};
        Py_SetProgramName(name);
        Py_SetPath(wide);
        free(path); free(wide);
        Py_InitializeEx(0);
    } else {
        gil = PyGILState_Ensure();
    }
    PyObject *globals = PyModule_GetDict(PyImport_AddModule("__main__"));
    set_string(globals, "_jgb_files", files_dir);
    set_string(globals, "_jgb_program", program_dir);
    release_string(env, files, files_dir);
    release_string(env, program, program_dir);
    release_string(env, python, python_dir);
    int rc = PyRun_SimpleString(
        "import sys, os, json, traceback\n"
        "_jgb_result = ''\n"
        "_jgb_error = ''\n"
        "try:\n"
        "    os.makedirs(os.path.join(_jgb_files, 'logs'), exist_ok=True)\n"
        "    if not getattr(sys.stderr, '_jgb_log', False):\n"
        "        _jgb_log = open(os.path.join(_jgb_files, 'logs', 'python.log'), 'a', buffering=1)\n"
        "        _jgb_log._jgb_log = True\n"
        "        sys.stdout = sys.stderr = _jgb_log\n"
        "    sys.dont_write_bytecode = True\n"
        "    from offline_android import backend as _jgb_backend\n"
        "    _jgb_result = json.dumps(_jgb_backend.start(_jgb_files, _jgb_program), ensure_ascii=True)\n"
        "except BaseException:\n"
        "    _jgb_error = traceback.format_exc()\n"
        "    print(_jgb_error, file=sys.stderr, flush=True)\n");
    PyObject *error_obj = PyDict_GetItemString(globals, "_jgb_error");
    const char *error = error_obj ? PyUnicode_AsUTF8(error_obj) : 0;
    PyObject *result_obj = PyDict_GetItemString(globals, "_jgb_result");
    const char *result = result_obj ? PyUnicode_AsUTF8(result_obj) : 0;
    int failed = rc || !result || !*result || (error && *error);
    char *copy = strdup(failed ? (error && *error ? error : "Python startup failed; see files/logs/python.log") : result);
    /* The asyncio backend owns a separate Python thread. Always release GIL. */
    if (first) PyEval_SaveThread(); else PyGILState_Release(gil);
    __sync_lock_release(&starting);
    jstring out = 0;
    if (failed) throw_error(env, copy);
    else out = ((jstring (*)(JNIEnv *, const char *))(*env)[167])(env, copy);
    free(copy);
    return out;
}
