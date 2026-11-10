"""Send real redemption and Land requests to the disposable ARM32 Android service."""
import hashlib
import http.client
import json
from pathlib import Path
import re
import secrets
import socket
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'.runtime/v111-three-updates-20261110/payload-new'))
from network_redirect.protocol import HEADER,encode,decode
from network_redirect.backend import login_fields
from network_redirect import summon

EVIDENCE=ROOT/'analysis/evidence/v111-three-updates-20261110'
ADB=[str(ROOT/'.runtime/sdk/platform-tools/adb'),'-s','emulator-5592']


def adb(*args,timeout=30):
    return subprocess.check_output(ADB+list(args),timeout=timeout,stderr=subprocess.STDOUT)


def packet(connection):
    def exact(size):
        result=b''
        while len(result)<size:
            chunk=connection.recv(size-len(result))
            if not chunk:raise EOFError('Android game connection closed')
            result+=chunk
        return result
    head=exact(HEADER.size)
    return decode(head+exact(HEADER.unpack(head)[1]-HEADER.size))


def main():
    assert adb('emu','avd','name').decode().splitlines()[0]=='v110refreshqa'
    end=time.monotonic()+180
    while adb('shell','getprop','sys.boot_completed').strip()!=b'1':
        assert time.monotonic()<end,'Android boot timed out'
        time.sleep(5)
    adb('shell','am','start','-n','com.sygame.jingubang.p360/com.jgbol.offline.LauncherActivity',timeout=60)
    port=int(adb('forward','tcp:0','tcp:18770').strip())
    def http_request(path,payload=None,csrf=''):
        c=http.client.HTTPConnection('127.0.0.1',port,timeout=60)
        c.request('POST' if payload is not None else 'GET',path,
                  json.dumps(payload) if payload is not None else None,
                  {'X-Local-CSRF':csrf,'Host':'127.0.0.1:18770'})
        response=c.getresponse();body=response.read();c.close()
        assert response.status==200,(path,response.status,body[:200])
        return body
    try:
        end=time.monotonic()+240
        while True:
            try:
                page=http_request('/local-login').decode();break
            except (OSError,http.client.HTTPException):
                assert time.monotonic()<end,'Android service startup timed out'
                print('Waiting for Android local service',flush=True);time.sleep(10)
        csrf=re.search(r"setRequestHeader\('X-Local-CSRF','([^']+)'\)",page)[1]
        username='qa_three_'+secrets.token_hex(3)
        password=secrets.token_urlsafe(15)
        result=json.loads(http_request('/local-auth',dict(action='register',username=username,
                          password=password,confirm=password,remember=False),csrf))
        assert result['ok'],result
        reports=[]
        with socket.create_connection(('127.0.0.1',port),timeout=90) as connection:
            connection.sendall(encode(3001,dict(id=68,data='{access_token="'+result['token']+'"}')))
            mid,_,ticket=packet(connection);assert mid==3002 and ticket['server_port']==18770
            connection.sendall(encode(1001,{k:ticket[k] for k in ('auth_key','seed','account')}))
            mid,_,login=packet(connection);assert mid==1002 and login['result']==0
            serial=100000
            def request(mid,**data):
                nonlocal serial
                serial+=1
                connection.sendall(encode(mid,dict(serial_num=serial,**data)))
                packets=[]
                while True:
                    p=packet(connection);packets.append(p)
                    if p[0]==1106 and p[2]['req_serial_num']==serial:break
                return packets
            def event(packets,ident):
                return next(login_fields(d['data']) for mid,_,d in packets if mid==2998 and d['id']==ident)
            config=json.loads((ROOT/'server_config/gift_code_rules.json').read_text())
            for row in config['codes'][-20:]:
                answer=event(request(1104,sn=row['code'],flag=0),18)
                assert answer['result']==1,(row['code'],answer)
                values=answer['attach_list'].values() if isinstance(answer['attach_list'],dict) else answer['attach_list']
                actual=[[p['object_type'],p['attach_type'],p['attach_count'],p['attach_level']] for p in values]
                assert actual==row['prizes'],(actual,row['prizes'])
                reports.append(dict(code=row['code'],result=1,rewards=actual))
                print('Android redeemed',row['code'],'successfully',flush=True)
            packets=request(1104,sn='CUTWP96BZCKY',flag=0)
            assert event(packets,18)['result']==1
            item=next(i for mid,_,d in packets if mid==1035 for i in d['attach_list'] if i['type_id']==1901)
            level=1
            for _ in range(37):
                answer=event(request(1051,item_type=1901,item_id=item['id'],item_count=1,des_type=1,des_id=0),2)
                level=answer['new_level']
            assert level==38,level
            land=event(request(1302,id=1,data='{}'),149)
            rows=land['tower_info'].values() if isinstance(land['tower_info'],dict) else land['tower_info']
            from network_redirect import activity,activity_land_npc as npc
            rules=activity.load_rules()
            towers=[]
            for row in rows:
                key=row['npc_id'];catalog=npc.catalog()[key]
                assert catalog['tier']==rules['land_guard_tier_by_type'][row['tower_type']-1]
                towers.append(dict(tower_type=row['tower_type'],npc_id=key,tier=catalog['tier'],
                                   full_power=npc.power(catalog,8)))
            assert len(towers)==4
            record=dict(passed=True,transport='host ADB forward -> ARM32 Android running APK service',
                        apk_sha256=hashlib.sha256((ROOT/'build/金箍棒ol离线正式版v111.apk').read_bytes()).hexdigest(),
                        temp_account_only=True,gift_redemptions=reports,role_level=level,land_towers=towers,
                        phone_or_virtual_machine_tested=False)
            (EVIDENCE/'android-live-protocol-validation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
            print('All 20 actual Android redemptions and T4/T5 Land guard requests passed',flush=True)
    finally:
        adb('forward','--remove',f'tcp:{port}')


if __name__=='__main__':main()
