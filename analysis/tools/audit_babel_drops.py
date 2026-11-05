"""Compare effective Babel drops to cached original resources; no player saves."""
import argparse
from collections import Counter
import csv
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import re
import sys
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity_babel as babel, summon
from audit_hotupdate_gap import index


def rows(raw):
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'), newline=None)))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', type=Path, default=Path('/private/tmp/jgb-hotupdate'))
    args = parser.parse_args()
    evidence = ROOT / 'analysis/evidence/hotupdate_gap_20261031'
    manifest = (evidence / 'update_list.txt').read_bytes()
    packages = [(int(a), int(b), name, int(size), md5)
                for a, b, name, size, md5 in re.findall(
                    r'\{\s*(\d+),\s*(\d+),\s*"([^"]+)",\s*(\d+),\s*"([a-f0-9]+)"', manifest.decode())
                if 1205 <= int(a) < int(b) <= 1263]
    base = ROOT / 'jgbol3.87/assets/release_'
    version, original_index = index((base / 'index.txt').read_bytes())
    assert version == 1205
    current = original_index
    available = {name: (base / name, None) for name in set(current.values())}
    package_checks = []
    for start, end, filename, size, md5 in packages:
        assert start == version
        path = args.cache / filename
        raw = path.read_bytes()
        assert len(raw) == size and hashlib.md5(raw).hexdigest() == md5, filename
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            assert archive.testzip() is None, filename
            version, current = index(archive.read('index.txt'))
            assert version == end
            for name in archive.namelist():
                if name.endswith('.data'):
                    available[name] = (path, name)
        package_checks.append(dict(file=filename, version=end, sha256=sha(raw), size_md5_crc_match=True))
    assert version == 1263 and len(package_checks) == 56

    def original(name):
        physical = current['csv_config/' + name]
        path, member = available[physical]
        if member is None:
            return path.read_bytes()
        with zipfile.ZipFile(path) as archive:
            return archive.read(member)

    tables = {}
    for name in ('babel_tower_floor_prize.csv', 'babel_secret_tower_floor_prize.csv',
                 'tongtianta_score_awards.csv'):
        raw = original(name)
        active = (ROOT / 'analysis/configs/babel_hotupdate' / name).read_bytes()
        assert active == raw == (evidence / 'official_csv' / name).read_bytes(), name
        assert summon.rows(name) == rows(raw), name
        tables[name] = dict(rows=len(rows(raw)), sha256=sha(raw), byte_match=True, runtime_rows_match=True,
                            logical_resource='csv_config/' + name,
                            physical_resource=current['csv_config/' + name])
    assert babel.FLOORS == rows(original('babel_tower_floor_prize.csv'))
    assert babel.SECRET_FLOORS == rows(original('babel_secret_tower_floor_prize.csv'))
    old_raw = (base / original_index['csv_config/babel_tower_floor_prize.csv']).read_bytes()
    assert rows(old_raw) == babel.FLOORS[:12]
    assert rows(old_raw) == rows((ROOT / 'analysis/configs/babel_tower_floor_prize.csv').read_bytes())

    original_names = {int(r['Ftype_id']): r['name'] for r in rows(original('item_name.csv'))}
    names = {int(r['Ftype_id']): r['name'] for r in summon.rows('item_name.csv')}
    original_items = {int(r['type_id']): r for r in rows(original('item_base.csv'))}
    items = {int(r['type_id']): r for r in summon.rows('item_base.csv')}
    rules = json.loads((ROOT / 'server_config/activity_rules.json').read_text())
    groups, floors, probes = [], [], 0
    for secret, source in ((False, babel.FLOORS), (True, babel.SECRET_FLOORS)):
        for row in source:
            specs = [list(map(int, value.split('|'))) for value in row['daoju'].split('/')]
            normalized = [spec if len(spec) == 4 else spec + [1] for spec in specs]
            weights = [babel.floor_reward_weight(spec, secret) for spec in normalized]
            weighted = [spec for spec, weight in zip(normalized, weights) for _ in range(weight)]
            draw_pool = weighted if not secret and any(spec[:2] == [5, 1246] for spec in normalized) else normalized
            counts = Counter(map(tuple, normalized))
            entries = []
            for spec in specs:
                typ, tid, count = spec[:3]
                assert typ == 5 and names[tid] == original_names[tid]
                assert items[tid] == original_items[tid], tid
                entries.append(dict(raw='|'.join(map(str, spec)), item_id=tid, name=names[tid],
                                    count=count, level=spec[3] if len(spec) == 4 else 1,
                                    local_entry_probability=str(Fraction(babel.floor_reward_weight(spec, secret), sum(weights)))))
            group = dict(secret=secret, floor_l=int(row['floor_l']), floor_r=int(row['floor_r']),
                         entries=entries, entry_count=len(specs),
                         duplicate_specs=[dict(spec=list(spec), occurrences=n,
                                               local_probability=str(Fraction(n * babel.floor_reward_weight(list(spec), secret), sum(weights))))
                                          for spec, n in counts.items() if n > 1])
            groups.append(group)
            for floor in range(group['floor_l'], group['floor_r'] + 1):
                # Force each entry once, verifying the real grant/inventory path.
                for selected in normalized:
                    role = dict(attachments=[], summon={})
                    state = dict(cur_floor=floor, secret=secret, coin_count=0)
                    def choose(pool):
                        assert pool == draw_pool, (floor, pool)
                        return selected
                    with patch.object(babel.secrets, 'choice', side_effect=choose):
                        reward = babel.floor_reward(role, state, rules)
                    extra = [] if secret else [[5, 20000, rules['babel_cell_coins'], 1]]
                    expected = [selected] + extra
                    assert reward == [dict(zip(('object_type', 'attach_type', 'attach_count', 'attach_level'), spec))
                                      for spec in expected]
                    inventory = Counter()
                    for item in role['attachments']:
                        inventory[item['type_id']] += item['count']
                    assert inventory == Counter({spec[1]: spec[2] for spec in expected})
                    probes += 1
                floors.append(dict(floor=floor, secret=secret, entries=entries,
                                   local_extra_coins=0 if secret else rules['babel_cell_coins']))
    assert [f['floor'] for f in floors] == list(range(1, 71)) + list(range(1001, 1016))
    report = dict(date='2026-11-04',passed=True,source='cached original 1205→1263 resource chain',
                  original_server_observed=False,manifest_sha256=sha(manifest),packages=package_checks,
                  tables=tables,base_1205_floor_table_sha256=sha(old_raw),
                  first_60_floors_unchanged_from_1205=True,item_names_and_definitions_match=True,
                  runtime_grant_probes=probes,groups=groups,floors=floors,
                  caveat='Entry probabilities, trigger locations and extra coins are local rules, not original server evidence.')
    out = ROOT / 'analysis/evidence/babel_drops_20261104'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(dict(passed=True, packages=len(packages), tables=len(tables),
                         normal_floors=70, secret_floors=15, runtime_grant_probes=probes), ensure_ascii=False))


if __name__ == '__main__':
    main()
