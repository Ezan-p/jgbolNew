"""Manual code-source registry, not proof that every achievement is reachable."""
import hashlib
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import achievements as a

# Explicit coverage registry is also included in the delivered rule document.
AUTO = {101,102,103,104,105,107,108,109,111,112,113,114,115,116,117,118,121,122,123,124,
126,127,128,130,131,137,138,225,226,227,228,229,230,231,232,239,240,241,242,243,244,245,246,
247,248,249,250,251,252,253,254,317,318,319,321,322,401,414,415,416,422,423,424,425,
440,441,443,444,446,447,450,451,452,453,454,455,456,459,460,466,467,468,469,470,471,
472,473,474,475,476,479,481,482,483,484,485,563,564,565}
AUTO.update(range(323,327))  # Native Lu claim with original dice result.
AUTO.add(125)  # Native Monday workshop event112/flag3, after successful exchange.
AUTO.update(range(201,216));AUTO.update(range(402,414));AUTO.update(range(417,422))
AUTO.update(range(426,431));AUTO.update(range(490,559))
# Successful settlements added after the original registry was written.
AUTO.add(106)  # achievements.track: convert_total delta.
AUTO.update(range(216,222))  # activity_duty / activity_party rank settlement.
AUTO.add(320)  # activity_party lucky settlement.
AUTO.update(range(431,440))  # activity_duty consecutive ranked days.
AUTO.add(445)  # activity_feed successful entry into the local champion position.
AUTO.update((461,462,463,464,465,560,561,562))  # spirit_array activation/max skills.
AUTO.update((119,139))  # Committed soul revival and guild treasure search deltas.
AUTO &= set(a.OPEN)
INDIRECTLY_BLOCKED = {401: [120,134]}
CONFIRMED_TRIGGER_GAPS = set()


def coverage(ident):
    if ident not in a.OPEN: return '【A】关闭，保持不触发'
    if ident in INDIRECTLY_BLOCKED: return '【B】有汇总结算代码，但受未接入的第一次成就间接阻塞；非自然可达认证'
    if ident in CONFIRMED_TRIGGER_GAPS: return '【B】已有玩法结算，缺成就联动；2026-10-27临时数据库协议探针确认'
    if ident == 126: return '【B】有战争参与触发代码；是否可参与受guild_rules.wars_enabled控制'
    if ident in AUTO: return '【B】有原生结算/存档事实代码来源；候选登记，非逐条闭环认证'
    return '【B】未发现普通玩法触发来源；保留显式模拟路径'


def audit():
    original = ROOT/'jgbol3.87/assets/release_/21e32184cfddbf4046201e0e98e8828e.data'
    exported = ROOT/'analysis/configs/achievements_config.csv'
    normalize = lambda p: p.read_text(encoding='utf-8-sig').strip()
    assert normalize(original) == normalize(exported)
    result = dict(audit_date='2026-10-27', timezone='Asia/Shanghai',
        scope='Manual code-source registry checked against original CSV; not gameplay completion coverage',
        catalogue_count=len(a.CATALOG), open_count=len(a.OPEN), closed_count=len(a.CATALOG)-len(a.OPEN),
        code_source_candidate_count=len(AUTO), no_natural_source_ids=sorted(set(a.OPEN)-AUTO),
        confirmed_trigger_gap_ids=sorted(CONFIRMED_TRIGGER_GAPS),
        indirectly_blocked_by_missing_first_achievements=INDIRECTLY_BLOCKED,
        configured_wars_enabled=json.loads((ROOT/'server_config/guild_rules.json').read_text())['wars_enabled'],
        original_catalogue_matches=True, sha256=hashlib.sha256(exported.read_bytes()).hexdigest(),
        coverage={str(i):coverage(i) for i in a.CATALOG})
    path=ROOT/'analysis/evidence/achievements/audit.json';path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result


if __name__ == '__main__':
    r=audit();print(json.dumps({k:v for k,v in r.items() if k!='coverage'},ensure_ascii=False,indent=2))
