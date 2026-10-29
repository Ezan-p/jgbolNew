# 离线单机 APK 构建依赖

运行 `python3 offline_android/prepare_toolchain.py` 下载并校验固定版本材料。
缓存完整后使用 `python3 offline_android/prepare_toolchain.py --offline`，无需连接设备或网络。
下载 URL 和 SHA256 固定在脚本内；缓存或提取文件校验失败会停止，不会默默换版本。

| 输入 | 版本及位置 | 用途 |
| --- | --- | --- |
| CPython ARM32 | Chaquopy target `3.11.0-2`，`.runtime/offline-toolchain/python-arm32/` | Python 3.11.0、OpenSSL 3.0.5、SQLite 和扩展模块 |
| Python 标准库 | `target-3.11.0-2-stdlib.zip` | 按原字节作为 APK runtime 的 `stdlib.zip` |
| Android Java API | Maven `com.google.android:android:4.1.1.4`，`android.jar` | 编译 Java 壳使用的旧版公共 API，仅构建时使用 |
| Android 构建工具 | 项目既有 `.runtime/sdk/build-tools/35.0.0/` | LLD、D8、zipalign、apksigner |
| Java / Clang | 项目既有 JDK 17 和 macOS Xcode Command Line Tools | Java 与 ARM32 C 编译 |
| APK 重建工具 | 项目既有 `.runtime/tools/apktool.jar` | 保留旧客户端资源与 smali |

这些下载只发生在开发电脑构建阶段。最终 APK 自带运行资源，首次启动也不下载 Python 或游戏资源。

Python 原生库从 `python-arm32/jniLibs/armeabi-v7a/` 中选取四个文件：
`libpython3.11.so`、`libcrypto_chaquopy.so`、`libssl_chaquopy.so`、`libsqlite3_chaquopy.so`。
扩展模块取 `python-arm32/lib-dynload/armeabi-v7a/*.so`，解压到私有 runtime 的 `modules/`。
头文件仅供参考，当前精简 JNI 桥通过明确声明的 CPython C API 编译。

`native/build_native.py` 和 `native/build_python_bridge.py` 自行生成 `libc.so`、`libdl.so`、
`liblog.so` 的链接占位符。它们只声明符号，SONAME 与 Android 系统库一致，运行时实际由系统提供。
因此不需要 ADB、正在运行的模拟器或从 system.img 提取系统库来构建。
**不得把 `.runtime/offline-native/` 或 `.runtime/offline-toolchain/link-stubs/` 下的占位库打进 APK。**
早期调查缓存根目录的 `libc.so`、`libdl.so` 同样不参与打包或后续构建，可删除。

现有本地账号 APK、冻结的客户端资源、规则、NPC 数据以及固定签名密钥仍是项目材料，
这个脚本不重新生成密钥，也不从设备读取玩家数据库。`release_w` 的基线核验清单单独保存；
开发测试使用全新的 `.runtime/offline-test/avd/standalone32.avd`，不会覆盖旧模拟器存档。

组件许可全文与来源保存在 `THIRD_PARTY_NOTICES`，并随 APK 内置。
