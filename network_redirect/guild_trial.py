"""Four persistent floors; random original five-star gods, local difficulty [B]."""
from . import summon
from .guild_offline import roll


def prepare(a,s,r,role_level):
    if a.get('train_bosses'):
        scale(a,r,role_level)
        return
    # Preserve earned rewards and the remaining HP ratio from single-boss saves.
    cleared=4 if a.get('train_done') else max(a.get('train_claimed_stage',0),
        (r['train_hp']-a['train_hp'])*4//r['train_hp'] if a.get('train_hp') is not None else 0)
    a['train_cleared']=min(4,cleared)
    a['train_floor']=min(4,cleared+1)
    a['train_floor_attempts']=a.get('train_attempts',0)
    pool=sorted(tid for tid,base in summon.BASES.items()
                if int(base['quality'])==5 and 5000<=tid<6000)
    bosses=[]
    for difficulty in r['train_floors']:
        tid=pool.pop(roll(s,len(pool)))
        bosses.append(dict(type_id=tid,**difficulty))
    a['train_bosses']=bosses
    if a.get('train_hp') is not None and not a.get('train_done'):
        a['train_hp']=(max(0,min(r['train_hp'],a['train_hp']))*current(a)['hp']+r['train_hp']-1)//r['train_hp']
    scale(a,r,role_level)


def scale(a,r,role_level):
    """Refresh strength without rerolling identities or resetting earned progress."""
    base_level=r['train_reference_level']
    level=max(base_level,int(role_level))
    old_hp=current(a)['hp']
    for boss,base in zip(a['train_bosses'],r['train_floors']):
        boss['level']=level+base['level']-base_level
        for key in ('hp','attack','defense','magic'):
            boss[key]=base[key]*level*level//(base_level*base_level)
    new_hp=current(a)['hp']
    if a.get('train_hp') is not None and old_hp!=new_hp:
        # Round up so a living boss cannot die from a balance/level refresh.
        hp=max(0,min(old_hp,a['train_hp']))
        a['train_hp']=(hp*new_hp+old_hp-1)//old_hp


def current(a):
    return a['train_bosses'][a['train_floor']-1]


def advance(a):
    if a['train_hp']>0:return
    a['train_cleared']=a['train_floor']
    a['train_done']=a['train_cleared']==len(a['train_bosses'])
    if not a['train_done']:
        a['train_floor']+=1
        a['train_floor_attempts']=0
        a['train_hp']=current(a)['hp']
