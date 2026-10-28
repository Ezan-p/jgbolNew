"""Realm wire config, original bytecode units, and transactional upgrade boundaries."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from analysis.tools.luajit_static import parse, decode as instruction
from network_redirect import reborn, summon, formation
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode

ROOT = Path(__file__).resolve().parents[1]


class RealmConfigTests(unittest.TestCase):
    def test_region_divisor_matches_original_bytecode(self):
        index = dict(line.split('====')[:2] for line in
                     (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
        chunk = parse((ROOT/'jgbol3.87/assets/release_'/index['lua/ui/roleRebornUI.lua']).read_bytes())
        divisors = []
        for proto in chunk['protos']:
            for line, code in zip(proto['lines'], proto['code']):
                op, _, _, c, _ = instruction(code)
                if line in (991, 997, 1004) and op == 'DIVVN':
                    divisors.append(proto['numbers'][c])
        self.assertEqual(divisors, [reborn.FLOORS_PER_REGION]*6)
        cfg = reborn.client_config(reborn.load_rules())
        ranges = [(cfg[i-1]['rights']['boss_layer']//divisors[0]+1,
                   cfg[i]['rights']['boss_layer']//divisors[0]) for i in range(1, 5)]
        self.assertEqual(ranges, [(1, 1), (2, 2), (3, 3), (4, 4)])

    def test_invalid_or_unreachable_config_rejected(self):
        rules = reborn.load_rules()
        cases = [(0, 'boss_layer', 3), (1, 'boss_layer', 9), (3, 'boss_layer', 90),
                 (0, 'required_layer', 1), (1, 'required_layer', 4),
                 (2, 'required_layer', -1), (1, 'max_layer', 6.5),
                 (1, 'level', 60)]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'rules.json'
            for i, field, value in cases:
                with self.subTest(field=field, value=value):
                    bad = copy.deepcopy(rules); bad['realms'][i][field] = value
                    path.write_text(json.dumps(bad))
                    with self.assertRaises(formation.Rejected): reborn.load_rules(path)


class RealmUpgradeTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        self.directory = Path(tmp.name)
        self.backend = Backend(self.directory, 18770, lambda *a, **kw: None)
        self.addCleanup(self.backend.close)
        self.serial = 5000

    def request(self):
        self.serial += 1
        # Original sendRebornRequest sends an empty data string, not '{}'.
        self.packet = encode(1328, dict(serial_num=self.serial, reborn_type=1, id=4, data=''))
        self.replies = self.backend.respond(self.packet, dict(authenticated=True))
        return [decode(p) for p in self.replies]

    def rejected(self):
        before = self.backend.profile()
        packets = self.request()
        self.assertTrue(any(mid == 2998 and data['id'] == 55 for mid, _, data in packets))
        self.assertEqual(before, self.backend.profile())

    def test_all_upgrade_boundaries_deltas_replay_and_persistence(self):
        b = self.backend
        for target, cfg in enumerate(b.reborn_rules['realms'], 1):
            role = b.profile(); role['level'] = cfg['level']-1
            while len(role['corteges']) < 3: role['corteges'].append(summon.companion(role, 5022))
            for c in role['corteges']: c['reborn_layer'] = cfg['required_layer']
            role['attachments'] = [x for x in role['attachments'] if x['type_id'] != cfg['material']]
            summon.add_item(role, cfg['material'], cfg['cost'])
            b.save(role); self.rejected()
            role = b.profile(); role['level'] = cfg['level']; b.save(role)
            if cfg['count']:
                role = b.profile(); role['corteges'][-1]['reborn_layer'] -= 1
                b.save(role); self.rejected()
                role = b.profile(); role['corteges'][-1]['reborn_layer'] += 1; b.save(role)
            for flag in ('is_lock', 'owner_id', 'equip_order'):
                role = b.profile(); item = next(x for x in role['attachments'] if x['type_id'] == cfg['material'])
                item[flag] = 1; b.save(role); self.rejected()
                role = b.profile(); next(x for x in role['attachments'] if x['id'] == item['id'])[flag] = 0; b.save(role)
            role = b.profile(); next(x for x in role['attachments'] if x['type_id'] == cfg['material'])['count'] -= 1
            b.save(role); self.rejected()
            role = b.profile(); summon.add_item(role, cfg['material'], 1); b.save(role)
            packets = self.request(); after = b.profile()
            self.assertEqual(after['reborn_layer'], target)
            self.assertFalse(any(x['type_id'] == cfg['material'] for x in after['attachments']))
            success = next(i for i, (mid, _, data) in enumerate(packets) if mid == 2998 and data['id'] == 172)
            attrs = {v['type']: v['value'] for mid, _, data in packets[:success] if mid == 1032 and data['unit_type'] == 1 for v in data['attr_list']}
            self.assertEqual(attrs[580], target)
            self.assertEqual(attrs[581], after['maxlayer_reborn_count'])
            self.assertEqual(b.respond(self.packet, dict(authenticated=True)), self.replies)
            self.assertEqual(b.profile(), after)
        self.rejected()
        # Reload from the same persistent store after a real close/open cycle.
        directory = self.directory
        b.close()
        again = Backend(directory, 18770, lambda *a, **kw: None)
        try: self.assertEqual(again.profile()['reborn_layer'], 4)
        finally: again.close()
