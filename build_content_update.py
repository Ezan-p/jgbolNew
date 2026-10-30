"""Ship current logic on the pre-animation v102 shell, preserving update identity."""
import io
import json
from pathlib import Path
import re
import shutil
import zipfile

from build_channel360 import TOOLS, apktool, run
from build_offline import CERTIFICATE, PACKAGE, SIGNING_KEY, program_bundle, signer_certificate
from opening_patch.apply_patch import apply, sha256
from opening_patch.build_patch import build_delta

ROOT = Path(__file__).resolve().parent
WORK = ROOT / '.runtime/content-update-v104'
BASE = ROOT / 'build/金箍棒3.87-离线单机-arm32-更新v1.apk'
BASE_SHA256 = 'ca6665204b386bcdb0bae50015626b1ce817d64fdfb8c9596e1eaef04454d630'
SHELL_BASE = ROOT / 'build/金箍棒3.87-离线单机-arm32.apk'
SHELL_SHA256 = '87b6a851c3a4edf0ef79f098792f765b699966a4b967022efcbf21fb822c3c95'
OUTPUT = ROOT / 'build/金箍棒3.87-离线单机-arm32-v104.apk'


def build():
    if sha256(BASE) != BASE_SHA256:
        raise ValueError('Expected the preserved opening-video v103 APK')
    if OUTPUT.exists():
        raise ValueError('Output exists; archive the previous release before rebuilding')
    signer_certificate(BASE)
    if sha256(SHELL_BASE) != SHELL_SHA256:
        raise ValueError('Expected the preserved pre-animation v102 APK')
    signer_certificate(SHELL_BASE)
    WORK.mkdir(parents=True, exist_ok=True)
    # The full packer includes newly added Lua modules and regenerated injection.
    program, payload, overlay = program_bundle()
    with zipfile.ZipFile(SHELL_BASE) as source:
        old_program = zipfile.ZipFile(io.BytesIO(source.read('assets/offline/program.zip')))
        with old_program, zipfile.ZipFile(program) as current:
            old_names, new_names = set(old_program.namelist()), set(current.namelist())
            changed_program = sorted(name for name in old_names | new_names
                                     if name not in old_names or name not in new_names
                                     or old_program.read(name) != current.read(name))
            if any(name.startswith('client/') for name in changed_program):
                raise ValueError('Unexpected client overlay change')
        properties = source.read('assets/offline/build.properties').decode()
        runtime_hash = sha256_bytes(source.read('assets/offline/runtime.zip'))
        if 'runtime_sha256=' + runtime_hash not in properties:
            raise ValueError('Baseline runtime hash mismatch')
    decoded = WORK / 'decoded'
    framework = ROOT / '.runtime/tools/apktool-framework'
    apktool('d', '-f', '-s', '-p', framework, '-o', decoded, SHELL_BASE)
    metadata = decoded / 'apktool.yml'
    text = metadata.read_text()
    for name, value in (('versionCode', '104'), ('versionName', '3.87-offline.3-content')):
        text, count = re.subn(r'(?m)^  ' + name + r':.*$', '  ' + name + ': ' + value, text)
        if count != 1:
            raise ValueError('Missing version metadata: ' + name)
    metadata.write_text(text)
    shell = WORK / 'manifest-shell.apk'
    apktool('b', '-p', framework, '-o', shell, decoded)
    replacements = {
        'assets/offline/program.zip': program.read_bytes(),
        'assets/offline/build.properties': (
            f'program_sha256={sha256(program)}\nruntime_sha256={runtime_hash}\nversion_code=104\n').encode(),
    }
    with zipfile.ZipFile(shell) as compiled:
        replacements['AndroidManifest.xml'] = compiled.read('AndroidManifest.xml')
    unsigned = WORK / 'unsigned.apk'
    with zipfile.ZipFile(SHELL_BASE) as source, zipfile.ZipFile(unsigned, 'w') as dest:
        for entry in source.infolist():
            if not entry.filename.startswith('META-INF/'):
                dest.writestr(entry, replacements.get(entry.filename, source.read(entry)))
    aligned = WORK / 'aligned.apk'
    run(TOOLS / 'zipalign', '-f', '4', unsigned, aligned)
    run(TOOLS / 'apksigner', 'sign', '--ks', SIGNING_KEY, '--ks-key-alias', 'channel360',
        '--ks-pass', 'pass:local-test-only', '--out', OUTPUT, aligned)
    signer_certificate(OUTPUT)
    run(TOOLS / 'apksigner', 'verify', '--verbose', OUTPUT)
    run(TOOLS / 'zipalign', '-c', '4', OUTPUT)
    with zipfile.ZipFile(SHELL_BASE) as source, zipfile.ZipFile(OUTPUT) as target:
        assert target.testzip() is None
        names = lambda z: {n for n in z.namelist() if not n.startswith('META-INF/')}
        assert names(source) == names(target)
        changed = sorted(n for n in names(source) if source.read(n) != target.read(n))
        assert set(changed) == set(replacements), changed
    with zipfile.ZipFile(BASE) as source, zipfile.ZipFile(OUTPUT) as target:
        changed = sorted(n for n in names(source) if source.read(n) != target.read(n))
    package = WORK / 'package'
    package.mkdir(exist_ok=True)
    delta = build_delta(BASE, OUTPUT, package / 'content.patch')
    rebuilt = WORK / 'reconstructed.apk'
    rebuilt.unlink(missing_ok=True)
    apply(BASE, package / 'content.patch', rebuilt)
    assert sha256(rebuilt) == sha256(OUTPUT)
    signer_certificate(rebuilt)
    shutil.copy2(ROOT / 'opening_patch/apply_patch.py', package / 'apply_patch.py')
    instructions = '''金箍棒离线单机 v104：三项内容更新、移除开场动画（2026-10-29）

推荐直接将完整 v104 APK 复制到手机，覆盖安装。不要卸载旧版或清除数据。
同包名、同项目签名的离线 v102 / v103 可使用完整 APK 更新。
其他渠道包、电脑联机版的存档不自动迁入手机离线版。

此 ZIP 是电脑合成用差分补丁，不能直接在手机内导入。
需要 Python 3.8+ 和未修改的 v103 原 APK（通常名为“金箍棒3.87-离线单机-arm32-更新v1.apk”）。
在解压目录运行（原包路径按实际位置修改）：
python3 apply_patch.py "金箍棒3.87-离线单机-arm32-更新v1.apk" --patch content.patch --output "金箍棒3.87-离线单机-arm32-v104.apk"
脚本检查原包及输出 SHA256，不会覆盖已有文件。将合成 APK 复制到手机覆盖安装。

更新内容：
0. 移除 v103 开场动画补丁，恢复 v102 不播放开场动画的启动流程。
1. 日常扩至十一类任务，调整奖励；北京时间零点重置活跃度及宝箱。累计签到保留。
2. 神仙升级潜能按品质分段：一至五星分别为1/2、3/4、5/7、7/10、10/15点，40升41级起取后值；一至三星为推定值。
3. 界魂箱 1:1 兑换，支持一次使用 1–99 个。

程序与存档独立；补丁不包含玩家数据库，不删除、替换或初始化已有存档。
首次进入后，旧周累计活跃度迁为当天积分，同日已领奖标记保留；下日按新规则重置。
旧档潜能统一重建总额并迁移至版本3：先追扣剩余潜能，不足时按比例扣回已培养属性，缺额补齐；包含当前等级、最低转生周期、飞升与转生奖励。历史流水缺失时按此统一口径处理，保留迁移前数值和调整记录，重复读取不再扣补。
设备要求沿用原离线版（ARM32）；不改变系统兼容范围。
'''
    (package / '使用说明.txt').write_text(instructions, encoding='utf-8')
    report = dict(version_code=104, package=PACKAGE, certificate_sha256=CERTIFICATE,
                  shell_base_sha256=SHELL_SHA256, opening_animation=False,
                  base_sha256=delta['base_sha256'], target_sha256=delta['target_sha256'],
                  target_bytes=OUTPUT.stat().st_size, program_sha256=sha256(program),
                  runtime_sha256=runtime_hash, changed_apk_entries=changed,
                  changed_program_entries=changed_program, payload=payload,
                  client_overlay=overlay, player_database='files/save/game.sqlite3',
                  exact_reconstruction_verified=True,
                  delta_bytes=(package / 'content.patch').stat().st_size)
    OUTPUT.with_suffix('.manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    (package / '校验清单.json').write_text(json.dumps({k: v for k, v in report.items()
        if k not in ('payload', 'client_overlay')}, ensure_ascii=False, indent=2) + '\n')
    bundle = ROOT / 'build/金箍棒3.87-三项更新补丁-v103到v104.zip'
    with zipfile.ZipFile(bundle, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(package.iterdir()):
            archive.write(path, path.name)
    for path in (OUTPUT, bundle):
        path.with_suffix(path.suffix + '.sha256').write_text(sha256(path) + '  ' + path.name + '\n')
    (ROOT / 'build/v104更新说明.txt').write_text(instructions, encoding='utf-8')
    print(json.dumps(dict(apk=str(OUTPUT), patch=str(bundle), changed_program=changed_program,
                          apk_bytes=OUTPUT.stat().st_size, patch_bytes=bundle.stat().st_size),
                     ensure_ascii=False, indent=2))


def sha256_bytes(data):
    import hashlib
    return hashlib.sha256(data).hexdigest()


if __name__ == '__main__':
    build()
