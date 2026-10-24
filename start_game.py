"""Start this game's isolated emulator, wait for Android, install once and launch."""
from pathlib import Path
import argparse
import subprocess
import sys
import time

from android_emulator.config import load_config
from android_emulator.manager import Manager, adb, error_text, ready_device

ROOT = Path(__file__).resolve().parent


def main(argv=None):
    parser = argparse.ArgumentParser(description='启动模拟器、本地登录服务和游戏')
    parser.add_argument('--client-only', action='store_true',
                        help='仅启动客户端，供单独调试渠道或重定向使用')
    parser.add_argument('--repair', action='store_true',
                        help='自动清理失效的登录注入后重启并自检，保留存档')
    args = parser.parse_args(argv)
    if args.repair and args.client_only:
        parser.error('--repair 不能与 --client-only 同时使用')
    config = load_config(ROOT / 'game.json')
    if not config['apk'].is_file():
        from build_apk import build
        build()
    manager = Manager(config)
    manager.start()
    print('等待安卓启动，首次启动可能需要几分钟……', flush=True)
    deadline = time.monotonic() + 600
    last_error = ''
    while time.monotonic() < deadline:
        try:
            ready_device(config)
            break
        except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
            last_error = error_text(exc)
            time.sleep(3)
    else:
        raise RuntimeError('等待安卓启动超时：' + last_error)
    installed = adb(config, 'shell', 'pm', 'path', config['package'], timeout=30)
    if not installed.startswith('package:'):
        manager.install()
    if args.client_only:
        if installed.startswith('package:'):
            manager.launch()
    else:
        # A fresh injection resets the SDK token and covers early native requests.
        # Opening the client alone leaves it dependent on unavailable old servers.
        redirect = [str(config['python_path']), str(ROOT / 'redirect_game.py'),
                    '--config', str(config['config_path'])]
        print('启动本地登录服务并检查连接……', flush=True)
        if args.repair:
            from network_redirect.repair import reset_login
            reset_login(config)
        else:
            subprocess.run(redirect + ['stop'], check=True)
        subprocess.run(redirect + ['start', '--offline', '--probe'], check=True)
    url = f"http://127.0.0.1:{config['web_port']}"
    subprocess.run(['open', url], check=True)
    print('游戏已启动：' + url)
    if not args.client_only:
        print('本地服务已就绪，在画面中点击“进入游戏”。')


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print(error_text(exc), file=sys.stderr)
        sys.exit(1)
