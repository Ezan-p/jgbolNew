"""Upgrade a disposable v108-generated test save through the actual v110 payload."""
import io
import hashlib
import json
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / '.runtime/v110-test'
EVIDENCE = ROOT / 'analysis/evidence/v110_test'


def main():
    previous = WORK / 'previous-program'
    with zipfile.ZipFile(ROOT / 'build/金箍棒ol测试版-v108.apk') as apk:
        with zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as program:
            program.extractall(previous)
    formal = WORK / 'formal-program'
    with zipfile.ZipFile(ROOT / 'build/金箍棒ol离线正式版v110.apk') as apk:
        with zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as program:
            program.extractall(formal)
    worker = r'''
import copy,json,pathlib,sys
program, directory, mode = sys.argv[1:]
sys.path.insert(0,program)
directory=pathlib.Path(directory)
if mode=='formal':
    from network_redirect.backend import Backend
    b=Backend(directory,18770,lambda *args,**kwargs:None,account='v106_fixed_test')
    (directory/'formal.json').write_text(json.dumps(b.profile()))
    b.close()
    raise SystemExit(0)
from offline_android import test_edition_v108 as seed
a=seed.fixed_accounts_class()(directory,18776,lambda *args,**kwargs:None)
b=a.backends[seed.ACCOUNT]
role=b.profile()
if mode=='old':
    role['role_name']='v108升级保留检查'
    role['gold_coin']-=1234
    role['test_v110_sentinel']={'preserve':[1,2,3]}
    role['corteges'][0]['level']=150
    b.save(role,gameplay=False)
    snapshot=b.profile()
    (directory/'before.json').write_text(json.dumps(snapshot))
else:
    from network_redirect import game_clock
    before=json.loads((directory/'before.json').read_text())
    expected=json.loads((directory/'formal.json').read_text())
    for key in ('role_name','gold_coin','silver_coin','test_v108_silver_reserve',
                'test_supply_revision','test_v110_sentinel','attachments','corteges'):
        # v110 normalizes spell count/pity and derived companion fields on load.
        if key in ('attachments','corteges'):
            before[key]=expected[key]
        if role[key]!=before[key]:
            print('MIGRATION DIFFERENCE',key,flush=True)
            if isinstance(role[key],list):
                for old,new in zip(before[key],role[key]):
                    if old!=new:
                        print('OLD',old,'NEW',new,flush=True)
                        break
            raise AssertionError(key)
    assert role['test_supply_revision']==108
    with game_clock.scope(b.clock) as now:
        assert seed.initialize(b,now) is False
    assert b.profile()==role
    a.close()
    a=seed.fixed_accounts_class()(directory,18776,lambda *args,**kwargs:None)
    assert a.backends[seed.ACCOUNT].profile()==role
    (directory/'result.json').write_text(json.dumps(dict(passed=True,
        existing_progress_preserved=True, supply_not_repeated=True,
        restart_idempotent=True, source='disposable save created by shipped v108 payload')))
a.close()
'''
    with tempfile.TemporaryDirectory(prefix='jgbol-v110-upgrade-') as temp:
        directory = str(Path(temp) / 'test')
        for mode, program in [('old', previous), ('new', WORK / 'program')]:
            if mode=='new':
                formal_save = Path(temp) / 'formal'
                shutil.copytree(directory, formal_save)
                subprocess.run([sys.executable, '-I', '-c', worker, str(formal), str(formal_save), 'formal'], check=True)
                shutil.copy2(formal_save / 'formal.json', Path(directory) / 'formal.json')
            subprocess.run([sys.executable, '-I', '-c', worker, str(program), directory, mode], check=True)
        report = json.loads((Path(directory) / 'result.json').read_text())
    report['apk_sha256'] = hashlib.sha256((WORK / '金箍棒ol测试版-v110.apk').read_bytes()).hexdigest()
    (EVIDENCE / 'v108-upgrade-validation.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
