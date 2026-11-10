"""Attempt installation/startup only on the existing disposable test110qa AVD."""
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from analysis.tools.build_v111_test import APK,WORK,EVIDENCE,digest
ADB=[str(ROOT/'.runtime/sdk/platform-tools/adb'),'-s','emulator-5574']
PACKAGE='com.sygame.jingubang.test106'

def call(*args,timeout=20):
    return subprocess.check_output(ADB+list(args),timeout=timeout,stderr=subprocess.STDOUT)


def main():
    meta=json.loads((EVIDENCE/'build-validation.json').read_text())
    result=dict(passed=False,apk_sha256=digest(APK.read_bytes()),device='test110qa / emulator-5574 / ARMv7',candidate_installed=False,physical_device_test=False)
    try:
        assert call('emu','avd','name').decode().splitlines()[0]=='test110qa'
        deadline=time.monotonic()+150
        while True:
            try:
                if call('shell','getprop','sys.boot_completed',timeout=15).strip()==b'1':break
            except subprocess.TimeoutExpired:pass
            if time.monotonic()>=deadline:raise RuntimeError('Dedicated QA Android boot did not finish within 150 seconds')
            print('Waiting for dedicated QA boot',flush=True);time.sleep(5)
        info=call('shell','dumpsys','package',PACKAGE).decode()
        (EVIDENCE/'device-before-package.txt').write_text(info)
        call('shell','am','force-stop',PACKAGE)
        if call('shell','ls',f'/data/data/{PACKAGE}/files/test-save-v106',timeout=20).strip():
            call('pull',f'/data/data/{PACKAGE}/files/test-save-v106',str(WORK/'device-save-backup'),timeout=90)
            result['backup']='.runtime/v111-test/device-save-backup'
        print('Installing candidate on disposable QA emulator',flush=True)
        install=call('install','--no-streaming','-r',str(APK),timeout=300).decode()
        assert 'Success' in install,install
        result['candidate_installed']=True
        info=call('shell','dumpsys','package',PACKAGE).decode()
        assert 'versionCode=111 ' in info and 'versionName=3.87-test.111.1' in info
        call('logcat','-c')
        call('shell','am','start','-n',PACKAGE+'/com.jgbol.offline.LauncherActivity')
        deadline=time.monotonic()+240
        while True:
            log=call('logcat','-d','-s','JGBOffline:I','*:S').decode()
            (EVIDENCE/'device-startup.log').write_text(log)
            if any(s in log for s in ('Offline startup failed','native_install_failed:','offline_lua_error:')):
                raise RuntimeError('Candidate startup error; see device-startup.log')
            if 'OFFLINE_READY '+meta['program_sha256'] in log and 'offline_native_ready:' in log:break
            if time.monotonic()>=deadline:raise RuntimeError('Candidate startup timed out; see device-startup.log')
            print('Waiting for packaged runtime and native readiness',flush=True);time.sleep(5)
        (EVIDENCE/'device-startup.png').write_bytes(call('exec-out','screencap','-p'))
        result.update(passed=True,runtime_ready=True,native_ready=True,note='专用ARM32 QA模拟器覆盖安装及运行时、原生补丁启动检查通过；未逐玩法触摸验收。')
    except Exception as exc:
        result.update(status='device_validation_incomplete',reason=str(exc),note='本轮未完成设备安装启动验收：'+str(exc)+'。包内回归与临时存档升级检查不能替代设备验收。')
        print(result['note'],flush=True)
    (EVIDENCE/'device-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
