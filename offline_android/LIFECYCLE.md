# Android 进程恢复

Android 在后台回收进程后，可以直接恢复任务中的原游戏 Activity，而不经过桌面启动页。
因此不能在原 Activity 的 `onCreate` 中等待 Python 服务就绪：资源解包或后端初始化可能超过
输入响应时限，阻塞主线程会产生 ANR。[Android ANR 说明](https://developer.android.com/topic/performance/vitals/anr)

构建时由 `patch_lifecycle.patch(decoded)` 对构建暂存目录做以下适配：

- 游戏原生库加载统一放进 `OfflineRuntime` 工作线程，顺序为 Python、游戏、语音、内置补丁。
- Cocos `onCreate` 先调用 Android 框架的父方法；服务未就绪时不创建 GL 视图并立即返回。
- 原游戏 `onCreate` 检查该实例是否确实建立 GL 视图；尚未建立时转到启动页并结束该恢复实例。
- 未初始化实例的 `onResume`、`onPause`、`onDestroy` 仍调用框架父方法，但跳过依赖游戏视图的代码。
- 服务就绪后由启动页新建游戏 Activity；正常路径保留原生命周期方法的完整逻辑。
- 启动页仅在前台检查就绪状态。用户按 Home 后后台初始化继续，但不会自动把游戏抢回前台。

使用实例的 GL 状态判断，避免服务恰好在两次检查间就绪、导致未初始化实例继续执行的竞态。
恢复时清理的是失效的 Activity 任务栈，独立 SQLite 存档不受影响。重建后按原登录流程恢复角色。
调用 Activity 的父生命周期方法是框架约定；不能在调用父 `onCreate` 之前简单返回。
[Android Activity API](https://developer.android.com/reference/android/app/Activity)

静态验证包括基线方法精确匹配、补丁重复执行结果不变、Java 编译，以及修改后的两个 smali
类实际组装为 DEX。设备验收应在隔离测试设备上执行 Home → 杀死后台进程 → 恢复原游戏 Activity，
检查 `RESTORE_REDIRECT`、`OFFLINE_READY`，并确认没有 ANR、父方法漏调或空 GL 视图异常。
