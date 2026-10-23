"""CLI for any game config; serve imports browser dependencies only on demand."""
import argparse
import subprocess
import sys
import zipfile
from pathlib import Path
from .config import load_config
from .manager import Manager, error_text


def main(argv=None, *, config_loader=None, manager_factory=Manager):
    parser = argparse.ArgumentParser(description='通用安卓模拟器游戏台')
    parser.add_argument('--config', type=Path, help='游戏 JSON 配置；相对路径以此文件所在目录为准')
    parser.add_argument('command', choices=['start', 'stop', 'install', 'launch', 'status', 'doctor',
                                          'restart-web', 'serve', 'prepare-avd', 'download-runtime',
                                          'setup-runtime', 'setup-compat32'])
    parser.add_argument('--apk', type=Path, help='install 使用的原始 APK，保留其签名')
    args = parser.parse_args(argv)
    if not config_loader and not args.config:
        parser.error('请使用 --config 指定游戏配置')
    try:
        config = load_config(args.config) if args.config else config_loader()
        manager = manager_factory(config)
        if args.command == 'start': manager.start()
        elif args.command == 'stop': manager.stop()
        elif args.command == 'install': manager.install(args.apk)
        elif args.command == 'launch': manager.launch()
        elif args.command == 'restart-web':
            manager.stop(gateway_only=True)
            manager.start()
        elif args.command == 'serve':
            from .gateway import serve
            serve(config)
        elif args.command == 'prepare-avd':
            from .avd import create_avd
            create_avd(config)
        elif args.command == 'download-runtime':
            from .download import download_runtime
            download_runtime(config)
        elif args.command == 'setup-runtime':
            from .runtime_setup import setup_runtime
            setup_runtime(config)
        elif args.command == 'setup-compat32':
            from .compat32 import setup_compat32
            setup_compat32(config)
        else:
            return 0 if manager.doctor() else 1
    except (RuntimeError, ValueError, OSError, KeyError, zipfile.BadZipFile, subprocess.SubprocessError) as exc:
        print(error_text(exc), file=sys.stderr)
        return 1
    return 0
