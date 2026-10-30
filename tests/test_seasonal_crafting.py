"""Batch crafting through the actual local common-event wire envelope."""
from unittest.mock import patch
from test_activity import ActivityCase, NOW
from network_redirect import activity, activity_seasonal as season, formation, summon


class SeasonalCraftTests(ActivityCase):
    def count(self, tid):
        return sum(i['count'] for i in self.b.profile()['attachments'] if i['type_id']==tid and i['attach_type']==5)

    def fund(self, name, n=100):
        r=self.b.profile()
        for tid in (range(1134,1139) if name=='moon' else range(1208,1213)):
            summon.add_item(r,tid,15*n)
        self.b.save(r)

    def craft(self, name, index=1, n=1, **changes):
        data=dict(activity=name,count=n)
        if name=='moon':data['src_type']=1134+index
        else:
            data.update(compose_type=index,material_count=2,material_list=[dict(id=next(
                i['id'] for i in self.b.profile()['attachments'] if i['type_id']==tid)) for tid in (1208,1208+index)])
        data.update(changes)
        return self.req(2998,id=season.BATCH_EVENT,data=summon.lua(data))

    def test_all_eight_recipes_and_multiple_bonus_thresholds(self):
        for name,base,common in (('moon',1129,1134),('rice',1212,1208)):
            self.fund(name)
            before=self.count(1001)
            for index in range(1,5):
                out=self.craft(name,index,23);self.ok(out)
                result=next(d for e,d in out if e==(178 if name=='moon' else 126))
                self.assertEqual(result['local_craft_remaining'],100-23*index)
                self.assertEqual(self.count(base+index),23)
            self.assertEqual(self.count(common),15*8)
            self.assertEqual(self.count(1001)-before,90)
            self.assertEqual(self.b.profile()['activity']['seasonal'][name+'_count'],92)

    def test_hundred_at_once_replay_and_independent_daily_limits(self):
        for name in ('moon','rice'):
            self.fund(name,101);self.ok(self.craft(name,n=100))
            before=self.b.profile()
            self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
            self.assertEqual(self.b.profile(),before)
            self.assertEqual(self.craft(name)[0][0],55)
            self.assertEqual(self.b.profile(),before)
            with patch('network_redirect.backend.time.time',return_value=NOW+86400):self.ok(self.craft(name))
            self.assertEqual(self.b.profile()['activity']['seasonal'][name+'_count'],101)

    def test_invalid_quantities_recipes_and_partial_materials_rollback(self):
        for name in ('moon','rice'):
            self.fund(name,2)
            for n in (0,-1,101,1.5,True,'2',3):
                before=self.b.profile();self.assertEqual(self.craft(name,n=n)[0][0],55)
                self.assertEqual(self.b.profile(),before)
            before=self.b.profile()
            changes=dict(src_type=999) if name=='moon' else dict(compose_type=9)
            self.assertEqual(self.craft(name,**changes)[0][0],55);self.assertEqual(self.b.profile(),before)
            # No partial batch when only one daily craft remains.
            r=self.b.profile();season.state(r)['counts'][f'{name}:{activity.day(NOW,self.b.activity_rules)}']=99;self.b.save(r)
            before=self.b.profile();self.assertEqual(self.craft(name,n=2)[0][0],55);self.assertEqual(self.b.profile(),before)

    def test_locked_or_occupied_materials_and_closed_events(self):
        for name,common in (('moon',1134),('rice',1208)):
            self.fund(name,3)
            for flag in ('is_lock','owner_id','equip_pos','equip_order'):
                r=self.b.profile();item=next(i for i in r['attachments'] if i['type_id']==common);ident=item['id']
                item[flag]=1;self.b.save(r);before=self.b.profile()
                self.assertEqual(self.craft(name,n=2)[0][0],55);self.assertEqual(self.b.profile(),before)
                r=self.b.profile();formation.lookup(r,'attachments',ident)[flag]=0;self.b.save(r)
            self.b.activity_rules['seasonal_games'][name]['enabled']=False
            before=self.b.profile();self.assertEqual(self.craft(name,n=2)[0][0],55);self.assertEqual(self.b.profile(),before)

    def test_rice_consumes_only_selected_stacks_and_moon_combines_stacks(self):
        for name,common in (('moon',1134),('rice',1208)):
            self.fund(name,2);r=self.b.profile();ids=[]
            for tid in (common,common+1):
                item=dict(id=formation.new_id(r),attach_type=5,type_id=tid,count=15,level=1)
                ids.append(item['id']);r['attachments'].append(item)
            self.b.save(r)
            if name=='rice':
                before=self.b.profile()
                self.assertEqual(self.craft(name,n=2,material_list=[dict(id=i) for i in ids])[0][0],55)
                self.assertEqual(self.b.profile(),before)
                self.ok(self.craft(name,n=2))
                self.assertTrue(all(formation.lookup(self.b.profile(),'attachments',i)['count']==15 for i in ids))
            else:self.ok(self.craft(name,n=3));self.assertEqual(self.count(common),0)

    def test_reward_encoding_failure_rolls_back_entire_batch(self):
        for name,event in (('moon',178),('rice',126)):
            self.fund(name);before=self.b.profile();original=summon.event
            def fail(kind,data):
                if kind==event:raise formation.Rejected('test reward encode')
                return original(kind,data)
            with patch.object(summon,'event',side_effect=fail):self.assertEqual(self.craft(name,n=25)[0][0],55)
            self.assertEqual(self.b.profile(),before)

    def test_malformed_payload_and_rice_sources_rejected(self):
        self.fund('rice')
        for data in ('{}','{activity="invalid",count=2}','{activity="moon"}'):
            before=self.b.profile();self.assertEqual(self.req(2998,id=249,data=data)[0][0],55);self.assertEqual(self.b.profile(),before)
        for materials in (False,[],[1,2],[dict(id=1),dict(id=1)]):
            before=self.b.profile();self.assertEqual(self.craft('rice',n=2,material_list=materials)[0][0],55)
            self.assertEqual(self.b.profile(),before)

    def test_status_reports_each_remaining_quota_and_next_midnight(self):
        for name in ('moon','rice'):self.fund(name);self.ok(self.craft(name,n=3 if name=='moon' else 7))
        data=next(d for e,d in self.req(1205,flag=0) if e==47)
        for key,left in (('midautumn_data',97),('dragon_boat_info',93)):
            self.assertEqual(data[key]['local_craft_remaining'],left)
            self.assertEqual(data[key]['local_craft_reset_time'],(activity.day(NOW,self.b.activity_rules)+1)*86400-8*3600)
