"""Reassemble the same ordered chunks consumed by the original-client adapter."""
import copy
import hashlib
import json
import re
import unittest

from network_redirect import battle_replay as transport, guild_combat, monument, summon
from network_redirect.backend import login_fields
from network_redirect.protocol import decode, encode


def parsed_payload(source):
    # Chunk envelopes have a fixed literal schema. Decode their JSON string
    # with the stdlib so multi-megabyte transport tests do not construct an
    # unnecessary Lua AST for every individual string fragment.
    match=re.match(r'^\{\["fight_id"\]=([^,]+),\["offline_battle_chunk"\]=\{\["kind"\]="(events|replay)",\["key"\]="([a-f0-9]+)",\["index"\]=(\d+),\["total"\]=(\d+),\["payload"\]=',source)
    if match:
        fight_id,kind,key,index,total=match.groups()
        return dict(fight_id=int(fight_id),offline_battle_chunk=dict(kind=kind,key=key,index=int(index),total=int(total),payload=json.loads(source[match.end():-2])))
    return login_fields(source)


def decoded_packets(packets):
    """A receive-side test oracle: finish preload before exposing a reference."""
    pending = {}; cache = {}; decoded = []
    def hydrate(value):
        if isinstance(value,dict):
            if transport.REFERENCE_KEY in value:
                return hydrate(cache[value[transport.REFERENCE_KEY]])
            if '_local_replay_parts' in value:
                merged = {}
                for part in value['_local_replay_parts'].values():
                    restored = hydrate(part)
                    if merged.keys() & restored.keys():
                        raise AssertionError('overlapping replay groups')
                    merged.update(restored)
                return merged
            return {key:hydrate(v) for key,v in value.items()}
        return value
    for packet in packets:
        mid, connection, value = decode(packet)
        if mid not in (2998,1301):
            decoded.append((mid,connection,value)); continue
        payload = parsed_payload(value['data'])
        chunk = payload.get(transport.CHUNK_KEY) if isinstance(payload,dict) else None
        if chunk:
            key = chunk['key']; parts = pending.setdefault(key, [])
            if chunk['index'] != len(parts)+1:
                raise AssertionError('out-of-order or duplicate chunk')
            parts.append(chunk['payload'])
            if len(parts) == chunk['total']:
                source = ''.join(parts)
                if hashlib.sha256(source.encode()).hexdigest() != key:
                    raise AssertionError('chunk payload changed')
                result = login_fields(source); del pending[key]
                if chunk['kind'] == 'events':
                    decoded.append((2998,connection,dict(value,data=summon.lua(result))))
                else:
                    cache[key] = hydrate(result)
            continue
        if isinstance(payload,dict) and transport.REFERENCE_KEY in payload:
            payload = hydrate(payload)
            value = dict(value,data=summon.lua(payload))
        decoded.append((mid,connection,value))
    if pending:
        raise AssertionError('missing final chunk')
    return decoded


def effects(count=100, fight_id=7):
    return dict({i:dict(cur_action=i%240+1,skill_type=10,src_order=i%8+1,is_src=True,
                skill_result_list=[dict(order=i%8+1,field=65,field_plus=123,
                                       text='治疗\\"与复活神仙'*8)]) for i in range(1,count+1)},fight_id=fight_id)


class BattleReplayTransportTests(unittest.TestCase):
    def assertBudget(self, packets):
        self.assertTrue(packets)
        self.assertTrue(all(len(p)<=transport.PACKET_BUDGET for p in packets))

    def test_small_and_empty_effects_keep_native_contract(self):
        for data in ({'fight_id':7}, effects(1)):
            packets=transport.effect_packets(data);self.assertEqual(len(packets),1)
            self.assertEqual(login_fields(decode(packets[0])[2]['data']),login_fields(summon.lua(data)))
            self.assertBudget(packets)

    def test_result_message_matches_native_defaults_without_byte_count_limit(self):
        fields = dict(fight_id=91, fight_type=28, final_result=0, fight_result=[dict(
            self_use=False, skill_type=1, is_src=True, src_order=1, des_order=2,
            cur_round=1, damage_list=[0, 100, 0, 0, 0, 0, 0, 0])])
        original = copy.deepcopy(fields)
        value = transport.result_message(fields)
        self.assertEqual(value, decode(encode(1027, value))[2])
        self.assertEqual(fields, original)
        value['fight_result'][0]['damage_list'][1] = 999
        self.assertEqual(fields, original)

    def test_long_direct_results_preload_all_actions_before_native_notice(self):
        for mid, slots in ((1027, 8), (1140, 9)):
            fields = dict(fight_id=91, fight_type=28, final_result=0, fight_result=[dict(
                skill_type=1, is_src=True, src_order=1, des_order=1, cur_round=i//18+1,
                damage_list=[i]+[0]*(slots-1)) for i in range(540)])
            packets = transport.result_packets(mid, fields)
            self.assertBudget(packets)
            decoded = decoded_packets(packets)
            self.assertEqual([row[0] for row in decoded], [2998, mid])
            preload = login_fields(decoded[0][2]['data'])['offline_battle_result']
            self.assertEqual(preload['fight_round'], 540)
            self.assertEqual(len(preload['fight_result']), 540)
            self.assertEqual(preload['fight_result'][540]['damage_list'][1], 539)
            self.assertEqual(decoded[-1][2]['fight_round'], 0)
            self.assertEqual(decoded[-1][2]['guide_stage'], transport.RESULT_MARKER)

    def test_short_direct_results_keep_original_binary_contract(self):
        fields = dict(fight_id=91, fight_type=28, final_result=0, fight_result=[])
        packets = transport.result_packets(1027, fields)
        self.assertEqual(packets, [encode(1027, transport.result_message(fields))])

    def test_large_effects_roundtrip_all_values_and_utf8_within_budget(self):
        data=effects();before=copy.deepcopy(data);packets=transport.effect_packets(data)
        self.assertGreater(len(packets),1);self.assertBudget(packets)
        decoded=decoded_packets(packets);self.assertEqual(len(decoded),1)
        self.assertEqual(login_fields(decoded[0][2]['data']),login_fields(summon.lua(data)))
        self.assertEqual(data,before)

    def test_full_nested_response_roundtrip_preserves_all_history(self):
        actions=list(range(240))
        records=[dict(line_up_msg=dict(fight_id=i,lineup=[dict(src_type=5001,des_type=5002)]*8),
                      fight_result_msg=dict(fight_type=28,final_result=0,fight_result=actions),
                      fight_events=effects(10,i)) for i in range(1,11)]
        original=dict(result=1,fight_result_list=records,free_times=3,fight_count=1)
        for mid,fields in ((1301,dict(id=85)),(2998,dict(id=149)),(2998,dict(id=152))):
            packets=transport.lua_packets(mid,fields,original)
            self.assertGreater(len(packets),2);self.assertBudget(packets)
            self.assertIn(transport.REFERENCE_KEY,login_fields(decode(packets[-1])[2]['data']))
            data=login_fields(decoded_packets(packets)[0][2]['data'])
            self.assertEqual(data,login_fields(summon.lua(original)))
            self.assertEqual(len(data['fight_result_list']),10)

    def test_same_fight_id_from_different_modes_has_distinct_content_key(self):
        one=transport.lua_packets(1301,dict(id=85),dict(fight_id=7,details='a'*40000))
        two=transport.lua_packets(1301,dict(id=80),dict(fight_id=7,details='b'*40000))
        keys=[login_fields(decode(p[-1])[2]['data'])[transport.REFERENCE_KEY] for p in (one,two)]
        self.assertNotEqual(*keys)
        self.assertEqual(len(decoded_packets(one+two)),2)

    def test_twenty_heavy_records_use_bounded_child_preloads(self):
        # A real 240-action Rulai/absorption replay is ~314 KiB. Twenty
        # persisted records exceed the client's 4 MiB per-transfer guard.
        # Long strings keep the oracle independent of costly syntax-node count.
        history={i:dict(fight_id=i,encoded_actions='a'*314000+str(i)) for i in range(20)}
        original=dict(records=history,fight_type=118)
        self.assertGreater(len(summon.lua(original).encode()),4*1024*1024)
        packets=transport.event_packets(152,original)
        self.assertBudget(packets)
        totals={};chunks={}
        for packet in packets[:-1]:
            part=parsed_payload(decode(packet)[2]['data'])[transport.CHUNK_KEY]
            self.assertLessEqual(part['total'],256)
            totals[part['key']]=totals.get(part['key'],0)+len(part['payload'].encode())
            chunks[part['key']]=part['total']
        self.assertLess(len(chunks), 20, 'small siblings should share bounded preload groups')
        self.assertTrue(all(size<=transport.PRELOAD_BUDGET for size in totals.values()))
        result=login_fields(decoded_packets(packets)[0][2]['data'])
        self.assertEqual(result,original)

    def test_large_flat_event_table_groups_siblings_instead_of_one_packet_per_event(self):
        data = dict({i: dict(cur_action=i, speak='x'*1400) for i in range(1, 2001)}, fight_id=9)
        self.assertGreater(len(summon.lua(data).encode()), transport.PRELOAD_BUDGET)
        packets = transport.effect_packets(data)
        self.assertBudget(packets)
        self.assertLess(len(packets), 180)
        self.assertEqual(login_fields(decoded_packets(packets)[0][2]['data']), data)

    def test_persisted_effect_keys_and_empty_latest_replay_are_retained(self):
        records=[dict(fight_events={str(k):v for k,v in effects(100,i).items()}) for i in range(3)]
        before=copy.deepcopy(records)
        normalized=guild_combat.recent_records(records)
        self.assertEqual(len(normalized),3)
        self.assertIn(1,normalized[0]['fight_events'])
        packets=guild_combat.record_events(normalized);self.assertBudget(packets)
        self.assertEqual(len(decoded_packets(packets)),3)
        self.assertEqual(records,before)

    def test_large_monument_record_list_does_not_drop_oldest_or_all(self):
        data=[]
        for i in range(10):
            data.append(dict(src_name='我',vip_level=0,tao_point=0,role_combat_power=1,name='对手',time=i,
                line_up_msg=dict(lineup=[dict(src_type=5001,des_type=5002)]*8),
                fight_result_msg=dict(final_result=0,fight_result=[dict(note='a'*4000)]),fight_events=effects(2,i)))
        packets=monument.record_packets(dict(records=data))
        self.assertBudget(packets)
        responses=decoded_packets(packets)
        self.assertEqual([v['id'] for _,_,v in responses],[152,44])
        self.assertEqual(len(login_fields(responses[0][2]['data'])['records']),10)


if __name__=='__main__':unittest.main()
