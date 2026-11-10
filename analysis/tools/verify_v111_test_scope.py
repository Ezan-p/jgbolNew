"""Verify release scope and the frozen build snapshot in the signed test APK."""
import io
import json
from pathlib import Path
import re
import sys
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from analysis.tools.build_v111_test import APK,BASE,BASE_SHA,PREVIOUS,PREVIOUS_SHA,WORK,EVIDENCE,digest
from offline_android.pack_payload import collect_files,verify_payload


def main():
    meta=json.loads((EVIDENCE/'build-validation.json').read_text())
    assert digest(APK.read_bytes())==meta['apk_sha256']
    assert digest(BASE.read_bytes())==BASE_SHA and digest(PREVIOUS.read_bytes())==PREVIOUS_SHA
    drift=[name for name,sha in meta['workspace_source_sha256'].items()
           if not (ROOT/name).exists() or digest((ROOT/name).read_bytes())!=sha]
    assert digest((WORK/'offline-test.c').read_bytes().replace(b'18776',b'18770'))==meta['native_source_sha256']
    for name,sha in meta['java_source_sha256'].items():assert digest((ROOT/name).read_bytes())==sha,name
    with zipfile.ZipFile(APK) as apk,zipfile.ZipFile(BASE) as base,zipfile.ZipFile(PREVIOUS) as previous:
        with zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as p,zipfile.ZipFile(io.BytesIO(base.read('assets/offline/program.zip'))) as b,zipfile.ZipFile(io.BytesIO(previous.read('assets/offline/program.zip'))) as old:
            files={n:p.read(n) for n in p.namelist()}
            assert p.testzip() is None
            for n,data in files.items():
                assert data==(WORK/'program'/n).read_bytes(),n
                assert Path(n).suffix not in ('.db','.sqlite3','.pyc') and 'save' not in Path(n).parts,n
            for n,sha in meta['workspace_source_sha256'].items():
                if n=='network_redirect/login.html':continue
                value=files[n]
                if n=='offline_android/backend.py':
                    value=value.replace(b'PORT = 18776',b'PORT = 18770').replace(b"self.files_dir / 'test-save-v106'",b"self.files_dir / 'save'")
                    value=value.replace(b'from offline_android.test_edition_v110 import fixed_accounts_class\n        Accounts = fixed_accounts_class()',b'from network_redirect.accounts import Accounts')
                assert digest(value)==sha,n
            assert files['network_redirect/login.html']==old.read('network_redirect/login.html')
            generated=subprocess.check_output([sys.executable,'-I','-c',
                'import sys;sys.path.insert(0,sys.argv[1]);from network_redirect.summon import client_source,load_rules;sys.stdout.buffer.write(client_source(load_rules()).encode())',str(WORK/'program')])
            assert generated==files['offline_client.lua']
            for n in ('network_redirect/activity_nine_sky.py','network_redirect/nine_sky_battle.py','network_redirect/nine_sky_client.lua','server_config/nine_sky_rules.json'):
                assert files[n]==b.read(n),n
            rules=json.loads(files['server_config/activity_rules.json'])
            shop={row['reward'][1]:row for row in rules['abyss_shop']}
            for tid in (1310,1311,1312):
                assert shop[tid]['reward'][2]==100 and shop[tid]['cost']==1000 and shop[tid]['limit']==5
            assert rules['abyss_shop_revision']=='2026-11-10-reborn-equip-v11'
            pool=json.loads(files['server_config/item_reward_rules.json'])['pools']['essence']
            assert [x['weight'] for x in pool]==[16,3,1]
            for row,count in zip(pool,(20,50,100)):
                assert row['candidates']==[[5,t,count,1] for t in (1310,1311,1312)]
            assert json.loads(files['server_config/save_monkey_rules.json'])['enabled'] is False
            assert rules['abyss_map_revision']=='2026-11-09-user-pool-v5'
            assert len(rules['fish_pool'])==12 and rules['home_shop_daily_count']==3
            assert rules['land_card_weights']['stone_10']==20 and rules['land_card_weights']['stone_20']==15
            guild=json.loads(files['server_config/guild_rules.json'])
            assert guild['hunt_gold']==100 and guild['lucky_weekend_only'] and guild['train_support_gold']==20
            assert guild['train_adoptions_per_floor']==3 and len(guild['store'])==16
            assert guild['escort_refresh']['grade_weights']=={'2':60,'3':25,'4':12,'5':3}
            assert guild['pet_shop_fixed_items']==[1338,1339,1345] and guild['pet_shop_random_slots']==3
            assert json.loads(files['server_config/taixu_rules.json'])['arena_rank_prizes'][0]['holy_peach']==200
            assert json.loads(files['server_config/pet_rules.json'])['training_box_pool']==[{'count':10,'weight':30},{'count':15,'weight':50},{'count':20,'weight':20}]
            backend=files['offline_android/backend.py'].decode()
            assert 'PORT = 18776' in backend and "self.files_dir / 'test-save-v106'" in backend
            assert 'from offline_android.test_edition_v110 import fixed_accounts_class' in backend
            assert 'network_time=True' in backend
            changed=sorted(n for n in files if files[n]!=(b.read(n) if n in b.namelist() else None))
            assert all(apk.read(n)==base.read(n) for n in base.namelist() if n.startswith('assets/') and not n.startswith('assets/offline/'))
            assert apk.read('assets/offline/runtime.zip')==base.read('assets/offline/runtime.zip')
            for n in ('classes.dex','classes2.dex','lib/armeabi-v7a/liboffline.so'):
                assert apk.read(n)==previous.read(n),n
    manifest=verify_payload(WORK/'program')
    assert manifest['player_database']=='files/test-save-v106/game.sqlite3' and manifest['loopback_port']==18776
    report=dict(passed=True,apk_sha256=meta['apk_sha256'],build_snapshot_sources_match=True,
        later_workspace_changes_excluded=drift,
        complete_generated_client_matches=True,latest_essence_gift_and_abyss_shop_verified=True,
        all_requested_rules_included=True,nine_sky_design_excluded=True,
        original_assets_and_python_runtime_preserved=True,previous_test_java_and_native_byte_identical=True,contains_player_database=False,
        isolated_test_identity=True,original_apks_unchanged=True,changed_program_entries=changed)
    (EVIDENCE/'scope-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Signed APK scope and frozen build snapshot verified:',len(changed),'changed payload entries')

if __name__=='__main__':main()
