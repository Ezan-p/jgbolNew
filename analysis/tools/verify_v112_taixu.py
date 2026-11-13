"""Run the existing formal-v112 checks against the appended Taixu APK."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools import build_v112_taixu as build
from analysis.tools import verify_v112 as verify

for name in ('WORK', 'EVIDENCE', 'OUTPUT', 'BASE', 'digest', 'report'):
    setattr(verify, name, getattr(build, name))


def scope():
    verify.scope()
    root = build.WORK / 'payload-new'
    activity = json.loads((root / 'server_config/activity_rules.json').read_text())
    arena = json.loads((root / 'server_config/taixu_rules.json').read_text())
    expected = {1310:(10,1000),1311:(10,1000),1312:(10,1000),1313:(100,10),
                1314:(1000,5),1334:(2000,1),1320:(50,20),1321:(200,20),
                1322:(500,5),1323:(1000,3),1335:(2000,1)}
    assert activity['undergo_shop_revision'] == 'taixu-shop-2026-11-13-v5'
    assert {p['reward'][1]:(p['cost'],p['limit']) for p in activity['undergo_shop']} == expected
    assert all(p['reward'][2] == 1 for p in activity['undergo_shop'])
    assert arena['revision'] == 'offline-taixu-8'
    assert [(p['gold'],p['holy_peach'],p['crystals']) for p in arena['arena_rank_prizes']] == [
        (1500,200,20000),(800,100,15000),(500,50,10000),(300,10,5000)]
    assert arena['arena_win_prize_crystals'] == 100
    assert 'local_forfeit' in (root / 'network_redirect/taixu_client.lua').read_text()
    record = json.loads((build.EVIDENCE / 'scope-validation.json').read_text())
    record.update(taixu_shop_v5=True, arena_rewards_v8=True, confirmed_forfeit=True,
                  appended_feature_groups=3, feature_groups=12)
    build.report('scope-validation', record)
    print('Three appended Taixu updates and previous nine update groups verified')


def lua():
    verify.lua()
    from lupa.lua51 import LuaRuntime
    LuaRuntime().execute((build.WORK / 'tests/taixu_client_regression.lua').read_text())
    record = json.loads((build.EVIDENCE / 'lua-validation.json').read_text())
    record.update(taixu_exit_confirmation=True, taixu_shop_token=True)
    build.report('lua-validation', record)


def save():
    verify.save()
    import sqlite3
    import subprocess
    import tempfile
    from analysis.tools.verify_v110_payload import WORKER
    from analysis.tools.verify_v105_update import database_snapshot
    source = ROOT / '.runtime/opening-qa/after-all-tests.sqlite3'
    original_hash = build.digest(source.read_bytes())
    directory = Path(tempfile.mkdtemp(prefix='v112-save-upgrade-', dir=build.WORK))
    database = directory / 'game.sqlite3'
    with sqlite3.connect(source.as_uri() + '?mode=ro', uri=True) as old, sqlite3.connect(database) as new:
        old.backup(new)
    snapshots = []
    for mode in ('baseline','new','new'):
        result = subprocess.run([sys.executable, '-I', '-c', WORKER,
            str(build.WORK / ('payload-' + mode)), str(directory)],
            capture_output=True, text=True, timeout=180)
        assert result.returncode == 0, result.stderr
        snapshots.append(database_snapshot(database))
    assert snapshots[0] == snapshots[1] == snapshots[2]
    assert original_hash == build.digest(source.read_bytes())
    record = json.loads((build.EVIDENCE / 'payload-save-validation.json').read_text())
    record.update(previous_v112_to_new_v112_all_tables_equal=True,
                  previous_v112_restart_all_tables_equal=True)
    build.report('payload-save-validation', record)
    print('Previous formal v112 -> appended v112 -> restart: all account tables equal')


def merge():
    verify.merge()
    record = json.loads((build.EVIDENCE / 'protocol-validation.json').read_text())
    record['note'] = ('All shards passed against this exact APK; test IDs are deduplicated.'
        if not record['environment_recheck_test_ids'] else
        'Initial failures remain in shard logs; successful same-APK environment rechecks are recorded separately.')
    build.report('protocol-validation', record)


def recheck():
    verify.setup()
    import unittest
    failed = {name for path in build.EVIDENCE.glob('protocol-shard-*.json')
              for name in json.loads(path.read_text())['failed_test_ids']}
    previous_path = build.EVIDENCE / 'protocol-environment-recheck.json'
    previous = json.loads(previous_path.read_text()) if previous_path.exists() else None
    done = set(previous['test_ids']) if previous and previous['passed'] else set()
    assert not previous or previous['apk_sha256'] == build.digest(build.OUTPUT.read_bytes())
    names = sorted(failed - done)
    assert names, 'No remaining failed tests to recheck'
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
    build.report('protocol-environment-recheck',dict(apk_sha256=build.digest(build.OUTPUT.read_bytes()),
        passed=result.wasSuccessful() and not result.skipped, tests=len(done)+result.testsRun,
        failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),
        test_ids=sorted(done|set(names)),failed_test_ids=[c.id() for c,_ in result.failures+result.errors]))
    raise SystemExit(not result.wasSuccessful() or bool(result.skipped))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['protocol','merge','lua','save','recheck','scope'])
    parser.add_argument('--shard', type=int, choices=range(3))
    args = parser.parse_args()
    if args.mode == 'protocol':
        assert args.shard is not None
        verify.protocol(args.shard)
    elif args.mode in ('scope','lua','save','merge','recheck'):
        globals()[args.mode]()
    else:
        getattr(verify, args.mode)()
