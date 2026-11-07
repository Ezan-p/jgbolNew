"""Verify actual APK contents and migrate a disposable copy of the historical QA save."""
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v110 import BASE, OUTPUT, WORK, EVIDENCE
from analysis.tools.verify_v105_update import database_snapshot
from offline_android.pack_payload import collect_files, verify_payload


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


WORKER = r'''
import json, pathlib, sys
from contextlib import ExitStack
from unittest.mock import patch
sys.path.insert(0, sys.argv[1])
from network_redirect.backend import Backend
save, now = pathlib.Path(sys.argv[2]), 1793923200
with ExitStack() as stack:
    stack.enter_context(patch('time.time', return_value=now))
    if (pathlib.Path(sys.argv[1]) / 'network_redirect/game_clock.py').exists():
        stack.enter_context(patch('network_redirect.game_clock.now', return_value=now))
    b = Backend(save, 18770, lambda *a, **kw: None)
    accounts = [r[0] for r in b.db.execute('SELECT account FROM roles ORDER BY account')]
    assert accounts
    for account in accounts:
        role = b.profile(account)
        if 'time_guard' in role:
            assert role['time_guard']['blocked'] == []
        b.save(role, account, gameplay=False)
    assert b.db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    b.close()
print(json.dumps(dict(roles=len(accounts), integrity='ok')))
'''


def main():
    for mode, apk in [('old', BASE), ('new', OUTPUT)]:
        tree = WORK / ('payload-' + mode)
        with zipfile.ZipFile(apk) as z, zipfile.ZipFile(io.BytesIO(z.read('assets/offline/program.zip'))) as payload:
            assert payload.testzip() is None
            assert not any(Path(n).suffix in ('.sqlite3', '.db', '.pyc') or 'save' in Path(n).parts for n in payload.namelist())
            payload.extractall(tree)
        verify_payload(tree)
    tree = WORK / 'payload-new'
    checked = 0
    for name, path in collect_files().items():
        if name == 'network_redirect/login.html':
            continue
        assert digest(path) == digest(tree / name), name
        checked += 1
    from network_redirect.summon import client_source, load_rules
    assert client_source(load_rules()) == (tree / 'offline_client.lua').read_text()
    source = ROOT / '.runtime/opening-qa/after-all-tests.sqlite3'
    before_hash = digest(source)
    save = Path(tempfile.mkdtemp(prefix='save-compatibility-', dir=WORK))
    database = save / 'game.sqlite3'
    with sqlite3.connect(source.as_uri() + '?mode=ro', uri=True) as src, sqlite3.connect(database) as dst:
        src.backup(dst)
    snapshots, passes = [], []
    for i, mode in enumerate(('old', 'new', 'new')):
        result = subprocess.run([sys.executable, '-I', '-c', WORKER, str(WORK / ('payload-' + mode)), str(save)],
                                capture_output=True, text=True, timeout=120)
        assert result.returncode == 0, result.stderr
        passes.append(dict(mode=mode, **json.loads(result.stdout)))
        snapshot = database_snapshot(database)
        snapshots.append(snapshot)
        (save / f'snapshot-{i}-{mode}.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2, default=lambda value: {'bytes_hex': value.hex()}))
    old, new, restart = snapshots
    assert set(new) == set(old) | {'time_guard'}
    assert new == restart, 'Restart changed the migrated database'
    for name in old:
        if name != 'roles':
            assert old[name] == new[name], name
    assert len(old['roles']) == len(new['roles'])
    for a, b in zip(old['roles'], new['roles']):
        assert a[0] == b[0] and a[2:] == b[2:]
        old_role, new_role = json.loads(a[1]), json.loads(b[1])
        guard = new_role.pop('time_guard')
        assert guard['blocked'] == [] and guard['status'] == 'legacy_unverified', guard
        assert old_role == new_role, 'Unexpected role changes outside time_guard metadata'
    for filename in ('clock.sqlite3', 'time_guard.key', 'clock_integrity.key'):
        assert (save / filename).is_file(), filename
    assert digest(source) == before_hash
    report = dict(apk_sha256=digest(OUTPUT), baseline_sha256=digest(BASE),
        current_source_files_verified=checked, all_payload_hashes_verified=True,
        generated_client_matches=True, contains_player_database=False,
        existing_role_values_preserved=True, added_game_database_table='time_guard',
        legacy_roles_unblocked=True, all_tables_equal_after_restart=True,
        source_qa_save_unchanged=True, save_load_passes=passes,
        evidence_save_directory=str(save.relative_to(ROOT)))
    (EVIDENCE / 'payload-save-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
