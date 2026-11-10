"""Reversion the verified ten-update test APK to v111 and replace the old release."""
import argparse
import copy
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v106_test import KEY, PACKAGE, certificate, digest
from build_channel360 import TOOLS, run
from offline_android.pack_payload import verify_payload

SOURCE = ROOT / 'build/金箍棒ol测试版-v110-20261110整合更新.apk'
SOURCE_SHA = 'c0193adb0fce8cb62f4270d2e29310c93031c823b00e9ef2eb7007fa82417119'
PREVIOUS = ROOT / 'build/金箍棒ol测试版-v111.apk'
PREVIOUS_SHA = '44a73e3c10be29af7d65a3e05fb0d00ea23751da731162f6b88b705a44162a76'
WORK = ROOT / '.runtime/v111-test-version-20261110'
EVIDENCE = ROOT / 'analysis/evidence/v111-test-version-20261110'
ARCHIVE = ROOT / 'build/archive/v111-test-before-ten-updates-20261110'
APK = WORK / PREVIOUS.name
PRIOR = ROOT / 'analysis/evidence/v110-test-refresh-20261110'


def report(name, data):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / (name + '.json')).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def payload(apk):
    with zipfile.ZipFile(apk) as z, zipfile.ZipFile(io.BytesIO(z.read('assets/offline/program.zip'))) as p:
        assert p.testzip() is None
        return {n: p.read(n) for n in p.namelist()}


def build():
    assert not APK.exists(), 'Do not replace an existing candidate'
    assert digest(SOURCE.read_bytes()) == SOURCE_SHA
    assert digest(PREVIOUS.read_bytes()) == PREVIOUS_SHA
    prior = json.loads((PRIOR / 'build-validation.json').read_text())
    assert prior['apk_sha256'] == SOURCE_SHA
    for name in ('protocol', 'grant', 'runtime', 'scope', 'lua', 'upgrade'):
        data = json.loads((PRIOR / (name + '-validation.json')).read_text())
        assert data['passed'] and data['apk_sha256'] == SOURCE_SHA
    WORK.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    backup = {}
    for path in sorted((ROOT / 'build').glob('金箍棒ol测试版-v111*')):
        if path.is_file():
            target = ARCHIVE / path.name
            if not target.exists():
                shutil.copy2(path, target)
            assert digest(path.read_bytes()) == digest(target.read_bytes())
            backup[path.name] = digest(path.read_bytes())
    report('backup', dict(files=backup, directory=str(ARCHIVE.relative_to(ROOT))))
    entries = payload(SOURCE)
    for name in ('offline_client.lua', 'network_redirect/login_branding_client.lua'):
        entries[name], count = re.subn(rb"label\('v110',0\.75\)", b"label('v111',0.75)", entries[name])
        assert count == 1, name
    manifest = json.loads(entries['payload-manifest.json'])
    for row in manifest['files']:
        if row['path'] in ('offline_client.lua', 'network_redirect/login_branding_client.lua'):
            data = entries[row['path']]
            row.update(size=len(data), sha256=digest(data), source='v111-test-version-20261110')
    manifest['bundle_id'] = digest(json.dumps(manifest['files'], sort_keys=True, separators=(',', ':')).encode())
    entries['payload-manifest.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as p:
        for name, data in entries.items():
            assert Path(name).suffix not in ('.db', '.sqlite3', '.pyc')
            p.writestr(name, data)
    program = buffer.getvalue()
    with zipfile.ZipFile(SOURCE) as source, zipfile.ZipFile(PREVIOUS) as old:
        # The already-shipped v111 test manifest carries exactly the desired
        # version/package/permissions. Every other Android-shell byte is retained.
        expected = {'AndroidManifest.xml', 'assets/offline/build.properties', 'assets/offline/program.zip'}
        names = lambda z: {n for n in z.namelist() if not n.startswith('META-INF/')}
        assert names(source) == names(old)
        shell_delta = {n for n in names(source) if source.read(n) != old.read(n)}
        assert shell_delta == expected, shell_delta
        props = source.read('assets/offline/build.properties')
        props = props.replace(digest(source.read('assets/offline/program.zip')).encode(), digest(program).encode())
        assert props.count(b'version_code=110\n') == 1
        props = props.replace(b'version_code=110\n', b'version_code=111\n')
        replacements = {'AndroidManifest.xml': old.read('AndroidManifest.xml'),
                        'assets/offline/program.zip': program, 'assets/offline/build.properties': props}
        with zipfile.ZipFile(WORK / 'unsigned.apk', 'w') as z:
            for entry in source.infolist():
                if not entry.filename.startswith('META-INF/'):
                    z.writestr(copy.copy(entry), replacements.get(entry.filename, source.read(entry)))
    run(TOOLS / 'zipalign', '-f', '4', WORK / 'unsigned.apk', WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', KEY, '--ks-key-alias', 'test106',
        '--ks-pass', 'pass:test-edition-only', '--out', APK, WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'verify', '--verbose', APK)
    run(TOOLS / 'zipalign', '-c', '4', APK)
    assert certificate(APK) == certificate(SOURCE) == certificate(PREVIOUS)
    badging = subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(APK)], text=True)
    assert f"package: name='{PACKAGE}' versionCode='111' versionName='3.87-test.111.1'" in badging
    assert badging == subprocess.check_output([str(TOOLS / 'aapt'), 'dump', 'badging', str(PREVIOUS)], text=True)
    with zipfile.ZipFile(APK) as z, zipfile.ZipFile(SOURCE) as source:
        assert z.testzip() is None and names(z) == names(source)
        assert {n for n in names(z) if z.read(n) != source.read(n)} == expected
        with zipfile.ZipFile(io.BytesIO(z.read('assets/offline/program.zip'))) as p:
            p.extractall(WORK / 'program')
    verify_payload(WORK / 'program')
    data = dict(apk=APK.name, apk_sha256=digest(APK.read_bytes()), apk_bytes=APK.stat().st_size,
        source=SOURCE.name, source_sha256=SOURCE_SHA, previous_test=PREVIOUS.name,
        previous_test_sha256=PREVIOUS_SHA, package=PACKAGE, version_code=111,
        version_name='3.87-test.111.1', program_sha256=digest(program),
        certificate_sha256=certificate(APK), player_database='files/test-save-v106/game.sqlite3',
        port=18776, contains_player_database=False, requested_updates=10,
        changed_apk_entries=sorted(expected), changed_program_entries=[
            'offline_client.lua','network_redirect/login_branding_client.lua','payload-manifest.json'])
    report('build-validation', data)
    (EVIDENCE / 'badging.txt').write_text(badging)
    APK.with_suffix('.apk.sha256').write_text(data['apk_sha256'] + '  ' + APK.name + '\n')
    APK.with_suffix('.manifest.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(data, ensure_ascii=False, indent=2))


def verify():
    before, after = payload(SOURCE), payload(APK)
    assert set(before) == set(after)
    changes = {n for n in before if before[n] != after[n]}
    assert changes == {'offline_client.lua', 'network_redirect/login_branding_client.lua', 'payload-manifest.json'}
    for n in changes - {'payload-manifest.json'}:
        assert after[n].replace(b"label('v111',0.75)", b"label('v110',0.75)") == before[n]
    assert verify_payload(WORK / 'program')['player_database'] == 'files/test-save-v106/game.sqlite3'
    generated = subprocess.check_output([sys.executable, '-I', '-c',
        'import sys;sys.path.insert(0,sys.argv[1]);from network_redirect.summon import client_source,load_rules;sys.stdout.buffer.write(client_source(load_rules()).encode())', str(WORK / 'program')])
    assert generated == after['offline_client.lua']
    evidence = {}
    for name in ('protocol', 'grant', 'runtime', 'scope'):
        data = json.loads((PRIOR / (name + '-validation.json')).read_text())
        assert data['passed'] and data['apk_sha256'] == SOURCE_SHA
        assert not any(data.get(k) for k in ('failures','errors','skipped'))
        evidence[name] = dict(path=str((PRIOR / (name + '-validation.json')).relative_to(ROOT)),
                              tests=data.get('tests'), sha256=digest((PRIOR / (name + '-validation.json')).read_bytes()))
    report('equivalence-validation', dict(passed=True, apk_sha256=digest(APK.read_bytes()),
        source_apk_sha256=SOURCE_SHA, gameplay_and_supply_byte_identical=True,
        requested_updates_verified=10, changed_program_entries=sorted(changes),
        original_tests_reused=1186, evidence=evidence,
        note='1186项为版本调整前同字节玩法、补给和运行时的既有通过记录，本轮不重复计数为新执行。'))
    print('Exact gameplay and supply equivalence verified; all ten updates retained')


def publish():
    checksum = digest(APK.read_bytes())
    meta = json.loads((EVIDENCE / 'build-validation.json').read_text())
    assert checksum == meta['apk_sha256']
    for name in ('equivalence', 'lua', 'upgrade', 'runtime'):
        data = json.loads((EVIDENCE / (name + '-validation.json')).read_text())
        assert data['passed'] and data['apk_sha256'] == checksum
        assert not any(data.get(k) for k in ('failures','errors','skipped'))
    assert digest(SOURCE.read_bytes()) == SOURCE_SHA and digest(PREVIOUS.read_bytes()) == PREVIOUS_SHA
    backup = json.loads((EVIDENCE / 'backup.json').read_text())['files']
    for name, sha in backup.items():
        assert digest((ROOT / 'build' / name).read_bytes()) == sha
        assert digest((ARCHIVE / name).read_bytes()) == sha
    from analysis.tools.publish_v110_test_refresh import UPDATES
    note = WORK / '金箍棒ol测试版-v111使用说明.txt'
    note.write_text(f'''金箍棒ol测试版 v111 · 2026-11-10十项更新整合

版本号111，版本名称3.87-test.111.1，登录页显示v111。
本包由已验证的v110十项更新整合测试包调整版本而来，保留全部十项更新与最新版v111基础修复。

安装与存档
可直接覆盖同签名旧测试版v111及v110；先退出游戏并备份完整test-save-v106目录，不卸载、不清除应用数据。
包名com.sygame.jingubang.test106、测试签名、18776端口和files/test-save-v106存档目录保留，与正式版共存。
旧测试v111分发文件已备份至build/archive/v111-test-before-ten-updates-20261110。
APK不含玩家数据库；沿用养成补给修订108及一次性500张一阶九幽宝图领取标记，已领不重发、消耗后不补满。
等级卡只通过礼包码领取：10张7KIEGUOTCKQN；20张K1MJI3166RT4；50张CUTWP96BZCKY，各档每账号一次。

本次保留的十项更新
{UPDATES}

验证
玩法、奖励配置、补给及运行时代码与v110整合测试包逐字节一致，沿用其1186项通过记录，本轮未重复执行全量回归。
本轮对实际新APK重新核验签名、对齐、版本号、生成Lua及v111登录标识，执行2项运行时回归，并完成原测试v111临时存档升级和重启验证；存档养成、库存及补给领取标记保留。
本轮未重新进行Android装机验收。前一轮专用ARM32模拟器因Android系统服务崩溃未完成启动，新APK的设备验收仍未完成。
ARM32（armeabi-v7a），最低API21，设备须支持32位ARM应用。
证据：analysis/evidence/v111-test-version-20261110。
APK SHA-256：{checksum}
''')
    meta.update(verification=dict(prior_same_byte_tests=1186, runtime_tests_rerun=2,
        lua_verified=True, old_v111_save_upgrade_verified=True, device_verified=False))
    APK.with_suffix('.manifest.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n')
    archive = APK.with_suffix('.apk.zip')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in (APK, APK.with_suffix('.apk.sha256'), APK.with_suffix('.manifest.json'), note):
            z.write(p, p.name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and digest(z.read(APK.name)) == checksum
    artifacts = [APK, APK.with_suffix('.apk.sha256'), APK.with_suffix('.manifest.json'),
                 APK.with_suffix('.apk.idsig'), archive, note]
    for path in artifacts:
        target = ROOT / 'build' / path.name
        assert target.name in backup, target
        temporary = target.with_name(target.name + '.version-tmp')
        shutil.copy2(path, temporary)
        assert digest(temporary.read_bytes()) == digest(path.read_bytes())
        temporary.replace(target)
    assert digest(PREVIOUS.read_bytes()) == checksum
    report('published-release', dict(published=True, apk=str(PREVIOUS.relative_to(ROOT)),
        apk_sha256=checksum, version_code=111, original_backed_up=str(ARCHIVE.relative_to(ROOT)),
        artifacts=['build/' + p.name for p in artifacts], source_v110_unchanged=True,
        device_verified=False))
    doc = ROOT / 'docs/v111测试版20261110十项更新与版本调整.md'
    assert not doc.exists()
    doc.write_text('# v111测试版十项更新与版本调整\n\n'
        '已替换原测试版v111分发文件：[APK](../build/金箍棒ol测试版-v111.apk)、[ZIP](../build/金箍棒ol测试版-v111.apk.zip)。\n\n'
        + note.read_text())
    print(PREVIOUS)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['build','verify','publish'])
    globals()[parser.parse_args().mode]()
