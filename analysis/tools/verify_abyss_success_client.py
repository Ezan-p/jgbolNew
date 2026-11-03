"""Check original victory rendering without fighting or modifying a live save."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis/tools')]
from android_emulator.config import load_config
from observability.collector import processes
from network_redirect import activity, abyss_balance, summon
from verify_guild_client import LUA_EVALUATOR


def main():
    import frida
    rewards = {str(floor): [activity.prize_spec(spec) for spec in abyss_balance.victory_rewards(floor)]
               for floor in (1, 40, 81)}
    source = 'local REWARDS=' + summon.lua(rewards) + '\n'
    source += 'local ABYSS_PATCH=' + summon.lua((ROOT / 'network_redirect/abyss_client.lua').read_text()) + '\n'
    source += (ROOT / 'analysis/tools/abyss_success_client_harness.lua').read_text()
    config = load_config(ROOT / 'game.json')
    pid = next(p for p, name in processes(config).items() if name == config['package'])
    session = frida.get_device(config['serial'], timeout=10).attach(pid)
    script = session.create_script(LUA_EVALUATOR.replace(
        'pending={code,resolve};',
        "const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);"))
    try:
        script.load()
        result = script.exports_sync.evaluate(source)
        if result.get('status') != 0:
            raise RuntimeError(result)
        report = json.loads(result['result'])
    finally:
        script.unload()
        session.detach()
    destination = ROOT / 'analysis/evidence/abyss/success_client_20261103.json'
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report['passed'] != report['total']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
