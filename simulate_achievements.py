"""Offline upstream settlement simulator. Defaults to preview; never opens a game socket."""
import argparse
import copy
import json
import time
from pathlib import Path
from network_redirect import achievements
from network_redirect.backend import Backend


def main():
    parser = argparse.ArgumentParser(description='【B】缺失上游成就结算模拟；默认仅预览，--apply 才保存')
    parser.add_argument('--directory', type=Path, required=True, help='已有 game.sqlite3 所在目录')
    parser.add_argument('--account', default='local-player')
    parser.add_argument('--events', type=Path, required=True, help='JSON 数组：id、amount、receipt')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    if not (args.directory / 'game.sqlite3').is_file(): parser.error('指定目录没有已有的 game.sqlite3')
    events = json.loads(args.events.read_text())
    if not isinstance(events, list): parser.error('模拟事件必须是数组')
    # Read-only preview must not migrate or create any role; SQLite is opened in
    # URI read-only mode until the explicitly requested apply transaction.
    import sqlite3
    db = sqlite3.connect((args.directory / 'game.sqlite3').resolve().as_uri() + '?mode=ro', uri=True)
    found = db.execute('SELECT data FROM roles WHERE account=?', (args.account,)).fetchone()
    db.close()
    if not found: parser.error('账号不存在')
    before = json.loads(found[0]); role = copy.deepcopy(before); now = int(time.time())
    for event in events:
        if isinstance(event, dict) and set(event) == {'event', 'value', 'receipt'}:
            achievements.simulate_fact(role, event['event'], event['value'], event['receipt'], now)
        elif isinstance(event, dict) and set(event) == {'id', 'amount', 'receipt'}:
            achievements.simulate(role, event['id'], event['amount'], event['receipt'], now)
        else: parser.error('事件需提供 event/value/receipt 或 id/amount/receipt')
    if args.apply:
        b = Backend(args.directory, 0, lambda *a, **kw: None, account=args.account)
        try:
            b.db.execute('BEGIN IMMEDIATE')
            latest = b.db.execute('SELECT data FROM roles WHERE account=?', (args.account,)).fetchone()
            if latest[0] != found[0]: raise RuntimeError('角色已被其他进程更新，请重新预览')
            b.save(role)
        finally: b.close()
    old = {r['id']: r for r in achievements.rows(before)}
    print(json.dumps(dict(source='B', applied=args.apply, tao_point=role['tao_point'],
        changed=[r for r in achievements.rows(role) if r != old.get(r['id'])]), ensure_ascii=False, indent=2))


if __name__ == '__main__': main()
