"""Verify original-table provenance and run a freshly packed backend in isolation."""
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/tools')]
from audit_hotupdate_gap import index, table
from offline_android.pack_payload import build_payload


def main():
    logical='csv_config/assist_shop_config.csv'
    audit=json.loads((ROOT/'analysis/evidence/hotupdate_gap_20261031/audit.json').read_text())
    expected=next(r['original_sha256'] for r in audit['csv'] if r['logical']==logical)
    with zipfile.ZipFile(ROOT/'build/金箍棒3.87离线正式版v107.apk') as apk:
        with zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as program:
            version,idx=index(program.read('client/release_w/index.txt'))
            raw=program.read('client/release_w/'+idx[logical])
    assert version==1263 and hashlib.sha256(raw).hexdigest()==expected
    with (ROOT/'analysis/configs/save_monkey/assist_shop_config.csv').open(newline='') as source:
        assert list(csv.reader(source))==table(raw)
    evidence=ROOT/'analysis/evidence/save_monkey'
    (evidence/'sources.json').write_text(json.dumps(dict(logical=logical,version=version,sha256=expected,
        origin='v107 APK embedded original hotupdate',matches_official_audit=True),ensure_ascii=False,indent=2)+'\n')
    with tempfile.TemporaryDirectory(prefix='save-monkey-payload-') as temp:
        dest=Path(temp);bundle=dest/'payload.zip';manifest=build_payload(bundle)
        required=['network_redirect/activity_save_monkey.py','network_redirect/save_monkey_client.lua',
                  'server_config/save_monkey_rules.json','analysis/configs/save_monkey/assist_shop_config.csv']
        with zipfile.ZipFile(bundle) as archive:
            assert all(n in archive.namelist() for n in required)
            archive.extractall(dest/'unpacked')
        code='''
from pathlib import Path
import tempfile
from network_redirect import activity_save_monkey as m
from network_redirect.backend import Backend,login_fields
from network_redirect.protocol import encode,decode
assert m.MONKEYS[1356][1]==[5,10000,10,1]
with tempfile.TemporaryDirectory() as temp:
 b=Backend(Path(temp),18770,lambda *a,**k:None)
 replies=b.respond(encode(1346,dict(serial_num=100000,id=1,data='{}')),{'authenticated':True})
 packet=next(p for p in replies if decode(p)[0]==2998 and decode(p)[2]['id']==197)
 data=login_fields(decode(packet)[2]['data'])
 assert len(data['local_assist'])==4 and len(data['grid_conf'])==8 and len(packet)<32768
 b.close()
print('isolated packaged backend entry and original rewards passed')
'''
        proc=subprocess.run([sys.executable,'-c',code],cwd=dest/'unpacked',
            env={**os.environ,'PYTHONPATH':str(dest/'unpacked')},text=True,capture_output=True,check=True)
        report=dict(passed=True,bundle_id=manifest.get('bundle_id'),required=required,
                    original_table_verified=True,output=proc.stdout.strip(),apk_built=False,live_save_accessed=False)
    (evidence/'payload_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
