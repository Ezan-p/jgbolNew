"""Reproduce formation evidence from unmodified original 3.87 assets.

No Lua execution. Numeric constant pools accompany listings so MULVN operands
are not mistaken for literal values. Run: python3 analysis/tools/audit_formation_rules.py
"""
import csv
import io
import hashlib
import json
import re
from pathlib import Path
from luajit_static import parse, listing

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'analysis/evidence'
ASSETS = ROOT / 'jgbol3.87/assets/release_'
FUNCTIONS = {
    'ui/charPositionUI': ['changeCharOrderSucceed', 'changeCharSucceed'],
    'ui/lineupUI': ['getDateFormServer', 'updateCharacterInfo', 'updateSkillInfo'],
    'ui/trainingUI': ['onGetDirectResult', 'confirmResult', 'updateCharacterInfo'],
    'ui/inheritUI': ['makeCharacterTableWithTag', 'recvInheritMsg'],
    'ui/expbookUI': ['getExpResult', 'getMaxLimitLevel', 'createExpbookMutilSelectLayer'],
    'ui/skillUpgradeUI': ['showServerRet'],
    'ui/equipAdvanceUI': ['showAdvanceInfoLayer', 'afterFakeShow'],
}
TABLES = ['cortege_base_0', 'skill_base', 'item_base', 'role_level_config',
          'cortege_experience', 'cortege_quality', 'cortege_evolution',
          'cortege_evolve_config', 'cortege_devolve', 'fate_config',
          'equip_enhance_cost', 'equip_enhance_weight',
          'skill_enhance_cost', 'skill_enhance_worth', 'equip_star_cost',
          'equip_advance_cost', 'equip_advance_worth']


def main():
    index = {p[0]: p[1] for line in (OUT / 'resource_index.decoded.txt').read_text().splitlines()
             if len(p := line.split('====')) == 3}
    inputs, excerpts = [], []
    encodings = {r['logical']: r['encoding'] for r in json.loads((OUT / 'config_inventory.json').read_text())}
    names = ['lua/' + n + '.lua' for n in FUNCTIONS]
    names += ['lua/ui/equipmentUpgradeUI.lua', 'lua/common/common_def.lua',
              'lua/common/msg_def.lua', 'lua/event_mgr.lua']
    names += [next(k for k in index if k.startswith('csv_config/') and Path(k).name == n + '.csv') for n in TABLES]
    for name in names:
        path = ASSETS / index[name]
        inputs.append(dict(logical=name, physical=str(path.relative_to(ROOT)),
                           sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
        if not name.endswith('.lua'):
            extracted = ROOT / 'analysis/configs' / name.removeprefix('csv_config/')
            original_rows = list(csv.reader(io.StringIO(path.read_bytes().decode(encodings[name]))))
            extracted_rows = list(csv.reader(io.StringIO(extracted.read_text(encoding='utf-8-sig'))))
            assert original_rows == extracted_rows, name
            inputs[-1]['extracted_sha256'] = hashlib.sha256(extracted.read_bytes()).hexdigest()
            inputs[-1]['csv_values_match'] = True
    for name, funcs in FUNCTIONS.items():
        chunk = parse((ASSETS / index['lua/' + name + '.lua']).read_bytes())
        root = listing(dict(source=chunk['source'], root=chunk['root'],
                            protos=[chunk['protos'][chunk['root']]]))
        lines = root.splitlines()
        for func in funcs:
            target = None
            for i, line in enumerate(lines):
                if 'GSET' in line and "'" + func + "'" in line:
                    for prior in reversed(lines[max(0, i - 4):i]):
                        match = re.search(r"FNEW.*'id': (\d+)", prior)
                        if match:
                            target = chunk['protos'][int(match[1])]
                            break
            assert target is not None, (name, func)
            excerpts.append('%s.%s NUMERIC CONSTANTS: %s' % (name, func, target['numbers']))
            excerpts.append(listing(dict(source=chunk['source'], root=target['id'], protos=[target])))
    # Explicit source-line arithmetic checks used by the implementation.
    for name, ident in [('ui/inheritUI', 21), ('ui/expbookUI', 24), ('ui/equipmentUpgradeUI', 26)]:
        c = parse((ASSETS / index['lua/' + name + '.lua']).read_bytes())
        p = c['protos'][ident]
        excerpts.append('%s proto%d NUMERIC CONSTANTS: %s' % (name, ident, p['numbers']))
        excerpts.append(listing(dict(source=c['source'], root=ident, protos=[p])))
    (OUT / 'formation_official_bytecode.txt').write_text('\n'.join(excerpts), encoding='utf-8')
    report = dict(date='2026-10-24', client='3.87', inputs=inputs,
                  implemented_requests=[1024, 1025, 1037, 1052, 1059, 1071, 1073, 1081, 1082, 1083, 1084, 1089, 1343],
                  source_classes={'A': 'Original client protocol, UI branches and CSV values',
                                  'B': 'Inferred server settlement; never claimed to be official'},
                  inference_config='server_config/formation_rules.json',
                  inference_sha256=hashlib.sha256((ROOT / 'server_config/formation_rules.json').read_bytes()).hexdigest(),
                  documentation='docs/阵容模块规则与调试.md',
                  official_server_available=False)
    (OUT / 'formation_official_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Wrote formation_official_audit.json and formation_official_bytecode.txt')


if __name__ == '__main__':
    main()
