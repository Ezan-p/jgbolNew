"""Catalogue coverage and original evidence audit; no official server claims."""
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
AUTO.add(125)  # Native pavilion event195/flag2, after successful exchange.
AUTO.update(range(201,216));AUTO.update(range(402,414));AUTO.update(range(417,422))
AUTO.update(range(426,431));AUTO.update(range(490,559))
AUTO &= set(a.OPEN)


def coverage(ident):
    if ident not in a.OPEN: return '【A】关闭，保持不触发'
    if ident in AUTO: return '【B】原生结算/存档事实自动接入；也可显式模拟'
    return '【B】缺失上游结算，使用带凭据的显式模拟'


def audit():
    original = ROOT/'jgbol3.87/assets/release_/21e32184cfddbf4046201e0e98e8828e.data'
    exported = ROOT/'analysis/configs/achievements_config.csv'
    normalize = lambda p: p.read_text(encoding='utf-8-sig').strip()
    assert normalize(original) == normalize(exported)
    result = dict(catalogue_count=len(a.CATALOG), open_count=len(a.OPEN), closed_count=len(a.CATALOG)-len(a.OPEN),
        automatic_count=len(AUTO), simulated_upstream_ids=sorted(set(a.OPEN)-AUTO),
        original_catalogue_matches=True, sha256=hashlib.sha256(exported.read_bytes()).hexdigest(),
        coverage={str(i):coverage(i) for i in a.CATALOG})
    path=ROOT/'analysis/evidence/achievements/audit.json';path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result


if __name__ == '__main__':
    r=audit();print(json.dumps({k:v for k,v in r.items() if k!='coverage'},ensure_ascii=False,indent=2))
