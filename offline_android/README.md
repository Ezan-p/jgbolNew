# 32 位离线单机 APK

本实现以当前 `build/jgbol3.87-local.apk`、实际生效的 `release_w`、当前 Python 业务、Lua 补丁、规则及 NPC 数据为基线。构建入口是仓库根目录 `build_offline.py`。它不会启动电脑服务，不会把个人玩家数据库打入 APK，也不会修改 `server_config` 中的数值、概率、奖励或活动开关。

## 安装和存档

安装完整 APK 后直接点击“金箍棒·离线单机”。首次打开会在手机内解包资源、准备本地服务，随后进入原游戏。注册本地账号即可游玩；账号只保存在本机。首次启动也无需联网、电脑、ADB、Frida、root 或额外安装 Python。

包名固定为 `com.sygame.jingubang.p360`，签名沿用当前本地账号版的证书。升级应直接覆盖安装新 APK，**不要卸载旧版或清除应用数据**。卸载和清除数据仍会删除手机存档。电脑 `.runtime/offline/game.sqlite3` 中的个人进度不随安装包分发，手机首次安装会创建独立存档。

| 数据 | 应用私有目录 |
| --- | --- |
| 玩家账号及角色 | `files/save/game.sqlite3` |
| 不可变程序、规则和 NPC | `files/program/<资源SHA256>/` |
| Python 解释器配套模块 | `files/runtime/<运行时SHA256>/` |
| 客户端覆盖资源 | `release_w/`，独立于 SQLite |
| 有限大小的诊断日志 | `files/logs/` |

资源先校验 SHA256，再在临时目录解包并原子替换；更新资源的路径不会进入 `files/save`。数据库继续使用原业务的 SQLite 事务。服务启动时检查数据库完整性，发现损坏会停止并保留文件，不会用空数据库覆盖进度。

## 设备条件

APK 仅含 `armeabi-v7a`。需要支持 32 位 ARM 应用的 Android 设备，最低 Android 5.0 / API 21；纯 64 位设备无法运行。当前实际验收环境为 Android 6.0 / API 23 ARMv7 模拟器。

保留的原游戏库含文本重定位，因此 `targetSdkVersion` 保持 22。[Android 链接器说明](https://android.googlesource.com/platform/bionic/+/master/android-changes-for-ndk-developers.md)明确目标 API 23 起拒绝这类库；[Android 14 安装限制](https://developer.android.com/about/versions/14/behavior-changes-all#minimum-target-api-level)又拒绝新装目标 API 低于 23 的应用。因此本包面向支持 ARM32 的 Android 5–13，**不能宣称支持 Android 14 及以上的普通安装**，也没有提供需 ADB 才能使用的安装方式。Android 5、7–13 的具体机型尚未逐一验证。

## 应用内运行

v103 起由启动页面在开场动画结束或跳过后创建后台初始化线程，资源和服务就绪后才进入原 Cocos Activity；进程恢复仍由生命周期守卫返回启动页。CPython 3.11 和扩展库随包携带，业务在同一 Python 服务线程中持有 SQLite 连接，监听 `127.0.0.1:18770`。原网络请求由 `liboffline.so` 接到手机回环服务，保留原 HTTP/TLS/游戏协议，不需要电脑反向端口。

`liboffline.so` 同时迁移原 CurlSocket 异步连接修复和 Lua 线程接入。Lua 脚本由原 `summon.client_source(load_rules())` 生成，现有模板及配置展开顺序保持一致。原引擎的 SHA256、关键指令和 ABI 在构建及初始化时检查，不适配时停止而非继续运行错误补丁。应用完全不含 Frida。

## 后续构建和覆盖补丁

开场动画 v103 更新可用 `python3 build_opening_patch.py` 单独生成，输入为保留的 v102 离线 APK；仅替换清单和启动代码，不重新生成后端或资源。输出完整更新 APK 和可用 Python 标准库合成的差分补丁，见 [开场动画补丁说明](../docs/开场动画补丁说明.md)。全量构建也包含开场动画，默认版本号现为 103；后续发布请递增。

在仓库根目录运行：

```sh
python3 offline_android/prepare_toolchain.py --offline
.runtime/venv/bin/python build_offline.py --version-code 104
```

首次配置构建工具时去掉 `--offline`，下载地址及 SHA256 已固定；这只发生在开发电脑。参见 [TOOLCHAIN.md](TOOLCHAIN.md)。现有游戏 APK、资源及签名不是在线下载依赖。`build_offline.py` 输出 APK 和完整 `.manifest.json` 清单，校验原游戏资源不变、所有规则与后端资源的哈希、ZIP、签名和对齐。

固定签名密钥为 `.runtime/channel360/local-test.p12`，别名 `channel360`，使用当前项目既有签名配置。应单独备份该文件；丢失后无法生成能直接覆盖已有安装的更新。构建器在密钥缺失时停止，绝不自动换签名。证书 SHA256：

```text
de10334b708a60c1edabcfa76b0115991f2554d19a475c23662120e723080c1e
```

后续补丁递增 `versionCode`，保持包名、证书、`files/save/game.sqlite3` 路径和兼容的数据库结构。现有业务自动建表逻辑保持原样；将来需要更改数据库结构时，必须另写事务式迁移并测试旧存档，不能直接替换数据库。

`verify_device.py` 是开发端验收工具，不在 APK 中。它连接实际手机内服务，完成新角色引导、战斗和召唤，再比较更新前后的账户与角色快照。其 ADB 正向端口仅用于测试观察，游戏运行不使用该端口。完整验收结果见输出目录的验证报告。
