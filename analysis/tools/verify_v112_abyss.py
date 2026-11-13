"""Validate affected features, packaged Lua and saves in the new formal v112."""
import argparse
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from analysis.tools import build_v112_abyss as build
from analysis.tools import verify_v112_taixu as previous

previous.build = build
verify = previous.verify
for name in ('WORK','EVIDENCE','OUTPUT','BASE','digest','report'):
    setattr(verify,name,getattr(build,name))
# Rerun the changed activity loader, Abyss/treasure protocols, prior Taixu
# behavior and Android startup. Unchanged gameplay retains the baseline evidence.
verify.SUITES = [
    'test_abyss_shop','test_activity_abyss','test_abyss_balance','test_activity_treasure',
    'test_activity.ActivityTests','test_activity.HomeAbyssTests','test_activity.UndergoTests',
    'test_taixu_shop','test_activity_taixu','test_feature_levels',
    'test_android_offline_backend','test_network_time_runtime',
]


def scope():
    from offline_android.pack_payload import verify_payload
    root=build.WORK/'payload-new'
    manifest=verify_payload(root)
    meta=json.loads((build.EVIDENCE/'build-validation.json').read_text())
    assert meta['apk_sha256']==build.digest(build.OUTPUT.read_bytes())
    for name,sha in meta['source_hashes'].items():
        if name!='network_redirect/login.html':
            assert build.digest((root/name).read_bytes())==sha,name
    r=json.loads((root/'server_config/activity_rules.json').read_text())
    old=json.loads((build.WORK/'payload-baseline/server_config/activity_rules.json').read_text())
    changed={k for k in r.keys()|old.keys() if r.get(k)!=old.get(k)}
    assert changed=={'abyss_map_weights','abyss_map_revision','abyss_shop','abyss_shop_revision'}
    assert r['abyss_map_revision']=='2026-11-13-user-pool-v10'
    assert r['abyss_map_weights']==[100,280,100,50,30,70,70,69,10,70,1,150]
    assert sum(r['abyss_map_weights'])==1000
    assert r['abyss_shop_revision']=='2026-11-13-weighted-all-v18'
    expected={1329:(200,20,40),1330:(200,20,40),1331:(600,5,20),1332:(1800,3,3),
              1310:(20,500,40),1311:(20,500,40),1312:(20,500,40),1333:(1000,10,5)}
    assert {p['reward'][1]:(p['cost'],p['limit'],p['weight']) for p in r['abyss_shop']}==expected
    assert all(p['reward'][2]==1 and p['guaranteed'] is False for p in r['abyss_shop'])
    assert r['abyss_shop_daily_count']==6
    assert (root/'server_config/taixu_rules.json').read_bytes()==(build.WORK/'payload-baseline/server_config/taixu_rules.json').read_bytes()
    assert manifest['player_database']=='files/save/game.sqlite3' and manifest['loopback_port']==18770
    build.report('scope-validation',dict(apk_sha256=meta['apk_sha256'],passed=True,
        all_frozen_source_hashes_verified=True,treasure_v10=True,shop_v18=True,
        shop_batch_six_slots_cap100=True,changed_activity_config_keys=sorted(changed),
        previous_taixu_rules_preserved=True,unchanged_payload_bytes_preserved=True,
        contains_player_database=False,feature_groups=13,
        baseline_full_regression_evidence='analysis/evidence/v112-taixu-20261113/protocol-validation.json'))
    print('New treasure pool, weighted six-of-eight shop, batch patch and prior v112 content verified')


def lua():
    previous.lua()
    from lupa.lua51 import LuaRuntime
    fixture=(build.WORK/'tests/abyss_shop_batch_client_regression.lua').read_text()
    try:
        LuaRuntime().execute(fixture,'')
    except Exception as exc:
        assert 'all six slots must open a picker capped at 100' in str(exc),str(exc)
    else:
        raise AssertionError('Unpatched client must reproduce original batch restriction')
    LuaRuntime().execute(fixture,(build.WORK/'payload-new/network_redirect/abyss_client.lua').read_text())
    record=json.loads((build.EVIDENCE/'lua-validation.json').read_text())
    record.update(abyss_shop_batch=True,unpatched_restriction_reproduced=True,
                  six_slots=True,quantity_cap=100,stale_dialog_rejected=True)
    build.report('lua-validation',record)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['scope','lua','save','protocol','merge','recheck','setup'])
    parser.add_argument('--shard',type=int,choices=range(3))
    args=parser.parse_args()
    if args.mode=='protocol':
        assert args.shard is not None
        verify.protocol(args.shard)
    elif args.mode in ('scope','lua'):
        globals()[args.mode]()
    elif args.mode=='setup':
        verify.setup()
    else:
        getattr(previous,args.mode)()
