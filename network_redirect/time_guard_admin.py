"""Offline reviewed-evidence quarantine. Preview by default; never infer guilt."""
import argparse
import json
from pathlib import Path
import shutil
import sqlite3
import uuid

from .time_guard import Guard
from .game_clock import GameClock


def main():
    parser = argparse.ArgumentParser(description='停服后登记已复核的时间异常；默认仅预览')
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--account', required=True)
    parser.add_argument('--scope', action='append', required=True,
                        help='可重复：activity_babel / daily / welfare / activity / *')
    parser.add_argument('--evidence', required=True, help='复核依据与流水编号，不能仅填未来日期')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    directory = args.directory.resolve()
    if not (directory / 'game.sqlite3').is_file():
        parser.error('存档不存在')
    with sqlite3.connect(directory / 'game.sqlite3') as db:
        row = db.execute('SELECT data FROM roles WHERE account=?', (args.account,)).fetchone()
        if row is None:
            parser.error('角色不存在')
        report = dict(account=args.account, scopes=args.scope, evidence=args.evidence,
                      previous=json.loads(row[0]).get('time_guard'), applied=False)
        if args.apply:
            # Operator must stop the service: game and clock are separate journals.
            backup = directory / 'backups' / ('time-guard-' + uuid.uuid4().hex)
            backup.mkdir(parents=True, mode=0o700)
            for filename in ('game.sqlite3', 'clock.sqlite3'):
                source = directory / filename
                if source.exists():
                    with sqlite3.connect(source) as src, sqlite3.connect(backup / filename) as dst:
                        src.backup(dst)
                    (backup / filename).chmod(0o600)
            for key in ('time_guard.key', 'clock_integrity.key'):
                if (directory / key).exists():
                    shutil.copy2(directory / key, backup / key)
            clock = GameClock(directory, legacy_db=db)
            try:
                report['result'] = Guard(db, directory).confirm(args.account, args.scope, args.evidence, clock.sample())
            finally:
                clock.close()
            report.update(applied=True, backup=str(backup))
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
