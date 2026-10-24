"""冥仙精魄: original descriptions/drugs [A], deterministic local resolution [B].

Events 121 carry healing/revival to the unmodified replay. Extra attacks are real
1027 actions. The base damage formula remains the documented offline simulator.
"""
import copy
import secrets
from . import formation, journey, summon, reborn_stars
DESC={int(x['type_id']):[int(v.rstrip('%')) for v in x['reduce_value'].split('|')] for x in summon.rows('specter_jp_desc.csv')}
DRUGS={int(x['drug_type']):[list(map(int,t.split('|'))) for t in next(v for k,v in x.items() if k.startswith('effect1')).split('/')]
       for x in summon.rows('specter_extr_skill_drug.csv')}


def effects(row,pills):
    out={}
    for token in filter(None,row['ext_skill_list'].split('/')):
        _,tid,level,_=map(int,token.split('|'));out[tid]=DESC[tid][level-1]
    for tid in pills.values():
        if tid not in DRUGS:continue
        for fields in DRUGS[tid]:
            kind=fields[0]
            if kind in out:out[kind]=max(0,out[kind]-sum(fields[3:]))
    return out


def battle(role,units,rules,effect_values,max_actions=80):
    ours,enemies=copy.deepcopy(units);b=rules['battle'];limit=min(max_actions,b['max_actions'])
    reborn_stars.attach_combat_traits(role, ours)
    for side_index,side in enumerate((ours,enemies),1):
        for u in side:
            u['side']=side_index;u['extras']=effect_values.copy() if side_index==2 else {}
            u['base_gongji']=u['gongji'];u['base_fangyu']=u['fangyu'];u['base_hp']=u['max_hp']
            u['armor_break']=0;u['revived']=False
            strong=u['extras'].get(10113,0);extra=u['max_hp']*strong//100;u['max_hp']+=extra;u['hp']+=extra
    home=role.get('activity',{}).get('home',{}).get('train',{})
    if home:
        from .activity_home import TRAIN
        bonuses=[tuple(map(int,TRAIN[i,home[str(i)]['level']]['worth'].split('|'))) if home[str(i)]['level'] else (0,0) for i in range(1,5)]
        for u in ours:u['training_bonuses']=bonuses
    initial=copy.deepcopy((ours,enemies));actions=[];events=[];round_no=0

    def event(actor,tid,delta,action):
        if delta:
            events.append(dict(cur_action=action,logic_type=tid*10+1,who_use=actor['side'],self_use=True,
                src_order=actor['order'],des_order=actor['order'],speak='',
                skill_result_list=[dict(field=65,field_plus=delta,des_order=actor['order'])]))

    def heal(actor,amount,tid,action):
        delta=min(max(0,amount),actor['max_hp']-actor['hp']);actor['hp']+=delta;event(actor,tid,delta,action)

    def attack(actor,targets,sk=1,level=1,scale=100,reactions=True):
        if not actor['hp'] or not targets or len(actions)>=limit:return
        index=len(actions)+1;skill=formation.SKILLS[sk];damage=[0]*8;react=[];total=0
        for target in targets:
            if not target['hp']:continue
            power=actor['gongji']
            if sk!=1:
                power+=reborn_stars.spell_power(float(skill['intensity'])+float(skill['upgrade_plus'])*(level-1),sk,actor.get('reborn_traits',{}))
                power+=actor['magic']*b['skill_magic_percent']//100
            buffs=actor.get('training_bonuses',[(0,0)]*4);guards=target.get('training_bonuses',[(0,0)]*4)
            rate,flat=buffs[0 if sk==1 else 2];power=power*(100+rate)//100+flat
            # [B] Repeated armor break refreshes the strongest reduction, never stacks.
            target['armor_break']=max(target['armor_break'],actor['extras'].get(10102,0))
            defense=target['base_fangyu']*(100-target['armor_break'])//100
            rate,flat=guards[1 if sk==1 else 3];defense=defense*(100+rate)//100+flat
            raw=max(1,power*b['minimum_damage_percent']//100,power-defense*b['defense_percent']//100)
            if sk==1:raw=raw*(100+actor['extras'].get(10111,0))//100
            raw=raw*(100-target['extras'].get(10106 if sk==1 else 10108,0))//100
            hit=reborn_stars.combat_hit(max(1,raw*scale//100),target['hp'],sk==1,actor.get('reborn_traits',{}),target.get('reborn_traits',{}));target['hp']-=hit;total+=hit
            damage[target['order']-1]=hit
            revive=target['extras'].get(10119,0)
            if not target['hp'] and revive and not target['revived']:
                target['revived']=True;target['armor_break']=0;target['hp']=max(1,target['max_hp']*revive//100)
                # [A] Revival event is attached to the lethal action so fightUI
                # can revive at the end of its damage animation.
                event(target,10119,target['hp'],index)
            if reactions and target['hp'] and target['extras'].get(10103,0):react.append(target)
        actions.append(dict(self_use=False,skill_type=sk,is_src=actor['side']==1,result=0,src_order=actor['order'],
            des_order=targets[0]['order'],cur_round=round_no,damage_count=8,damage_list=damage))
        if actor['extras'].get(10105,0):heal(actor,total*actor['extras'][10105]//100,10105,index)
        for target in react:
            if actor['hp']:attack(target,[actor],scale=target['extras'][10103],reactions=False)

    while any(u['hp'] for u in ours) and any(u['hp'] for u in enemies) and len(actions)<limit:
        round_no+=1
        for order in range(1,9):
            for side,opposing in ((ours,enemies),(enemies,ours)):
                actor=next((u for u in side if u['order']==order and u['hp']),None)
                targets=[u for u in opposing if u['hp']]
                if not actor or not targets or len(actions)>=limit:continue
                extra=actor['extras']
                if round_no>=2 and extra.get(10110):heal(actor,actor['base_hp']*extra[10110]//100,10110,len(actions)+1)
                actor['gongji']=actor['base_gongji']*(100+(round_no//2)*extra.get(10112,0))//100
                sk,level=1,1
                for tid,lv in actor['skills']:
                    skill=formation.SKILLS[tid]
                    if int(skill['use_mode(1-active，2-passive)'])==1 and secrets.randbelow(100)<actor.get('skill_probabilities',{}).get(tid,int(skill['use_probability'])):
                        sk,level=tid,lv;break
                if int(formation.SKILLS[sk]['effect_target(1-single，2-multi)'])!=2:targets=targets[:1]
                attack(actor,targets,sk,level)
                alive=[u for u in opposing if u['hp']]
                if not actor['hp'] or not alive:continue
                if extra.get(10107):attack(actor,alive[:1],scale=extra[10107])
                elif extra.get(10115) and alive[0]['hp']*100<alive[0]['max_hp']*extra[10115]:attack(actor,alive[:1])
    oh,eh=sum(u['hp'] for u in ours),sum(u['hp'] for u in enemies)
    om,em=sum(u['max_hp'] for u in ours),sum(u['max_hp'] for u in enemies)
    result=journey.stars(oh,om) if oh*em>eh*om else 7-journey.stars(eh,em) if oh*em<eh*om else 0
    lineup=[]
    for order in range(1,max(u['order'] for u in ours+enemies)+1):
        row={}
        for prefix,side in zip(('src','des'),initial):
            u=next((u for u in side if u['order']==order),None)
            if u:
                row.update({prefix+'_'+key:u[key] for key in ('type','evolve','hp','max_hp','magic','reborn')})
                if prefix=='des':row['des_level']=u['level']
        lineup.append(row)
    return result,lineup,actions,events
