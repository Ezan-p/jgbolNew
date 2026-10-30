"""Publish the verified candidate while retaining the previous v106 archive."""
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from offline_android.pack_payload import collect_files

WORK = ROOT / '.runtime/v106-update'
EVIDENCE = ROOT / 'analysis/evidence/v106_update'
NAME = '金箍棒3.87-离线单机-arm32-v106.apk'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    build = json.loads((EVIDENCE / 'build-validation.json').read_text())
    payload = json.loads((EVIDENCE / 'payload-save-validation.json').read_text())
    device = json.loads((EVIDENCE / 'device-validation.json').read_text())
    assert payload['apk_sha256'] == device['apk_sha256'] == build['apk_sha256']
    assert payload['all_database_tables_equal_after_upgrade_and_restart']
    assert device['same_version_update'] and device['new_program_ready']
    assert device['save_byte_identical_after_install_start_and_stop']
    for name, count in [('regression.log', 154), ('android-tests.log', 5),
                        ('packaged-protocol-tests.log', 35)]:
        log = (EVIDENCE / name).read_text()
        assert f'Ran {count} tests' in log and '\nOK\n' in log and 'FAILED (' not in log, name
    for name, path in collect_files().items():
        if name != 'network_redirect/login.html':
            assert digest(path) == digest(WORK / 'payload-new' / name), 'Source changed: ' + name
    latest = ROOT / 'build' / NAME
    archived = ROOT / build['previous_release_archive'] / NAME
    assert digest(archived) == build['baseline_sha256']
    assert digest(latest) == build['baseline_sha256'], 'Latest release changed during validation'
    assert digest(WORK / NAME) == build['apk_sha256']
    notes = WORK / 'v106更新说明.txt'
    text = notes.read_text()
    text += ('\n本轮验证：154项相关玩法回归、5项Android测试、35项实际包内协议测试全部通过。\n'
             '独立Android 6 ARMv7模拟器同版本覆盖更新成功，新程序启动成功；安装前后及首次启动后测试存档哈希一致。\n'
             '测试使用2个账号、2个角色，未操作玩家设备；尚未进行实体手机安装验收。\n')
    notes.write_text(text)
    # Publish the APK last, after preparing its matching sidecars and notes.
    files = [WORK / NAME.replace('.apk', '.manifest.json'), WORK / (NAME + '.sha256'),
             WORK / (NAME + '.idsig'), notes, WORK / NAME]
    for path in files:
        target = ROOT / 'build' / path.name
        temporary = target.with_name(target.name + '.publishing')
        shutil.copy2(path, temporary)
        assert digest(temporary) == digest(path)
        temporary.replace(target)
    assert digest(latest) == build['apk_sha256']
    report = dict(apk=str(latest.relative_to(ROOT)), apk_sha256=build['apk_sha256'],
                  baseline_archived=str(archived.relative_to(ROOT)), version_code=106,
                  published=True, all_19_changes=True, same_version_upgrade_verified=True)
    (EVIDENCE / 'published-release.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
