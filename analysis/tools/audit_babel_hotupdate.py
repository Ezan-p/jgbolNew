"""Verify active 1263 data and reproduce Babel/fate-star evidence (no saves)."""
import csv
import hashlib
import io
import json
from fractions import Fraction
from pathlib import Path
import plistlib
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import summon, reborn_stars as stars, formation, activity_babel as babel
from audit_hotupdate_gap import index
from luajit_static import parse, listing


def main():
    out=ROOT/'analysis/evidence/babel_hotupdate';out.mkdir(exist_ok=True)
    source=ROOT/'analysis/evidence/hotupdate_gap_20261031/official_csv'
    checks=[]
    for path in sorted((ROOT/'analysis/configs/babel_hotupdate').glob('*.csv')):
        with path.open(encoding='utf-8-sig',newline='') as f: active=list(csv.DictReader(f))
        with (source/path.name).open(encoding='utf-8-sig',newline='') as f: original=list(csv.DictReader(f))
        complete=path.name in summon.BABEL_HOTUPDATE_TABLES
        assert active==original if complete else all(row in original for row in active)
        checks.append(dict(file=str(path.relative_to(ROOT)),complete_table=complete,records=len(active),
                           sha256=hashlib.sha256(path.read_bytes()).hexdigest(),original_rows_match=True))
    strings={}
    with zipfile.ZipFile(ROOT/'build/金箍棒3.87离线正式版v107.apk') as apk,zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as z:
        version,idx=index(z.read('client/release_w/index.txt'));assert version==1263
        def resource(name):
            physical=idx[name];overlay='client/release_w/'+physical
            return z.read(overlay) if overlay in z.namelist() else apk.read('assets/release_/'+physical)
        for name in ('v2/String.plist','v2/String2.plist'):
            for k,v in plistlib.loads(resource(name)).items():
                if 'tongtianta' in str(k) or 'mxChange' in str(k): strings[k]=v
        (out/'original_strings.txt').write_text('\n'.join(f'{k}: {v}' for k,v in strings.items())+'\n')
        # These were not in the earlier gap report. Retain the exact native
        # compose request and event dispatch, not assumptions from enum names.
        for name in ('lua/data.lua','lua/ui/smithUI.lua','lua/event_mgr.lua'):
            if name in idx:
                d=parse(resource(name))
                lines=listing(d).splitlines()
                wanted=('fateStar_transform', 'fate_star_switch', 'babel_tower_info',
                        'd_tongtiantaSecretUI', 'g_mxTransformUI', 'onGetFateStarResult',
                        'msg_material_transform', 'csv_config/material_transform.csv')
                kept=set()
                for i,line in enumerate(lines):
                    if any("'"+term+"'" in line for term in wanted):
                        kept.update(range(max(0,i-14),min(len(lines),i+15)))
                excerpts=[];previous=-2
                for i in sorted(kept):
                    if i!=previous+1:excerpts.append('...')
                    excerpts.append(lines[i]);previous=i
                (out/(Path(name).name+'.txt')).write_text('Original resource 1263; instruction excerpts around named references.\n'+'\n'.join(excerpts)+'\n')
        secret=parse(resource('lua/ui/tongtiantaSecretUI.lua'))
        teleport=next(p for p in secret['protos'] if p['line']==1238)
        assert teleport['numbers']==[3,2,1000]
    probabilities=[]
    for pos,row in stars.POSITIONS.items():
        pool=[list(map(int,p.split('|'))) for p in list(row.values())[2].split('/')]
        weight=sum(p[0] for p in pool if p[2]==1378)
        if weight:
            total=sum(p[0] for p in pool)
            probabilities.append(dict(position=pos,name=row['star_name'],fragment_weight=weight,total_weight=total,
                                      probability=str(Fraction(weight,total)),percent=weight/total*100,
                                      silver=int(row['consume_silver'])))
    groups=[]
    for source_id,row in sorted(stars.TRANSFORMS.items()):
        targets=[int(x.split('|')[1]) for x in list(row.values())[4].split('/')]
        by_subtype={}
        for target in targets:by_subtype.setdefault(formation.ITEMS[target]['sub_type'],[]).append(target)
        groups.append(dict(source=source_id,by_subtype=by_subtype,token=1376,token_count=1,
                           gold=200 if source_id>=14000 else 0,min_level=int(row['min_role_level'])))
    report=dict(date='2026-10-31',resource_version=1263,tables=checks,maximum_floor=babel.MAX_FLOOR,
                stages=babel.STAGES,fragment_position_probabilities=probabilities,conversions=groups,
                proven_secret_teleport_formula='3 * selected_group - 2 + 1000',
                original_string_keys=list(strings),original_server_observed=False,
                inferred=['stage awards cumulative and delivered by permanent mail at Thursday cutoff',
                          'map layouts, NPC difficulty, equal Babel reward-entry probabilities',
                          'new paid secret teleport resets run; weekly reset preserves secret run',
                          'weekly 20-floor token and 40-floor ticket supply',
                          'uniform conversion result within selected subtype; no failure roll',
                          'reject partially fed level-one stars; create fresh result ID'])
    (out/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(passed=True,tables=len(checks),conversions=len(groups),fragment_positions=len(probabilities)),ensure_ascii=False))


if __name__=='__main__':main()
