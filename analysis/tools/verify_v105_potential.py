"""Verify the shipped potential update and allowed save migration using QA copies."""
import copy
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
from analysis.tools.verify_v105_update import digest, database_snapshot, WORKER

WORK = ROOT / '.runtime/v105-potential-qa'
APK = WORK / '金箍棒3.87-离线单机-arm32-v105.apk'
RATES = {'1': [1, 2], '2': [3, 4], '3': [5, 7], '4': [7, 10], '5': [10, 15]}

SEED = r'''
import json, pathlib, sys
from unittest.mock import patch
sys.path.insert(0, sys.argv[1])
from network_redirect.backend import Backend
from network_redirect import summon, formation
with patch('time.time', return_value=int(sys.argv[3])):
    b = Backend(pathlib.Path(sys.argv[2]), 18770, lambda *a, **kw: None)
    account = b.db.execute('SELECT account FROM roles ORDER BY account LIMIT 1').fetchone()[0]
    role = b.profile(account)
    for quality in range(1, 6):
        tid = next(t for t, row in summon.BASES.items() if int(row['quality']) == quality)
        for level in (1, 39, 40, 41, 200):
            for version in (0, 1):
                c = summon.companion(role, tid)
                c.update(level=level, culture_point=1234, hp_plus=13, evolve_level=2,
                         reborn_layer=1, cur_exp=0, qa_quality=quality, qa_version=version,
                         pending_training=dict(points=3))
                role['corteges'].append(c)
    formation.prepare(role, b.formation_rules)
    b.save(role, account, gameplay=False)
    b.close()
'''


def run_worker(script, mode, save, now):
    result = subprocess.run([sys.executable, '-I', '-c', script, str(WORK / mode), str(save), now],
                            capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    return result.stdout


def expected_migration(snapshot):
    expected = copy.deepcopy(snapshot)
    changes = []
    roles = []
    for account, data in snapshot['roles']:
        role = json.loads(data)
        for c in role['corteges']:
            version = c.get('level_culture_version', 0)
            if version >= 2:
                continue
            topup = 0
            if version == 0:
                early, late = RATES[str(c['qa_quality'])]
                total = min(39, c['level'] - 1) * early + max(0, c['level'] - 40) * late
                topup = max(0, total - (c['level'] - 1) * 5)
                c['culture_point'] += topup
            c['level_culture_version'] = 2
            changes.append(dict(previous_version=version, level=c['level'], topup=topup))
        roles.append((account, role))
    expected['roles'] = roles
    return expected, changes


def decoded_snapshot(database):
    snapshot = database_snapshot(database)
    snapshot['roles'] = [(account, json.loads(data)) for account, data in snapshot['roles']]
    return snapshot


def main():
    with zipfile.ZipFile(WORK / 'baseline-v105.apk') as old, zipfile.ZipFile(APK) as new:
        names = set(old.namelist()) | set(new.namelist())
        changed = [n for n in sorted(names) if not n.startswith('META-INF/')
                   and (n not in old.namelist() or n not in new.namelist() or old.read(n) != new.read(n))]
        assert changed == ['assets/offline/build.properties', 'assets/offline/program.zip'], changed
        programs = {}
        for mode, apk in [('old', old), ('new', new)]:
            with zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as bundle:
                assert bundle.testzip() is None
                assert not any(n.endswith(('.sqlite3', '.db')) or 'save' in Path(n).parts for n in bundle.namelist())
                bundle.extractall(WORK / mode)
                programs[mode] = {n: bundle.read(n) for n in bundle.namelist()}
        changed_program = [n for n in sorted(set(programs['old']) | set(programs['new']))
                           if programs['old'].get(n) != programs['new'].get(n)]
        assert set(changed_program) == {
            'network_redirect/formation.py', 'network_redirect/journey.py',
            'network_redirect/summon.py', 'server_config/formation_rules.json', 'payload-manifest.json'}
        config = json.loads(programs['new']['server_config/formation_rules.json'])['level_culture']
        assert config == dict(late_from_level=41, points_by_quality=RATES)
        manifest = json.loads(programs['new']['payload-manifest.json'])
        checked = 0
        for row in manifest['files']:
            if row['path'].startswith(('network_redirect/', 'server_config/')) and row['source'] == 'baseline':
                assert digest(ROOT / row['path']) == row['sha256'], row['path']
                checked += 1
        assert programs['old']['server_config/gift_code_rules.json'] == programs['new']['server_config/gift_code_rules.json']
    source = ROOT / '.runtime/opening-qa/after-all-tests.sqlite3'
    source_hash = digest(source)
    save = WORK / 'save'
    save.mkdir(exist_ok=True)
    database = save / 'game.sqlite3'
    with sqlite3.connect(source.as_uri() + '?mode=ro', uri=True) as src, sqlite3.connect(database) as dst:
        src.backup(dst)
    now = str(int(time.time()))
    run_worker(WORKER, 'old', save, now)
    before = database_snapshot(database)
    expected, changes = expected_migration(before)
    for _ in range(2):
        run_worker(WORKER, 'new', save, now)
        assert decoded_snapshot(database) == expected, 'Unexpected archived QA save change'
    # Add 50 synthetic companions only to a separate QA copy, then exercise both
    # legacy versions across every quality and the relevant level boundaries.
    matrix_save = WORK / 'matrix-save'
    matrix_save.mkdir(exist_ok=True)
    matrix_db = matrix_save / 'game.sqlite3'
    with sqlite3.connect(source.as_uri() + '?mode=ro', uri=True) as src, sqlite3.connect(matrix_db) as dst:
        src.backup(dst)
    run_worker(SEED, 'old', matrix_save, now)
    run_worker(WORKER, 'old', matrix_save, now)
    with sqlite3.connect(matrix_db) as db:
        for account, data in db.execute('SELECT account, data FROM roles').fetchall():
            role = json.loads(data)
            for c in role['corteges']:
                if 'qa_version' in c:
                    c['level_culture_version'] = c['qa_version']
            db.execute('UPDATE roles SET data=? WHERE account=?', (json.dumps(role), account))
    matrix_expected, matrix_changes = expected_migration(database_snapshot(matrix_db))
    for _ in range(2):
        run_worker(WORKER, 'new', matrix_save, now)
        assert decoded_snapshot(matrix_db) == matrix_expected, 'Unexpected synthetic QA save change'
    assert digest(source) == source_hash
    report = dict(apk_sha256=digest(APK), baseline_sha256=digest(WORK / 'baseline-v105.apk'),
                  changed_apk_entries=changed, changed_program_entries=changed_program,
                  current_source_files_verified=checked, level_culture=config,
                  all_51_gift_codes_preserved=True, contains_player_database=False,
                  archived_qa_roles=len(before['roles']), archived_migrations=changes,
                  matrix_companions=50, matrix_migrations=matrix_changes,
                  only_expected_version_markers_and_positive_topups_changed=True,
                  all_other_role_fields_and_database_tables_unchanged=True,
                  repeated_load_does_not_credit_again=True, source_qa_save_unchanged=True,
                  original_game_java_native_runtime_video_unchanged=True)
    destination = ROOT / 'analysis/evidence/v105_potential/payload-save-validation.json'
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('matrix_migrations', 'archived_migrations')},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
