"""Spend only the packaged starter's stock through unmodified v106 rules."""
import sys,tempfile,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'.runtime/v106-test/program'))
from offline_android.test_edition_seed import fixed_accounts_class,ACCOUNT
from network_redirect import formation as f, reborn as r, summon, immortal, skill_insight
from network_redirect.backend import login_fields
report={}
with tempfile.TemporaryDirectory() as d:
 a=fixed_accounts_class()(Path(d),18776,lambda *a,**k:None)
 a.authenticate({}); b=a.backends[ACCOUNT];role=b.profile()
 # Check original protocol serialization before spending any seed resources.
 b.bootstrap()
 assert (role['level'],role['vip_level'],role['gold_coin'])==(99,10,10000)
 assert role['guild']['unions']['2']['level']==5
 assert set(immortal.ESSENCES)<=set(i['type_id'] for i in role['attachments'])
 yu=role['corteges'][0]
 for n in range(1,300):f.evolve(role,dict(flag=0,cortege_id=yu['id']))
 assert yu['evolve_level']==299 and role['souls']['5046']==0
 report['evolution']=299
 def reb(kind,op,data):r.settle(role,dict(reborn_type=kind,id=op,data=summon.lua(data)),b.reborn_rules,login_fields)
 for _ in range(4):reb(1,4,{})
 assert role['reborn_layer']==4
 book=1080
 def feed_to_200():
  exp=sum(f.EXPERIENCE[5,lv] for lv in range(yu['level'],200))-yu['cur_exp']
  if exp<=0:return
  worth=int(f.ITEMS[book]['experience_plus']);n=(exp+worth-1)//worth
  f.feed(role,dict(flag=1,first_send=True,cortege_id=yu['id'],roll_count=1,roll_list=[dict(type_id=book,count=n)]),b.formation_rules)
 for layer in range(1,10):
  feed_to_200()
  for vein in range(1,10):
   row=r.VEINS[layer,vein];parts=[tuple(map(int,p.split('|'))) for p in row['consume_list'].split('/')]
   fixed=int(row['fixed_count(fix>0|unfix=0)']);m={parts[0][1]:fixed} if fixed else {p[1]:p[3] for p in parts}
   reb(2,1,dict(cortege_id=yu['id'],material_list=m))
  reb(2,2,dict(cortege_id=yu['id']))
 assert yu['reborn_layer']==9
 report['rebirth']=9;report['realm']=4
 skill=next(i for i in role['attachments'] if i['attach_type']==6 and i['type_id']==42 and i.get('equip_order')==1)
 donors=[i['id'] for i in role['attachments'] if i['attach_type']==6 and i['type_id']==25]
 for ident in donors:f.enhance_skill(role,dict(data=summon.lua(dict(des_skill_id=skill['id'],src_skill_list=[ident]))),b.formation_rules,login_fields)
 assert skill['level']==10
 mats=[dict(id=i['id']) for i in role['attachments'] if i['attach_type']==6 and i['type_id'] in (42,46) and not i.get('equip_order')]
 skill_insight.insight(role,dict(upgrade_type=6,des_id=skill['id'],material_count=2,material_list=mats))
 assert skill['upgrade_level']==1
 report['skill']={'level':10,'insight':1}
 eq=next(i for i in role['attachments'] if i['type_id']==2044)
 # Force minimum random enhancement gain to test worst-case silver requirement.
 original=summon.weighted_choice;summon.weighted_choice=lambda weights:1
 while eq['level']<198:f.enhance_equipment(role,dict(equip_id=eq['id'],equip_order=1,inbatch=True),b.formation_rules)
 summon.weighted_choice=original
 for advance in range(10):
  for star in range(7):f.advance_equipment(role,dict(equip_id=eq['id'],equip_order=1,flag=1,is_one_key=True),b.formation_rules)
  f.advance_equipment(role,dict(equip_id=eq['id'],equip_order=1,flag=2,is_one_key=True),b.formation_rules)
 reb(3,5,dict(equip_id=eq['id'],equip_order=1))
 while (1,eq['cast_level']+1) in r.CAST:reb(3,6,dict(equip_id=eq['id'],equip_order=1))
 report['equipment']={k:eq[k] for k in ('level','advance_level','cast_level','reborn_bit')}
 assert role['gold_coin']==10000
 assert all(sum(i['count'] for i in role['attachments'] if i['type_id']==tid and i['attach_type']==5)>=1 for tid in immortal.ESSENCES)
 b.save(role);b.bootstrap()
 # Bootstrap encodes the entire seed/progress with original protocol widths.
 a.close();a=fixed_accounts_class()(Path(d),18776,lambda *a,**k:None);a.authenticate({'action':'register','username':'unwanted'})
 saved=a.backends[ACCOUNT].profile()
 assert saved['corteges'][0]['reborn_layer']==9 and saved['gold_coin']==10000
 assert a.db.execute('select account from roles').fetchall()==[(ACCOUNT,)]
 report['restart_preserves_progress']=True;report['one_role_only']=True;report['all_38_essences_remain']=True
 a.close()
(ROOT/'analysis/evidence/v106_test').mkdir(parents=True,exist_ok=True)
(ROOT/'analysis/evidence/v106_test/progression-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(report)
