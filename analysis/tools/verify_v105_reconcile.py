"""Check the actual v105 v3 APK and migrate QA copies with an independent oracle."""
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
from network_redirect import formation, reborn, summon

WORK = ROOT / '.runtime/v105-reconcile-qa'
EVIDENCE = ROOT / 'analysis/evidence/v105_reconcile'
APK = WORK / '金箍棒3.87-离线单机-arm32-v105.apk'
RATES = {1: (1, 2), 2: (3, 4), 3: (5, 7), 4: (7, 10), 5: (10, 15)}
STATS = ('hp', 'gongji', 'fangyu', 'magic')

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
        for level in (1, 39, 40, 41, 155, 200):
            for version in (0, 1, 2):
                for balance, trained in ((10000, 0), (3, 20000), (0, 0)):
                    c = summon.companion(role, tid)
                    c.update(level=level, culture_point=balance, hp_plus=trained // 2,
                             gongji_plus=trained // 4, fangyu_plus=trained // 8, magic_plus=trained // 8,
                             evolve_level=2 if level >= 155 else 0,
                             reborn_layer=1 if level >= 155 else 0, cur_exp=0,
                             qa_version=version, pending_training=dict(points=3, deltas=dict(hp=3)))
                    role['corteges'].append(c)
    formation.prepare(role, b.formation_rules)
    b.save(role, account, gameplay=False)
    b.close()
'''


def run_worker(script, mode, save, now):
    result = subprocess.run([sys.executable, '-I', '-c', script, str(WORK / mode), str(save), now],
                            capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr


def expected_migration(snapshot):
    expected = copy.deepcopy(snapshot)
    changes = []
    roles = []
    for account, data in snapshot['roles']:
        role = json.loads(data)
        for c in role['corteges']:
            version = c.get('level_culture_version', 0)
            if version >= 3:
                continue
            quality = int(summon.BASES[c['type']]['quality'])
            early, late = RATES[quality]
            def interval(first, last):
                return sum(early if n <= 40 else late for n in range(first + 1, last + 1))
            components = dict(ordinary=interval(1, c['level']), rebirth_cycles=0, evolution=0, rebirth=0)
            for n in range(1, c.get('reborn_layer', 0) + 1):
                row = reborn.LAYERS[n]
                components['rebirth_cycles'] += interval(int(row['reset_level']), int(row['min_level']))
                components['rebirth'] += int(row['ret_culture'])
            components['evolution'] = sum(int(row['culture_point'])
                for row in summon.rows('cortege_evolve_config.csv')
                if int(row['cortege_quality']) == quality and 1 <= int(row['level']) <= c.get('evolve_level', 0))
            # Test fixtures use <=2 evolutions, avoiding the CSV's repeated level-120 row.
            assert c.get('evolve_level', 0) <= 2
            budget = sum(components.values())
            original = {s: c.get(s + '_plus', 0) for s in STATS}
            spent = sum(original.values())
            available = c.get('culture_point', 0)
            if spent > budget:
                allocation = {s: divmod(original[s] * budget, spent) for s in STATS}
                remaining = budget - sum(v[0] for v in allocation.values())
                winners = sorted(STATS, key=lambda s: (-allocation[s][1], STATS.index(s)))[:remaining]
                for s in STATS:
                    c[s + '_plus'] = allocation[s][0] + int(s in winners)
            c['culture_point'] = max(0, budget - spent)
            c['level_culture_version'] = 3
            c['level_culture_migration'] = dict(previous_version=version, previous_available=available,
                previous_training=original, budget=components, total_adjustment=budget - available - spent)
            changes.append(dict(version=version, quality=quality, level=c['level'],
                                adjustment=budget - available - spent, training_reduced=spent > budget))
        # Only derived panel/power fields may follow the corrected training.
        # The migration itself above never calls production migration functions.
        formation.recalculate(role, formation.load_rules())
        roles.append((account, role))
    expected['roles'] = roles
    return expected, changes


def decoded_snapshot(database):
    snapshot = database_snapshot(database)
    snapshot['roles'] = [(a, json.loads(d)) for a, d in snapshot['roles']]
    return snapshot


def check_save(source, name, matrix=False):
    save = WORK / name
    save.mkdir(exist_ok=True)
    database = save / 'game.sqlite3'
    with sqlite3.connect(source.as_uri() + '?mode=ro', uri=True) as src, sqlite3.connect(database) as dst:
        src.backup(dst)
    now = str(int(time.time()))
    run_worker(SEED if matrix else WORKER, 'old', save, now)
    run_worker(WORKER, 'old', save, now)
    if matrix:
        with sqlite3.connect(database) as db:
            for account, data in db.execute('SELECT account, data FROM roles').fetchall():
                role = json.loads(data)
                for c in role['corteges']:
                    if 'qa_version' in c:
                        c['level_culture_version'] = c['qa_version']
                db.execute('UPDATE roles SET data=? WHERE account=?', (json.dumps(role), account))
    expected, changes = expected_migration(database_snapshot(database))
    for attempt in range(2):
        run_worker(WORKER, 'new', save, now)
        actual = decoded_snapshot(database)
        assert actual == expected, f'Unexpected save change: {name}, load {attempt + 1}'
    return dict(roles=len(expected['roles']), migrated=len(changes),
                debit_cases=sum(c['adjustment'] < 0 for c in changes),
                topup_cases=sum(c['adjustment'] > 0 for c in changes),
                training_reduction_cases=sum(c['training_reduced'] for c in changes))


def main():
    with zipfile.ZipFile(WORK / 'baseline-v105.apk') as old, zipfile.ZipFile(APK) as new:
        changed = [n for n in sorted(set(old.namelist()) | set(new.namelist()))
                   if not n.startswith('META-INF/') and
                   (n not in old.namelist() or n not in new.namelist() or old.read(n) != new.read(n))]
        assert changed == ['assets/offline/build.properties', 'assets/offline/program.zip'], changed
        programs = {}
        for mode, apk in [('old', old), ('new', new)]:
            assert apk.testzip() is None
            with zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as bundle:
                assert bundle.testzip() is None
                assert not any(n.endswith(('.sqlite3', '.db')) or 'save' in Path(n).parts for n in bundle.namelist())
                bundle.extractall(WORK / mode)
                programs[mode] = {n: bundle.read(n) for n in bundle.namelist()}
        changed_program = [n for n in sorted(set(programs['old']) | set(programs['new']))
                           if programs['old'].get(n) != programs['new'].get(n)]
        assert set(changed_program) == {'network_redirect/formation.py', 'network_redirect/summon.py',
                                        'server_config/formation_rules.json', 'payload-manifest.json'}, changed_program
        manifest = json.loads(programs['new']['payload-manifest.json'])
        checked = 0
        for row in manifest['files']:
            if row['path'].startswith(('network_redirect/', 'server_config/')) and row['source'] == 'baseline':
                assert digest(ROOT / row['path']) == row['sha256'], row['path']
                checked += 1
        assert programs['new']['offline_client.lua'].decode() == summon.client_source(summon.load_rules())
        assert programs['old']['server_config/gift_code_rules.json'] == programs['new']['server_config/gift_code_rules.json']
    source = ROOT / '.runtime/opening-qa/after-all-tests.sqlite3'
    source_hash = digest(source)
    archived = check_save(source, 'save')
    matrix = check_save(source, 'matrix-save', matrix=True)
    assert digest(source) == source_hash
    report = dict(apk_sha256=digest(APK), baseline_sha256=digest(WORK / 'baseline-v105.apk'),
                  changed_apk_entries=changed, changed_program_entries=changed_program,
                  current_source_files_verified=checked, generated_client_matches=True,
                  all_51_codes_preserved=True, contains_player_database=False,
                  archived_qa=archived, matrix_synthetic_companions=270, matrix_qa=matrix,
                  only_expected_potential_training_audit_and_derived_power_changed=True,
                  all_other_role_fields_and_database_tables_unchanged=True,
                  repeated_load_identical=True, source_qa_save_unchanged=True,
                  original_game_java_native_runtime_video_unchanged=True)
    (EVIDENCE / 'payload-save-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
