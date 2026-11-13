"""Publish exact verified v112 bytes locally while preserving all older APKs."""
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v112 import WORK, EVIDENCE, OUTPUT, BASE, BASE_SHA, VERSION_NAME, digest, report

UPDATES = '''1. 九幽宝图改为v9十二格养成奖池，加入魂晶、三类经验丹和精魄石，重配各阶数量及概率；已开始旧盘保留。
2. 九幽冥仙恢复原表属性和初始技能；挂机魂晶为旧版6倍、首胜魂晶为旧版2倍，已领取首胜不补差额。
3. 九幽商店v17：三种精华常驻，20魂晶/个、每天各限500个；其他五种材料抽三种。移除精魄石、神装灵器和神源水晶；补天石1000魂晶/个、每天限10个。
4. 普通粽子各0.25%产出五星粽子；五星粽子支持批量开启，1000元宝40%、大传世金卡30%、武器/防具各9%、法宝/被动各6%，移除大乘经。
5. 蛋莲月饼、五仁粽子移除仙币，仙晶改为100个、6.5%概率。
6. 九重商会王母魂魄和五法界魂箱常驻，其余商品加权不重复抽四种，低级单件权重4、高级单件权重1。
7. 八卦40级开放前两位，正后六位60级后消耗材料依次开启；正逆八卦助阵一对一绑定神仙ID，换位跟随、下阵暂停，修复后同步封神榜派生数据。
8. 仙盟捐献每1元宝获得10贡献，同步贡献余额、成员缓存和到账提示。
9. 修复等级卡升级奖励弹窗；1000魂元神石祈福固定奖励100元宝；仙灵店铺部分商品降价并移除精魄石。'''


def main():
    sha = digest(OUTPUT.read_bytes())
    records = {name: json.loads((EVIDENCE / (name + '.json')).read_text()) for name in (
        'build-validation', 'scope-validation', 'protocol-validation', 'lua-validation',
        'payload-save-validation', 'device-validation')}
    assert all(r['apk_sha256'] == sha for r in records.values())
    assert all(records[n]['passed'] for n in ('scope-validation', 'protocol-validation',
                                             'lua-validation', 'payload-save-validation'))
    protocol, device = records['protocol-validation'], records['device-validation']
    assert protocol['failures'] == protocol['errors'] == protocol['skipped'] == 0
    assert digest(BASE.read_bytes()) == BASE_SHA
    assert records['payload-save-validation']['all_tables_equal_after_restart']
    preserved = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in (ROOT / 'build').glob('*.apk')}
    destination = ROOT / 'build' / OUTPUT.name
    assert not destination.exists(), 'Do not overwrite an existing released v112'
    if device['passed']:
        device_text = ('独立Android 6 ARM32 QA模拟器v111→v112覆盖安装通过，安装前后完整save目录逐字节一致，'
            '回读安装APK的SHA-256与候选一致，新程序及原生引擎启动就绪。')
        device_text += ('登录画面经截图人工核对显示v112。' if device.get('startup_ui_verified')
                        else '登录画面尚未完成截图人工验收。')
    else:
        device_text = '本轮Android装机验收未完成：' + device.get('error', device['status']) + '。'
    device_text += '未完成物理手机、光速虚拟机和各玩法逐项触摸验收。'
    note = WORK / 'v112更新说明.txt'
    note.write_text(f'''金箍棒ol离线正式版 v112 · 2026-11-13

版本号112；版本名称{VERSION_NAME}；登录页v112。
沿用正式包名com.sygame.jingubang.p360、原签名、18770端口和files/save存档目录。
可覆盖安装同签名正式v111及v110。先退出游戏，备份完整save目录，再覆盖安装；不要卸载或清除应用数据。
ARM32（armeabi-v7a），最低Android API21；设备须支持32位ARM应用。
安装包不含玩家数据库或测试版自动补给；保留原正式版100个兑换码及已有领取记录。

相对于最新正式v111安装包的更新
{UPDATES}

存档迁移
已有道具、养成和货币保留；九幽商店首次访问按v17刷新货架和限购。
九重商会按商品身份保留已兑次数；旧宝图已开始奖盘保留。
八卦旧目标首次按原阵位解析为神仙ID，重复目标按正位到逆位顺序保留首项；已有开位及培养进度保留。
重复助阵清理后当前战力可能变化，历史最高战力保留。

验证
实际APK内{protocol['tests']}项不同玩法、奖励、协议、客户端和运行时回归通过，零失败、零错误、零跳过。
完整生成Lua编译及v112登录标识验证通过；旧v111历史QA账号副本升级、重启验证通过。
APK签名、对齐、完整性、源码冻结哈希和九项更新范围核对通过。
{device_text}

APK SHA-256：{sha}
证据：analysis/evidence/v112-20261113。
旧正式v111及其他安装包保持原文件不变。
''')
    meta = records['build-validation']
    meta['verification'] = dict(protocol_tests=protocol['tests'], lua_verified=True,
        old_save_compatibility_verified=True, device_verified=device['passed'],
        startup_ui_verified=device.get('startup_ui_verified', False), physical_device_tested=False)
    OUTPUT.with_suffix('.manifest.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n')
    distribution = WORK / (OUTPUT.name + '.zip')
    with zipfile.ZipFile(distribution, 'w', zipfile.ZIP_DEFLATED) as z:
        for path in (OUTPUT, OUTPUT.with_suffix('.apk.sha256'), OUTPUT.with_suffix('.manifest.json'), note):
            z.write(path, path.name)
    with zipfile.ZipFile(distribution) as z:
        assert z.testzip() is None and digest(z.read(OUTPUT.name)) == sha
    for path in (OUTPUT, OUTPUT.with_suffix('.apk.sha256'), OUTPUT.with_suffix('.manifest.json'),
                 OUTPUT.with_suffix('.apk.idsig'), distribution, note):
        if path.exists():
            shutil.copy2(path, ROOT / 'build' / path.name)
    assert digest(destination.read_bytes()) == sha
    assert all(digest((ROOT / name).read_bytes()) == h for name, h in preserved.items())
    document = ROOT / 'docs/v112内容整合与验证说明.md'
    bullets = '\n'.join(UPDATES.splitlines())
    document.write_text(f'''# 离线正式版v112内容整合与验证说明

发布日期：2026-11-13。版本号112，版本名称`{VERSION_NAME}`，登录页显示v112。

下载：[正式APK](../build/{OUTPUT.name})、[ZIP分发包](../build/{distribution.name})、[更新说明](../build/{note.name})。

## 更新范围

基于11月10日最新正式v111（三项追加更新版），整合下列九组工作区更新。

{bullets}

## 安装与存档

沿用正式包名、原签名与`files/save`目录，可覆盖同签名正式v111/v110。先退出游戏并备份完整save目录，直接覆盖安装，不卸载、不清除数据。APK不含玩家数据库和测试版自动补给，原100个兑换码保留。

九幽商店升级刷新货架及限购；九重商会保留已兑次数；已开始宝图保留旧盘。助阵迁移新增神仙ID绑定，清理重复目标，已有开位、培养和库存保留；历史最高战力保留。

仅替换Android版本清单、程序载荷与载荷校验信息；原生引擎、Java、游戏资源和Python运行时沿用最新v111字节。全部源码在构建前冻结，回归使用实际APK内模块。

## 验证结果

{protocol['tests']}项不同用例最终通过，零失败、零错误、零跳过。首次测试因缺少开发辅助脚本、原版证据或沙箱禁止本机端口而未通过的记录保留；一条旧捐献断言仍期待1贡献，已按新规则修正为10贡献。补齐环境及修正旧断言后使用同一APK逐项复测，合并时按用例ID去重。完整Lua编译、登录v112标识、九幽输入、节日批量使用及战报回归通过。

历史QA存档中的两个账号经v111→v112→重启验证，既有账号字段和其他数据表保留，仅新增预期的助阵ID绑定字段，重启后所有表逐值一致；原QA存档未改动。

{device_text}

APK SHA-256：`{sha}`。

构建、范围、回归、Lua、存档与装机证据见[验证目录](../analysis/evidence/v112-20261113)。构建脚本`analysis/tools/build_v112.py`，验证脚本`verify_v112.py`及`verify_v112_device.py`，本地分发脚本`publish_v112.py`。
''')
    for name in ('build', 'lua', 'save', 'device', 'tests-0', 'tests-1', 'tests-2', 'recheck'):
        log = Path('/private/tmp') / ('jgbol-v112-' + name + '.log')
        if log.exists():
            shutil.copy2(log, EVIDENCE / (name + '.log'))
    report('published-release', dict(published=True, apk_sha256=sha, apk_bytes=destination.stat().st_size,
        version_code=112, version_name=VERSION_NAME, package=meta['package'],
        downloads=[str(p.relative_to(ROOT)) for p in (destination, ROOT / 'build' / distribution.name)],
        feature_groups=9, packaged_protocol_tests=protocol['tests'], old_save_compatibility_verified=True,
        device_verified=device['passed'], startup_ui_verified=device.get('startup_ui_verified', False),
        physical_device_tested=False, prior_apks_preserved=True))
    print('Published', destination, sha)


if __name__ == '__main__':
    main()
