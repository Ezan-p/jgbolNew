# 通用安卓模拟器游戏台

从当前游戏中提取的独立运行模块。可将整个 `android_emulator/` 文件夹复制到其他项目，保留文件夹名，然后用 `run.py --config /路径/game.json` 运行其他安卓游戏；不依赖金箍棒的资源、源码、本地服务或存档。

包含内置模拟器管理、外部 ADB 设备连接、APK 安装、Activity 启动、ABI 检查、浏览器画面、触摸/键盘/音频、AVD 创建和原项目的运行环境部署代码。游戏解包、重签名、业务接口、账号服务、数值规则和存档逻辑仍归各游戏项目负责。

## 接入另一个游戏

1. 将 `examples/` 中相应 JSON 复制到新游戏目录，修改 `title`、`package`、`activity`、`apk`。包名和启动 Activity 应取自该游戏的 APK；支持 `.MainActivity` 形式。
2. 选择内置模拟器或外部 ADB 设备，部署以下对应环境。
3. 执行 `start` → `doctor` → `install`。后续使用 `launch`，无需重复安装。

所有配置路径都相对于 **JSON 文件所在目录**，不受终端当前目录影响。`install --apk` 的参数则相对于终端当前目录。

### 使用已有 ADB 设备/模拟器

以 `examples/adb-game.json` 为模板，设置 `mode: adb`、`serial`（`adb devices` 的第一列）、`adb_path`。TCP 设备需先自行 `adb connect`，USB 设备需已授权调试。内置环境部署脚本无需运行。

以下例子假设模块与 `my-game/` 都在当前目录，且配置中的 `runtime_dir` 为 `.runtime`：

```sh
python3 -m venv my-game/.runtime/venv
my-game/.runtime/venv/bin/python -m pip install -r android_emulator/requirements.lock.txt
python3 android_emulator/run.py --config my-game/game.json start
python3 android_emulator/run.py --config my-game/game.json doctor
python3 android_emulator/run.py --config my-game/game.json install
```

浏览器打开 `http://127.0.0.1:<web_port>`。ADB 模式使用截图，最高 5 FPS，支持单指点击、长按及抬起后的直线滑动；声音由设备播放。不会启动或停止外部安卓设备。

### 内置 ARM32 / ARM64 环境

当前随代码保留的下载与 ARM32 引擎准备流程针对 **Apple Silicon macOS**，沿用原项目的固定下载地址和镜像校验；未扩展成 Windows/Linux 自动安装器。

| 配置 | 引擎/镜像 | 用途 |
|---|---|---|
| `arm32-native` | 原生宿主 ARM32 引擎 + Android 6.0/API 23 | 原项目使用的旧 ARM 游戏环境，软件仿真，通过 gRPC 转发游戏音频至浏览器（已验证引擎 37.2.12） |
| `arm64` | SDK emulator + Android 11/API 30 ARM64 | ARM64 游戏；不代表支持旧 `armeabi` 原生库 |
| `arm32-software` | 旧 Intel launcher + API 23 ARM32 | 保留的实验配置；新部署不自动安装此旧 launcher |

复制 `examples/arm32-game.json` 或 `examples/arm64-game.json`，为新游戏设置独立 `runtime_dir`、`avd_name`、`console_port`、`grpc_port` 和 `web_port`。内置模式的 `serial` 必须等于 `emulator-<console_port>`。

配置和 Python 环境准备好后：

```sh
python3 android_emulator/run.py --config my-game/game.json download-runtime
python3 android_emulator/run.py --config my-game/game.json setup-runtime
# ARM32：准备 ARM32 镜像、独立签名引擎，并按配置创建 AVD
python3 android_emulator/run.py --config my-game/game.json setup-compat32
# ARM64：使用 prepare-avd 创建 AVD（不要同时执行上面的 ARM32 命令）
# python3 android_emulator/run.py --config my-game/game.json prepare-avd
python3 android_emulator/run.py --config my-game/game.json start
python3 android_emulator/run.py --config my-game/game.json doctor
python3 android_emulator/run.py --config my-game/game.json install
```

部署脚本下载体积较大的 SDK、镜像和原项目构建工具；已有环境可通过 `sdk_path`、`adb_path`、`python_path` 指定。`runtime_dir` 保存 AVD、进程记录与日志；ARM32 独立引擎放在其中的 `compat32/native-engine/`。不要让不同游戏配置共享同一个运行目录。AVD 已存在时，`prepare-avd` 拒绝覆盖。

## 配置字段

| 字段 | 含义 |
|---|---|
| `title` | 网页/命令行游戏名称 |
| `package`、`activity` | 目标包名和启动 Activity，必填 |
| `apk` | 默认安装的完整 APK 路径；也可通过 `install --apk` 指定 |
| `required_abis` | 可运行 ABI 的候选列表，设备支持任一项即可；`null`/省略时读取 APK，纯 Java 游戏可填 `[]` |
| `mode` | `emulator` 或 `adb` |
| `runtime_profile` | 上表中的成套引擎/镜像配置，默认 `arm64` |
| `runtime_dir` | 游戏独立运行目录，默认 `.runtime` |
| `sdk_path` | 默认 `<runtime_dir>/sdk` |
| `adb_path` | 默认 `<sdk_path>/platform-tools/adb` |
| `python_path` | 默认 `<runtime_dir>/venv/bin/python`，须安装模块依赖 |
| `avd_name` | 内置虚拟设备名，默认 `android_game` |
| `console_port`、`grpc_port`、`web_port` | 默认 5556/8556/8767；控制端口为 5554—5682 偶数，下一端口由 ADB 使用，各端口不可重叠 |
| `serial` | 默认跟随控制端口，外部设备必须显式指定 |
| `dns` | 模拟器 DNS，默认 `8.8.8.8,1.1.1.1` |
| `token_discovery_dir` | 可选 gRPC token 发现目录，默认沿用 macOS emulator 目录 |
| `ui` | 可选网页文案：`eyebrow`、`edition`、`help`；文本按 HTML 转义 |
| `services` | 可选附加 Python 服务数组，每项包含 `name`、`script`、`port` |

`ANDROID_GAME_MODE`、`ANDROID_GAME_SERIAL`、`ANDROID_GAME_ADB_PATH` 可临时覆盖配置。旧游戏适配层继续支持原 `JGB_*` 环境变量。

安装时始终检查**本次实际 APK** 的 `lib/<abi>/*.so`，避免 `--apk` 换包后沿用旧 ABI 判断。不会改库目录、重签名、自动卸载或清空已安装应用。此接口面向完整 APK，不自动处理 split APK/XAPK 安装集合。

ABI 兼容是必要条件；游戏所需 Android API、Google 服务、图形扩展、渠道登录和远端服务器仍可能影响运行。不能保证所有安卓游戏无需适配即可运行。

## 命令与 Python 接口

所有命令均带 `--config /路径/game.json`：

- `start` / `stop`：管理当前配置的设备、网页和附加服务。
- `doctor` / `status`：检查实际设备、启动状态、ABI 和端口，失败返回非零状态码。
- `install [--apk /路径/game.apk]`：安装并启动配置中的游戏。
- `launch`：启动已安装游戏。
- `restart-web`：仅重启网页；正常运行中的模拟器和附加服务保持运行。
- `serve`：前台运行网页，方便调试。
- `prepare-avd`、`download-runtime`、`setup-runtime`、`setup-compat32`：环境准备。

在模块父目录也可使用 `python3 -m android_emulator --config ... doctor`。

```python
from android_emulator.config import load_config
from android_emulator.manager import Manager
from android_emulator.gateway import make_app

config = load_config('/path/to/game.json')
manager = Manager(config)
manager.start()
app = make_app(config)  # aiohttp application，按应用隔离配置和控制会话
```

网页与控制接口只监听本机，保留会话验证、同源检查、单控制者和帧背压。不同游戏使用独立 cookie 名，避免同一浏览器访问多个本机端口时会话相互覆盖。

## 与当前金箍棒项目的关系

`../安卓模拟器游戏台源码_2026-10-20/cloud_android/` 中的 `manage.py`、`server.py` 和部署脚本已改为调用本模块。原 `game.json`、`.runtime`、AVD、APK、存档和 `启动游戏台.command` 沿用原位置；通过原入口执行 `start`、`doctor`、`launch` 等命令即可。

`game_config.py` 适配层负责提供金箍棒专用的 `armeabi` 要求、APK 路径、界面文案及本地服务 8770。不要直接把该旧配置交给通用入口，因为它需要适配层补充这些游戏专用设置。新游戏使用 `examples/`，无需复制原游戏目录。

`local_game/`、`scripts/prepare_apk.py`、`scripts/build_local_game.py`、逆向与资源导出脚本仍属于原游戏。共享网页资源和 gRPC 协议已移到本目录，保留一份实现。

## 本机画面延迟优化

内置模拟器的新网页通过 `?format=rgba` 协商 RGBA 原始像素传输，省去逐帧 PNG 压缩与浏览器图片解码，传输上限为 30 FPS。保持原始分辨率，逐帧等待浏览器绘制确认，避免慢客户端积压旧画面；未协商的旧客户端仍使用 PNG / 20 FPS，ADB 仍使用 PNG / 5 FPS。拖动事件按浏览器动画帧合并为每根手指的最新位置，按下和抬起立即发送。

2026-10-24 在本项目 960×540 ARM32 环境中的一次测量：30 次截图的中位耗时 PNG 41.4 ms、RGBA 3.13 ms；网关连续 61 帧、立即确认的传输测试分别约 19.6 / 28.6 FPS。这不是游戏内部帧率或点击到显示的端到端延迟；ARM32 软件仿真的 CPU 限制仍存在。RGBA 每帧约 2.07 MB，适用于当前本机回环连接。

修改生效只需 `restart-web` 后刷新浏览器并重新连接画面，无需重启安卓或重新安装游戏。

## 验证

在模块父目录、安装了依赖的 Python 环境中执行：

```sh
python -m unittest discover -s android_emulator/tests -v
node --check android_emulator/web/app.js
node android_emulator/tests/test_web_input.cjs
```

测试覆盖复制后的独立运行、多游戏配置与浏览器会话隔离、实际 APK ABI 检查、启动目标、端口冲突、外部设备保护及 AVD 数据保留。原游戏测试仍在原 `cloud_android` 目录运行。
