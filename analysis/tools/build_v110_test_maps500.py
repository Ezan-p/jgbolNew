"""Add a once-only treasure-map allowance to the exact published v110 test APK."""
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v106_test import KEY, certificate, digest
from build_channel360 import TOOLS, run
from offline_android.pack_payload import verify_payload

BASE = ROOT / 'build/金箍棒ol测试版-v110.apk'
BASE_SHA = 'a3c53a02507ee7fe20913575293a907a8fee3cd40fe5298bb902ed66944f2d3c'
WORK = ROOT / '.runtime/v110-test-maps500'
EVIDENCE = ROOT / 'analysis/evidence/v110_test_maps500'
APK = WORK / '金箍棒ol测试版-v110-九幽宝图500.apk'


def build():
    assert digest(BASE.read_bytes()) == BASE_SHA
    assert not APK.exists(), 'Refusing to replace a built candidate'
    WORK.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(BASE) as base:
        with zipfile.ZipFile(io.BytesIO(base.read('assets/offline/program.zip'))) as before:
            entries = {n: before.read(n) for n in before.namelist()}
        original = dict(entries)
        name = 'offline_android/test_edition_v110.py'
        entries[name] = (ROOT / name).read_bytes()
        backend = entries['offline_android/backend.py']
        old = b'from offline_android.test_edition_v108 import fixed_accounts_class'
        assert backend.count(old) == 1
        entries['offline_android/backend.py'] = backend.replace(old,
            b'from offline_android.test_edition_v110 import fixed_accounts_class')
        changed = sorted(n for n in entries if entries[n] != original.get(n))
        assert changed == ['offline_android/backend.py', name]
        manifest = json.loads(entries['payload-manifest.json'])
        indexed = {r['path']: r for r in manifest['files']}
        for n in changed:
            indexed[n] = dict(path=n, size=len(entries[n]), sha256=digest(entries[n]), source='test-maps500')
        manifest['files'] = sorted(indexed.values(), key=lambda r: r['path'])
        manifest['bundle_id'] = digest(json.dumps(manifest['files'], sort_keys=True, separators=(',', ':')).encode())
        entries['payload-manifest.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as out:
            for n, data in entries.items():
                assert Path(n).suffix not in ('.db', '.sqlite3', '.pyc')
                out.writestr(n, data)
        program = buffer.getvalue()
        with zipfile.ZipFile(io.BytesIO(program)) as p:
            p.extractall(WORK / 'program')
        verify_payload(WORK / 'program')
        properties = base.read('assets/offline/build.properties')
        previous_program_hash = digest(base.read('assets/offline/program.zip')).encode()
        assert properties.count(previous_program_hash) == 1
        properties = properties.replace(previous_program_hash, digest(program).encode())
        replacements = {'assets/offline/program.zip': program, 'assets/offline/build.properties': properties}
        with zipfile.ZipFile(WORK / 'unsigned.apk', 'w') as out:
            for entry in base.infolist():
                if not entry.filename.startswith('META-INF/'):
                    out.writestr(entry, replacements.get(entry.filename, base.read(entry)))
    run(TOOLS / 'zipalign', '-f', '4', WORK / 'unsigned.apk', WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'sign', '--ks', KEY, '--ks-key-alias', 'test106',
        '--ks-pass', 'pass:test-edition-only', '--out', APK, WORK / 'aligned.apk')
    run(TOOLS / 'apksigner', 'verify', '--verbose', APK)
    run(TOOLS / 'zipalign', '-c', '4', APK)
    assert certificate(APK) == certificate(BASE)
    with zipfile.ZipFile(BASE) as base, zipfile.ZipFile(APK) as result:
        assert result.testzip() is None
        actual = sorted(n for n in base.namelist() if not n.startswith('META-INF/') and base.read(n) != result.read(n))
        assert actual == sorted(replacements)
    from offline_android.test_edition_v110 import MAP_ITEMS, MARKER
    report = dict(apk=APK.name, apk_sha256=digest(APK.read_bytes()), apk_bytes=APK.stat().st_size,
        baseline=BASE.name, baseline_sha256=BASE_SHA, version_code=110,
        version_name='3.87-test.110.1', package='com.sygame.jingubang.test106',
        certificate_sha256=certificate(APK), program_sha256=digest(program),
        save_path='files/test-save-v106/game.sqlite3',
        grant_items=dict(MAP_ITEMS), grant_total=sum(n for _, n in MAP_ITEMS), grant_marker=MARKER,
        contains_player_database=False, android_shell_unchanged=True,
        changed_apk_entries=actual, changed_program_entries=changed + ['payload-manifest.json'])
    assert report['grant_total'] == 500
    text = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    (EVIDENCE / 'build-validation.json').write_text(text)
    APK.with_suffix('.manifest.json').write_text(text)
    APK.with_suffix('.apk.sha256').write_text(report['apk_sha256'] + '  ' + APK.name + '\n')
    print(text)


def publish():
    meta = json.loads((EVIDENCE / 'build-validation.json').read_text())
    tests = json.loads((EVIDENCE / 'grant-validation.json').read_text())
    assert tests['passed'] and not tests['skipped'] and tests['apk_sha256'] == meta['apk_sha256'] == digest(APK.read_bytes())
    assert digest(BASE.read_bytes()) == BASE_SHA
    assert (ROOT / 'offline_android/test_edition_v110.py').read_bytes() == (WORK / 'program/offline_android/test_edition_v110.py').read_bytes()
    output = ROOT / 'build' / APK.name
    assert not output.exists(), 'Published APK already exists'
    for suffix in ('.apk', '.manifest.json', '.apk.sha256', '.apk.idsig'):
        shutil.copy2(APK.with_suffix(suffix), output.with_suffix(suffix))
    note = output.with_name(output.stem + '使用说明.txt')
    allocation = '、'.join(f'{int(tid)-1430}阶×{count}' for tid, count in meta['grant_items'].items())
    note.write_text(f'金箍棒ol测试版v110 九幽宝图补给更新\n\n新增：九幽宝图共500张（{allocation}）。\n'
        '覆盖安装原v110测试版后，首次启动向固定测试账号一次性追加，不覆盖已有数量。新档也会领取。\n'
        '领取后重启、重装覆盖或消耗宝图均不会重复补发；原v108养成补给不重发。\n'
        '沿用测试版包名、签名、版本号110和test-save-v106存档目录。请勿卸载或清除数据。\n'
        '本次只更新测试补给入口与载荷校验；玩法、奖池、概率、Java、原生库和资源均与此前v110测试包一致。\n'
        f'本轮包内验证：{tests["tests"]}项通过，无失败、错误或跳过。已验证追加数量、保存失败回滚、消耗后重启不补发、旧补给不重发及新档初始化。\n'
        '此前v110的525项回归作为未改动玩法的基线证据，本次未重复全量运行。未完成安卓设备装机验收。\n'
        '安装包不携带玩家数据库；本次未直接编辑手机或其他游戏实例中的存档。\n'
        f'APK SHA-256：{meta["apk_sha256"]}\n')
    with zipfile.ZipFile(output.with_suffix('.apk.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for p in (output, note, output.with_suffix('.apk.sha256'), output.with_suffix('.manifest.json')):
            z.write(p, p.name)
    with zipfile.ZipFile(output.with_suffix('.apk.zip')) as z:
        assert z.testzip() is None and digest(z.read(output.name)) == meta['apk_sha256']
    (EVIDENCE / 'published-release.json').write_text(json.dumps(dict(published=True,
        apk=str(output.relative_to(ROOT)), apk_sha256=meta['apk_sha256'], tests=tests['tests']), ensure_ascii=False, indent=2)+'\n')
    print(output)


if __name__ == '__main__':
    globals()[sys.argv[1]]()
