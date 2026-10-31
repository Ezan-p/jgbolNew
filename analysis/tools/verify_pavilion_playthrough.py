"""A fresh temporary account completes every pavilion branch over the real wire."""
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity_pavilion as p,summon
from network_redirect.backend import Backend,login_fields
from network_redirect.protocol import encode,decode
sys.path.insert(0,str(ROOT/'tests'))
from recharge_helpers import funded_order
NOW=1792987200


def main():
    records=[];serial=100000
    with tempfile.TemporaryDirectory() as tmp,patch('network_redirect.backend.time.time',return_value=NOW) as clock:
        b=Backend(Path(tmp),18770,lambda *a,**k:None)
        role=b.profile();role['level']=30;b.save(role)
        def request(name,mid,expected=True,**data):
            nonlocal serial
            serial+=1;before=b.profile()
            packet=encode(mid,dict(serial_num=serial,**data));reply=b.respond(packet,{'authenticated':True})
            decoded=[decode(x) for x in reply]
            errors=[login_fields(d['data'])['op_string'] for m,_,d in decoded if m==2998 and d['id']==55]
            if mid==1111:assert errors==['金卡充值成功，计入充值1000元'],errors
            else:assert bool(errors)!=expected,(name,errors)
            after=b.profile()
            if not expected:assert before==after
            assert b.respond(packet,{'authenticated':True})==reply
            assert after==b.profile()
            records.append(dict(name=name,mid=mid,accepted=expected,errors=errors,
                bricks=sum(x['count'] for x in after['attachments'] if x['type_id']==1141),
                bought=after.get('pavilion',{}).get('bought',{}),claimed=after.get('pavilion',{}).get('claimed',[])))
        def call(name,flag,index=0,count=0,expected=True,**kw):
            request(name,1227,expected,flag=flag,index=index,count=count,**kw)
        def mail_claims():
            for key,m in list(b.profile()['welfare'].get('mails',{}).items()):
                if key.startswith('pavilion-') and not m['claimed']:
                    request('领取活动邮件:'+key,1103,mail_id=m['mail_id'])
        request('原版活动入口',1205,flag=0);call('首次进入',1)
        for i in range(20):request('金卡充值'+str(i+1),1111,event_id=251,data=funded_order(b,106,'pavilion-run-'+str(i)))
        mail_claims();call('查看全民奖励',1)
        for i in range(1,5):call('领取全民档位'+str(i),3,index=i)
        call('拒绝重复领奖',3,index=1,expected=False)
        for index in sorted(p.SHOP):
            row=p.catalog(b.profile(),NOW,p.load_rules())['exchange_info'][index]
            cards={'ten_card':2,'five_card':2} if index==4 else {}
            call('兑换完整限额:'+p.SHOP[index][next(k for k in p.SHOP[index] if k.startswith('name'))],2,index,row['left_buy_count'],**cards)
            call('限额用尽拒绝',2,index,1,expected=False)
            if index==5:
                before=b.profile();b.close();b=Backend(Path(tmp),18770,lambda *a,**k:None)
                assert b.profile()==before
                call('中途重启继续',1)
        mail_claims();role=b.profile()
        stones=[x for x in role['attachments'] if x['type_id'] in (1090,1091,1092)]
        assert sum(x['count'] for x in stones if x['type_id']==1090 and x['level']==9)==3
        assert sum(x['count'] for x in stones if x['type_id']==1091 and x['level']==9)==3
        assert any(x['type_id']==1092 and x['level']==8 for x in stones)
        assert all(x['count']==1 for x in stones)
        assert role['achievements']['totals'].get('125',0)==0  # belongs to mondayUI/menu32
        old_currency=records[-1]['bricks'];old_mails=role['welfare']['mails'];clock.return_value=role['pavilion']['end']
        call('双周新一期',1)
        assert records[-1]['bricks']==0
        refund=next(m for k,m in b.profile()['welfare']['mails'].items() if k.startswith('pavilion-recycle-'))
        assert refund['prizes']==[[5,1001,old_currency,1]]
        request('新一期重新充值',1111,event_id=251,data=funded_order(b,106,'pavilion-next-period'))
        mail_claims();call('新一期再兑换和首次邮件',2,9,1);mail_claims()
        assert b.profile()['pavilion']['bought']=={'9':1}
        assert all(b.profile()['welfare']['mails'][k]==v for k,v in old_mails.items())
        b.close()
    report=dict(passed=True,date='2026-10-31',temporary_database=True,seeded_gold_cards=True,seeded_bricks=False,
        requests=len(records),replayed_every_packet=True,all_ten_limits_exhausted=True,
        stones=stones,steps=records,boundary='原版协议端到端流程；充值通过背包金卡扣除模拟；界面验证另见client_validation.log')
    out=ROOT/'analysis/evidence/pavilion/catalog_1263_playthrough.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f'{len(records)} original-wire requests passed; 10 catalogs exhausted; restart and new season passed')

if __name__=='__main__':main()
