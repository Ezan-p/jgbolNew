"""Replay disposable escort rewards in native Cocos; intercept every send."""
import json
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT/'analysis/tools')]
from android_emulator.config import load_config
from observability.collector import processes
from network_redirect import summon, item_rewards
from network_redirect.backend import login_fields
from tests.test_guild_escort_rewards import EscortRewardTests
from verify_guild_client import LUA_EVALUATOR


def fixtures():
    test = EscortRewardTests()
    test.setUp()
    try:
        test.prepare(14)
        singles = []
        for tid in range(1304, 1308):
            with patch.object(summon, 'weighted_choice', return_value=str(tid)):
                test.compose()
            bag = next(i for i in test.b.profile()['attachments'] if i['type_id'] == tid)
            singles.append(dict(response=test.response(), bag=bag))
        with patch.object(summon, 'weighted_choice', side_effect=['1304','1305','1306','1307','1304']*2), \
                patch.object(item_rewards, 'draw', side_effect=[[5,1001,50,1],[11,1,50,1],[5,1029,9,1],[5,6002,5,1],[5,1007,1,1]]*2):
            test.compose(10)
        return dict(singles=singles, ten=test.response(), const=test.b.guild_rules['west_config'])
    finally:
        test.doCleanups()


def main():
    import frida
    data = fixtures()
    config = load_config(ROOT/'game.json')
    pid = next(p for p,n in processes(config).items() if n == config['package'])
    session = frida.get_device(config['serial'], timeout=10).attach(pid)
    evaluator = LUA_EVALUATOR.replace('pending={code,resolve};',
        "const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
    script = session.create_script(evaluator)
    report = dict(passed=False, native_cocos=True, live_account_resources_changed=False)
    try:
        script.load()
        code = (ROOT/'analysis/tools/escort_rewards_client_harness.lua').read_text().replace('__FIXTURES__', summon.lua(data))
        answer = script.exports_sync.evaluate(code)
        if answer.get('status') != 0:
            raise RuntimeError(answer)
        report.update(login_fields(answer['result']))
    finally:
        restored = script.exports_sync.evaluate("if escortRewardsRestore then escortRewardsRestore() end;return 'restored'")
        report['restored'] = restored.get('status') == 0
        script.unload()
        session.detach()
        (ROOT/'analysis/evidence/guild/escort_rewards_client_20261030.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report['passed'] or not report['restored']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
