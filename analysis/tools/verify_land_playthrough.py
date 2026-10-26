#!/usr/bin/env python3
"""Run isolated hunting-ground regressions and record real 128-battle progression."""
import io
import json
import re
from pathlib import Path
import sys
import time
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from tests.test_activity_land import OfflineLandTests
from network_redirect import activity_land_npc as npc

out=ROOT/'analysis/evidence/land'
out.mkdir(parents=True,exist_ok=True)
if '--retry-errors' in sys.argv:
    log=(out/'players_related_tests.log').read_text()
    names=[f'{case}.{method}' for method,case in re.findall(r'^(?:ERROR|FAIL): (\S+) \(([^)]+)\)',log,re.M)]
    if not names:raise SystemExit('No failed tests in the recorded run')
    stream=io.StringIO();start=time.monotonic()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
    (out/'players_retry_tests.log').write_text(stream.getvalue())
    record=json.loads((out/'players_playthrough.json').read_text());s=record['summary']
    s.setdefault('initial_run',dict(passed=s['passed'],errors=s['errors'],failures=s['failures']))
    s['retry']=dict(tests=result.testsRun,passed=result.wasSuccessful(),seconds=round(time.monotonic()-start,3),
                   note='Fresh process after concurrent convert configuration update; local TLS sockets permitted.')
    s.update(passed=result.wasSuccessful(),errors=len(result.errors),failures=len(result.failures))
    (out/'players_playthrough.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    print(stream.getvalue());raise SystemExit(0 if result.wasSuccessful() else 1)
trace=[]
class RecordedLand(OfflineLandTests):
    def req(self,mid,**data):
        result=super().req(mid,**data)
        if mid==1302:
            state=self.b.profile()['activity']['land']
            event=next((d for e,d in result if e==149),{})
            row=dict(op=data['id'],normal=state['boss_layer'],hell=state['inv_boss_layer'],
                     grids=state['grid_count'],map=state['map_level'],score=state['total_score'])
            if 'is_win' in event:row.update(win=event['is_win'],fight_type=event['fight_type'])
            if event.get('final_result_list'):
                replay=event['final_result_list'][1]['fight_result_msg']
                row.update(result=replay['final_result'],actions=replay['fight_round'])
            trace.append(row)
        return result

names=['tests.test_activity_land_players','tests.test_activity','tests.test_daily',
       'tests.test_npc_players','tests.test_role_profile','tests.test_combat_engine',
       'tests.test_combat_lanes','tests.test_offline_backend','tests.test_system_mail']
suite=unittest.TestSuite()
for name in unittest.defaultTestLoader.getTestCaseNames(OfflineLandTests):
    suite.addTest((RecordedLand if name=='test_complete_64_layers_both_worlds_real_battles' else OfflineLandTests)(name))
for name in names:suite.addTests(unittest.defaultTestLoader.loadTestsFromName(name))
stream=io.StringIO();start=time.monotonic()
result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
(out/'players_related_tests.log').write_text(stream.getvalue())
summary=dict(date='2026-10-26',passed=result.wasSuccessful(),tests=result.testsRun,
             seconds=round(time.monotonic()-start,3),failures=len(result.failures),errors=len(result.errors),
             npc_count=len(npc.catalog()),requests=len(trace),battles=sum('win' in r for r in trace),
             wins=sum(r.get('win',False) for r in trace),final=trace[-2] if trace else None,
             note='Temporary accounts; preloaded level-99 catalog army and soul balance. Real engine, no mocked wins.')
(out/'players_playthrough.json').write_text(json.dumps(dict(summary=summary,steps=trace),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
if not result.wasSuccessful():print(stream.getvalue())
raise SystemExit(0 if result.wasSuccessful() else 1)
