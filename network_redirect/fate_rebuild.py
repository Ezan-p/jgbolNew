"""Active release_w fate rebuilding: original costs/attributes, local server formula.

The activation and node contracts come from the frozen 1263 client. All state
changes run inside Backend.rebirth's detached transaction before serialization.
"""
from collections import Counter
from decimal import Decimal
import json
from . import formation as f, reborn, summon

ATTRS = json.loads((f.ROOT / 'server_config/fate_rebuild_attributes.json').read_text())
BY_ID = {v:k for k,v in ATTRS.items()}
PARTS = {1:'spirit_heaven', 2:'spirit_fortune', 3:'spirit_earth',
         4:'physic_tc', 5:'physic_lh', 6:'physic_qp', 7:'physic_lp',
         8:'physic_zs', 9:'physic_jp', 10:'physic_yp'}
ACTIVE = {int(x['cort_id']) for x in summon.rows('fate_rebuild/faterebuild_cort_active.csv')}
COSTS = {(int(x['Soul_part']),int(x['Level']),int(x['Stars'])):x['Cost']
         for x in summon.rows('fate_rebuild/rebuild_material_costs.csv')}
MAX_LEVEL = {p:max(l for pp,l,s in COSTS if pp == p)+1 for p in PARTS}

def pairs(text):
    return [(int(a),Decimal(b)) for a,b in (x.split('|') for x in text.split('/') if x)]

STARS = {(int(x['Soul_part']),int(x['Stars'])):pairs(list(x.values())[2])
         for x in summon.rows('fate_rebuild/stars_effect_config.csv')}
MILESTONES = {(int(x['Soul_part']),int(x['Level'])):pairs(list(x.values())[2])
              for x in summon.rows('fate_rebuild/level_effect_config.csv')}
CHOICES = {(int(x['ChoiceType']),int(x['EffectType'])):list(map(Decimal,x['EffectValues'].split('|')))
           for x in summon.rows('fate_rebuild/select_effect_config.csv')}
# Skill type -> the original middle-soul passive consumption bonus.
PASSIVES = {25:(377,Decimal('.1')),27:(377,Decimal('.1')),22:(377,Decimal('.4')),23:(377,Decimal('.4')),
            42:(376,Decimal('.4')),43:(376,Decimal('.4')),45:(376,Decimal('.1')),46:(376,Decimal('.1')),
            51:(374,Decimal(1)),52:(374,Decimal(1)),31:(375,Decimal('.4')),32:(375,Decimal('.4')),
            34:(375,Decimal('.1')),35:(375,Decimal('.1')),36:(375,Decimal('.1'))}

def star_count(part): return 9 if part <= 3 else 7

def essence_slots(c):
    slots = list(range(1, max(0,min(4,c.get('equiped_ext_skill_limit',0)))+1))
    if c.get('fate_rebullding_state') and c.get('spirit_earth_level',0)>=50:
        slots.append(5)
    return slots

def progress(c, part):
    stem = PARTS[part]
    return c.get(stem+'_level',0), c.get(stem+'_stars',0)

def refresh(c):
    """Rebuild derived values from progression, never compound saved panels."""
    for name in ATTRS: c.setdefault(name,0)
    effects = Counter()
    if c['fate_rebullding_state']:
        for part in PARTS:
            level, stars = progress(c,part)
            for star in range(1,star_count(part)+1):
                for attr,value in STARS[part,star]:
                    if attr: effects[attr] += value*(level + int(star <= stars))
        for (part,level), rows in MILESTONES.items():
            if progress(c,part)[0] >= level:
                for attr,value in rows:
                    if attr in (380,383,387,388,389): effects[attr] = max(effects[attr],value)
                    else: effects[attr] += value
        for attr,value in c.get('fate_passive_bonuses',{}).items(): effects[int(attr)] += Decimal(str(value))
        # [B] Soul amplification is applied to its corresponding seven-soul
        # contributions. Original UI associates heaven with tc/lh, fortune with
        # qp/lp/zs, and earth with jp/yp.
        for part,rate in ((4,382),(5,382),(6,385),(7,385),(9,386),(10,386)):
            level,stars = progress(c,part)
            for star in range(1,star_count(part)+1):
                for attr,value in STARS[part,star]:
                    if attr: effects[attr] += value*(level+int(star<=stars))*effects[rate]/100
        for attr,value in c.get('fate_passive_bonuses',{}).items():
            effects[int(attr)] += Decimal(str(value))*effects[385]/100
        for part,choice_id in ((1,380),(2,383)):
            chosen = c.get('fate_choices',{}).get(str(part),0)
            tier = int(effects[choice_id])
            if tier and (choice_id,chosen) in CHOICES:
                effects[chosen] = CHOICES[choice_id,chosen][tier-1]
    for attr in range(360,391):
        if attr in BY_ID:
            value = effects[attr]
            c[BY_ID[attr]] = int(value) if value == int(value) else float(value)
    # Choice fields in the native character hold the chosen attribute ID and
    # its value, not the unlock tier (the tier is read from level_effect_config).
    for part,attr in ((1,380),(2,383)):
        selected = c.get('fate_choices',{}).get(str(part),0)
        c[BY_ID[attr]] = selected
        c[BY_ID[attr+1]] = float(effects[selected]) if selected else 0


def state(role):
    result = {}
    for c in role['corteges']:
        refresh(c)
        if c['fate_rebullding_state']:
            result[c['id']] = {name:c[name] for name in ATTRS}
    return result


def sync(role):
    rows=list(state(role).items())
    # Keep fate out of the already large login config. Ten characters per
    # packet also bounds the Lua string and the protocol's uint16 frame size.
    return [summon.event(80, {'local_fate_rebuild':dict(rows[start:start+10]),
                             'local_fate_append':start>0})
            for start in range(0,max(1,len(rows)),10)]


def consume_node(role,c,part,raw,supplied):
    f.require(isinstance(supplied,dict) and supplied and all(type(k) is int and type(v) is int and v>0
              for k,v in supplied.items()), '逆天改命材料参数无效')
    tokens = list(map(int,raw.split('|'))); mode = tokens[0]
    passive_gain = Counter()
    if mode == 3:
        expected = dict(zip(tokens[1::2],tokens[2::2]))
        f.require(supplied == expected, '逆天改命材料种类或数量不符')
    else:
        f.require(set(supplied) <= set(tokens[1:-1]) and sum(supplied.values()) == tokens[-1],
                  '逆天改命所选材料种类或数量不符')
    if mode == 2:
        selected = []
        for tid,n in supplied.items():
            candidates = sorted((i for i in role['attachments'] if i['attach_type']==6 and i['type_id']==tid
                and i.get('count',1)>0 and i.get('level',1)==1 and not any(i.get(k) for k in
                ('is_lock','owner_id','equip_order','innate_owner_id','awaken','upgrade_level'))),key=lambda i:i['id'])
            f.require(len(candidates)>=n, '可用的1级未装备被动法术不足')
            selected.extend(candidates[:n])
            attr,value = PASSIVES[tid]; passive_gain[attr] += value*n
        remove = {i['id'] for i in selected}
        role['attachments'] = [i for i in role['attachments'] if i['id'] not in remove]
        bonuses = c.setdefault('fate_passive_bonuses',{})
        for attr,value in passive_gain.items(): bonuses[str(attr)] = float(Decimal(str(bonuses.get(str(attr),0)))+value)
    else:
        for tid,n in supplied.items(): reborn.debit_material(role,tid,n)
    # Exact debit ledger supports lossless, repeat-safe soul resets.
    ledger = c.setdefault('fate_materials',{}).setdefault(str(part),{})
    for tid,n in supplied.items(): ledger[str(tid)] = ledger.get(str(tid),0)+n


def settle(role,req,parse):
    data = parse(req['data'])
    f.require(isinstance(data,dict), '逆天改命参数无效')
    c = f.lookup(role,'corteges',data.get('cortege_id'))
    op = req['id']
    f.require(c['type'] in ACTIVE, '该神仙暂未开放逆天改命')
    f.require(role.get('reborn_layer',0)>=4 and c.get('reborn_layer',0)==9,
              '逆天改命需要主角四重境界、神仙九转')
    refresh(c)
    events = []
    if op == 3:
        f.require(not c['fate_rebullding_state'], '该神仙已激活逆天改命')
        reborn.debit_material(role,1371,20)
        c['fate_rebullding_state'] = 1
    else:
        f.require(c['fate_rebullding_state']==1, '请先消耗天命石激活逆天改命')
        if op == 0:
            part = data.get('soul_part')
            f.require(type(part) is int and part in PARTS, '魂魄位置无效')
            level,stars = progress(c,part)
            f.require((part,level,stars+1) in COSTS, '该魂魄已培养至上限')
            # Original soulSevenUI.judgeUnlockLayer: total is zero-based levels +7.
            if part>=4:
                total = sum(progress(c,p)[0] for p in range(4,11))+7
                f.require(level<=30 or total >= (100 if level<=60 else 200), '七魄总层数未达到要求')
            old_culture = c['fate_rebuilding_culture_point']
            consume_node(role,c,part,COSTS[part,level,stars+1],data.get('material_list'))
            stars += 1
            if stars == star_count(part): level,stars = level+1,0
            c[PARTS[part]+'_level'], c[PARTS[part]+'_stars'] = level,stars
            refresh(c)
            c['culture_point'] = c.get('culture_point',0) + int(c['fate_rebuilding_culture_point'])-int(old_culture)
        elif op == 2:
            part,selected = data.get('soul_part'),data.get('effect_type')
            f.require(type(part) is int and part in (1,2) and type(selected) is int, '三魂特性选择无效')
            choice = 380 if part==1 else 383
            tier = max((int(v) for (p,l),rows in MILESTONES.items() if p==part and l<=progress(c,part)[0]
                        for a,v in rows if a==choice),default=0)
            f.require(tier>0 and (choice,selected) in CHOICES, '此特性尚未解锁')
            old = c.setdefault('fate_choices',{}).get(str(part),0)
            f.require(old!=selected, '已经选择该特性')
            # Native confirmation charges only when replacing an existing choice.
            if old: f.debit_money(role,'gold_coin',50)
            c['fate_choices'][str(part)] = selected
        elif op in (4,5):
            part = 1 if op==4 else 2
            f.require(any(progress(c,part)), '此魂尚未培养，无需重置')
            ledger = c.get('fate_materials',{}).get(str(part),{})
            f.require(bool(ledger), '缺少消耗记录，无法安全返还')
            # Original client exposes resets but not a server price. Local rule:
            # refund exactly recorded materials, no invented fee or random loss.
            for tid,n in ledger.items(): summon.add_item(role,int(tid),n)
            events.append(summon.event(226,[dict(object_type=5,attach_type=int(tid),attach_count=n,attach_level=1)
                                           for tid,n in ledger.items()]))
            c[PARTS[part]+'_level']=c[PARTS[part]+'_stars']=0
            c.get('fate_choices',{}).pop(str(part),None)
            c['fate_materials'].pop(str(part),None)
        else:
            f.require(False,'逆天改命操作无效')
    refresh(c)
    return events


def base_bonuses(c,base,values):
    refresh(c)
    if not c['fate_rebullding_state']: return
    for stat,growth,attr in zip(f.STATS,f.GROWTH_COLUMNS,(374,376,377,375)):
        values[stat] += Decimal(base[growth])*(c['level']-1)*Decimal(str(c['fate_rebuilding_achive_rate']))/100
        values[stat] *= 1+Decimal(str(c[BY_ID[attr]]))/100


def bonuses(c,values):
    if not c.get('fate_rebullding_state'): return
    for stat,flat,rate in (('hp',360,366),('gongji',362,368),('fangyu',363,369),('magic',361,367)):
        values[stat] = (values[stat]+Decimal(str(c[BY_ID[flat]])))*(1+Decimal(str(c[BY_ID[rate]]))/100)


def combat_bonuses(c,unit):
    if not c.get('fate_rebullding_state'): return
    special_bonuses(c,unit)
    traits = unit.setdefault('reborn_traits',{})
    traits['fate_damage'] = c.get('fate_rebuilding_damage_train_rate',0)
    traits['fate_absorb'] = c.get('fate_rebuilding_absorb_train_rate',0)
    training = unit.get('training_bonuses',[(0,0)]*4)
    unit['training_bonuses'] = [(a,float(b)+c.get(name,0)) for (a,b),name in zip(training,
        ('fate_rebuilding_gongji_train','fate_rebuilding_fangyu_train','fate_rebuilding_magic_train','fate_rebuilding_fakang_train'))]

# Latest visible character descriptions cover all 15 enabled characters; the
# older cor/jp parameter CSVs contain only the first three. Keep the visible
# values as data and reconstruct battle timing using the shared local engine.
import re
DESCRIPTIONS = {(int(r['id']),int(r['soul_type']),int(r['property_layer'])):r['info']
                for r in summon.rows('fate_rebuild/faterebuild_cort_property.csv')}
ESSENCE_FAMILY = {5051:19,5052:5,5053:6,5022:2,5044:10,5034:13,5048:3,
                  5046:9,5024:18,5027:1,5013:16,5025:2,5023:18,5036:8,5021:7}
CHARACTER_TRAIT = {5051:'round_defense',5052:'target_hp_damage',5053:'shield',5022:'round_attack',
  5044:'round_heal',5034:'reflect',5048:'absorb',5046:'spell_damage',5024:'death_spell',
  5027:'damage',5013:'poison_damage',5025:'death_heal',5023:'ally_heal',5036:'absorb',5021:'spell_combo'}

def trait_values(c,kind):
    tier=c.get('fate_rebuilding_jp_effect_level' if kind==1 else 'fate_rebuilding_cor_effect_level',0)
    return [float(x) for x in re.findall(r'(\d+(?:\.\d+)?)',DESCRIPTIONS.get((c['type'],kind,tier),''))]


def special_bonuses(c,unit):
    if not c.get('fate_rebullding_state'):return
    from fractions import Fraction
    values=trait_values(c,1);family=ESSENCE_FAMILY.get(c['type'])
    effects=unit.get('essences',{})
    # A trait strengthens its engraved essence; it does not invent an unequipped one.
    if values and family in effects:
        old=list(effects[family])
        if family==16:
            old[1]+=Fraction(str(values[0]))
        elif family==9:
            unit['fate_penetration_proc']=values[0];old[0]+=Fraction(str(values[1]))
        else:
            for i,value in enumerate(values):
                if i<len(old):old[i]+=Fraction(str(value))
        effects[family]=tuple(old)
    values=trait_values(c,2)
    if values:unit['fate_traits']={CHARACTER_TRAIT[c['type']]:values}
