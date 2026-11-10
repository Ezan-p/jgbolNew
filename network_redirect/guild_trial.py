"""Four persistent floors; random original five-star gods, local difficulty [B]."""
from . import summon
from .guild_offline import roll


def support_info(a,r):
    """One bounded source for UI percentages and battle snapshot bonuses."""
    used=a.get('train_support',0)
    used=max(0,min(r['train_support_limit'],used)) if type(used)is int else 0
    return dict(support=used,support_limit=r['train_support_limit'],
                support_remaining=r['train_support_limit']-used,
                support_percent=r['train_support_percent'],
                support_gold=r['train_support_gold'],
                support_bonus_percent=used*r['train_support_percent'])


def prepare(a,s,r,role_level):
    a['train_support']=support_info(a,r)['support']
    if a.get('train_bosses'):
        scale(a,r,role_level)
        return
    # Preserve confirmed clears/claims; partial damage is not a cleared floor.
    cleared=4 if a.get('train_done') else max(a.get('train_claimed_stage',0),a.get('train_cleared',0))
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
    scale(a,r,role_level)


def scale(a,r,role_level):
    """Refresh strength without rerolling identities or resetting earned progress."""
    base_level=r['train_reference_level']
    level=max(base_level,int(role_level))
    for boss,base in zip(a['train_bosses'],r['train_floors']):
        boss['level']=level+base['level']-base_level
        for key in ('hp','attack','defense','magic'):
            boss[key]=base[key]*level*level//(base_level*base_level)
    # Every attempt starts at full health, including migrated partial-HP saves.
    a['train_hp']=0 if a.get('train_done') else current(a)['hp']


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


from .time_guard import protect as _protect_time_rewards
_protect_time_rewards(globals())
