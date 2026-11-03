#!/usr/bin/env python3
"""100 distinct five-star rebirth NPC designs; never registers live players."""
import argparse
import copy
import csv
import hashlib
import json
import random
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools import build_npc_extreme as base

b, fr = base.b, base.fr
OUT = ROOT / 'analysis/npc_design/extreme_expansion'
OLD = ROOT / 'analysis/npc_design/extreme'
POOL = sorted(t for t in b.reborn.CORTS if t in b.f.BASES and b.quality(t) == 5
              and int(b.f.BASES[t]['base_type_id']) == t)
TANKS = [t for t in POOL if float(b.f.BASES[t]['base_fangyu_plus']) >= 10 or t == 5053]
RANGES = [{k: int(v) if k in ('lower','upper') and v else v for k,v in r.items()}
          for r in csv.DictReader((OLD/'power_ranges.csv').open())]
QUOTAS = {'E6':16, 'E5':17, 'E4':17, 'E3':17, 'E2':17, 'E1':16}
STAGES = {'E6':[0,1], 'E5':[0,1,2], 'E4':[1,2,3], 'E3':[2,3,4], 'E2':[3,4,5], 'E1':[4,5]}
THEMES = [
    dict(key='assault',name='破阵强袭',styles=['attack','endurance','attack','attack','attack','endurance','magic','attack'],
         anchors=[5022,5027,5052,5046,5048], slot=1, intent='后位与边路集中物理输出，法术替补补足伤害类型。'),
    dict(key='spell',name='群法压制',styles=['magic','endurance','magic','magic','magic','endurance','attack','magic'],
         anchors=[5024,5025,5035,5046,5013],slot=1,intent='法力核心承担主要施法，双承伤位争取施法轮次，攻击替补处理残局。'),
    dict(key='counter',name='反伤守御',styles=['attack','endurance','endurance','magic','attack','endurance','endurance','magic'],
         anchors=[5034],slot=2,intent='菩提前位与防御精魄组成反击结构，两名攻击核心维持清场能力；反伤特性需实际逆天解锁。'),
    dict(key='sustain',name='续航反攻',styles=['magic','endurance','endurance','attack','magic','endurance','endurance','attack'],
         anchors=[5044,5023,5025],slot=3,intent='恢复类候选与双输出协作，恢复特性仅在实际解锁后生效，低进度依靠防御与愈合精魄。'),
    dict(key='hybrid',name='攻法双核',styles=['attack','endurance','magic','attack','magic','endurance','attack','magic'],
         anchors=[5027,5046,5048,5052,5022],slot=1,intent='物理与法术核心分担输出，后备继承不同伤害方向，降低单一防御克制。'),
    dict(key='reserve',name='替补接力',styles=['magic','endurance','attack','endurance','attack','endurance','magic','attack'],
         anchors=[5052,5048,5022,5021],slot=5,intent='首发先建立局面，后位替补承担第二轮主攻；替补不在场时没有伤害或治疗。'),
]
PREFIX = ['苍梧','玄霄','赤霄','青冥','太微','紫宸','扶摇','沧溟','灵墟','玉衡']
SUFFIX = ['问剑','听澜','照雪','逐星','守真','渡厄','临风','观海','归云','破晓']
STYLE_NAME = {'attack':'强袭','magic':'法术','endurance':'承伤续航'}


def signature(npc):
    return tuple(sorted(c['type'] for c in npc['role']['corteges'] if c['order']))


def seed_for(index, attempt):
    return int.from_bytes(hashlib.sha256(f'20261103:extreme100:{index}:{attempt}'.encode()).digest()[:8], 'big')


def choose(rng, candidates, style, used, coverage):
    column = {'attack':'base_gongji_plus','magic':'base_maxmagic_plus','endurance':'base_fangyu_plus'}[style]
    available = sorted(t for t in candidates if t not in used)
    peak = max(float(b.f.BASES[t][column]) for t in available)
    weights = [(1+3*float(b.f.BASES[t][column])/peak) / (1+coverage[t]/12) for t in available]
    return rng.choices(available,weights=weights,k=1)[0]


def roster(rng, theme, coverage):
    result = {}; used = set()
    anchor = choose(rng,theme['anchors'],theme['styles'][theme['slot']-1],used,coverage)
    result[theme['slot']] = anchor; used.add(anchor)
    for pos in (2,6,1,3,4,5,7,8):
        if pos in result: continue
        style = theme['styles'][pos-1]
        candidates = TANKS if pos in (2,6) else POOL
        if pos == 8 and used <= fr.ACTIVE:
            candidates = [t for t in candidates if t not in fr.ACTIVE]
        # Damage cores receive a minimum natural growth in their main stat.
        if pos in (1,5):
            column = 'base_gongji_plus' if style == 'attack' else 'base_maxmagic_plus'
            candidates = [t for t in candidates if float(b.f.BASES[t][column]) >= (18 if style=='attack' else 14)]
            candidates = [t for t in candidates if unit_style(t,style,pos) != 'endurance']
        tid = choose(rng,candidates,style,used,coverage)
        result[pos] = tid; used.add(tid)
    return result


def unit_style(tid, planned, pos):
    """Respect recognizable native specializations inside mixed team themes."""
    if pos in (2,6) or tid in (5034,5036,5044,5051,5023,5033,5050):
        return 'endurance'
    if tid in (5022,5027,5048,5052):
        return 'attack'
    if tid in (5024,5025,5035):
        return 'magic'
    return planned


@lru_cache(maxsize=None)
def fate_payload(stage, style, tank):
    c = dict(type=5022,order=2 if tank else 1)
    base.fate_plan(c,base.PROFILES[stage],style)
    return {k:v for k,v in c.items() if k not in ('type','order')}


def outfit(role,c,style,stone_level,rng):
    b.outfit(role,c,style,'T1')
    gear = [i for i in role['attachments'] if i['attach_type']==5 and i.get('equip_order')==c['order']]
    for item in gear:
        old = b.f.ITEMS[item['type_id']]
        fates = {int(t) for row in b.f.FATES if int(row['cortege_type[effected_cortege]'])==c['type']
                 and row['tartege_type[4-cortege/5-equip/6-skill]']=='5' for t in row['target_object_type[1/2/3]'].split('/')}
        candidates = sorted(t for t,cfg in b.f.ITEMS.items() if cfg['quality']=='5' and cfg['main_type']==old['main_type'])
        preferred = [t for t in candidates if t in fates]
        item['type_id'] = rng.choice(preferred or candidates)
        cfg = b.f.ITEMS[item['type_id']]
        item['level'] = min(198,int(cfg['top_level']))
        item['equip_pos'] = int(cfg['equip_pos'])
        item['stone1_level'] = stone_level
        stone = next(i for i in role['attachments'] if i.get('owner_id')==item['id'])
        stone['level'] = stone_level
    ess = [i for i in role['attachments'] if i.get('owner_id')==c['id'] and i['type_id'] in b.cp.ESSENCE_SCORES]
    # Variation within a style, retaining its useful pair interactions.
    packages = {'attack':[[11,4,7,5],[11,4,2,5],[11,7,5,12]],
                'magic':[[9,8,12,18],[9,8,13,18],[9,8,16,17]],
                'endurance':[[10,14,6,3],[10,14,8,19],[10,14,13,3]]}
    families = rng.choice(packages['endurance' if c['order'] in (2,6) else style]).copy()
    active = c.get('fate_rebullding_state')
    if active and fr.ESSENCE_FAMILY[c['type']] not in families:
        if 5 in fr.essence_slots(c): families.append(fr.ESSENCE_FAMILY[c['type']])
        else: families[-1] = fr.ESSENCE_FAMILY[c['type']]
    if active and 5 in fr.essence_slots(c) and len(families)==4:
        families.append(rng.choice([t for t in (2,6,8,10,13,14,17,18,19) if t not in families]))
    for i,family in zip(ess,families): i.update(type_id=10200+family,level=5)
    if len(families)==5: b.attach(role,5,10200+families[-1],level=5,owner_id=c['id'],ext_skill_pos=5)


def generate(index,attempt,tier,coverage):
    seed=seed_for(index,attempt);rng=random.Random(seed)
    theme=THEMES[(index+attempt//16)%len(THEMES)]
    stage=rng.choice(STAGES[tier]);p=base.PROFILES[stage]
    selected=roster(rng,theme,coverage)
    styles=[unit_style(selected[pos],theme['styles'][pos-1],pos) for pos in range(1,9)]
    role=dict(role_id=961000001+index,name=PREFIX[index//10]+SUFFIX[index%10],level=99,
              corteges=[],attachments=[],summon={'next_id':1},reborn_layer=4,max_combat_power=0)
    hs=base.home.storage(role)
    hs.update(level=2,build={'1':p['home'],'2':p['home'],'3':p['home'],'4':0,'5':0})
    role['cortege_limit_plus']=int(base.home.BUILD[1][p['home']]['coretege_limit_plus'])
    role['hole_hp_plus']=base.home.point(hs)
    active_orders=[pos for pos in (1,2,3,4,5,6,7,8) if selected[pos] in fr.ACTIVE][:p['active']]
    culture_percent=rng.choice((90,93,95,97))
    for pos,tid in sorted(selected.items()):
        style=styles[pos-1]
        c=b.make_companion(role,style,'T1',tid,order=pos)
        c.update(level=p['level'],evolve_level=p['evolve'],reborn_layer=9,level_culture_version=3)
        if pos in active_orders: c.update(copy.deepcopy(fate_payload(stage,style,pos in (2,6))))
        base.allocate(c,style,culture_percent)
    remaining=[t for t in POOL if t not in selected.values()];rng.shuffle(remaining)
    targets=list(range(1,9));rng.shuffle(targets)
    reverse=list(range(1,9));rng.shuffle(reverse);targets+=reverse
    for support,tid in enumerate(remaining[:16],1):
        style=styles[targets[support-1]-1]
        c=b.make_companion(role,style,'T1',tid,support=support)
        c.update(level=200,evolve_level=49,reborn_layer=0,level_culture_version=3)
        base.allocate(c,style,75)
        name=b.cheer.NAMES[support-1]
        role['cheer_'+name+'_level']=10;role['cheer_'+name+'_effect']=targets[support-1]
    c=b.make_companion(role,'endurance','T1',remaining[-1],reserve=True)
    c.update(level=100,evolve_level=0,reborn_layer=0,level_culture_version=3)
    base.allocate(c,'endurance',0)
    b.cheer.prepare(role,b.CHEER);b.f.prepare(role,b.RULES)
    for c in role['corteges']:
        if c['order']:outfit(role,c,styles[c['order']-1],p['stone'],rng)
    b.cp.recalculate(role,b.RULES,now=base.NOW)
    nearest=min(OLD_NPCS,key=lambda n:abs(n['role']['role_combat_power']-role['role_combat_power']))
    return dict(npc_id=f'npc_extreme100_{index+1:03d}',status='design_only',tier=tier,stage=p['stage'],
                theme=theme['key'],theme_name=theme['name'],intent=theme['intent'],unit_styles=styles,
                seed=seed,attempt=attempt,culture_percent=culture_percent,active_orders=active_orders,
                profile=copy.deepcopy(p),source_template_id=nearest['npc_id'],role=role)


OLD_NPCS=json.loads((OLD/'catalog.json').read_text())['npcs']


def validate(n):
    base.validate(n,expected_roster=25)
    role=n['role'];assert {c['type'] for c in role['corteges']}==set(POOL)
    assert all(b.quality(c['type'])==5 and c['type'] in b.reborn.CORTS for c in role['corteges'])
    members=[c for c in role['corteges'] if c['order']]
    assert all(c['reborn_layer']==9 for c in members)
    assert all(n['unit_styles'][pos-1] != 'endurance' for pos in (1,5))
    assert all(next(c for c in members if c['order']==pos)['type'] in TANKS for pos in (2,6))
    assert any(c['type'] not in fr.ACTIVE for c in members)
    r=next(r for r in RANGES if r['tier']==n['tier'])
    assert r['lower']<=role['role_combat_power'] and (not r['upper'] or role['role_combat_power']<=r['upper'])
    for name in b.cheer.NAMES:
        assert role['cheer_'+name+'_level']==10 and role['cheer_'+name+'_effect'] in range(1,9)
    assert Counter(role['cheer_'+name+'_effect'] for name in b.cheer.NAMES)==Counter({p:2 for p in range(1,9)})
    for c in members:
        assert bool(c.get('fate_rebullding_state'))==(c['order'] in n['active_orders'])
        if c.get('fate_rebullding_state'):
            expected=copy.deepcopy(fate_payload(int(n['stage'][1:])-1,n['unit_styles'][c['order']-1],c['order'] in (2,6)))
            assert c['fate_materials']==expected['fate_materials'] and c['fate_passive_bonuses']==expected['fate_passive_bonuses']
        else:
            assert all(fr.progress(c,p)==(0,0) for p in fr.PARTS)
    units=base.combat_loadout.player_units(copy.deepcopy(role))
    assert len(units)==8
    for u in units:
        c=next(c for c in members if c['id']==u['companion_id'])
        if c.get('fate_rebuilding_cor_effect_level',0): assert u.get('fate_traits')


def build():
    accepted=[];used={signature(n) for n in OLD_NPCS};coverage=Counter();attempts=0
    for tier,count in QUOTAS.items():
        for _ in range(count):
            index=len(accepted)
            for attempt in range(640):
                n=generate(index,attempt,tier,coverage);attempts+=1
                r=next(r for r in RANGES if r['tier']==tier);power=n['role']['role_combat_power']
                sig=signature(n)
                if power<r['lower'] or r['upper'] and power>r['upper'] or sig in used: continue
                validate(n);accepted.append(n);used.add(sig);coverage.update(sig)
                break
            else: raise AssertionError(f'Cannot fill {tier} index {index}')
        print(f'{tier}: {count} accepted, {len(accepted)} total, {attempts} candidates',flush=True)
    assert len(accepted)==100 and len({signature(n) for n in accepted})==100
    assert set(coverage)==set(POOL) and min(coverage.values())>=8
    assert len({n['role']['role_id'] for n in accepted+OLD_NPCS})==118
    assert len({n['role']['name'] for n in accepted+OLD_NPCS})==118
    return accepted,attempts


def battles(npcs):
    rows=[];pairs=[]
    # Same-tier cyclic pairs: every NPC fights two opponents, on both sides.
    for tier in QUOTAS:
        group=sorted([n for n in npcs if n['tier']==tier],key=lambda n:n['role']['role_combat_power'])
        pairs += [('same_tier',a,group[(i+1)%len(group)]) for i,a in enumerate(group)]
    for n in npcs:
        template=next(x for x in OLD_NPCS if x['npc_id']==n['source_template_id'])
        pairs.append(('template',n,template))
    for kind,a,z in pairs:
        for seed in (17,83):
            for left,right in ((a,z),(z,a)):
                ar,br=copy.deepcopy(left['role']),copy.deepcopy(right['role'])
                # Frozen templates retain their original saved progression; refresh panels only.
                for role in (ar,br):b.cp.recalculate(role,b.RULES,now=base.NOW)
                rng=random.Random(seed);error='';result=''
                with patch('network_redirect.combat.secrets.randbelow',side_effect=rng.randrange):
                    engine=b.combat_engine.Battle(ar,(base.combat_loadout.player_units(ar),base.combat_loadout.player_units(br)),b.journey.load_rules(),slots=8)
                    try:
                        result,_,actions=engine.run();reason=actions.stop_reason
                        assert all(hp>=0 for s in actions.final_hp.values() for hp in s.values())
                    except TypeError as exc:
                        if str(exc)!='both arguments should be Rational instances':raise
                        actions=engine.actions;reason='runtime_error';error=str(exc)
                rows.append(dict(kind=kind,left=left['npc_id'],right=right['npc_id'],seed=seed,
                                 left_power=ar['role_combat_power'],right_power=br['role_combat_power'],result=result,
                                 action_count=len(actions),stop_reason=reason,error=error))
        if len(rows)%160==0:print(f'battles: {len(rows)}/800',flush=True)
    assert len(rows)==800
    return rows


def file_hash(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def view(item):
    names=b.SKILL_NAMES if item['attach_type']==6 else b.ITEM_NAMES
    return f"{names.get(item['type_id'],str(item['type_id']))}({item['type_id']}) Lv{item['level']}"


def export(npcs,checks,attempts):
    files={};overview=[];companions=[];coverage=Counter();themes=Counter();ranges=[]
    detailed={t:[f'# {t} {base.LABELS[t]}：新增NPC详细配置','',
                    '日期：2026-11-03。设计快照未注册进游戏；全名册五星且均可转生。4首发＋4替补＋16助威＋1背包候补。', '',
                    '[返回100名总览](../逐名配置.md)。装备强化按模板上限（通常198）、进阶10、封神、铸造4、六星；每件1孔。主力九转，助威与候补具资格但尚未转生。', ''] for t in QUOTAS}
    for n in npcs:
        r=n['role'];tier=n['tier'];coverage.update(signature(n));themes[n['theme_name']]+=1
        affected=[c for c in checks if c['stop_reason']=='runtime_error' and n['npc_id'] in (c['left'],c['right'])]
        n['battle_status']='runtime_error_observed' if affected else 'sampled_engine_only'
        n['fate_combo_risk']=any(c['type']==5021 and c.get('fate_rebullding_state') for c in r['corteges'] if c['order'])
        n['battle_error_count']=len(affected)
        path=f"npcs/{n['npc_id']}.json";files[path]=b.json_text(n)
        overview.append(dict(npc_id=n['npc_id'],name=r['name'],reserved_role_id=r['role_id'],tier=tier,stage=n['stage'],
                             theme=n['theme_name'],power=r['role_combat_power'],fate_count=len(n['active_orders']),
                             culture_percent=n['culture_percent'],template=n['source_template_id'],seed=n['seed'],attempt=n['attempt'],
                             battle_status=n['battle_status'],fate_combo_risk=n['fate_combo_risk'],file=path,
                             roster=' / '.join(f"{c['order']}:{b.NAMES[c['type']]}" for c in r['corteges'] if c['order'])))
        lines=detailed[tier]
        lines += [f"## {r['name']}｜{n['npc_id']}｜{r['role_combat_power']:,}",'',
                  f"{n['stage']}，{n['theme_name']}；逆天{len(n['active_orders'])}名（阵位{','.join(map(str,n['active_orders'])) or '无'}），培养{n['culture_percent']}%。预留角色ID {r['role_id']}。",'',
                  n['intent'],'',f"参照模板：`{n['source_template_id']}`；对战状态：`{n['battle_status']}`；地藏连击潜在风险：{'有' if n['fate_combo_risk'] else '无'}。",'',
                  f"[完整快照](../{path})。主殿／药园／佛堂{n['profile']['home']}级；洞府生命+{r['hole_hp_plus']:,}。",'',
                  '| 位 | 神仙 | 职责 | 等级／飞升／转生 | 三魂 | 七魄 | 生命／攻击／防御／法力 | 战力 |',
                  '|---|---|---|---|---|---|---|---:|']
        for c in r['corteges']:
            pos=c['order'];soul='/'.join(str(fr.progress(c,p)[0]) for p in range(1,4));body='/'.join(str(fr.progress(c,p)[0]) for p in range(4,11))
            owned=[i for i in r['attachments'] if i.get('owner_id')==c['id']]
            equipped=[i for i in r['attachments'] if pos and i.get('equip_order')==pos]
            skills=[i for i in equipped if i['attach_type']==6];gear=[i for i in equipped if i['attach_type']==5]
            ess=[i for i in owned if i['type_id'] in b.cp.ESSENCE_SCORES];stars=[i for i in owned if i['type_id'] in b.reborn_stars.STARS]
            row=dict(npc_id=n['npc_id'],order=pos,cheer_order=c['cheer_order'],type=c['type'],name=b.NAMES[c['type']],quality=5,rebirth_eligible=True,
                     level=c['level'],evolve=c['evolve_level'],reborn=c['reborn_layer'],fate_active=bool(c.get('fate_rebullding_state')),
                     style=n['unit_styles'][pos-1] if pos else 'support' if c['cheer_order'] else 'idle',power=c['combat_power'],
                     culture='/'.join(str(c[s+'_plus']) for s in b.f.STATS),remaining=c['culture_point'],
                     budget=b.budget(c)+int(c.get('fate_rebuilding_culture_point',0)),souls=soul,bodies=body,
                     equipment=' / '.join(view(i) for i in gear),skills=' / '.join(view(i) for i in skills),
                     essences=' / '.join(view(i) for i in ess),stars=' / '.join(view(i) for i in stars))
            companions.append(row)
            if pos:lines.append(f"| {pos} | {b.NAMES[c['type']]} {c['type']} | {STYLE_NAME[row['style']]} | {c['level']}/{c['evolve_level']}/{c['reborn_layer']} | {soul} | {body} | "+'/'.join(f"{c[s]:,}" for s in b.f.STATS)+f" | {c['combat_power']:,} |")
        lines += ['','### 逐仙养成','']
        for c in r['corteges']:
            if not c['order']:continue
            row=next(x for x in companions if x['npc_id']==n['npc_id'] and x['order']==c['order'])
            skills=[i for i in r['attachments'] if i['attach_type']==6 and i.get('equip_order')==c['order']]
            lines += [f"**{c['order']}号 {b.NAMES[c['type']]}**",'',f"- 装备：{row['equipment']}；每件1枚{n['profile']['stone']}级对应灵石。",
                      '- 法术：'+' / '.join(view(i)+f"，觉醒{i.get('awaken',0)}" for i in skills)+'。',
                      f"- 精魄：{row['essences']}；命星：{row['stars']}。",
                      f"- 培养（生／攻／防／法）：{row['culture']}；预算{row['budget']:,}、剩余{row['remaining']:,}。",
                      f"- 逆天选择：{json.dumps(c.get('fate_choices',{}),ensure_ascii=False)}；中枢被动：{json.dumps(c.get('fate_passive_bonuses',{}),ensure_ascii=False)}。",'']
        lines += ['### 助威与候补','','助威均五星可转生、200级、49飞升、0转生、75%培养、八卦10级，无普通装备与额外助威法术；1～8为正位、9～16为逆位。','',
                  '| 助威位 | 神仙 | 受益阵位 |','|---|---|---|']
        for c in r['corteges']:
            if c['cheer_order']:
                name=b.cheer.NAMES[c['cheer_order']-1];lines.append(f"| {c['cheer_order']} | {b.NAMES[c['type']]} {c['type']} | {r['cheer_'+name+'_effect']} |")
        idle=next(c for c in r['corteges'] if not c['order'] and not c['cheer_order'])
        lines += ['',f"背包候补：{b.NAMES[idle['type']]} {idle['type']}，五星可转生、100级、0飞升／转生、未培养，不参战。",'']
    coverage_rows=[dict(type=t,name=b.NAMES[t],quality=5,rebirth_eligible=True,fate_eligible=t in fr.ACTIVE,
                        active_occurrences=coverage[t],support_occurrences=sum(c['type']==t and bool(c['cheer_order']) for n in npcs for c in n['role']['corteges'])) for t in POOL]
    for r in RANGES:
        powers=[n['role']['role_combat_power'] for n in npcs if n['tier']==r['tier']]
        ranges.append(dict(tier=r['tier'],lower=r['lower'],upper=r['upper'],count=len(powers),sample_min=min(powers),sample_max=max(powers)))
    summary=dict(date='2026-11-03',new_npcs=100,previous_npcs=18,combined_npcs=118,unique_new_rosters=100,
                 unique_old_rosters=len({signature(n) for n in OLD_NPCS}),old_roster_overlap=0,
                 candidate_count=len(POOL),candidate_min_occurrences=min(coverage.values()),candidate_max_occurrences=max(coverage.values()),
                 total_members=2500,active_members=800,support_members=1600,idle_members=100,all_members_five_star_rebirth_eligible=True,
                 tier_counts=QUOTAS,theme_counts=dict(themes),attempted_candidates=attempts,max_attempt=max(n['attempt'] for n in npcs),
                 data_validation='passed',battle_attempts=len(checks),battle_stop_reasons=dict(Counter(x['stop_reason'] for x in checks)),
                 battle_validation='failed' if any(x['stop_reason']=='runtime_error' for x in checks) else 'engine_sampled',
                 battle_error_npcs=sum(n['battle_status']=='runtime_error_observed' for n in npcs),
                 fate_combo_risk_npcs=sum(n['fate_combo_risk'] for n in npcs),backend_registered=False,native_client_validated=False)
    lines=['# 新增100名极高战力NPC：逐名配置目录','','日期：2026-11-03。原18名模板保留，合计118名极高战力设计NPC；本批100套出战神仙集合彼此不同且不与原3套组合重复。','',
           '全名册均五星、均具真实转生资格；每人8名九转出战＋16助威＋1背包候补。数字ID尚未注册为游戏查询ID。','',
           '[扩充设计说明](../../../docs/极高战力NPC新增100名多样阵容设计说明.md) · [原18名模板](../extreme/逐名配置.md)','','## 分档与实算范围','',
           '| 档位 | 人数 | 本批战力范围 | 详细配置 |','|---|---:|---:|---|']
    for r in ranges:lines.append(f"| {r['tier']} | {r['count']} | {r['sample_min']:,}～{r['sample_max']:,} | [{r['tier']}逐名配置](tiers/{r['tier']}.md) |")
    lines += ['','## 全部新增NPC','','| NPC／姓名 | 档／阶段 | 战术 | 战力 | 逆天人数 | 1～8号阵容 |','|---|---|---|---:|---:|---|']
    for row in sorted(overview,key=lambda r:-r['power']):lines.append(f"| {row['npc_id']}／{row['name']} | {row['tier']}/{row['stage']} | {row['theme']} | {row['power']:,} | {row['fate_count']} | {row['roster']} |")
    lines += ['','## 验证边界','',f"数据校验通过；800场尝试结果：{json.dumps(summary['battle_stop_reasons'],ensure_ascii=False)}。已知逆天连击错误保留逐局记录，未完成原生客户端验收或后端注册。",'']
    files.update({'catalog.json':b.json_text(dict(schema_version=1,status='design_only',previous_catalog='../extreme/catalog.json',npcs=overview)),
                  'overview.csv':b.csv_text(overview),'companions.csv':b.csv_text(companions),'coverage.csv':b.csv_text(coverage_rows),
                  'power_ranges.csv':b.csv_text(ranges),'battle_checks.csv':b.csv_text(checks),'validation.json':b.json_text(summary),
                  '逐名配置.md':'\n'.join(lines)+'\n'})
    files.update({f'tiers/{t}.md':'\n'.join(lines)+'\n' for t,lines in detailed.items()})
    paths=[Path(__file__),Path(base.__file__),Path(b.__file__),OLD/'catalog.json',OLD/'power_ranges.csv']
    paths += list((ROOT/'analysis/configs').rglob('*.csv'))+list((ROOT/'server_config').glob('*.json'))
    paths += [Path(m.__file__) for name,m in tuple(sys.modules.items()) if name.startswith('network_redirect.') and getattr(m,'__file__','').endswith('.py')]
    files['source_manifest.json']=b.json_text({str(p.relative_to(ROOT)):file_hash(p) for p in sorted(set(paths))})
    return files,summary


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    frozen={p:file_hash(p) for p in (OLD/'catalog.json',OLD/'power_ranges.csv',OLD/'overview.csv',OLD/'companions.csv')}
    npcs,attempts=build();checks=battles(npcs);files,summary=export(npcs,checks,attempts)
    assert all(file_hash(p)==v for p,v in frozen.items()),'original snapshots changed'
    if args.check:
        different=[name for name,data in files.items() if not (OUT/name).exists() or (OUT/name).read_bytes()!=data.encode('utf-8')]
        assert not different,f'generated artifacts differ: {different}'
    else:
        for name,data in files.items():
            path=OUT/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data.encode('utf-8'))
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':main()
