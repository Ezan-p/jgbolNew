"""Reproducible static evidence for the summon client/server boundary.

Reads only this repository's original APK assets; never executes game Lua or
infers a probability distribution from the preview table.
"""
import csv
import hashlib
import io
import json
from pathlib import Path

from luajit_static import parse, listing

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'jgbol3.87/assets/release_'
EVIDENCE = ROOT / 'analysis/evidence'


def main():
    index = dict((parts[0], parts[1]) for line in
                 (EVIDENCE / 'resource_index.decoded.txt').read_text().splitlines()
                 if len(parts := line.split('====')) == 3)
    wanted = ['lua/ui/summonUI.lua', 'lua/common/common_def.lua',
              'lua/common/msg_def.lua', 'lua/event_mgr.lua', 'lua/data.lua',
              'lua/ui/mainUI.lua', 'csv_config/summon_cortege_set.csv',
              'csv_config/cortege_quality.csv', 'csv_config/item_name.csv']
    inputs = []
    for name in wanted:
        path = ASSETS / index[name]
        inputs.append(dict(logical=name, physical=str(path.relative_to(ROOT)),
                           sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    chunk = parse((ASSETS / index['lua/ui/summonUI.lua']).read_bytes())
    # Original bytecode and numeric operands, including constant-folded branches.
    excerpts = []
    for ident in [1, 2, 5, 7, 23, 27, 32, 33, 48, 53, 54, 55, 57, 61]:
        proto = chunk['protos'][ident]
        excerpts.append('NUMERIC CONSTANTS proto%d: %s\n' % (ident, proto['numbers']))
        excerpts.append(listing(dict(source=chunk['source'], root=ident, protos=[proto])))
    (EVIDENCE / 'summon_official_bytecode.txt').write_text('\n'.join(excerpts))
    configs = json.loads((EVIDENCE / 'config_inventory.json').read_text())
    scripts = json.loads((EVIDENCE / 'script_inventory.json').read_text())
    quality = list(csv.DictReader(io.StringIO(
        (ASSETS / index['csv_config/cortege_quality.csv']).read_text(encoding='utf-8-sig'))))
    preview = list(csv.DictReader(io.StringIO(
        (ASSETS / index['csv_config/summon_cortege_set.csv']).read_text(encoding='utf-8-sig'))))
    native = (ROOT / 'jgbol3.87/lib/armeabi/libxiyoujilua.so').read_bytes()
    report = dict(
        date='2026-10-24', inputs=inputs,
        coverage=dict(indexed_csv_files=len(configs), indexed_lua_files=len(scripts),
                      native_sha256=hashlib.sha256(native).hexdigest()),
        verified_client_contract={
            'request_id':1042, 'result_event':23, 'error_event':55, 'last_pick_event':79,
            'soul_delta_event':3, 'soul_inventory_message':1046, 'free_normal_ui_limit':5,
            'gold_prices_in_client_branch':{'1':10,'2':100,'3':300},
            'token_ids':{'2':1006,'3':1007}, 'token_ten_count':10,
            'remaining_time_unit':'seconds',
            'result_variants':['cortege_type','convert_count','token_type','prize_info','ten_pick/event_data'],
            'soul_inventory_shape':'1046: {first_send=true,spirit_count=N,spirit_list={{type_id=...,count=...},...}}',
            'soul_delta_shape':'event 3: {type_id=...,total_count=...}',
            'vip_limit_path':'g_new_config[vip_config][vip_level].day_pick_cortege_limit[pick_grade]',
            'client_banshu_default':True,
            'client_show_activity_branch':'proto7 pc2 unconditionally jumps to isPrizeOpen=true',
            'client_ten_activity_time_check':'proto27 pc47 jumps past getRestTime check',
            'super_first_banner':'super_first_pick_time == 0 displays gold_pick_5.png; settlement trigger is not determined',
            'daily_reset_display':'mainUI.getRefreshTime uses os.date/os.time to compute next local midnight; server timezone not established',
        },
        preview_sets=[dict(index=int(row['index']), count=len(row['type_set(id1/id2/id3...)'].split('/')),
                           columns=list(row), interpretation='UI preview only; no probabilities') for row in preview],
        quality_conversion_table=quality,
        findings={
            'random_selection_in_summon_ui':'No random-selection call found; startSummon sends request and getSummonResult consumes server data.',
            'cooldown_values':'getTimeTable only divides server supplied seconds by 60/3600; no source for previous 600/86400/259200 defaults.',
            'duplicate_conversion':'Quality CSV contains 2/4/9/12/15 conversion quantities, but no proof all duplicate summon cases apply it unconditionally.',
            'activity_window':'UI true branch and bypassed timer check do not prove server activity is always enabled.',
            'capacity':'255 is the 1034 per-packet record limit; it is not evidence of an official account inventory cap.',
            'native_search':'No summon/pick/lottery business function names found in existing native_symbols.txt; absence alone is not proof of no hidden logic.',
        },
        unresolved=json.loads((ROOT / 'server_config/summon_official.json').read_text())['server_rules'],
        conclusion='Official server settlement cannot be uniquely recovered from these client-only inputs. User-authorized inferred rules are configured separately in server_config/summon_rules.json; they are not official evidence.'
    )
    path = EVIDENCE / 'summon_official_audit.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(path.relative_to(ROOT))


if __name__ == '__main__':
    main()
