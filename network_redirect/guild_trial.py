"""Four persistent floors; random original five-star gods, local difficulty [B]."""
from . import summon
from .guild_offline import roll


def prepare(a,s,r):
    if a.get('train_bosses'):return
    # Preserve already earned rewards and remaining HP from single-boss saves.
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
        a['train_hp']=min(a['train_hp'],current(a)['hp'])


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
