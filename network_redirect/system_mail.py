"""Local operator mail delivery. Original client events 13/14/15, permanent rewards."""
import argparse
import copy
import fcntl
import json
import sqlite3
import time
from pathlib import Path
from . import formation as f, journey, summon, welfare

ROOT = Path(__file__).resolve().parents[1]
PERMANENT_NOTE = '【永久有效】附件无领取期限，每个存档仅可领取一次。'


def deliver(role, key, title, body, prizes, now, rules, mail_id=None):
    """Validate on a detached role; retrying the same delivery never resets claims."""
    f.require(isinstance(key, str) and 0 < len(key) <= 100, '发放批次标识无效')
    f.require(isinstance(title, str) and 0 < len(title) <= 100, '邮件标题无效')
    f.require(isinstance(body, str) and len(body) <= 4000, '邮件正文无效')
    f.require(isinstance(prizes, list) and 1 <= len(prizes) <= 200, '附件须为1至200类')
    for p in prizes:
        f.require(isinstance(p, list) and len(p) == 4 and all(type(x) is int for x in p), '附件格式须为[类型,编号,数量,等级]')
        kind, tid, count, level = p
        f.require(kind in (4,5,6,10,11,12,15) and 0 < count <= 2147483647 and level > 0, '附件类型、数量或等级无效')
        if kind in (4,10): f.require(tid in summon.BASES, '未知神仙或魂魄')
        if kind == 4: f.require(count == 1 and level == 1, '神仙附件须为单个初始神仙')
        if kind in (6,15): f.require(count <= 500, '实体附件数量过多')
        if kind == 6: f.require(tid in f.SKILLS and level <= int(f.SKILLS[tid]['top_level']), '法术等级无效')
        if kind == 5:
            from . import equipment
            # Gem levels live in stone_cost_worth, not item_base.top_level (=1).
            valid_level = ((equipment.STONES[tid], level) in equipment.STONE_VALUES
                           or (equipment.STONES[tid], level) in equipment.STONE_REBORN) if tid in equipment.STONES else (
                               tid in f.ITEMS and level <= max(1, int(f.ITEMS[tid]['top_level'])))
            f.require(valid_level, '物品等级无效')
    trial = copy.deepcopy(role)
    state = welfare.prepare(trial, now, rules)
    mails = state.setdefault('mails', {})
    existing = mails.get(key)
    if existing:
        f.require(existing['prizes'] == prizes and existing['mail_title'] == title, '该批次已存在且内容不同，拒绝重复发放')
        f.require(mail_id is None or existing['mail_id'] == mail_id, '已有批次邮件编号不同')
        mail = existing
        status = 'already_claimed' if mail['claimed'] else 'already_delivered'
    else:
        used = {m['mail_id'] for m in mails.values()}
        identity = mail_id if mail_id is not None else max(used | {800000000}) + 1
        f.require(type(identity) is int and 0 < identity <= 2147483647 and identity not in used, '邮件编号冲突或无效')
        mail = dict(mail_id=identity, mail_title=title, mail_body=body, recv_time=now,
                    send_time=now, prizes=copy.deepcopy(prizes), claimed=False)
        mails[key] = mail
        status = 'delivered'
    mail.update(expires_at=None, no_expiry=True, sender='系统', delivery_key=key)
    mail['mail_body'] = body if PERMANENT_NOTE in body else body + '\n' + PERMANENT_NOTE
    # Exercise the real grant path and encoder without crediting the target role.
    check = copy.deepcopy(trial)
    for p in prizes: journey.grant(check, p)
    welfare.mail_request(trial, 1102, dict(mail_id=mail['mail_id'], flag=0), now, rules, state)
    welfare.mail_snapshot(trial, now, rules)
    role.clear(); role.update(trial)
    return status, copy.deepcopy(mail)


def issue(database, account, payload, *, write=False, now=None):
    now = int(time.time()) if now is None else now
    database = Path(database)
    with sqlite3.connect(database, timeout=30) as db:
        db.execute('BEGIN IMMEDIATE' if write else 'BEGIN')
        row = db.execute('SELECT data FROM roles WHERE account=?', (account,)).fetchone()
        f.require(row is not None, '账号存档不存在')
        role = json.loads(row[0])
        status, mail = deliver(role, now=now, rules=welfare.load_rules(), **payload)
        if write:
            backups = database.parent / 'backups'; backups.mkdir(exist_ok=True)
            backup = backups / ('system-mail-' + str(time.time_ns()) + '.json')
            with backup.open('x', encoding='utf-8') as stream:
                json.dump(dict(account=account, data=json.loads(row[0])), stream, ensure_ascii=False)
            backup.chmod(0o600)
            db.execute('CREATE TABLE IF NOT EXISTS system_mail_audit (id INTEGER PRIMARY KEY, account TEXT, delivery_key TEXT, mail_id INTEGER, action TEXT, created_at INTEGER, payload TEXT)')
            db.execute('UPDATE roles SET data=? WHERE account=?', (json.dumps(role,ensure_ascii=False),account))
            db.execute('INSERT INTO system_mail_audit(account,delivery_key,mail_id,action,created_at,payload) VALUES(?,?,?,?,?,?)',
                       (account,payload['key'],mail['mail_id'],status,now,json.dumps(mail,ensure_ascii=False)))
        else: db.rollback()
    return dict(account=account, status=status, written=write, mail_id=mail['mail_id'],
                claimed=mail['claimed'], no_expiry=True, attachment_types=len(mail['prizes']))


def main():
    parser=argparse.ArgumentParser(description='本地运营系统邮件：默认预览，--send落盘；邮件永久有效。')
    parser.add_argument('--account', required=True)
    source=parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--file', type=Path, help='JSON: key/title/body/prizes，可选mail_id')
    source.add_argument('--launch-gift', action='store_true')
    parser.add_argument('--send', action='store_true')
    args=parser.parse_args()
    if args.launch_gift:
        from analysis.tools.send_launch_gift import build, KEY, MID
        prizes,_=build()
        payload=dict(key=KEY,mail_id=MID,title='开服大礼包',body='四位神仙及元始天尊飞升、九转材料；无上至尊初始三件及满进阶、封神、铸造材料；五星主动袖里乾坤、被动指地成钢及满级素材；天翼虎和养成丹药；金紫精魄各五；仙佛密卷和培元丹。养成仍需满足等级及境界条件。',prizes=prizes)
    else: payload=json.loads(args.file.read_text(encoding='utf-8'))
    # Same exclusive lock as the controller: no lost updates from in-flight saves.
    with (ROOT/'.runtime/redirect/run.lock').open('a') as lock:
        if args.send:
            try: fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError: parser.error('请先运行 python3 redirect_game.py stop，发放后恢复 start --offline --probe')
        print(json.dumps(issue(ROOT/'.runtime/offline/game.sqlite3',args.account,payload,write=args.send),ensure_ascii=False))

if __name__ == '__main__': main()
