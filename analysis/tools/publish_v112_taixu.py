"""Publish the verified v112 Taixu revision and archive the previous local release."""
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v112_taixu import WORK, EVIDENCE, OUTPUT, BASE, BASE_SHA, digest, report
from analysis.tools.publish_v112 import UPDATES

TAIXU = '''10. 幻境商店v5调整价格与限购。每份1件，以下为仙晶单价/当日上架限购：白虎、玄武、青龙精华各10/1000，四星灵器100/10，五星灵器1000/5，神装灵器2000/1，近古水晶50/20，上古水晶200/20，远古水晶500/5，太古水晶1000/3，神源水晶2000/1。每日六格、三种精华和近古水晶必上架，其余七种抽两种，原权重保留；当天已兑次数保留。
11. 血战最终排名奖励提高：第1名1500元宝、200圣母蟠桃、20000仙晶；第2—3名800/100/15000；第4—10名500/50/10000；第11—20名300/10/5000。所有阶段每次胜利另得100仙晶；已结算比赛不追溯补发，同周未结算使用新奖励。
12. 血战中途关闭增加确认：继续血战保留进度；确认退出按第20名结算300元宝、10圣母蟠桃、5000仙晶，成功后退出，本周不能再参赛。断线或关闭游戏保留未结算进度；未参赛分组页、其他组榜单、已结算榜单正常关闭。'''


def main():
    sha = digest(OUTPUT.read_bytes())
    records = {name: json.loads((EVIDENCE / (name + '.json')).read_text()) for name in (
        'build-validation','scope-validation','protocol-validation','lua-validation','payload-save-validation')}
    assert all(r['apk_sha256'] == sha for r in records.values())
    assert all(records[n]['passed'] for n in records if n != 'build-validation')
    protocol = records['protocol-validation']
    assert protocol['failures'] == protocol['errors'] == protocol['skipped'] == 0
    assert records['lua-validation']['taixu_exit_confirmation']
    assert records['payload-save-validation']['previous_v112_to_new_v112_all_tables_equal']
    assert digest(BASE.read_bytes()) == BASE_SHA
    public = ROOT / 'build'
    archive = public / 'archive/v112-before-taixu-20261113'
    canonical = public / '金箍棒ol离线正式版v112.apk'
    assert digest(canonical.read_bytes()) == BASE_SHA, 'Unexpected current v112 release'
    assert not (public / OUTPUT.name).exists()
    archive.mkdir(parents=True, exist_ok=False)
    old_files = [p for p in public.glob('金箍棒ol离线正式版v112*') if p.is_file()]
    old_files.append(public / 'v112更新说明.txt')
    preserved = {}
    for path in old_files:
        shutil.copy2(path, archive / path.name)
        preserved[path.name] = digest(path.read_bytes())
    doc = ROOT / 'docs/v112内容整合与验证说明.md'
    shutil.copy2(doc, archive / doc.name)
    note = WORK / 'v112三项更新说明.txt'
    verification = (f"实际APK内{protocol['tests']}项不同回归通过，零失败、零错误、零跳过。"
        '完整生成Lua编译、v112登录标识、五阶段退出确认/取消/末名结算、商店令牌回归通过。'
        'v111→新v112→重启存档迁移通过；旧v112→新v112→重启所有账号数据表逐值一致。'
        '签名、对齐、载荷哈希、十二组更新范围核对通过。')
    if protocol['environment_recheck_test_ids']:
        verification += '本机端口受沙箱限制的项目已在允许回环端口的环境中复测通过，首次失败及复测记录均保留。'
    limitation = '本次未进行Android装机、物理手机或光速虚拟机实机验收；此前专用Android QA环境的系统异常记录不作为本包装机结果。'
    note.write_text(f'''金箍棒ol离线正式版 v112 · 三项更新 · 2026-11-13

版本号112；版本名称3.87-offline.12；登录页v112。本批次以“三项更新-20261113”文件名和下方SHA-256区分。
沿用正式包名com.sygame.jingubang.p360、原签名、18770端口和files/save存档目录。
支持覆盖同签名正式v112/v111/v110。先退出游戏并备份完整save目录，覆盖安装；不要卸载或清除应用数据。
ARM32（armeabi-v7a），最低Android API21。APK不含玩家数据库和测试版自动补给，原100个兑换码及领取记录保留。

保留原v112九组更新，并追加三项
{UPDATES}
{TAIXU}

存档
幻境商店按道具ID保留当天已兑次数；血战保留同周阶段、名单、积分、血量及次数，已发奖励不重复发放。
九幽商店按v17迁移；九重商会保留已兑次数；已开始宝图保留旧盘；八卦助阵ID绑定迁移沿用原v112。

验证
{verification}
{limitation}

APK SHA-256：{sha}
证据：analysis/evidence/v112-taixu-20261113。
原v112及其分发附件备份在build/archive/v112-before-taixu-20261113。
''')
    meta = records['build-validation']
    meta['verification'] = dict(protocol_tests=protocol['tests'],lua_verified=True,
        taixu_exit_confirmation_verified=True,old_save_compatibility_verified=True,
        device_verified=False,physical_device_tested=False)
    OUTPUT.with_suffix('.manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    distribution = WORK / (OUTPUT.name + '.zip')
    with zipfile.ZipFile(distribution,'w',zipfile.ZIP_DEFLATED) as z:
        for path in (OUTPUT,OUTPUT.with_suffix('.apk.sha256'),OUTPUT.with_suffix('.manifest.json'),note):
            z.write(path,path.name)
    with zipfile.ZipFile(distribution) as z:
        assert z.testzip() is None and digest(z.read(OUTPUT.name)) == sha
    for path in (OUTPUT,OUTPUT.with_suffix('.apk.sha256'),OUTPUT.with_suffix('.manifest.json'),
                 OUTPUT.with_suffix('.apk.idsig'),distribution,note):
        if path.exists():
            shutil.copy2(path,public/path.name)
    # The default download also points to the latest verified v112 revision.
    shutil.copy2(OUTPUT,canonical)
    shutil.copy2(OUTPUT.with_suffix('.apk.idsig'),canonical.with_suffix('.apk.idsig'))
    canonical.with_suffix('.apk.sha256').write_text(sha+'  '+canonical.name+'\n')
    shutil.copy2(OUTPUT.with_suffix('.manifest.json'),canonical.with_suffix('.manifest.json'))
    shutil.copy2(distribution,canonical.with_suffix('.apk.zip'))
    shutil.copy2(note,public/'v112更新说明.txt')
    assert digest(canonical.read_bytes()) == digest((public/OUTPUT.name).read_bytes()) == sha
    assert all(digest((archive/name).read_bytes())==h for name,h in preserved.items())
    for path in Path('/private/tmp').glob('jgbol-v112-taixu-*.log'):
        shutil.copy2(path,EVIDENCE/path.name.removeprefix('jgbol-v112-taixu-'))
    doc.write_text(f'''# 离线正式版v112内容整合与验证说明

更新日期：2026-11-13。版本号112，版本名称`3.87-offline.12`，登录页显示v112。当前为“三项更新-20261113”批次。

下载：[正式APK](../build/{OUTPUT.name})、[ZIP分发包](../build/{distribution.name})、[更新说明](../build/{note.name})。[默认v112下载](../build/金箍棒ol离线正式版v112.apk)已同步为相同APK。

## 更新范围

保留原正式v112九组更新，追加幻境商店、血战奖励及退出流程，共十二组。

{UPDATES}
{TAIXU}

## 安装与存档

沿用正式包名、原签名与`files/save`目录，可覆盖同签名正式v112/v111/v110。先退出游戏并备份完整save目录，直接覆盖安装，不卸载、不清除数据。APK不含玩家数据库和测试版自动补给，原100个兑换码保留。

幻境商店保留当天已兑次数；同周未结算血战保留进度并使用新奖励，已结算不重复发奖。九幽商店、九重商会、旧宝图及八卦助阵迁移沿用原v112规则。

本批次相对首批v112仅修改五份太虚源码/配置及生成的客户端Lua、载荷清单；APK仅替换程序载荷和载荷校验信息。Android版本清单、原生引擎、Java、游戏资源和Python运行时逐字节保留。

## 验证结果

{verification}

{limitation}

APK SHA-256：`{sha}`。

本批次[构建与验证证据](../analysis/evidence/v112-taixu-20261113)，脚本为`build_v112_taixu.py`、`verify_v112_taixu.py`及`publish_v112_taixu.py`（均位于`analysis/tools/`）。首批v112的APK、附件及说明保存在[历史目录](../build/archive/v112-before-taixu-20261113)，原[首批验证记录](../analysis/evidence/v112-20261113)保留。
''')
    report('published-release',dict(published=True,apk_sha256=sha,apk_bytes=canonical.stat().st_size,
        version_code=112,version_name='3.87-offline.12',feature_groups=12,
        packaged_protocol_tests=protocol['tests'],device_verified=False,prior_v112_archived=True,
        archive_sha256=preserved,downloads=[str((public/p.name).relative_to(ROOT)) for p in (OUTPUT,distribution)]))
    print('Published',public/OUTPUT.name,sha)


if __name__ == '__main__':
    main()
