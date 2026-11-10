"""Original packets through detached DB settlement; no live save touched."""
import copy
from unittest.mock import patch
from tests.test_activity import ActivityCase, NOW
from network_redirect import activity, activity_party as party, achievements
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode
from pathlib import Path

class PartyTests(ActivityCase):
    def fight(self, paid=0):
        out=self.req(1026,fight_type=6,des_value=paid)
        self.ok(out)
        return dict(out)[29]

    def test_full_free_paid_cycle_and_replay(self):
        initial=self.b.profile()['gold_coin']
        peaches=0
        for _ in range(10):
            data=self.fight()
            peaches+=min(100,data['cur_damage']//10000)
            self.assertGreater(data['cur_damage'],0)
            self.assertTrue(data['damage_list'])
            self.assertLessEqual(data['cur_damage'],party.rules()['boss_hp'])
        before=self.b.profile()
        self.assertEqual(self.req(1026,fight_type=6)[0][0],55)
        self.assertEqual(before,self.b.profile())
        for _ in range(5):peaches+=min(100,self.fight(1)['cur_damage']//10000)
        before=self.b.profile();self.assertEqual(before['gold_coin'],initial-100)
        self.assertEqual(before['activity']['party']['week_lucky'],0)
        self.assertEqual(before['activity']['party']['peaches'],peaches)
        self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(before,self.b.profile())
        self.assertEqual(self.req(1026,fight_type=6,des_value=1)[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_daily_history_felstar_and_no_double_award(self):
        self.fight();before=self.b.profile();gold=before['gold_coin']
        with patch('network_redirect.game_clock.now',return_value=NOW+86400):
            h=dict(self.req(1049,query_type=2))[30];self.assertEqual(h['fight_count'],1)
            self.assertEqual(len(h['damage_list']),10);self.assertIn('id',h['felstar_info'])
            self.assertEqual(self.b.profile()['gold_coin'],gold)
            mail=self.b.profile()['welfare']['mails'][f"party-rank-{before['activity']['party']['day']}"]
            self.assertEqual(mail['prizes'],party.rewards('daily',h['self_order']))
            self.assertFalse(mail['claimed'])
            snapshot=self.b.profile();self.ok(self.req(1049,query_type=2));self.assertEqual(snapshot,self.b.profile())
            self.assertEqual(snapshot['activity']['party_count'],0)
            self.ok(self.req(1049,query_type=5,flag=2))
            self.assertEqual(self.req(1049,query_type=5,flag=2)[0][0],55)
            self.assertEqual(self.b.profile()['activity']['party']['history']['top_list'][1]['liked_times'],1)
        with patch('network_redirect.game_clock.now',return_value=NOW):
            self.ok(self.req(1049,query_type=1))
            self.assertEqual(self.req(1049,query_type=5,flag=2)[0][0],55)

    def test_lucky_disabled_including_legacy_pending_and_restart(self):
        self.fight()
        r=self.b.profile();p=r['activity']['party']
        p.update(pending=[[5,1001,1000,1]],week_lucky=100,week_history={'self_order':1})
        self.b.save(r)
        for days in (0,2,50):
            with patch('network_redirect.game_clock.now',return_value=NOW+days*86400):
                for mid,args in ((1049,dict(query_type=3)),(1201,dict(flag=1))):
                    out=self.req(mid,**args)
                    self.assertEqual(out[0][0],55)
                    self.assertIn('离线模式，暂不开启',str(out))
                self.ok(self.req(1049,query_type=1))
                saved=self.b.profile()
                self.assertFalse(saved['activity']['party']['pending'])
                self.assertEqual(saved['party_take_prize'],1)
                self.assertEqual(saved['party_order'],0)
                self.assertEqual(saved['activity']['party']['week_lucky'],0)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.b.profile()['activity']['party'],saved['activity']['party'])

    def test_damage_reward_boundaries_and_inventory(self):
        for damage,expected in ((0,0),(9999,0),(10000,1),(19999,1),(349380,34),(999999,99),(1000000,100),(10**9,100)):
            r=copy.deepcopy(self.b.profile())
            gain=party.fight_rewards(r,damage,self.b.activity_rules)
            self.assertEqual(sum(x['attach_count'] for x in gain if x['attach_type']==1001),expected)
            before=sum(x['count'] for x in self.b.profile()['attachments'] if x['type_id']==1001)
            after=sum(x['count'] for x in r['attachments'] if x['type_id']==1001)
            self.assertEqual(after-before,expected)

    def test_npcs_deterministic_and_inspectable(self):
        r=self.b.profile();day=activity.day(NOW,self.b.activity_rules)
        board=party.daily_board(r,day,86400,self.b.activity_rules)
        other=copy.deepcopy(r);other['role_combat_power']=99999999
        self.assertEqual(board,party.daily_board(other,day,86400,self.b.activity_rules))
        for ident in (next(iter(party.catalog())),next(reversed(party.catalog()))):
            self.ok(self.req(1039,des_type=1,des_id=ident,flag=3))
        self.assertTrue(all(n['role']['level']>=13 for n in party.catalog().values()))

    def test_catalog_does_not_initialize_entire_ladder(self):
        from network_redirect import activity_rank
        party.catalog.cache_clear()
        self.addCleanup(party.catalog.cache_clear)
        with patch.object(activity_rank, 'catalog', side_effect=AssertionError('Full ladder loaded')):
            entries = party.catalog()
            self.assertEqual(len(entries), 109)
            self.assertTrue(all(ident in entries for ident in range(950101, 950111)))

    def test_top_ten_use_rank_11_to_20_templates_and_inspection(self):
        from network_redirect import activity_rank, npc_players, summon
        r=self.b.profile();day=r['activity']['party']['day']
        original_ladder={ident:copy.deepcopy(activity_rank.catalog()[ident]) for ident in range(930011,930021)}
        for offset in (0,1,7,30):
            board=party.daily_board(r,day+offset,0,self.b.activity_rules)
            self.assertEqual(len(board),20)
            self.assertEqual(len({row['id'] for row in board}),20)
            for position,row in enumerate(board[:10],1):
                source=activity_rank.catalog()[930010+position]
                self.assertEqual(party.catalog()[row['id']],source)
                self.assertEqual(row['name'],source['role']['role_name'])
                self.assertEqual(row['power'],source['role']['role_combat_power'])
                self.assertIn(row['damage'],party.rules()['npc_damage_tiers'][position-1]['values'])
                if offset==0:
                    actual=dict(self.req(1039,des_type=1,des_id=row['id'],flag=3))[11]
                    packet=summon.event(11,npc_players.inspection_data(source,scene_id=row['id']))
                    expected=login_fields(decode(packet)[2]['data'])
                    self.assertEqual(actual,expected)
        before=party.daily_board(r,day,0,self.b.activity_rules)
        activity_rank.swap(r['activity'],11)
        r['activity']['party'].update(count=1,damage=100_000_000)
        after=party.daily_board(r,day,0,self.b.activity_rules)
        self.assertEqual([(x['id'],x['damage']) for x in before],
                         [(x['id'],x['damage']) for x in after if x['id']!=r['role_id']])
        party.finish_day(r,self.b.activity_rules,NOW)
        saved=copy.deepcopy(r['activity']['party']['history'])
        party.prepare(r,NOW+86400,self.b.activity_rules)
        self.assertEqual(r['activity']['party']['history'],saved)
        for row in saved['top_list']:
            if row['id']!=r['role_id']:
                self.assertEqual(party.inspection(r,row['id']),
                                 summon.event(11,npc_players.inspection_data(
                                     original_ladder[930010+row['id']-950100],scene_id=row['id'])))
        self.assertEqual({ident:activity_rank.catalog()[ident] for ident in original_ladder},original_ladder)

    def test_fixed_damage_tiers_daily_draw_and_restart(self):
        r=self.b.profile();day=r['activity']['party']['day']
        tiers=party.rules()['npc_damage_tiers']
        seen=[set() for _ in tiers]
        first=party.daily_board(r,day,0,self.b.activity_rules)
        for offset in range(365):
            board=party.daily_board(r,day+offset,0,self.b.activity_rules)
            self.assertEqual(len(board),20)
            self.assertEqual([x['id'] for x in board[:10]],list(range(950101,950111)))
            self.assertEqual([x['damage'] for x in board],sorted((x['damage'] for x in board),reverse=True))
            for i,row in enumerate(board[:10]):
                self.assertIn(row['damage'],tiers[i]['values'])
                self.assertTrue(79_150_000<=row['damage']<=117_700_000)
                seen[i].add(row['damage'])
            for row in board[10:]:
                self.assertEqual(row['damage'],10000+party.stable('party-score',day+offset,row['id'])%party.rules()['boss_hp'])
        self.assertEqual(seen,[set(t['values']) for t in tiers])
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        party.rules.cache_clear()
        self.assertEqual(first,party.daily_board(self.b.profile(),day,43200,self.b.activity_rules))
        r=self.b.profile();r['activity']['party'].update(count=1,damage=100_000_000)
        board=party.daily_board(r,day,0,self.b.activity_rules)
        player=next(x for x in board if x['id']==r['role_id'])
        self.assertEqual(player['damage'],100_000_000)
        self.assertEqual(player['rank'],1+sum(x['damage']>100_000_000 for x in first))

    def test_invalid_fixed_damage_tiers_are_rejected(self):
        import json
        base=copy.deepcopy(party.rules())
        variants=[]
        bad=copy.deepcopy(base);bad['npc_damage_tiers'].pop();variants.append(bad)
        bad=copy.deepcopy(base);bad['npc_damage_tiers'][0]['values'][0]=117_700_001;variants.append(bad)
        bad=copy.deepcopy(base);bad['npc_damage_tiers'][-1]['values'][-1]=79_149_999;variants.append(bad)
        bad=copy.deepcopy(base);bad['npc_damage_tiers'][1]['values'][0]=base['npc_damage_tiers'][0]['values'][-1];variants.append(bad)
        bad=copy.deepcopy(base);bad['npc_damage_tiers'][0]['values']=[117_700_000]*5;variants.append(bad)
        try:
            for bad in variants:
                party.rules.cache_clear()
                with patch.object(Path,'read_text',return_value=json.dumps(bad)),self.assertRaises(ValueError):
                    party.rules()
        finally:
            party.rules.cache_clear()

    def test_bonus_cost_cap_and_atomic_failure(self):
        gold=self.b.profile()['gold_coin']
        for _ in range(10):self.ok(self.req(1202,flag=1))
        self.assertEqual(self.b.profile()['gold_coin'],gold-275)
        before=self.b.profile();self.assertEqual(self.req(1202,flag=1)[0][0],55);self.assertEqual(before,self.b.profile())
        r=self.b.profile();r['gold_coin']=0;self.b.save(r);before=self.b.profile()
        self.assertEqual(self.req(1026,fight_type=6,des_value=1)[0][0],55);self.assertEqual(before,self.b.profile())

    def test_restricted_period_level_and_no_lineup(self):
        self.b.activity_rules['party_period']=[39600,46800]
        with patch('network_redirect.game_clock.now',return_value=NOW+7200):
            self.assertEqual(self.req(1026,fight_type=6)[0][0],55)
            self.assertEqual(self.req(1202,flag=1)[0][0],55)
        r=self.b.profile();r['level']=12;self.b.save(r)
        self.assertEqual(self.req(1026,fight_type=6)[0][0],55)
        r=self.b.profile();r['level']=60
        for c in r['corteges']:c['order']=0
        self.b.save(r);before=self.b.profile()
        self.assertEqual(self.req(1026,fight_type=6)[0][0],55);self.assertEqual(before,self.b.profile())

    def test_legacy_migration_and_backwards_clock(self):
        r=self.b.profile();r['activity'].pop('party');r['activity'].update(party_count=2,party_damage=1234)
        self.b.save(r);self.ok(self.req(1049,query_type=1));p=self.b.profile()['activity']['party']
        self.assertEqual((p['count'],p['damage'],p['week_lucky']),(2,1234,0))
        before=self.b.profile()
        with patch('network_redirect.game_clock.now',return_value=NOW-86400):
            self.assertEqual(self.req(1026,fight_type=6)[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_daily_npcs_are_static_scores_and_never_reduce_hp(self):
        r=self.b.profile();day=r['activity']['party']['day']
        board=party.daily_board(r,day,0,self.b.activity_rules)
        self.assertEqual(len(board),20)
        self.assertTrue(all(x['name'] and x['damage']>0 for x in board))
        for second in (39600,43200,46799,86400):
            self.assertEqual(board,party.daily_board(r,day,second,self.b.activity_rules))
            r['activity']['party']['clock']=(day*86400-self.b.activity_rules['timezone_offset_hours']*3600)+second
            info=party.info(r,self.b.activity_rules)
            self.assertEqual(info['cur_hp'],party.rules()['boss_hp'])
            self.assertEqual(info['total_damage'],0)
        self.assertNotEqual(board,party.daily_board(r,day+1,0,self.b.activity_rules))
        self.fight();r=self.b.profile();info=party.info(r,self.b.activity_rules)
        self.assertEqual(len(info['damage_list']),21)
        self.assertEqual(info['total_damage'],r['activity']['party']['damage'])
        self.assertEqual(info['cur_hp'],party.rules()['boss_hp']-info['total_damage']%party.rules()['boss_hp'])

    def test_wave_replenishes_and_rank_achievements(self):
        r=self.b.profile();p=r['activity']['party'];p.update(count=1,damage=10**12,lucky=10000,week_lucky=10000)
        day=p['day'];rows=party.daily_board(r,day,86400,self.b.activity_rules)
        # Deterministic selection can pick the human, not only NPCs.
        with patch.object(party,'stable',side_effect=lambda *args: 0):
            party.finish_day(r,self.b.activity_rules,NOW)
        party.prepare(r,NOW+2*86400,self.b.activity_rules)
        totals=achievements.state(r)['totals']
        for ident in (218,219,320):self.assertEqual(totals[str(ident)],1)
        for ident in (220,221):self.assertEqual(totals.get(str(ident),0),0)
        self.assertGreater(party.info(r,self.b.activity_rules)['cur_hp'],0)

    def test_query_on_backwards_clock_cannot_restore_chances(self):
        self.fight();self.ok(self.req(1202,flag=1))
        before=self.b.profile()['activity']['party']
        with patch('network_redirect.game_clock.now',return_value=NOW-86400):
            self.ok(self.req(1049,query_type=1))
            self.assertEqual(self.req(1202,flag=1)[0][0],55)
        after=self.b.profile()['activity']
        self.assertEqual(after['party_count'],before['free'])
        self.assertEqual(after['party_bonus'],before['bonus'])
        self.fight();self.assertEqual(self.b.profile()['activity']['party_count'],2)

    def test_materials_tasks_and_entry_usage(self):
        data=self.fight()
        self.assertGreater(len(data['fight_prize']),1)
        status=dict(self.req(1205,flag=1))[48]
        self.assertEqual((status['party_free_count'],status['party_pay_count']),(1,0))
        for _ in range(9):self.fight()
        r=self.b.profile()
        self.assertEqual(r['welfare']['task_progress'][str(activity.day(NOW,self.b.activity_rules))]['2'],10)

    def test_original_hours_boundaries_and_close_settlement(self):
        self.assertEqual(self.b.activity_rules['party_period'],[39600,46800])
        r=self.b.profile();r['activity']['party']['clock']=NOW-3601;self.b.save(r)
        for timestamp,allowed in ((NOW-3601,False),(NOW-3600,True),(NOW+3599,True),(NOW+3600,False)):
            with patch('network_redirect.game_clock.now',return_value=timestamp):
                result=self.req(1026,fight_type=6)
                if allowed:self.ok(result)
                else:self.assertEqual(result[0][0],55)
        with patch('network_redirect.game_clock.now',return_value=NOW+3600):
            h=dict(self.req(1049,query_type=2))[30]
            self.assertEqual(h['fight_count'],2)
            self.assertTrue(self.b.profile()['activity']['party']['closed'])
            self.assertEqual(self.req(1202,flag=1)[0][0],55)

    def test_boss_daily_stability_restart_and_actual_lineup(self):
        r=self.b.profile();p=r['activity']['party'];p['count']=1
        seen={};start=p['day']
        for offset in range(30):
            p['day']=start+offset
            expected=None
            for wave in range(5):
                p['damage']=wave*party.rules()['boss_hp']+123
                info=party.info(r,self.b.activity_rules)
                pair=(info['boss_type'],info['name'])
                if expected is None:expected=pair
                self.assertEqual(pair,expected)
                seen.setdefault(info['boss_type'],copy.deepcopy(r))
        self.assertEqual(set(seen),{4020,5025,3015})
        for tid,r in seen.items():
            timestamp=NOW+(r['activity']['party']['day']-start)*86400
            with patch('network_redirect.game_clock.now',return_value=timestamp):
                self.b.save(r)
                expected=party.info(self.b.profile(),self.b.activity_rules)
                self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
                actual=dict(self.req(1049,query_type=1))[29]
                self.assertEqual((actual['boss_type'],actual['name']),(tid,expected['name']))
                self.fight()
                lineup=next(d for m,_,d in self.decoded if m==1028)
                self.assertEqual(lineup['des_name'],expected['name'])
                self.assertEqual([x['des_type'] for x in lineup['lineup'] if x['des_type']],[tid])
                self.assertEqual(lineup['lineup'][0]['des_magic'],party.BOSS_MAGIC_CAP)

    def test_all_bosses_one_aoe_defeats_full_team_and_preserves_damage(self):
        from network_redirect import combat_engine, journey
        from tests.test_combat_engine import unit
        for boss in party.rules()['boss_pool']:
            with self.subTest(boss=boss['type']):
                ours=[unit(i,hp=2147483647,max_hp=2147483647,gongji=100,
                           essences={8:(100,),19:(100,100)},
                           reborn_traits=dict(survival=100,survival_count=10),
                           fate_traits=dict(absorb=[100],reflect=[100],death_heal=[100,100]))
                      for i in range(1,9)]
                enemy=journey.fighters({'corteges':[]},dict(cortege_list=f"{boss['type']}|60"))[1][0]
                party.prepare_boss(enemy,dict(boss_type=boss['type'],cur_hp=10000000))
                battle=combat_engine.Battle({},(ours,[enemy]),journey.load_rules())
                for target in battle.sides[0]:target['shield']=2147483647
                with patch('network_redirect.combat.secrets.randbelow',return_value=0):
                    result,lineup,actions=battle.run()
                self.assertIn(result,(4,5,6))
                attacks=[a for a in actions if not a['is_src']]
                self.assertEqual(len(attacks),1)
                self.assertEqual(attacks[0]['skill_type'],boss['aoe_skill'])
                self.assertEqual(attacks[0]['damage_list'],[2147483647]*8)
                self.assertEqual(actions.final_hp[1],dict.fromkeys(range(1,9),0))
                self.assertGreater(actions.damage_totals[1],0)
                self.assertLess(actions.damage_totals[1],10000000)
                self.assertEqual(actions.damage_totals[2],2147483647*8)
                self.assertEqual(lineup[0]['des_magic'],party.BOSS_MAGIC_CAP)
                # Exercise the same signed-int wire fields used by actual fights.
                from network_redirect.protocol import encode
                decoded=decode(encode(1027,dict(fight_id=1,fight_type=6,final_result=result,
                    fight_round=len(actions),fight_result=actions)))[2]
                self.assertEqual(decoded['fight_result'][-1]['damage_list'],[2147483647]*8)

    def test_boss_skill_probability_boundaries_are_party_only(self):
        from network_redirect import combat, journey
        for boss in party.rules()['boss_pool']:
            with self.subTest(boss=boss['type']):
                ordinary=journey.fighters({'corteges':[]},dict(cortege_list=f"{boss['type']}|60|{boss['aoe_skill']}"))[1][0]
                enemy=copy.deepcopy(ordinary)
                party.prepare_boss(enemy,dict(boss_type=boss['type'],cur_hp=10000000))
                for draw, triggered in [(99999,True),(100000,True),(199999,True),(200000,False)]:
                    with patch('network_redirect.combat.secrets.randbelow',return_value=draw):
                        self.assertEqual(combat.select_skill(enemy), (boss['aoe_skill'],1) if triggered else (1,1))
                        self.assertEqual(combat.select_skill(ordinary), (boss['aoe_skill'],1) if draw < 100000 else (1,1))

    def test_finisher_is_not_in_other_encounters(self):
        from network_redirect import combat_engine, journey
        from tests.test_combat_engine import unit
        for boss in party.rules()['boss_pool']:
            enemies=journey.fighters({'corteges':[]},dict(cortege_list=f"{boss['type']}|60|{boss['aoe_skill']}"))[1]
            self.assertNotIn('party_finisher_skill',enemies[0])
            battle=combat_engine.Battle({},([unit(i) for i in range(1,9)],enemies),journey.load_rules())
            actor=battle.sides[1][0]
            battle.attack(actor,battle.targets(actor,boss['aoe_skill']),boss['aoe_skill'])
            self.assertEqual(battle.actions[0]['damage_list'][4:],[0]*4)
