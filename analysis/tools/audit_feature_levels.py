"""Reproducible level-gate inventory from original 3.87 assets, without execution."""
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from luajit_static import parse, decode, listing
from network_redirect import feature_levels

OUT = ROOT / 'analysis/evidence/feature_levels'


def audit():
    index = dict(line.split('====')[:2] for line in
                 (ROOT / 'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    modules, snippets, activities, recovered = [], [], {}, {}
    for logical, resource in sorted(index.items()):
        if not logical.startswith('lua/') or not logical.endswith('.lua'):
            continue
        raw = (ROOT / 'jgbol3.87/assets/release_' / resource).read_bytes()
        if not raw.startswith(b'\x1bLJ\x01'):
            continue
        chunk = parse(raw)
        functions = []
        for p in chunk['protos']:
            strings = [v for v in p['kgc'] if isinstance(v, str)]
            fields = sorted({v for v in strings if re.search(
                r'level|Level|LEVEL|Lvlimit|RequireLv|UnlockLv|cheer_level|needLv', v)})
            if fields:
                functions.append(dict(line=p['line'], last_line=p['last_line'], fields=fields))
            if logical == 'lua/ui/activityUI.lua':
                for v in p['kgc']:
                    if isinstance(v, dict) and v.get('kind') == 'table' and 'fengshenbang' in v['value']:
                        activities = v['value']
                if p['line'] == 1492:
                    code = [decode(x) for x in p['code']]
                    for i, (op, a, b, c, d) in enumerate(code):
                        if op == 'TGETS' and p['kgc'][c] in feature_levels.ACTIVITY_LEVELS:
                            name = p['kgc'][c]
                            if name == 'friends':
                                continue  # region-dependent 1 / 15, recorded separately
                            constants = [v[4] for v in code[i+1:i+5] if v[0] == 'KSHORT']
                            if constants:
                                recovered[name] = constants[0]
        if functions:
            modules.append(dict(logical=logical, asset=resource,
                                sha256=hashlib.sha256(raw).hexdigest(), functions=functions))
        # Preserve the complete relevant gate functions as auditable bytecode.
        if logical in {'lua/ui/activityUI.lua', 'lua/ui/petUI.lua', 'lua/ui/packageUI.lua',
                       'lua/ui/worldTreeUI.lua', 'lua/ui/undergoOrdealUI.lua',
                       'lua/ui/mainUI.lua', 'lua/ui/stoneUI.lua', 'lua/ui/xianmengUI.lua'}:
            text = listing(chunk)
            # listing returns plain text, including original source-line markers.
            for section in re.split(r'(?=FUNCTION proto)', text):
                if any(s in section for s in ("'getRequireLevel'", "'pet_open_level'",
                       "'g_playerInfo'", "'Lvlimit'", "'g_cross_min_level'")):
                    snippets.append(logical + '\n' + section)
    assert len(activities) == 43, len(activities)
    expected = {k: v for k, v in feature_levels.ACTIVITY_LEVELS.items()
                if k not in ('friends', 'tongtianta')}
    assert recovered == expected, (recovered, expected)
    encodings = {r['logical']: r['encoding'] for r in json.loads(
        (ROOT / 'analysis/evidence/config_inventory.json').read_text())}
    tables = []
    for logical, resource in sorted(index.items()):
        if not logical.startswith('csv_config/') or not logical.endswith('.csv'):
            continue
        extracted = ROOT / 'analysis/configs' / logical.removeprefix('csv_config/')
        if not extracted.exists():
            continue
        raw = (ROOT / 'jgbol3.87/assets/release_' / resource).read_bytes()
        encoding = encodings[logical]
        local_text = extracted.read_bytes().decode('utf-8-sig')
        original_text = raw.decode(encoding)
        # rune.csv embeds bare CR inside unquoted descriptions; LF alone
        # separates records (same rule as role_profile.RUNES).
        if logical == 'csv_config/rune.csv':
            local_text = local_text.replace('\r', '')
            original_text = original_text.replace('\r', '')
        rows = list(csv.reader(io.StringIO(local_text, newline=None)))
        if not rows:
            continue
        columns = [i for i, key in enumerate(rows[0]) if re.search(
            r'require_level|min_role_level|active_level|open_level|min_level|need_role_level|cortege_count', key)]
        if not columns:
            continue
        original = list(csv.reader(io.StringIO(original_text, newline=None)))
        assert original == rows, logical
        tables.append(dict(logical=logical, asset=resource, sha256=hashlib.sha256(raw).hexdigest(),
                           rows=len(rows)-1, csv_values_match=True,
                           fields={rows[0][i]: sorted({row[i] for row in rows[1:] if len(row)>i}) for i in columns}))
    return dict(client='3.87', official_server_available=False,
                activity_ids=activities, recovered_fixed_activity_levels=recovered,
                regional_exception={'friends': {'default': 15, 'isTW': 1}},
                dynamic_activity_levels=['snowman', 'dream', 'alchemy', 'summer', 'destiny'],
                separate_activity_check={'tongtianta': 36},
                modules=modules, tables=tables), snippets


if __name__ == '__main__':
    report, snippets = audit()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'official_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    (OUT / 'gate_bytecode.txt').write_text('\n'.join(snippets))
    print(f"Verified {len(report['activity_ids'])-1} activity IDs, "
          f"{len(report['modules'])} modules with level references, {len(report['tables'])} original CSV tables")
