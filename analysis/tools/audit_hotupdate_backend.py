"""Inspect current effective tables and reproduce selected gaps in memory only."""
import copy
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/tools')]
from audit_hotupdate_gap import OUT, table
from audit_server_integration import SELECTORS, INFRASTRUCTURE
from network_redirect.backend import Backend
from network_redirect import formation as f, summon, reborn, immortal, achievements
from network_redirect import activity_babel as babel, activity_home as home, protocol, fate_rebuild, equipment


def probe(mid, selectors):
    class Routed(Exception):
        pass
    backend=object.__new__(Backend)
    logs=[]
    def intercept(name):
        def call(*args,**kwargs):
            raise Routed(name)
        return call
    # All public business entry points are stopped before touching state.
    for name in dir(Backend):
        if not name.startswith('_') and callable(getattr(Backend,name)) and name!='respond':
            setattr(backend,name,intercept(name))
    backend.emit=lambda kind,**values:logs.append(dict(kind=kind,**values))
    backend.complete=lambda serial,packets:packets
    try:
        replies=backend.respond(protocol.encode(mid,dict(serial_num=1,**selectors)),{'authenticated':True})
        result=dict(status='unhandled' if any(x['kind']=='game_unimplemented' for x in logs) else 'inline_response',
                    responses=[dict(id=protocol.decode(p)[0],data=protocol.decode(p)[2]) for p in replies])
    except Routed as route:
        result=dict(status='routed_not_executed',handler=str(route))
    return dict(selectors=selectors,logs=logs,**result)


def main():
    latest=json.loads((OUT/'protocol_tables_1263.json').read_text())
    refs=json.loads((OUT/'client_request_references.json').read_text())
    route=[]
    for ident, locations in sorted(refs.items(),key=lambda p:int(p[0])):
        mid=int(ident)
        if mid in INFRASTRUCTURE:
            status='infrastructure_excluded'; samples=[]
        elif mid not in protocol.DEFS:
            status='codec_absent'; samples=[]
        else:
            samples=[probe(mid,s) for s in [{},*SELECTORS.get(mid,[])]]
            status='unhandled' if all(s['status']=='unhandled' for s in samples) else 'has_sampled_route'
        route.append(dict(id=mid,status=status,references=locations,probes=samples))
    newer={int(v['id']):v['def'] for v in latest['gscl_msg'].values() if 1354<=v['id']<=1360}
    cases=[]
    def reject(label, role, call):
        before=copy.deepcopy(role)
        try:
            call()
        except (f.Rejected,ValueError) as error:
            cases.append(dict(case=label,result='rejected',message=str(error),input_unchanged=role==before))
        else:
            raise AssertionError('Expected rejection: '+label)
        assert role==before,label
    role=dict(level=99,corteges=[dict(id=1,type=5001,evolve_level=299)])
    reject('飞升299→300',role,lambda:f.evolve(role,dict(flag=0,cortege_id=1)))
    role=dict(level=99,corteges=[dict(id=1,type=5001,evolve_level=121)])
    reject('飞升121级回收',role,lambda:f.evolve(role,dict(flag=1,cortege_id=1)))
    role=dict(level=99,cortege_limit_plus=400,corteges=[dict(id=1,type=5001,level=300)])
    reject('即使提供洞府+400，300级喂书仍拒绝',role,lambda:f.feed(role,
        dict(flag=1,first_send=True,cortege_id=1,roll_count=1,roll_list=[dict(type_id=1041,count=1)]),{}))
    for ident in (5,12,13,14):
        role=dict(level=99)
        reject('通天塔操作'+str(ident),role,lambda:babel.settle(role,dict(id=ident,data='{}'),0,{}, {},lambda _:{}))
    role=dict(level=99,corteges=[dict(id=1,type=5001,reborn_layer=0)])
    reject('热更新新增阎罗王转生',role,lambda:reborn.settle(role,
        dict(id=1,reborn_type=2,data='{}'),{},lambda _:dict(cortege_id=1)))
    purple=[tid for tid in immortal.ESSENCES if int(f.ITEMS[tid]['quality'])==5][:5]
    role=dict(level=99,corteges=[dict(id=1,type=5001,equiped_ext_skill_limit=4,
        fate_rebullding_state=1,spirit_earth_level=50)],attachments=[
            dict(id=10+i,attach_type=5,type_id=tid,count=1,owner_id=1 if i<4 else 0,ext_skill_pos=i+1)
            for i,tid in enumerate(purple)])
    reject('已有第五精魄槽时锁定四槽',role,lambda:immortal.engrave(role,
        dict(ext_skill_id=14,des_cortege_id=1,lock_list='{1,2,3,4}'),
        dict(adaptive_visible=True),lambda _:[1,2,3,4]))
    csv_audit=json.loads((OUT/'audit.json').read_text())['csv']
    alternates={}
    for row in csv_audit:
        name=row['logical'].removeprefix('csv_config/')
        official=table((OUT/'official_csv'/name).read_bytes())
        options=[]
        for path in (ROOT/'analysis/configs').rglob(Path(name).name):
            if path==ROOT/'analysis/configs'/name:continue
            options.append(dict(path=str(path.relative_to(ROOT)),equals_latest=table(path.read_bytes())==official))
        if options:alternates[name]=options
    result=dict(date='2026-10-31',scope='Imported effective tables; in-memory negative probes; no player database opened',
        effective=dict(evolve_max=max(f.EVOLVE_COST),evolve_recycle_max=max(int(r['evolve_level']) for r in summon.rows('cortege_devolve.csv')),
            experience_max={q:max(l for qq,l in f.EXPERIENCE if qq==q) for q in range(1,6)},
            home_building_max={i:max(rows) for i,rows in home.BUILD.items()},home_owner_max=max(int(r['max_building_level']) for r in home.OWNER.values()),
            home_main_bonus=int(home.BUILD[1][max(home.BUILD[1])]['coretege_limit_plus']),
            reborn_types=sorted(reborn.CORTS),fate_active_types=sorted(fate_rebuild.ACTIVE),
            fate_active_but_reborn_missing=sorted(fate_rebuild.ACTIVE-set(reborn.CORTS)),
            babel_max=babel.MAX_FLOOR,achievement_count=len(achievements.CATALOG),achievement_open_count=len(achievements.OPEN),
            new_achievement_ids_present=[i for i in range(580,591) if i in achievements.CATALOG],
            refine_achievement_caps={i:achievements.CATALOG[i]['max_repeatable_times'] for i in (563,564,565)},
            lock_cost=immortal.LOCK_COST,stone_max=equipment.STONE_MAX_LEVEL,
            new_items_present={i:i in f.ITEMS for i in range(1370,1379)},skill_11_present=11 in f.SKILLS),
        new_protocols={mid:dict(definition=definition,codec_present=mid in protocol.DEFS) for mid,definition in newer.items()},
        route_summary={status:sum(r['status']==status for r in route) for status in sorted({r['status'] for r in route})},
        routes=route,negative_probes=cases,alternate_csv_candidates=alternates,
        caveat='A sampled route is not an end-to-end pass; alternate files require checking their actual loader. Request scan is bounded to identifiable direct sends.')
    (OUT/'backend_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result['effective'],ensure_ascii=False,indent=2))
    print('routes',result['route_summary'])
    print('negative probes',len(cases),'unchanged',all(c['input_unchanged'] for c in cases))
    print('missing',[(r['id'],r['references'][0]['name']) for r in route if r['status'] in ('codec_absent','unhandled')])


if __name__=='__main__':
    main()
