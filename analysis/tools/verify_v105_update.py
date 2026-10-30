"""Verify the actual v105 APK payload against its predecessor and a QA save copy."""
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
WORK = ROOT / '.runtime/v105-update-qa'
APK = WORK / '金箍棒3.87-离线单机-arm32-v105.apk'

WORKER = r'''
import json, pathlib, sys
from unittest.mock import patch
sys.path.insert(0, sys.argv[1])
from network_redirect.backend import Backend
save, now = pathlib.Path(sys.argv[2]), int(sys.argv[3])
with patch('time.time', return_value=now):
    b = Backend(save, 18770, lambda *a, **kw: None)
    accounts = [row[0] for row in b.db.execute('SELECT account FROM roles ORDER BY account')]
    assert accounts
    for account in accounts:
        role = b.profile(account)
        b.save(role, account, gameplay=False)
    assert b.db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    b.close()
print(json.dumps(dict(roles=len(accounts), integrity='ok')))
'''


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def database_snapshot(path):
    with sqlite3.connect(path.as_uri() + '?mode=ro', uri=True) as db:
        names = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        return {name: sorted(db.execute('SELECT * FROM "' + name.replace('"', '""') + '"').fetchall(), key=repr)
                for name in names}


def main():
    with zipfile.ZipFile(WORK / 'baseline-v105.apk') as old, zipfile.ZipFile(APK) as new:
        names = set(old.namelist()) | set(new.namelist())
        changed = [name for name in sorted(names) if not name.startswith('META-INF/')
                   and (name not in old.namelist() or name not in new.namelist() or old.read(name) != new.read(name))]
        assert changed == ['assets/offline/build.properties', 'assets/offline/program.zip'], changed
        for mode, apk in [('old', old), ('new', new)]:
            with zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as bundle:
                assert not any(n.endswith(('.sqlite3', '.db')) or 'save' in Path(n).parts for n in bundle.namelist())
                bundle.extractall(WORK / mode)
        original = json.loads((WORK / 'old/server_config/gift_code_rules.json').read_text())
        updated = json.loads((WORK / 'new/server_config/gift_code_rules.json').read_text())
        assert updated['codes'][:len(original['codes'])] == original['codes']
        assert len(updated['codes']) - len(original['codes']) == 24
        manifest = json.loads((WORK / 'new/payload-manifest.json').read_text())
        checked = 0
        for row in manifest['files']:
            if row['path'].startswith(('network_redirect/', 'server_config/')) and row['source'] == 'baseline':
                assert digest(ROOT / row['path']) == row['sha256'], row['path']
                checked += 1
        from network_redirect import summon
        assert (WORK / 'new/offline_client.lua').read_text() == summon.client_source(summon.load_rules())
    source = ROOT / '.runtime/opening-qa/after-all-tests.sqlite3'
    source_hash = digest(source)
    save = WORK / 'save'
    save.mkdir(exist_ok=True)
    database = save / 'game.sqlite3'
    with sqlite3.connect(source.as_uri() + '?mode=ro', uri=True) as src, sqlite3.connect(database) as dst:
        src.backup(dst)
    now = str(int(time.time()))
    reports = []
    expected = None
    for mode in ('old', 'new', 'new'):
        result = subprocess.run([sys.executable, '-I', '-c', WORKER, str(WORK / mode), str(save), now],
                                capture_output=True, text=True, timeout=60)
        assert result.returncode == 0, result.stderr
        reports.append(dict(mode=mode, **json.loads(result.stdout)))
        snapshot = database_snapshot(database)
        if expected is None:
            expected = snapshot
        else:
            assert snapshot == expected, 'Saved database tables changed after payload upgrade'
    assert digest(source) == source_hash
    report = dict(apk_sha256=digest(APK), changed_apk_entries=changed,
                  current_source_files_verified=checked, generated_lua_matches=True,
                  original_codes_preserved=len(original['codes']), added_codes=24,
                  all_database_tables_equal_after_upgrade_and_restart=True,
                  source_qa_save_unchanged=True, contains_player_database=False,
                  original_game_java_native_runtime_video_unchanged=True, passes=reports)
    (WORK / 'payload-save-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
