"""Start this game's isolated emulator, wait for Android, install once and launch."""
from pathlib import Path
import subprocess
import sys
import time

from android_emulator.config import load_config
from android_emulator.manager import Manager, adb, error_text, ready_device

ROOT = Path(__file__).resolve().parent


def main():
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
    if installed.startswith('package:'):
        manager.launch()
    else:
        manager.install()
    url = f"http://127.0.0.1:{config['web_port']}"
    subprocess.run(['open', url], check=True)
    print('游戏已启动：' + url)


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print(error_text(exc), file=sys.stderr)
        sys.exit(1)
