"""Check all ten requested changes and the exact frozen artifact boundary."""
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v110_test_refresh import APK, BASE, BASE_SHA, PREVIOUS, PREVIOUS_SHA, WORK, EVIDENCE, digest, report
from offline_android.pack_payload import verify_payload


def main():
    meta = json.loads((EVIDENCE / 'build-validation.json').read_text())
    assert digest(APK.read_bytes()) == meta['apk_sha256']
    assert digest(BASE.read_bytes()) == BASE_SHA and digest(PREVIOUS.read_bytes()) == PREVIOUS_SHA
    with zipfile.ZipFile(APK) as a, zipfile.ZipFile(PREVIOUS) as old, zipfile.ZipFile(BASE) as formal:
        with zipfile.ZipFile(io.BytesIO(a.read('assets/offline/program.zip'))) as z:
            files = {n: z.read(n) for n in z.namelist()}
        with zipfile.ZipFile(io.BytesIO(old.read('assets/offline/program.zip'))) as z:
            assert files['network_redirect/login.html'] == z.read('network_redirect/login.html')
            assert files['offline_android/test_edition_seed.py'] == z.read('offline_android/test_edition_seed.py')
        for n, content in files.items():
            assert content == (WORK / 'program' / n).read_bytes(), n
            assert Path(n).suffix not in ('.db', '.sqlite3', '.pyc') and 'save' not in Path(n).parts
        for n, sha in meta['workspace_source_sha256'].items():
            if n == 'network_redirect/login.html':
                continue
            value = files[n]
            if n == 'network_redirect/login_branding_client.lua':
                value = re.sub(rb"label\('v110',0\.75\)", b"label('v111',0.75)", value)
            if n == 'offline_android/backend.py':
                value = value.replace(b'PORT = 18776', b'PORT = 18770').replace(b"self.files_dir / 'test-save-v106'", b"self.files_dir / 'save'")
                value = value.replace(b'from offline_android.test_edition_v110 import fixed_accounts_class\n        Accounts = fixed_accounts_class()', b'from network_redirect.accounts import Accounts')
            assert digest(value) == sha, n
        generated = subprocess.check_output([sys.executable, '-I', '-c',
            'import sys;sys.path.insert(0,sys.argv[1]);from network_redirect.summon import client_source,load_rules;sys.stdout.buffer.write(client_source(load_rules()).encode())', str(WORK / 'program')])
        assert generated == files['offline_client.lua']
        read = lambda n: json.loads(files['server_config/' + n + '_rules.json'])
        gifts = read('gift_code')['codes']
        cards = [x for x in gifts if any(p[:2] == [5,1901] for p in x['prizes'])]
        assert sorted(x['prizes'] for x in cards) == [[[5,1901,n,1]] for n in (10,20,50)]
        assert all(x['enabled'] for x in cards)
        party = read('party')
        assert len(party['npc_damage_tiers']) == 10 and all(len(x['values']) == 5 for x in party['npc_damage_tiers'])
        assert [x['end'] for x in party['daily_rewards']] == [5,10,20,50]
        assert [x['prizes'] for x in party['daily_rewards']] == [[[5,1343,150,1]],[[5,1343,100,1]],[[5,1343,50,1]],[[5,1001,200,1]]]
        nine = read('nine_sky')['star_shop']
        low = [x for x in nine if x['tier'] == 'low']
        assert len(nine) == 17 and len(low) == 7
        assert all(x['limit'] == (1 if x['reward'][1] == 1024 else 5) for x in low)
        assert not {1041,1042} & {x['reward'][1] for x in nine}
        guild = read('guild')
        essence = next(x for x in guild['store'] if x['prize'][1] == 1327)
        assert essence['cost'] == 200 and essence['limit'] == 3
        assert '活动倒计时：%d天 %02d:%02d:%02d' in files['network_redirect/seasonal_craft_client.lua'].decode()
        taixu = read('taixu')
        assert taixu['arena_top_power_count'] == 15 and 'arena_extreme_slots' not in taixu
        activity = read('activity')
        shop = activity['undergo_shop']
        assert {x['reward'][1] for x in shop if x['guaranteed']} == {1310,1311,1312,1320}
        assert all(x['reward'][2] == 1 for x in shop)
        hunt = read('hunt')
        assert hunt['upgrade_box_weights'] == {str(t): (6 if t in (1314,1322,1323) else 17) for t in hunt['upgrade_box_pool']}
        assert hunt['upgrade_box_counts'] == {str(t): (10 if t in (1310,1311,1312) else 1) for t in hunt['upgrade_box_pool']}
        rewards = read('item_reward')
        assert rewards['items']['1325']['mode'] == 'fixed_random'
        assert rewards['items']['1325']['prizes'] == [[5,10000,10,1]]
        assert [x['weight'] for x in rewards['pools']['hunt']] == [5,95]
        for n in a.namelist():
            if not n.startswith('META-INF/') and n not in meta['changed_apk_entries']:
                assert a.read(n) == old.read(n), n
        assert a.read('assets/offline/runtime.zip') == formal.read('assets/offline/runtime.zip')
    manifest = verify_payload(WORK / 'program')
    assert manifest['player_database'] == 'files/test-save-v106/game.sqlite3' and manifest['loopback_port'] == 18776
    drift = [n for n, sha in meta['workspace_source_sha256'].items() if digest((ROOT / n).read_bytes()) != sha]
    report('scope-validation', dict(passed=True, apk_sha256=meta['apk_sha256'], requested_updates_verified=10,
        frozen_sources_verified=True, later_workspace_changes_excluded=drift, generated_client_verified=True,
        shell_and_test_identity_preserved=True, player_database_included=False, baselines_preserved=True))
    print('All ten changes, generated Lua, frozen sources and isolated test identity verified')


if __name__ == '__main__':
    main()
