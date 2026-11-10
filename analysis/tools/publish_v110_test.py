"""Publish the validated isolated v110 test artifact without replacing old APKs."""
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
WORK = ROOT / '.runtime/v110-test'
EVIDENCE = ROOT / 'analysis/evidence/v110_test'
APK = WORK / '金箍棒ol测试版-v110.apk'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    meta = json.loads((EVIDENCE / 'build-validation.json').read_text())
    assert sha(APK) == meta['apk_sha256']
    reports = {}
    for name in ('protocol', 'lua', 'v108-upgrade'):
        report = json.loads((EVIDENCE / (name + '-validation.json')).read_text())
        assert report['passed'] and report['apk_sha256'] == meta['apk_sha256'], name
        assert not report.get('skipped') and not report.get('errors') and not report.get('failures'), name
        reports[name] = report
    device = json.loads((EVIDENCE / 'device-validation.json').read_text())
    assert device['apk_sha256'] == meta['apk_sha256']
    if not device.get('passed'):
        assert '--allow-unverified-device' in sys.argv and device['status'] == 'environment_blocked'
    progression = json.loads((EVIDENCE / 'progression-validation.json').read_text())
    assert progression['apk_sha256'] == meta['apk_sha256']
    assert progression['progression']['stone_level'] == 14
    assert progression['migration']['restart_does_not_duplicate']
    for source, expected in meta['workspace_source_sha256'].items():
        assert sha(ROOT / source) == expected, source
    from network_redirect.summon import client_source, load_rules
    generated, count = re.subn(r"label\('v\d+',0\.75\)", "label('v110',0.75)", client_source(load_rules()))
    assert count == 1 and generated.encode() == (WORK / 'program/offline_client.lua').read_bytes()
    assert sha(ROOT / 'offline_android/native/offline.c') == meta['native_source_sha256']
    for source, expected in meta['java_source_sha256'].items():
        assert sha(ROOT / source) == expected, source
    for name in ('native-guard-validation', 'native-retry-validation'):
        report = json.loads((ROOT / 'analysis/evidence/game_clock_resume_20261109' / (name + '.json')).read_text())
        assert report['passed'] and report['native_source_sha256'] == meta['native_source_sha256']
        shutil.copy2(ROOT / 'analysis/evidence/game_clock_resume_20261109' / (name + '.json'), EVIDENCE / (name + '.json'))
    assert sha(ROOT / 'build' / meta['baseline']) == meta['baseline_sha256']
    assert sha(ROOT / 'build/金箍棒ol测试版-v108.apk') == meta['previous_test_sha256']
    with zipfile.ZipFile(APK) as apk:
        with zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as program:
            for name in program.namelist():
                assert program.read(name) == (WORK / 'program' / name).read_bytes(), name
                assert Path(name).suffix not in ('.db', '.sqlite3', '.pyc')
    output = ROOT / 'build' / APK.name
    assert not output.exists(), 'Refusing to replace a published test APK'
    notes = ROOT / 'build/金箍棒ol测试版-v110使用说明.txt'
    assert notes.is_file()
    text = notes.read_text().split('\n本轮验证\n')[0].rstrip()
    device_note = ("本次独立Android 6 ARMv7 QA模拟器完成v108→v110覆盖安装，安装前后数据库字节一致，启动后既有养成保留，补给未重复；重启角色值一致。"
                   if device.get('passed') else
                   "本轮安卓装机验收未完成：专用Android 6 ARMv7模拟器安装旧v108基线包时超时；待后台安装完成后，旧版本地服务初始化再次超时。尚未进入新v110测试包安装与启动阶段，本包未宣称通过本轮设备验收。")
    text += (f"\n\n本轮验证\n{reports['protocol']['tests']}项去重回归通过，0失败、0错误、0跳过；"
             "包括已完成的正式版基线检查及本次改动定向检查。\n"
             "Lua 5.1完整补丁编译、登录前v110标识、客户端回归、原生时钟与重试检查通过。\n"
             "v108生成的旧测试存档升级、重复启动及一次性补给检查通过；完整材料消耗养成验证通过。\n"
             f"{device_note}\n"
             "尚未进行物理手机、光速虚拟机及全部玩法逐项触摸验收。\n"
             f"APK SHA-256：{meta['apk_sha256']}\n")
    notes.write_text(text)
    for suffix in ('.apk', '.apk.sha256', '.manifest.json', '.apk.idsig'):
        shutil.copy2(APK.with_suffix(suffix), output.with_suffix(suffix))
    published_meta = dict(meta, verification=dict(protocol_tests=reports['protocol']['tests'],
        failures=0, errors=0, skipped=0, lua_passed=True,
        host_v108_upgrade_passed=True, progression_passed=True,
        device_verified=bool(device.get('passed')), device_status=device.get('status', 'passed'),
        physical_device_test=False))
    output.with_suffix('.manifest.json').write_text(json.dumps(published_meta, ensure_ascii=False, indent=2) + '\n')
    supplies = ROOT / 'build/金箍棒ol测试版-v110沿用补给清单.json'
    shutil.copy2(ROOT / 'build/金箍棒ol测试版-v108补给清单.json', supplies)
    archive = output.with_suffix('.apk.zip')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in (output, output.with_suffix('.apk.sha256'), output.with_suffix('.manifest.json'), notes, supplies):
            z.write(p, p.name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert hashlib.sha256(z.read(output.name)).hexdigest() == meta['apk_sha256']
    assert sha(output) == meta['apk_sha256']
    result = dict(published=True, apk_sha256=meta['apk_sha256'], apk=str(output.relative_to(ROOT)),
        archive=str(archive.relative_to(ROOT)), tests=reports['protocol']['tests'],
        baseline_and_previous_test_preserved=True, device_verified=bool(device.get('passed')),
        physical_device_test=False)
    (EVIDENCE / 'published-release.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
