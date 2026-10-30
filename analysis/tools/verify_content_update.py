"""Verify v104's packaged code on a copy of the archived Android QA save."""
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / '.runtime/content-update-qa'
NOW = 1793232000

WORKER = r'''
import copy, json, pathlib, sqlite3, sys
from unittest.mock import patch
sys.path.insert(0, sys.argv[1])
from network_redirect.backend import Backend
from network_redirect import daily, formation
save, mode = pathlib.Path(sys.argv[2]), sys.argv[3]
now = int(sys.argv[4])
with patch('time.time', return_value=now):
    b = Backend(save, 18770, lambda *a, **kw: None)
    if mode == 'old':
        role = b.profile()
        role.update(level=80, gold_coin=123456, silver_coin=654321)
        for c in role['corteges']:
            c.update(level=4, culture_point=188, hp_plus=7, cur_exp=12)
            c.pop('level_culture_version', None)
        role['daily'] = dict(day=daily.day(now, b.daily_rules), week=daily.week(now, b.daily_rules),
                             points={'1':10, '4':10}, total=400, claimed=[1,2],
                             checkin_count=7, bonus_claimed=[3,7])
        role['checkin_time'] = now
        b.save(role)
    accounts = [r[0] for r in b.db.execute('SELECT account FROM roles ORDER BY account')]
    before = {a: json.loads(b.db.execute('SELECT data FROM roles WHERE account=?', (a,)).fetchone()[0])
              for a in accounts}
    result = {}
    for account in accounts:
        role = b.profile(account)
        daily.prepare(role, now, b.daily_rules)
        b.save(role, account, gameplay=False)
        result[account] = b.profile(account)
    if mode == 'new':
        for account in accounts:
            expected = copy.deepcopy(before[account])
            for c in expected['corteges']:
                if c.get('level_culture_version', 0) < 1:
                    q = int(formation.BASES[c['type']]['quality'])
                    c['culture_point'] += formation.level_culture_points(q, 1, c['level']) - (c['level']-1)*5
                    c['level_culture_version'] = 1
            state = expected['daily']
            state.pop('week', None)
            state['total'] = sum(state['points'].values())
            assert result[account] == expected, 'Unexpected role field change: ' + repr([
                k for k in set(expected) | set(result[account]) if expected.get(k) != result[account].get(k)])
    assert b.db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    b.close()
    b = Backend(save, 18770, lambda *a, **kw: None)
    for account in accounts:
        role = b.profile(account)
        daily.prepare(role, now, b.daily_rules)
        assert role == result[account], 'Migration repeated on reopen'
    b.close()
print(json.dumps(dict(mode=mode, roles=len(accounts), integrity='ok', restart_idempotent=True)))
'''


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    source = ROOT / '.runtime/opening-qa/after-all-tests.sqlite3'
    before_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    save = WORK / 'save'
    save.mkdir(exist_ok=True)
    destination = save / 'game.sqlite3'
    with sqlite3.connect(source.as_uri() + '?mode=ro', uri=True) as old, sqlite3.connect(destination) as new:
        old.backup(new)
    with sqlite3.connect(destination) as db:
        auth = db.execute('SELECT * FROM accounts ORDER BY name').fetchall()
    reports = []
    for mode, filename in [('old', '金箍棒3.87-离线单机-arm32-更新v1.apk'),
                           ('new', '金箍棒3.87-离线单机-arm32-v104.apk')]:
        program = WORK / mode
        with zipfile.ZipFile(ROOT / 'build' / filename) as apk, \
                zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as bundle:
            assert not any(n.endswith(('.sqlite3', '.db')) for n in bundle.namelist())
            bundle.extractall(program)
        result = subprocess.run([sys.executable, '-I', '-c', WORKER, str(program), str(save), mode, str(NOW)],
                                capture_output=True, text=True, timeout=90)
        if result.returncode:
            raise RuntimeError(result.stderr)
        reports.append(json.loads(result.stdout))
    with sqlite3.connect(destination) as db:
        assert db.execute('SELECT * FROM accounts ORDER BY name').fetchall() == auth
    assert hashlib.sha256(source.read_bytes()).hexdigest() == before_hash
    report = dict(passes=reports, original_save_unchanged=True, account_credentials_preserved=True,
                  exact_role_comparison_except_intended_migrations=True,
                  source='Archived Android QA save copy plus legacy level/daily fixture',
                  device_install_test=False)
    (WORK / 'save-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
