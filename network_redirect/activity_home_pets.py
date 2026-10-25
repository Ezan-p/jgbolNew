"""Home spirit-beast transformation: original materials, local growth memory [B]."""
import copy
from . import activity as a, summon
from . import activity_home as h

BASE={int(x['type_id']):{k.split('(')[0]:v for k,v in x.items()} for x in summon.rows('animal_base.csv')}
COST={int(x['quality']):x['consume_list'] for x in h.table('transform_pet_config')}
ATTR=('gongji','fangyu','hp','magic')


def initialize(s,r):
    s.setdefault('pets',[]);s.setdefault('pet_growth',{})
    # Missing acquisition service: a one-time starter when the spirit hall opens.
    if s['build']['5'] and not s.get('pet_starter_given'):
        from . import pets
        # Defer the gift at capacity so queries and consuming pets remain usable.
        if len(s['pets']) >= pets.load_rules()['capacity']:
            return
        active=any(p['order'] for p in s['pets'])
        pet=pets.add(s,r['home_starter_pet'],2)
        pet['order']=0 if active else 1
        s['pet_starter_given']=True


def memory(s):return {int(k):{int(q):copy.deepcopy(v) for q,v in x.items()} for k,x in s['pet_growth'].items()}


def wire(pet):
    data=copy.deepcopy(pet)
    # addInfo exits early when main_type is present, leaving name/next_exp unset.
    data.pop('main_type',None)
    data.setdefault('prob_compen',0)
    return data


def view(s):
    # Omitting pet_list triggers original query_pet_list, which enriches names and caches company_pet.
    data=dict(transform_info=memory(s))
    current=next((p for p in s.get('pets',[]) if p['order']),None)
    if current:data['fight_pet']=wire(current)
    return data


def settle(role,s,op,d,r):
    initialize(s,r)
    if op==22:return [h.response(op,dict(update_list={p['id']:wire(p) for p in s['pets']},transform_info=memory(s)))]
    a.require(s['build']['5']>0,'请先建造灵兽殿')
    pid,tid=d.get('pet_id'),d.get('des_type')
    a.require(type(pid)is int and type(tid)is int,'灵兽幻化参数无效')
    pet=next((p for p in s['pets'] if p['id']==pid),None)
    a.require(pet is not None and pet['main_type']>=2 and pet['quality'] in COST,'该灵兽不能幻化')
    a.require(tid in BASE and int(BASE[tid]['main_type'])>=2 and tid!=pet['type_id'],'目标灵兽类型无效')
    h.cost(role,COST[pet['quality']])
    s['pet_growth'].setdefault(str(pet['type_id']),{})[str(pet['quality'])]=copy.deepcopy(pet['grow_values'])
    saved=s['pet_growth'].get(str(tid),{}).get(str(pet['quality']))
    # Revisit restores recorded values; first visit keeps the source's increase over base.
    growth=saved or [max(1,int(BASE[tid]['base_'+k])+pet['grow_values'][i]-int(BASE[pet['type_id']]['base_'+k])) for i,k in enumerate(ATTR)]
    pet.update(type_id=tid,main_type=int(BASE[tid]['main_type']),grow_values=copy.deepcopy(growth))
    s['pet_growth'].setdefault(str(tid),{})[str(pet['quality'])]=copy.deepcopy(growth)
    return [h.response(op,dict(update_list={pet['id']:wire(pet)},transform_info=memory(s)))]
