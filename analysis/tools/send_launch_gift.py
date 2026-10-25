"""One-time local launch gift; calculate costs from installed rules, verify before issue."""
import argparse, collections, copy, json, math, sqlite3, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import formation as f, reborn as b, summon, welfare as w, journey
KEY='launch_gift_20261025_v1'
MID=800000025

def build():
    totals=collections.Counter()
    def add(t,n=1,kind=5,level=1): totals[kind,t,level]+=n
    def consume(text):
        for token in text.split('/'):
            kind,t,level,n=map(int,token.split('|')); add(t,n,kind,level)
    for t in (5046,5044,5048,5051):add(t,kind=4)
    maximum=max(l for q,l in f.EVOLVE_POINTS if q==5)
    add(5046,sum(f.EVOLVE_COST[l] for l in range(1,maximum+1)),10)
    for row in b.VEINS.values():
        fixed=int(row['fixed_count(fix>0|unfix=0)'])
        if fixed:add(int(row['consume_list'].split('|')[1]),fixed)
        else:consume(row['consume_list'])
    for row in b.LAYERS.values():consume(row['consum_list'])
    for row in b.load_rules()['realms']:add(row['material'],row['cost'])
    for kind,t in enumerate((2009,3003,4003),1):
        add(t)
        for advance in range(10):
            add({1:1310,2:1311,3:1312}[kind],sum(int(f.STAR_COST[5,s][advance].split('|')[kind-1]) for s in range(1,8)))
            for token in f.ADVANCE_COST[5,advance+1][{1:'wuqi_cost',2:'fangyu_cost',3:'fabao_cost'}[kind]].split('/'):
                mat,n=map(int,token.split('|'));add(mat,n)
        consume(list(b.EQUIP[kind].values())[1])
        for (k,lv),row in b.CAST.items():
            if k==kind and lv>1:consume(list(row.values())[2])
    add(202,kind=6);add(22,kind=6)
    # One level-10 five-star fodder per upgrade guarantees 100%, within the 500-item request cap.
    add(203,9,6,10)
    for lv in range(1,10):assert float(f.SKILL_WORTH[10]['quality_worth5'])>=float(f.SKILL_COST[lv]['quality5_cost'])
    add(201,1,15,2)
    for t,n in ((1345,10000),(1347,100),(1348,100),(1349,100)):add(t,n)
    for t in range(10101,10106):add(t)
    for t in range(10201,10206):add(t)
    # Full 1->200 progression plus experience lost by all nine rebirths.
    exp=sum(f.EXPERIENCE[5,l] for l in range(1,200))
    exp+=sum(sum(f.EXPERIENCE[5,l] for l in range(int(r['reset_level']),int(r['min_level']))) for r in b.LAYERS.values())
    add(1041,math.ceil(exp/2/int(f.ITEMS[1041]['experience_plus'])))
    add(1401,math.ceil(exp/2/int(f.ITEMS[1401]['experience_plus'])))
    return [[kind,t,n,lv] for (kind,t,lv),n in totals.items()],dict(evolve_max=maximum,reborn_max=9,cast_max=max(l for k,l in b.CAST),experience=exp)

def verify(role,mail,rules):
    test=copy.deepcopy(role);state=w.prepare(test,int(time.time()),rules)
    state.setdefault('mails',{})[KEY]=copy.deepcopy(mail)
    w.mail_request(test,1102,dict(mail_id=MID,flag=0),int(time.time()),rules,state)
    w.mail_request(test,1103,dict(mail_id=MID),int(time.time()),rules,state)
    assert state['mails'][KEY]['claimed']
    before=copy.deepcopy(test)
    try:w.mail_request(test,1103,dict(mail_id=MID),int(time.time()),rules,state)
    except f.Rejected:pass
    else:raise AssertionError('duplicate claim accepted')
    assert test==before
    assert all(any(c['type']==t for c in test['corteges']) for t in (5046,5044,5048,5051))
    assert any(p['type_id']==201 for p in test['activity']['home']['pets'])
    # Spend all calculated gear costs on the claimed copy through real settlement.
    test['reborn_layer']=4
    for tid in (2009,3003,4003):
        item=next(x for x in test['attachments'] if x['type_id']==tid)
        for advance in range(10):
            for star in range(7):f.advance_equipment(test,dict(equip_id=item['id'],equip_order=0,flag=1,is_one_key=True),f.load_rules())
            f.advance_equipment(test,dict(equip_id=item['id'],equip_order=0,flag=2),f.load_rules())
        data=dict(equip_id=item['id'],equip_order=0)
        b.settle(test,dict(id=5,reborn_type=3,data=data),b.load_rules(),lambda x:x)
        for lv in range(2,max(l for k,l in b.CAST if k==int(f.ITEMS[tid]['main_type']))+1):
            b.settle(test,dict(id=6,reborn_type=3,data=data),b.load_rules(),lambda x:x)
    c=next(c for c in test['corteges'] if c['type']==5046)
    f.prepare(test,f.load_rules())
    for lv in range(1,max(l for q,l in f.EVOLVE_POINTS if q==5)+1):
        f.evolve(test,dict(flag=0,cortege_id=c['id']))
    for layer in range(1,10):
        for vein in range(1,10):
            row=b.VEINS[layer,vein];fixed=int(row['fixed_count(fix>0|unfix=0)'])
            supplied={int(x.split('|')[1]):int(x.split('|')[3]) for x in row['consume_list'].split('/')}
            if fixed:supplied={next(iter(supplied)):fixed}
            d=dict(cortege_id=c['id'],material_list=supplied)
            b.settle(test,dict(id=1,reborn_type=2,data=d),b.load_rules(),lambda x:x)
        c['level']=int(b.LAYERS[layer]['min_level']);c['cur_exp']=0
        b.settle(test,dict(id=2,reborn_type=2,data=dict(cortege_id=c['id'])),b.load_rules(),lambda x:x)
    target=next(x for x in test['attachments'] if x['attach_type']==6 and x['type_id']==202 and x['level']==1)
    fodder=[x for x in test['attachments'] if x['attach_type']==6 and x['type_id']==203 and x['level']==10][-9:]
    for material in fodder:
        f.enhance_skill(test,dict(data=dict(des_skill_id=target['id'],src_skill_list=[material['id']])),f.load_rules(),lambda x:x)
    assert target['level']==10 and c['reborn_layer']==9
    return 'preview, claim, duplicate rejection, three maxed equipment paths, full ascension/rebirth materials, guaranteed level-10 skill passed'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--account',required=True);ap.add_argument('--send',action='store_true');args=ap.parse_args()
    db=sqlite3.connect(ROOT/'.runtime/offline/game.sqlite3',timeout=30)
    prizes,limits=build();now=int(time.time());rules=w.load_rules()
    mail=dict(mail_id=MID,mail_title='开服大礼包',mail_body='四位神仙；元始天尊满飞升、九转材料；无上至尊初始三件及满进阶、封神、铸造材料；五星主动袖里乾坤、被动指地成钢及满级法术素材；天翼虎与养成丹药；金紫精魄各五；仙佛密卷和培元丹。转生仍需满足境界条件。',recv_time=now,send_time=now,prizes=prizes,claimed=False)
    if args.send:db.execute('BEGIN IMMEDIATE')
    raw=db.execute('select data from roles where account=?',(args.account,)).fetchone();assert raw,'account not found'
    role=json.loads(raw[0]);assert KEY not in role.get('welfare',{}).get('mails',{}),'already sent'
    result=verify(role,mail,rules)
    report=dict(account=args.account,role_name=role['role_name'],limits=limits,mail=mail,verification=result)
    if args.send:
        directory=ROOT/'.runtime/offline/backups';directory.mkdir(exist_ok=True)
        (directory/f'{args.account}-{KEY}-before.json').write_text(raw[0])
        w.prepare(role,now,rules).setdefault('mails',{})[KEY]=mail
        db.execute('update roles set data=? where account=?',(json.dumps(role,ensure_ascii=False),args.account));db.commit()
        assert json.loads(db.execute('select data from roles where account=?',(args.account,)).fetchone()[0])['welfare']['mails'][KEY]==mail
    out=ROOT/'analysis/evidence/launch_gift_20261025.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(dict(sent=args.send,account=args.account,attachment_types=len(prizes),limits=limits,verification=result),ensure_ascii=False))
if __name__=='__main__':main()
