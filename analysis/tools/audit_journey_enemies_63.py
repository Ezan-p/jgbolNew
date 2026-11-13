"""Compare journey enemies to original 3.87 resources, including v111 payloads.

Reads configuration and constructs snapshots only; never opens a player save.
Run from any directory with the repository's Python environment.
"""
import csv
from decimal import Decimal, ROUND_FLOOR
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import combat_engine, journey
from network_redirect.protocol import decode, encode

OUT = ROOT / 'analysis/evidence/journey_enemies_63_20261112.json'


def main():
    index = {p[0]: p[1] for line in (ROOT / 'analysis/evidence/resource_index.decoded.txt').read_text().splitlines()
             if len(p := line.split('====')) == 3}
    encodings = {r['logical']: r['encoding'] for r in json.loads(
        (ROOT / 'analysis/evidence/config_inventory.json').read_text())}
    names = ['map_config.csv', 'map_name.csv', 'tollgate_config.csv', 'tollgate_name.csv',
             'elite/elite_map_config.csv', 'elite/elite_map_name.csv',
             'elite/elite_tollgate_config.csv', 'elite/elite_tollgate_name.csv',
             'elite/elite_cortege_base.csv', 'elite/elite_cortege_name.csv',
             'skill_base.csv', 'skill_name.csv']
    names += ['cortege/' + p.name for p in sorted((ROOT / 'analysis/configs/cortege').glob('*.csv'))
              if p.name.startswith(('cortege_base_', 'cortege_name_'))]
    records, originals = [], {}
    for name in names:
        logical = 'csv_config/' + name
        path = ROOT / 'jgbol3.87/assets/release_' / index[logical]
        raw = path.read_bytes()
        original = list(csv.reader(io.StringIO(raw.decode(encodings[logical]))))
        current = list(csv.reader(io.StringIO((ROOT / 'analysis/configs' / name).read_text(encoding='utf-8-sig'))))
        assert original == current, ('CSV differs from original', name)
        originals[name] = [{k.split('(')[0]: v for k, v in zip(original[0], row)} for row in original[1:]]
        records.append(dict(logical=logical, physical=str(path.relative_to(ROOT)),
                            sha256=hashlib.sha256(raw).hexdigest(), rows=len(original) - 1,
                            csv_values_match=True))

    def keyed(name, key):
        return {int(r[key]): r for r in originals[name]}

    npcs, npc_names = {}, {}
    for name in names:
        if name.startswith('cortege/cortege_base_') or name == 'elite/elite_cortege_base.csv':
            for tid, row in keyed(name, 'type_id').items():
                assert tid not in npcs or npcs[tid] == row, ('conflicting NPC ID', tid)
                npcs[tid] = row
        if name.startswith('cortege/cortege_name_') or name == 'elite/elite_cortege_name.csv':
            npc_names.update(keyed(name, 'type_id'))
    skills = keyed('skill_base.csv', 'type_id')
    skill_names = keyed('skill_name.csv', 'type_id')
    gates = {1: keyed('tollgate_config.csv', 'id'),
             2: keyed('elite/elite_tollgate_config.csv', 'tollgate_id')}
    gate_names = {1: keyed('tollgate_name.csv', 'id'), 2: keyed('elite/elite_tollgate_name.csv', 'id')}
    maps = keyed('map_name.csv', 'id')
    rules = journey.load_rules()
    details, passive_adjustments, counts, wire_checks = [], [], {}, 0
    stat_columns = {'hp': ('base_max_hp', 'base_maxhp_plus'),
                    'gongji': ('base_gongji', 'base_gongji_plus'),
                    'fangyu': ('base_fangyu', 'base_fangyu_plus'),
                    'magic': ('base_max_magic', 'base_maxmagic_plus')}
    floor = lambda n: int(n.to_integral_value(rounding=ROUND_FLOOR))
    for kind, catalog in gates.items():
        assert catalog == journey.GATES[kind], ('loaded gate catalog differs', kind)
        total_enemies = 0
        for gid, cfg in catalog.items():
            actual = journey.fighters({'corteges': []}, journey.GATES[kind][gid])[1]
            expected, entries = [], []
            for order, token in enumerate(cfg['cortege_list'].split('/'), 1):
                parts = token.split('|')
                tid, level = map(int, parts[:2])
                if tid == 8888:
                    entries.append(dict(order=order, type_id=tid, placeholder=True))
                    continue
                base = npcs[tid]
                assert base == journey.NPCS[tid], ('loaded NPC differs', tid)
                skill_ids = list(map(int, parts[2].split('+'))) if len(parts) > 2 and parts[2] else [int(base['chushijineng'])]
                skill_level = int(cfg.get('skill_level', 1))
                for sid in skill_ids:
                    # Current SKILLS preserves full annotated column headers.
                    assert all(v == journey.formation.SKILLS[sid][next(
                        col for col in journey.formation.SKILLS[sid] if col.split('(')[0] == k)]
                               for k, v in skills[sid].items()), ('loaded skill differs', sid)
                raw_stats = {stat: max(1, int(Decimal(base[col]) + Decimal(base[growth]) * (level - 1)))
                             for stat, (col, growth) in stat_columns.items()}
                rates = {stat: 0 for stat in raw_stats}
                for sid in skill_ids:
                    skill = skills[sid]
                    if skill['use_mode'] == '2':
                        stat, column = {1: ('gongji', 'gongji_plus'), 2: ('fangyu', 'fangyu_plus'),
                                        3: ('magic', 'magic_plus'), 5: ('hp', 'hp_plus')}.get(
                                            int(skill['effect_field']), (None, None))
                        if stat:
                            rates[stat] += floor(Decimal(skill[column]) + Decimal(skill['upgrade_plus']) * (skill_level - 1))
                settled = {stat: value * (100 + rates[stat]) // 100 for stat, value in raw_stats.items()}
                unit = dict(type=tid, order=order, level=level, evolve=0, reborn=0,
                            skills=[(sid, skill_level) for sid in skill_ids], **settled, max_hp=settled['hp'])
                expected.append(unit)
                entry = dict(order=order, type_id=tid, name=npc_names[tid]['name'],
                             base_type_id=int(base['base_type_id']), resource=int(base['resource']),
                             level=level, skills=[dict(id=sid, name=skill_names[sid]['name'], level=skill_level)
                                                  for sid in skill_ids],
                             original_stats=raw_stats, current_stats=settled)
                entries.append(entry)
                if raw_stats != settled:
                    passive_adjustments.append(dict(kind=kind, gate_id=gid, **entry))
            assert expected == actual, ('generated enemy snapshot differs', kind, gid)
            total_enemies += len(actual)
            if int(cfg['map_id']) >= 63:
                # No player unit: run() produces the real initial roster without
                # executing battle turns. Verify protocol slots, including holes.
                _, lineup, _ = combat_engine.Battle({'corteges': []}, ([], actual), rules).run()
                wire = decode(encode(1028, dict(lineup_count=len(lineup), lineup=lineup)))[2]['lineup']
                for entry in entries:
                    row = wire[entry['order'] - 1] if entry['order'] <= len(wire) else {}
                    if entry.get('placeholder'):
                        assert row.get('des_type', 0) == row.get('des_hp', 0) == row.get('des_max_hp', 0) == 0
                    else:
                        assert row['des_type'] == entry['type_id'] and row['des_level'] == entry['level']
                        assert row['des_hp'] == row['des_max_hp'] == entry['current_stats']['hp']
                        assert row['des_magic'] == entry['current_stats']['magic']
                wire_checks += 1
                details.append(dict(kind=kind, map_id=int(cfg['map_id']), map_name=maps[int(cfg['map_id'])]['name'],
                                    gate_id=gid, gate_name=gate_names[kind][gid]['name'], enemies=entries))
        ordered = []
        chapter_maps = keyed('map_config.csv' if kind == 1 else 'elite/elite_map_config.csv', 'id')
        mid = next(mid for mid, m in chapter_maps.items() if m['pre_map'] == '0')
        while mid:
            gid = int(chapter_maps[mid]['first_tollgate'])
            while gid:
                assert gid not in ordered
                ordered.append(gid)
                gid = int(catalog[gid]['next_tollgate'])
            mid = int(chapter_maps[mid]['next_map'])
        assert set(ordered) == set(catalog)
        counts[kind] = dict(gates=len(catalog), actual_enemies=total_enemies,
                            ordinal_63_gate=ordered[62], gates_from_ordinal_63=len(ordered[62:]),
                            chapter_63_onwards=sum(int(g['map_id']) >= 63 for g in catalog.values()))

    apk_reports = []
    code_paths = ['network_redirect/' + n + '.py' for n in
                  ('journey', 'summon', 'formation', 'combat', 'combat_engine', 'combat_loadout', 'role_profile', 'protocol')]
    for filename in ('金箍棒ol离线正式版v111.apk', '金箍棒ol测试版-v111.apk'):
        path = ROOT / 'build' / filename
        with zipfile.ZipFile(path) as apk:
            for source in records:
                original_path = ROOT / source['physical']
                assert apk.read('assets/release_/' + original_path.name) == original_path.read_bytes(), (
                    'APK client resource differs', filename, source['logical'])
            with zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as payload:
                checks = ['analysis/configs/' + name for name in names] + code_paths
                for name in checks:
                    assert payload.read(name) == (ROOT / name).read_bytes(), ('APK payload differs', filename, name)
        apk_reports.append(dict(path=str(path.relative_to(ROOT)), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                                checked_files=len(checks), all_match_workspace=True,
                                client_original_csvs_checked=len(records), all_client_csvs_match_original=True))

    report = dict(date='2026-11-12', original_client='repository packaged 3.87 resources',
                  official_server_available=False, tables_checked=len(records), inputs=records,
                  full_catalog=counts, target_gate_count=len(details), target_wire_snapshots_checked=wire_checks,
                  target_actual_enemies=sum(sum(not e.get('placeholder', False) for e in d['enemies']) for d in details),
                  target_passive_adjustments=[a for a in passive_adjustments if int(gates[a['kind']][a['gate_id']]['map_id']) >= 63],
                  all_passive_adjustment_count=len(passive_adjustments), apk_payloads=apk_reports,
                  limitations=['NPC passive inclusion is inferred; original server may already include it in base stats.',
                               'Elite skill level 1 is a local default; original elite gate CSV has no skill_level column.',
                               'Snapshot audit does not validate original server damage, difficulty, or live installed APK.'],
                  gates=details)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('tables_checked', 'full_catalog', 'target_gate_count',
                                           'target_wire_snapshots_checked', 'target_actual_enemies',
                                           'all_passive_adjustment_count')}, ensure_ascii=False, indent=2))
    print('Report:', OUT.relative_to(ROOT))


if __name__ == '__main__':
    main()
