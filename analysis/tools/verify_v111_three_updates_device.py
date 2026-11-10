"""Check replacement installation only on the existing disposable ARM32 QA AVD."""
import io
import json
from pathlib import Path
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from analysis.tools.build_v111_three_updates import WORK,EVIDENCE,OUTPUT,BASE,digest,report

ADB=[str(ROOT/'.runtime/sdk/platform-tools/adb'),'-s','emulator-5592']
PACKAGE='com.sygame.jingubang.p360'
DEVICE=WORK/'device-validation'


def call(*args,timeout=30):
    return subprocess.check_output(ADB+list(args),timeout=timeout,stderr=subprocess.STDOUT)


def save_copy(label):
    destination=DEVICE/label
    assert not destination.exists()
    call('pull',f'/data/data/{PACKAGE}/files/save',str(destination),timeout=120)
    return {str(p.relative_to(destination)):digest(p.read_bytes())
            for p in destination.rglob('*') if p.is_file()}


def main():
    DEVICE.mkdir(parents=True,exist_ok=True)
    sha=digest(OUTPUT.read_bytes())
    record=dict(apk_sha256=sha,passed=False,device='v110refreshqa / emulator-5592 / Android 6 ARM32',
                candidate_installed=False,startup_ui_verified=False,physical_device_tested=False)
    try:
        deadline=time.monotonic()+180
        while True:
            try:
                if call('shell','getprop','sys.boot_completed',timeout=10).strip()==b'1':break
            except (subprocess.CalledProcessError,subprocess.TimeoutExpired):pass
            if time.monotonic()>=deadline:raise RuntimeError('QA Android environment did not boot in 180 seconds')
            print('Waiting for dedicated QA Android boot',flush=True)
            time.sleep(10)
        assert call('emu','avd','name').decode().splitlines()[0]=='v110refreshqa'
        installed=call('shell','pm','path',PACKAGE).decode().strip().removeprefix('package:')
        assert installed.startswith('/data/app/'),installed
        old=DEVICE/'installed-old.apk'
        call('pull',installed,str(old),timeout=120)
        assert digest(old.read_bytes())==digest(BASE.read_bytes()),'Unexpected baseline installed in QA AVD'
        call('shell','am','force-stop',PACKAGE)
        before=save_copy('old-save')
        assert before
        print('Installing exact candidate over baseline v111',flush=True)
        assert b'Success' in call('install','--no-streaming','-r',str(OUTPUT),timeout=600)
        record['candidate_installed']=True
        after=save_copy('after-install-save')
        assert before==after,'Replacement install changed save bytes'
        record.update(same_version_replacement_verified=True,complete_save_preserved_after_install=True,
                      old_save_hashes=before,after_install_save_hashes=after)
        installed=call('shell','pm','path',PACKAGE).decode().strip().removeprefix('package:')
        pulled=DEVICE/'installed.apk'
        call('pull',installed,str(pulled),timeout=120)
        assert digest(pulled.read_bytes())==sha
        record['installed_apk_hash_verified']=True
        info=call('shell','dumpsys','package',PACKAGE).decode()
        assert 'versionCode=111 ' in info and 'versionName=3.87-offline.11' in info
        call('logcat','-c')
        call('shell','am','start','-n',PACKAGE+'/com.jgbol.offline.LauncherActivity',timeout=60)
        current=json.loads((EVIDENCE/'build-validation.json').read_text())
        deadline=time.monotonic()+240
        while True:
            logs=call('logcat','-d','-s','JGBOffline:I','*:S').decode(errors='replace')
            (EVIDENCE/'device-startup.log').write_text(logs)
            assert not any(s in logs for s in ('Offline startup failed','native_install_failed:','offline_lua_error:')),logs
            if 'OFFLINE_READY '+current['program_sha256'] in logs and 'offline_native_ready:' in logs:break
            if time.monotonic()>=deadline:raise RuntimeError('QA native engine/runtime startup exceeded 240 seconds')
            print('Waiting for packaged runtime and native engine',flush=True)
            time.sleep(10)
        record.update(passed=True,new_program_ready=True,native_ready=True,
                      status='installation_and_runtime_passed_ui_unreviewed')
        # Native READY precedes the Cocos login scene's first visible frame.
        time.sleep(20)
        (EVIDENCE/'startup-home.png').write_bytes(call('exec-out','screencap','-p',timeout=60))
        (EVIDENCE/'device-window.log').write_bytes(call('shell','dumpsys','window','windows'))
        record['screenshot']='startup-home.png'
        print('QA replacement install, exact APK hash, save bytes and native startup passed',flush=True)
    except Exception as exc:
        record.update(status='device_validation_incomplete',error=str(exc))
        report('device-validation',record)
        raise
    report('device-validation',record)


if __name__=='__main__':
    main()
