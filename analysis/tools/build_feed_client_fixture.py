"""Detached original Cocos round, with real local response payloads."""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode


def main():
    now = 1792814400
    with tempfile.TemporaryDirectory() as tmp:
        b = Backend(Path(tmp), 18770, lambda *a, **k: None)
        role = b.profile();rules = b.activity_rules
        def request(count, at=now):
            activity.prepare(role, at, rules)
            return login_fields(decode(activity.feed(role, dict(feed_count=count), at, rules)[0])[2]['data'])
        fixtures = dict(now=now, entry=request(0), result=request(30),
                        dinner=request(0, now+21600), dinner_result=request(10, now+21600),
                        next_day=request(0, now+86400))
        b.close()
    patch = (ROOT/'network_redirect/feed_client.lua').read_text().replace(
        '__FEED_REWARD_TIERS__', summon.lua(rules['feed_reward_tiers'])).replace(
        '__FEED_MAX_COUNT__', str(rules['feed_max_count']))
    script = 'assert(loadstring('+summon.lua(summon.client_source(summon.load_rules()))+'))\n'
    script += 'local FIXTURE='+summon.lua(fixtures)+'\n'+(
        ROOT/'analysis/tools/feed_client_harness.lua').read_text().replace('-- INSTALL_PATCH', patch)
    path = ROOT/'.runtime/feed-native-fixture.lua';path.write_text(script)
    print(path)


if __name__ == '__main__':
    main()
