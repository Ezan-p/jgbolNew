"""Original 1204/35 onboarding contract [A], explicit offline battle policy [B]."""
import re

from . import formation, summon, journey, combat_engine, role_profile, tian_shu
from .protocol import encode

SCHEDULE = {int(r['stage']): int(r['pre_stage']) for r in summon.rows('guide_schedule.csv')}
FIRST = {1: 4061, 2: 4053}  # guideUI.startChat
GATES = {3: 101, 4: 102, 7: 102, 8: 103, 10: 104, 12: 105}
LEGACY_COMPLETE = 0x7fffffff


def done(role, stage):
    # getBitInGuideIndex removes bit zero before indexing by stage.
    return bool(role.get('guide_progress', LEGACY_COMPLETE) & (1 << stage))


def attributes(role):
    return encode(1032, dict(id=role['role_id'], unit_type=1, attr_count=2,
        attr_list=[dict(type=9, value=role['guide_progress']),
                   dict(type=29, value=role['head_type'])]))


def fight(role, stage, now, backend):
    gid = GATES[stage]
    cfg = journey.GATES[1][gid]
    formation.require(journey.unlocked(role, 1, gid), '教学关卡尚未解锁')
    journey.check_attempt(role, 1, gid, cfg, 1)
    units = journey.fighters(role, cfg)
    # [B] Tutorial two demonstrates defeat; other lessons demonstrate victory.
    # Use real combat actions rather than announcing a result with an empty replay.
    for unit in units[0 if stage == 4 else 1]:
        unit.update(hp=1, max_hp=1, magic=1, gongji=1, fangyu=1)
    result, lineup, actions = journey.battle(role, cfg, backend.journey_rules, units=units)
    formation.require((4 <= result <= 6 if stage == 4 else 1 <= result <= 3), '教学战斗结果异常')
    outcome, prizes = journey.attempt(role, 1, gid, cfg, result, now,
                                     backend.journey_rules, backend.formation_rules)
    role['journey']['fight_id'] = role['journey']['fight_id'] % 0x7ffffffe + 1
    fid = role['journey']['fight_id']
    return combat_engine.event_packets(actions, fid) + [
        encode(1028, dict(fight_id=fid, first_hand=1, des_name='旅途', lineup_count=len(lineup), lineup=lineup)),
        *combat_engine.result_packets(1027, dict(fight_id=fid, fight_type=7, guide_stage=stage,
                                               final_result=result, fight_result=actions)),
        summon.event(45, dict(fight_id=fid, obj_type=1, exp_plus=outcome['role_add_exp'])),
        summon.event(45, dict(fight_id=fid, obj_type=4, exp_list=outcome['exp_list']))
    ] + prizes + [summon.event(44, dict(fight_id=fid, fight_type=7, **getattr(actions, 'talent', {})))]


def settle(role, req, now, backend):
    stage = req['stage']
    formation.require(stage in SCHEDULE, '未知的新角色引导阶段')
    formation.require(not done(role, stage), '该引导阶段已经完成，请重新登录恢复进度')
    pre = SCHEDULE[stage]
    formation.require(not pre or done(role, pre), '请先完成前置引导')
    response = dict(stage=stage)
    events = []
    if stage == 1:
        name, rules = req['name'], backend.profile_rules
        names = {r['role_name'] for r in backend.duty_peers()}
        code = (4 if len(name) < rules['name_min'] else 5 if len(name) > rules['name_max'] else
                3 if not re.fullmatch(r'[\u3400-\u4dbf\u4e00-\u9fff]+', name)
                or any(w and w in name for w in rules['blocked_names']) else 2 if name in names else 0)
        if code:
            return [summon.event(35, dict(stage=stage, result=code))]
        formation.require(req['head_type'] in role_profile.HEADS, '请选择有效头像')
        role.update(role_name=name, head_type=req['head_type'], profile_head_changed=True)
        response['new_name'] = name
        # Successful naming deliberately omits result: native callback tests nil.
    elif stage in (2, 5):
        if stage == 2:
            formation.require(req['name'] in ('1', '2'), '请选择原版初始神仙')
            tid = FIRST[int(req['name'])]
        else:
            # [B] Guaranteed other starting companion; original server pool unavailable.
            tid = next(t for t in FIRST.values() if t != role['corteges'][0]['type'])
        role.setdefault('summon', {})
        c = summon.companion(role, tid)
        c['order'] = 1 if stage == 2 else 0
        role['corteges'].append(c)
        response.update(cortege_type=tid, left_time=0)
    elif stage == 6:
        formation.require(req['name'].isdigit(), '神仙编号无效')
        c = formation.lookup(role, 'corteges', int(req['name']))
        formation.require(c.get('order', 0) == 0, '请选择待上阵神仙')
        formation.change_order(role, dict(flag=4, count=1, change_info=[dict(id=c['id'], new_order=2)]))
    elif stage == 9:
        formation.require(req['name'].isdigit(), '装备编号无效')
        item = formation.lookup(role, 'attachments', int(req['name']))
        formation.require(item['attach_type'] == 5 and item['type_id'] == 2041, '请选择教学掉落的装备')
        formation.bind(role, dict(flag=3, obj_type=5, src_id=item['id'], src_order=item.get('equip_order', 0),
                                  des_order=1, des_equip_pos=int(formation.ITEMS[2041]['equip_pos'])))
    elif stage in GATES:
        events = fight(role, stage, now, backend)
    elif stage == 13:
        # Both native entry paths share the persistent task receipt.
        if not tian_shu.has(role, 'task_prize', 1):
            tian_shu.claim(role, 1, now, backend.tian_shu_rules)
    elif stage != 11:
        # 21..30 are activity entry acknowledgements, not combat/reward requests.
        # Actual gameplay continues through the existing activity protocols.
        pass
    role['guide_progress'] |= 1 << stage
    return events if stage in GATES else [summon.event(35, response)]
