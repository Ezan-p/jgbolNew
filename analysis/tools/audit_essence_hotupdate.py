"""Audit 1263 essence inputs, v107 native assets and future backend packaging.

Reads preserved original evidence; never opens player saves or overwrites APKs.
Optional Lua checks require lupa.lua51, e.g. PYTHONPATH=/private/tmp/jgbol-rank-lua.
"""
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from audit_hotupdate_gap import index, table
from luajit_static import parse, listing
from network_redirect import summon, combat, combat_power, immortal, spirit_array, journey
from offline_android.pack_payload import build_payload

OUT = ROOT/'analysis/evidence/essence_hotupdate'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    previous = json.loads((ROOT/'analysis/evidence/hotupdate_gap_20261031/audit.json').read_text())
    evidence = {row['logical']:row for row in previous['csv']}
    report = dict(date='2026-10-31', official_server_available=False, tables=[],
                  native_rendering_test=False, player_save_modified=False, released_apk_modified=False)
    apk = ROOT/'build/金箍棒3.87离线正式版v107.apk'
    with zipfile.ZipFile(apk) as a, zipfile.ZipFile(io.BytesIO(a.read('assets/offline/program.zip'))) as p:
        version, mapping = index(p.read('client/release_w/index.txt'))
        assert version == 1263
        def native(logical):
            path = 'client/release_w/' + mapping[logical]
            return p.read(path) if path in p.namelist() else a.read('assets/release_/' + mapping[logical])
        for name in sorted(summon.ESSENCE_HOTUPDATE_TABLES):
            logical = 'csv_config/' + name
            raw = (ROOT/'analysis/configs/essence_hotupdate'/name).read_bytes()
            original = (ROOT/'analysis/evidence/hotupdate_gap_20261031/official_csv'/name).read_bytes()
            assert raw == original, name
            assert sha(native(logical)) == evidence[logical]['original_sha256'], name
            rows = list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
            assert summon.rows(name) == rows
            assert table(native(logical)) == table(raw), name
            report['tables'].append(dict(name=name, sha256=sha(raw), rows=len(rows),
                versions=evidence[logical]['versions'], extracted_evidence_byte_match=True,
                original_sha256=evidence[logical]['original_sha256'], original_hash_verified=True,
                shipped_client_row_match=True, runtime_row_match=True,
                shipped_client_byte_match=native(logical)==raw))
        raw = native('lua/ui/jpmkUI.lua')
        dump = listing(parse(raw))
        (OUT/'jpmkUI.lua.txt').write_text(dump)
        assert "'MAX_JP'" in dump and "'fate_rebullding_jp_slots'" in dump
        report['native_lock_window'] = dict(sha256=sha(raw), source='v107 client release_w 1263',
            observed_static_max_jp=4, correction='set shared MAX_JP to 5 for unlocked extra slot; otherwise 4')
    assert combat.ESSENCES == immortal.ESSENCES
    assert combat_power.ESSENCE_PARAMS == {k:v['parameter'] for k,v in combat.ESSENCES.items()}
    assert immortal.LOCK_COST == {1:100, 2:300, 3:700, 4:1000}
    assert spirit_array.ESSENCE_MAP[111] == (16,0)
    report['mechanics'] = journey.load_rules()['battle']['mechanics']
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)/'backend.zip'
        manifest = build_payload(path)
        with zipfile.ZipFile(path) as z:
            for name in summon.ESSENCE_HOTUPDATE_TABLES:
                relative = 'analysis/configs/essence_hotupdate/' + name
                assert z.read(relative) == (ROOT/relative).read_bytes()
            for relative in ('network_redirect/essence_hotupdate_client.lua', 'network_redirect/immortal.py',
                             'network_redirect/combat.py', 'network_redirect/combat_engine.py',
                             'network_redirect/spirit_array.py', 'network_redirect/summon.py',
                             'server_config/journey_rules.json'):
                assert z.read(relative) == (ROOT/relative).read_bytes()
        report['payload'] = dict(verified=True, bundle_id=manifest['bundle_id'], temporary_only=True)
    from lupa.lua51 import LuaRuntime
    vm = LuaRuntime(unpack_returned_tuples=True)
    report['lua51_checks'] = list(vm.execute((ROOT/'tests/essence_hotupdate_client_regression.lua').read_text(),
                            (ROOT/'network_redirect/essence_hotupdate_client.lua').read_text()).values())
    vm.execute('assert(loadstring(...))', summon.client_source(summon.load_rules()))
    report['full_production_lua_compiles'] = True
    (OUT/'audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
