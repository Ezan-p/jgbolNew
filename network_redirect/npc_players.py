"""Saved NPC identities over immutable V1/V2 combat snapshots; native read-only views."""
import copy
from functools import lru_cache
import json
import math
from pathlib import Path
from . import formation as f, summon, combat_power, combat, reborn_stars, cheer, role_profile
from .protocol import encode

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / 'analysis/npc_design/players/catalog.json'


@lru_cache(maxsize=1)
def rules():
    r = json.loads((ROOT / 'server_config/npc_player_rules.json').read_text())
    f.require(r['schema_version'] == 1 and r['mode'] == 'inferred', 'NPC资料配置版本无效')
    f.require(set(r['heads']) == role_profile.HEADS, 'NPC头像须为原版八种头像')
    f.require(0 < r['id_min'] < r['id_max'] < 2147483647, 'NPC编号范围无效')
    f.require(1 <= r['search_page_size'] <= 100, 'NPC搜索页大小无效')
    return r


@lru_cache(maxsize=1)
def catalog():
    data = json.loads(CATALOG_PATH.read_text())
    f.require(data['schema_version'] == 1, 'NPC资料库版本无效')
    result, identities, names = {}, set(), set()
    for entry in data['players']:
        p = entry['profile']
        f.require(entry['npc_id'] not in result and p['role_id'] not in identities
                  and p['role_name'] not in names, 'NPC资料编号或姓名重复')
        f.require(rules()['id_min'] <= p['role_id'] <= rules()['id_max'] and p['head_type'] in role_profile.HEADS,
                  'NPC编号或头像无效')
        result[entry['npc_id']] = entry
        identities.add(p['role_id']); names.add(p['role_name'])
    return result


@lru_cache(maxsize=1)
def identity_index():
    out = {}
    for key, row in catalog().items():
        for identity in (row['profile']['role_id'], row['legacy_role_id']):
            f.require(identity not in out, 'NPC兼容编号冲突')
            out[identity] = key
    return out


def resolve(identity):
    # Non-integral floating IDs and bools must never alias an existing player.
    if type(identity) not in (int, float) or not math.isfinite(identity) or identity <= 0 or identity != int(identity):
        return None
    return identity_index().get(int(identity))


def handles(identity):
    return type(identity) in (int,float) and math.isfinite(identity) and (
        rules()['id_min'] <= identity <= rules()['id_max'] or resolve(identity) is not None)


@lru_cache(maxsize=8)
def source_file(relative):
    path = (ROOT / relative).resolve()
    f.require(path.is_relative_to(ROOT / 'analysis/npc_design') and path.suffix == '.json', 'NPC阵容路径无效')
    return {n['npc_id']: n for n in json.loads(path.read_text())['npcs']}


def decorate(npc):
    """Never mutate a source snapshot or an activity's cached shared NPC."""
    entry = catalog()[npc['npc_id']]
    result = copy.deepcopy(npc)
    profile = copy.deepcopy(entry['profile'])
    result['player_profile'] = profile
    result['legacy_role_id'] = entry['legacy_role_id']
    result['role'].update({k: profile[k] for k in ('role_id', 'role_name', 'head_type', 'vip_level', 'cur_genius_type')})
    result['role'].update(name=profile['role_name'], union_id=0, union_name='', title_id=0,
                          title_begintime=0, title_endtime=0, profile_titles={}, profile_head_changed=True)
    return result


def get(key_or_id):
    key = key_or_id if isinstance(key_or_id, str) and key_or_id in catalog() else resolve(key_or_id)
    if not key:
        return None
    entry = catalog()[key]
    n = decorate(source_file(entry['source_file'])[key])
    combat_power.recalculate(n['role'], f.load_rules())
    return n


def character(c):
    fields = ('order', 'level', 'evolve_level', 'reborn_layer', 'reborn_vein_level', 'reborn_plus_type',
              'culture_point', 'hp_plus', 'gongji_plus', 'fangyu_plus', 'magic_plus',
              'combat_power', 'equiped_ext_skill_limit', 'cheer_order', 'hp', 'gongji', 'fangyu', 'magic', 'potential')
    return dict({k: c.get(k, 0) for k in fields}, type_id=c['type'], quality=int(f.BASES[c['type']]['quality']),
                max_hp_show=c['hp'], max_magic_show=c['magic'], wuligongji_show=c['gongji'], wulifangyu_show=c['fangyu'])


def inspection_data(npc, *, scene_id=None, count=8):
    n = decorate(npc) if 'player_profile' not in npc else copy.deepcopy(npc)
    role, profile = n['role'], n['player_profile']
    members = sorted((c for c in role['corteges'] if 1 <= c.get('order', 0) <= count), key=lambda c: c['order'])
    data = dict(role_id=role['role_id'], npc_scene_id=scene_id or 0,
                npc_player_id=role['role_id'], role_name=profile['role_name'], level=role['level'],
                vip_level=profile['vip_level'], head_type=profile['head_type'], rank=0, union_name='',
                reborn_layer=role.get('reborn_layer',0), cur_genius_type=profile['cur_genius_type'],
                role_combat_power=sum(c['combat_power'] for c in members),
                title_info={}, animal_info={}, hole_train={}, cortege_list=[character(c) for c in members],
                equip_list=[], skill_list=[], ext_skill_list={}, ext_star_list={},
                owner_cheer_info={v: role.get(k,0) for k,v in cheer.ATTRS.items()},
                cheer_cortege={c['cheer_order']: character(c) for c in role['corteges'] if c.get('cheer_order')},
                npc_profile=profile)
    owners = {c['id']: c['order'] for c in members}
    for i in role['attachments']:
        owner = owners.get(i.get('owner_id'))
        if owner and i['type_id'] in combat.ESSENCES:
            data['ext_skill_list'].setdefault(owner, []).append(dict(type_id=i['type_id'], level=i['level'], order=i['ext_skill_pos']))
        if owner and i['type_id'] in reborn_stars.STARS:
            data['ext_star_list'].setdefault(owner, []).append(dict(type_id=i['type_id'], level=i['level'], order=i['ext_awaken_pos']))
        order = i.get('equip_order', 0)
        if not i.get('equip_pos') or not (1 <= order <= count or 9 <= order <= 24 and i['attach_type'] == 6):
            continue
        # Avoid sending caches, internal owner IDs or entire growth histories.
        keys = ('type_id','level','equip_pos','protogenic','awaken','upgrade_level','effect_value',
                'advance_level','star_count','cur_spirit_count','reborn_bit','cast_level','star_level',
                'drill_count','stone1_level','stone2_level','stone3_level','stone4_level')
        row = dict({k: i[k] for k in keys if k in i}, order=order, goss_plus=i.get('goss_plus',0))
        if i['attach_type'] == 6:
            data['skill_list'].append(row)
        elif int(f.ITEMS.get(i['type_id'],{}).get('main_type',0)) in (1,2,3):
            data['equip_list'].append(row)
    return data


def inspection(key_or_id, **options):
    npc = get(key_or_id)
    f.require(npc is not None, 'NPC玩家不存在')
    return summon.event(11, inspection_data(npc, **options))


def search(req, viewer_level=1, excluded_ids=()):
    f.require(req['search_type'] in (1,2) and req['search_index'] >= 1, 'NPC搜索参数无效')
    query = req['search_string'].strip()
    entries = list(catalog().values())
    if req['search_type'] == 1:
        f.require(query.isdecimal() and 1 <= int(query) <= 99, '搜索等级须为1至99')
        entries = [e for e in entries if e['profile']['level'] == int(query)]
    elif query:
        entries = [e for e in entries if query in e['profile']['role_name'] or query in e['npc_id']
                   or query in (str(e['profile']['role_id']), str(e['legacy_role_id']))]
    entries = [e for e in entries if e['profile']['role_id'] not in excluded_ids]
    entries.sort(key=lambda e: (abs(e['profile']['level']-viewer_level), e['profile']['role_id']))
    start = (req['search_index'] - 1) * rules()['search_page_size']
    rows = [dict(id=e['profile']['role_id'], name=e['profile']['role_name'], level=e['profile']['level'])
            for e in entries[start:start+rules()['search_page_size']]]
    return encode(1092,dict(result=1 if rows else 2, search_index=req['search_index'], player_count=len(rows),player_list=rows))


def clear_cache():
    rules.cache_clear(); catalog.cache_clear(); identity_index.cache_clear(); source_file.cache_clear()
