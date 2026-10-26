"""Audit original direct-send sites against current dispatch, without a player DB.

Business handler entry is intercepted; a routed result is NOT a functionality
test. Only fallthrough into game_unimplemented proves a missing sampled route.
"""
import hashlib
import json
from datetime import datetime
from pathlib import Path
import re
import sys
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect.backend import Backend
from network_redirect.protocol import TABLES, decode, encode

OUT = ROOT / 'analysis/evidence/server_integration/current_audit.json'
NAMES = TABLES['gscl_msg_id'] | TABLES['lscl_msg_id']
BY_ID = {value: key for key, value in NAMES.items()}
INFRASTRUCTURE = {3001, 1001, 1016, 2999, 1105}
SELECTORS = {
    1026: [{'fight_type': n} for n in range(1, 13)],
    1097: [{'channel': n} for n in (1, 2, 6)],
    1111: [{'event_id': 250}],
    1112: [{'event_id': 3, 'item_id': 8}],
    1201: [{'flag': n} for n in (1, 2, 5, 6, 7)],
    1244: [{'fight_type': n} for n in (2, 3, 4)],
}


class Routed(Exception):
    pass


def probe(mid, selectors):
    # Deliberately skip __init__: no DB, credentials, socket, or player state.
    backend = object.__new__(Backend)
    logs = []
    backend.emit = lambda kind, **values: logs.append(dict(kind=kind, **values))
    backend.complete = lambda serial, packets: packets

    def intercept(name):
        def call(*args, **kwargs):
            raise Routed(name)
        return call

    for name in ('npc_queries', 'spirit_arrays', 'role_profiles', 'monuments',
                 'welfares', 'redeem_gift_code', 'vips', 'guilds', 'dailies',
                 'activities', 'journeys', 'rebirth', 'immortals', 'formation',
                 'summon', 'market', 'inventory', 'profile', 'save', 'bootstrap'):
        setattr(backend, name, intercept(name))
    request = dict(serial_num=1, **selectors)
    packet = encode(mid, request)
    try:
        replies = backend.respond(packet, {'authenticated': True})
        result = dict(status='unhandled' if any(x['kind'] == 'game_unimplemented' for x in logs)
                      else 'inline_response',
                      responses=[dict(id=decode(p)[0], data=decode(p)[2]) for p in replies])
    except Routed as route:
        result = dict(status='routed_not_executed', handler=str(route))
    return dict(selectors=selectors, logs=logs, **result)


def main():
    refs = {}
    for path in sorted((ROOT / 'analysis/evidence/lua_named').rglob('*.lua.txt')):
        lines = path.read_text().splitlines()
        for i, line in enumerate(lines):
            if "'main_server_send_msg'" not in line:
                continue
            for j in range(i + 1, min(i + 13, len(lines))):
                if ' CALL ' in lines[j] or lines[j].startswith('FUNCTION'):
                    break
                match = re.search(r"'(msg_\w+)'", lines[j])
                if match and match[1] in NAMES:
                    refs.setdefault(NAMES[match[1]], []).append(f'{path.relative_to(ROOT)}:{j + 1}')
    rows = []
    for mid, locations in sorted(refs.items()):
        samples = [] if mid in INFRASTRUCTURE else [probe(mid, s) for s in [{}, *SELECTORS.get(mid, [])]]
        missing = bool(samples) and all(s['status'] == 'unhandled' for s in samples)
        rows.append(dict(id=mid, name=BY_ID[mid], client_references=locations,
                         status='unhandled' if missing else 'infrastructure_excluded' if not samples else 'has_sampled_route',
                         probes=samples))
    missing = [r for r in rows if r['status'] == 'unhandled']
    previous = json.loads((OUT.parent / 'unhandled_requests.json').read_text())
    old_ids = {r['id'] for r in previous['missing_requests']}
    new_ids = {r['id'] for r in missing}
    sources = sorted(set((ROOT / 'network_redirect').glob('*.py')) |
                     {ROOT / 'analysis/evidence/protocol_tables.json', Path(__file__).resolve()} |
                     {ROOT / loc.rsplit(':', 1)[0] for locs in refs.values() for loc in locs})
    result = dict(
        audit_time=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),
        scope='当前工作区（含未提交文件）；不创建Backend数据库，不读写角色、不连接模拟器或网络',
        method='扫描具名Lua中main_server_send_msg后12行、首次CALL前的协议常量；真实Backend.respond分发，业务入口拦截；未路由候选实际落入game_unimplemented。默认零/空编码及少量显式选择器只验证分发，不验收业务或UI。',
        limitations=['动态/间接发送可能未被静态窗口捕获，统计不是协议全集完整性证明',
                     '有路由不代表所有flag/id/event_id/channel分支完成；另见文档人工审计',
                     '返回1106或空列表不代表业务完成；旧渠道与关闭活动也计入未路由ID'],
        direct_send_id_count=len(rows), missing_request_count=len(missing),
        previous_audit_time=previous['audit_time'], previous_missing_count=len(old_ids),
        previous_now_routed_ids=sorted(old_ids - new_ids),
        newly_found_missing_ids=sorted(new_ids - old_ids),
        missing_requests=missing, scanned_requests=rows,
        reserved_without_direct_send=[dict(id=mid, name=BY_ID[mid], probe=probe(mid, {}))
                                      for mid in (1065, 1075, 1240) if mid not in refs],
        sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: result[key] for key in ('direct_send_id_count', 'missing_request_count',
          'previous_now_routed_ids', 'newly_found_missing_ids')}, ensure_ascii=False))
    print('Missing IDs:', ', '.join(str(r['id']) for r in missing))
    print('Evidence:', OUT.relative_to(ROOT))


if __name__ == '__main__':
    main()
