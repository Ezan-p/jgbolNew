"""药神殿 original recipe/cost/recycling tables [A], craft quality/XP [B]."""
from . import activity as a, formation, summon
RECIPES={int(x['study_type']):x for x in summon.rows('specter_drug_study.csv')}
LEVELS={int(x['level']):int(x['need_exp(shuliandu)']) for x in summon.rows('specter_druggist_config.csv')}
TRANSFORM={int(x['src_material(object_type|attach_type|attach_level|attach_count)'].split('|')[1]):x
           for x in summon.rows('specter_material_transform.csv')}
MATERIALS={}
for row in RECIPES.values():
    for token in row['study_material(attach_type|attach_count|need_silver)'].split('/'):
        tid,n,cost=map(int,token.split('|'));MATERIALS[tid]=cost


def bag(role):
    result={1:{},2:{}}
    for item in role['attachments']:
        if item['attach_type']!=5:continue
        tid=item['type_id'];kind=2 if tid in MATERIALS else 1 if tid in TRANSFORM else 0
        if kind:result[kind][tid]=result[kind].get(tid,0)+item['count']
    return result


def flags(role,s):
    nums=[0,0]
    for i in s.setdefault('recipes',[]):nums[(i-1)//32]|=1<<((i-1)%32)
    role['drug_study_flag'],role['drug_study_flag2']=nums
    return dict(drug_study_flag=nums[0],drug_study_flag2=nums[1])


def shop():return [dict(object_type=5,attach_type=tid,attach_count=1,attach_level=1,need_silver=price) for tid,price in sorted(MATERIALS.items())]


def add_exp(role,n):
    role['drug_exp']+=n
    while role['drug_level']<max(LEVELS) and role['drug_exp']>=LEVELS[role['drug_level']]:
        role['drug_exp']-=LEVELS[role['drug_level']];role['drug_level']+=1


def use_exp(role,req):
    a.require(role['level']>=70 and req['flag']==3 and req['cortege_id']==0,'药灵丹使用目标无效')
    items=req['roll_list'];a.require(0<len(items)<=255 and req['roll_count']==len(items),'药灵丹选择无效')
    a.require(len({i['type_id'] for i in items})==len(items),'药灵丹不能重复选择')
    a.require(role['drug_level']<max(LEVELS),'炼药等级已满')
    total=0
    for item in items:
        tid,n=item['type_id'],item['count'];row=formation.ITEMS.get(tid,{})
        a.require(row.get('sub_type')=='101' and type(n)is int and 1<=n<=10000,'请选择药灵丹')
        a.consume(role,tid,n);total+=int(row['experience_plus'])*n
    add_exp(role,total)
    return [summon.event(65,dict(flag=3))]


def settle(role,s,op,d,r):
    from .activity_abyss import response
    role.setdefault('drug_level',1);role.setdefault('drug_exp',0);flags(role,s)
    extra={}
    if op in (18,19):
        if op==19:
            idx,n=d.get('index'),d.get('count',1)
            a.require(type(idx)is int and 1<=idx<=len(MATERIALS) and type(n)is int and 1<=n<=10000,'药材购买参数无效')
            row=shop()[idx-1];a.spend(role,'silver_coin',row['need_silver']*n);summon.add_item(role,row['attach_type'],n)
        return [response(op,shop_list=shop(),drug_bag=bag(role))]
    if op in (20,21,23):
        idx=d.get('index1') if op==23 else d.get('index');a.require(type(idx)is int and idx in RECIPES,'药方无效')
        row=RECIPES[idx];parts=[list(map(int,t.split('|'))) for t in row['study_material(attach_type|attach_count|need_silver)'].split('/')]
        if op==20:
            a.require(idx not in s['recipes'] and role['drug_level']>=int(row['min_level']),'已学习药方或炼药等级不足')
            a.spend(role,'gold_coin',int(row['consume_gold']));s['recipes'].append(idx);extra['modify_proper']=flags(role,s)
        elif op==23:
            i,n=d.get('index2'),d.get('count',1)
            a.require(type(i)is int and 1<=i<=len(parts) and type(n)is int and 1<=n<=10000,'药材购买参数无效')
            tid,_,price=parts[i-1];a.spend(role,'silver_coin',price*n);summon.add_item(role,tid,n)
        else:
            a.require(idx in s['recipes'] and role['drug_level']>=int(row['min_level']),'尚未学会该药方')
            for tid,n,_ in parts:a.consume(role,tid,n)
            # [B] Deterministic grade bands make the absent quality distribution
            # reproducible; only real item variants are emitted.
            grade=min(3,max(0,role['drug_level']-int(row['min_level']))//r['drug_quality_level_step'])
            tid=int(row['attach_type'])+grade
            a.require(tid in formation.ITEMS,'药品产出未配置')
            extra['drug_item']=a.prizes(role,[[5,tid,1,1]])
            add_exp(role,r['drug_craft_exp'])
        return [response(op,drug_bag=bag(role),**extra)]
    if op==8:
        tid,n=d.get('type_id'),d.get('num')
        a.require(type(tid)is int and tid in TRANSFORM and type(n)is int and 1<=n<=10000,'炼化参数无效')
        row=TRANSFORM[tid];typ,_,lv,count=map(int,row['src_material(object_type|attach_type|attach_level|attach_count)'].split('|'))
        a.require(typ==5 and lv==1,'炼化物品等级无效');a.consume(role,tid,count*n)
        gains=[]
        for token in row['des_material(object_type|attach_type|attach_level|attach_count/..)'].split('/'):
            typ,dest,lv,count=map(int,token.split('|'));gains.append([typ,dest,count*n,lv])
        a.prizes(role,gains)
        return [response(8,drug_bag=bag(role))]
    a.require(op==22 and d.get('client_flag',1) in (1,2,3),'药神殿查询参数无效')
    return [response(22,client_flag=d.get('client_flag',1),drug_bag=bag(role))]
