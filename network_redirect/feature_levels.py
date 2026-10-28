"""Role-level access checks recovered from the shipped 3.87 client.

Original fixed gates and explicitly requested local activity gates live here.
Other server-supplied levels and per-recipe / per-object requirements remain
in their owning modules. A missing gate is not
evidence that the original server opened a feature at level one.
"""
from . import formation

# activityUI.getRequireLevel, original source lines 1492–1541.
ACTIVITY_LEVELS = {
    'xiulian': 5, 'fengshenbang': 6, 'dujie': 8,
    'tianmingzhizhan': 12, 'undergo': 12, 'pantaohui': 13,
    'qifu': 15, 'cortegeRecycle': 15, 'friends': 15,
    'cortCall': 16, 'soulHunt': 20, 'answer': 20,
    'land': 38, 'home': 50, 'abyss': 70,
    # Separate explicit check in activityUI.pressBtn, lines 1378–1381.
    'tongtianta': 36,
}
# User-requested local policy; keep separate from the original-asset audit.
LOCAL_ACTIVITY_LEVELS = {
    'monday': 15, 'fishrush': 20, 'twoyears': 20, 'rulaitable': 20,
    'tower': 20, 'destiny': 30, 'forge': 30,
}
NAMES = {
    'xiulian': '主角修炼', 'fengshenbang': '封神榜', 'dujie': '渡劫',
    'tianmingzhizhan': '天命之战', 'undergo': '太虚幻境',
    'pantaohui': '蟠桃会', 'qifu': '神石祈福', 'cortegeRecycle': '神仙回收',
    'friends': '好友邀请', 'cortCall': '天缘召唤', 'soulHunt': '捕魂达人',
    'answer': '科举', 'land': '猎魂之地', 'home': '洞府', 'abyss': '九幽',
    'tongtianta': '通天塔', 'undergo_play': '太虚幻境历劫', 'pet': '宠物系统',
    'exp_pill': '经验丹', 'exp_drug': '药灵丹',
    'equip_asc': '装备封神', 'buff': '新手每日礼包',
    'monday': '天工制物阁', 'fishrush': '东海寻宝', 'twoyears': '元始祈愿',
    'rulaitable': '如来大转盘', 'tower': '九重天', 'destiny': '天机阁',
    'forge': '装备兑换',
}
LEVELS = dict(ACTIVITY_LEVELS, undergo_play=50, pet=50, exp_pill=65,
              exp_drug=70, equip_asc=70, buff=3)
LEVELS.update(LOCAL_ACTIVITY_LEVELS)

# Shared messages are intentionally resolved below, not assigned wholesale.
MESSAGES = {
    1021: 'fengshenbang', 1203: 'fengshenbang',
    1029: 'dujie', 1041: 'dujie', 1060: 'dujie', 1072: 'dujie',
    1043: 'tianmingzhizhan', 1085: 'qifu', 1086: 'cortegeRecycle',
    1226: 'soulHunt', 1302: 'land',
    1329: 'abyss', 1348: 'home',
    1353: 'tongtianta', 1330: 'pet', 1202: 'pantaohui',
    1219: 'monday', 1243: 'monday', 1208: 'fishrush', 1334: 'twoyears',
    1351: 'rulaitable', 1309: 'tower', 1227: 'destiny', 1055: 'forge',
}
FIGHTS = {2: 'fengshenbang', 3: 'dujie', 12: 'dujie', 4: 'xiulian',
          5: 'tianmingzhizhan', 6: 'pantaohui', 10: 'cortCall'}


def feature(mid, request):
    if mid == 1053 and request.get('compose_type') in (2, 3):
        return 'forge'
    if mid == 1349:
        # Outer activity/menu and its shop: 12; enter the ordeal maps: 50.
        return 'undergo' if request.get('id') in (3, 5) else 'undergo_play'
    if mid == 1303:
        return 'land' if request.get('id') == 1 else None
    if mid == 1328 and request.get('reborn_type') == 3 and request.get('id') == 5:
        return 'equip_asc'
    if mid == 1026:
        return FIGHTS.get(request.get('fight_type'))
    if mid == 1049:
        return 'tianmingzhizhan' if request.get('query_type') == 4 else (
            'pantaohui' if request.get('query_type') in (1, 2, 3, 5) else None)
    if mid == 1201:
        return {1: 'pantaohui', 2: 'fengshenbang'}.get(request.get('flag'))
    if mid == 1244:
        return {2: 'fengshenbang'}.get(request.get('fight_type'))
    if mid == 1059:
        return {2: 'exp_pill', 3: 'exp_drug'}.get(request.get('flag'))
    if mid == 1131 and request.get('flag') == 2:
        # The original UI/heartbeat may query this status before unlocking.
        return 'buff'
    return MESSAGES.get(mid)


def require(role, key):
    formation.require(role['level'] >= LEVELS[key],
                      f'{NAMES[key]}需角色{LEVELS[key]}级开放')


def check(role, mid, request):
    key = feature(mid, request)
    if key:
        require(role, key)
