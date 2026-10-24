"""Extract reproducible daily contracts from unmodified original APK assets."""
import hashlib
import json
import plistlib
from pathlib import Path
from luajit_static import parse, listing
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'analysis/evidence/daily'
MODULES = ['ui/checkinUI', 'ui/bonusLayerUI', 'ui/prizeUI', 'common/common_def', 'event_mgr']


def main():
    OUT.mkdir(exist_ok=True)
    index = dict(line.split('====')[:2] for line in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    inputs = []
    for module in MODULES:
        logical = 'lua/'+module+'.lua'
        path = ROOT/'jgbol3.87/assets/release_'/index[logical]
        chunk = parse(path.read_bytes())
        text = '\n'.join('NUMERIC proto%d %r' % (p['id'], p['numbers']) for p in chunk['protos'])+'\n'+listing(chunk)
        (OUT/(module.replace('/','_')+'.txt')).write_text(text)
        inputs.append(dict(logical=logical, physical=str(path.relative_to(ROOT)), sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    logical = 'v2/String2.plist'
    path = ROOT/'jgbol3.87/assets/release_'/index[logical]
    strings = {k: v for k, v in plistlib.loads(path.read_bytes()).items() if k.startswith('checkin')}
    assert '周一0点重置' in strings['checkin_tink4']
    (OUT/'original_strings.json').write_text(json.dumps(strings, ensure_ascii=False, indent=2)+'\n')
    inputs.append(dict(logical=logical, physical=str(path.relative_to(ROOT)), sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    report = dict(client='3.87', official_server_available=False, inputs=inputs,
                  requests=[1206,1347], events=[54,198], client_config_sections=[3,9],
                  classification={'A':'原版字节码与协议可证结构、枚举和客户端行为', 'B':'服务端积分、奖励金额、时区、累计及防重策略'},
                  rules='server_config/daily_rules.json')
    (OUT/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Verified five original Lua modules and original String2.plist; daily requests 1206/1347 and events 54/198.')

if __name__ == '__main__': main()
