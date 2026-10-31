"""Capture the installed APK's cold-start UI without injecting any UI patches."""
import hashlib,json,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
EVIDENCE=ROOT/'analysis/evidence/v108'
ADB=[str(ROOT/'.runtime/sdk/platform-tools/adb'),'-s','emulator-5572']
PACKAGE='com.sygame.jingubang.p360'
def call(*args):return subprocess.check_output(ADB+list(args),timeout=60)
def main():
    assert call('emu','avd','name').decode().splitlines()[0]=='standalone32'
    deadline=time.monotonic()+240
    while not (EVIDENCE/'device-validation.json').exists():
        if time.monotonic()>deadline:raise TimeoutError('Upgrade verification not finished')
        time.sleep(2)
    device=json.loads((EVIDENCE/'device-validation.json').read_text())
    build=json.loads((EVIDENCE/'build-validation.json').read_text())
    assert device['apk_sha256']==build['apk_sha256']
    ps=call('shell','ps').decode()
    assert not any('/data/local/tmp/branding-preview-server' in line for line in ps.splitlines())
    call('logcat','-c')
    call('shell','am','start','-n',PACKAGE+'/com.jgbol.offline.LauncherActivity')
    deadline=time.monotonic()+180
    while True:
        logs=call('logcat','-d','-s','JGBOffline:I','*:S').decode()
        assert 'offline_lua_error:' not in logs and 'native_install_failed:' not in logs,logs
        if 'offline_native_ready:' in logs and 'OFFLINE_READY '+build['program_sha256'] in logs:break
        if time.monotonic()>deadline:raise TimeoutError(logs)
        time.sleep(2)
    # Wait for the game's first scene, independently of the offline server ready signal.
    time.sleep(18)
    (EVIDENCE/'startup-home.png').write_bytes(call('exec-out','screencap','-p'))
    logs=call('logcat','-d','-s','JGBOffline:I','*:S').decode()
    (EVIDENCE/'native-startup.log').write_text(logs)
    assert 'offline_lua_error:' not in logs and 'native_install_failed:' not in logs,logs
    call('shell','am','force-stop',PACKAGE)
    data=call('exec-out','cat','/data/data/'+PACKAGE+'/files/save/game.sqlite3')
    sha=hashlib.sha256(data).hexdigest()
    assert sha==device['baseline']['sha256'],'UI startup changed QA database'
    report=dict(apk_sha256=build['apk_sha256'],no_external_ui_patch=True,no_lua_error=True,
      cold_start_native_branding_verified=False,awaiting_screenshot_review=True,
      save_hash_after_ui=sha,screenshot='startup-home.png')
    (EVIDENCE/'startup-ui-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Native cold-start captured; QA save unchanged. Review screenshot before publishing.',flush=True)
if __name__=='__main__':main()
