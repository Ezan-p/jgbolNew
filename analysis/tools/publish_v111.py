"""Publish the tested v111 APK without replacing the preserved official v110."""
import json
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v111 import BASE, BASE_SHA, OUTPUT, WORK, EVIDENCE, digest, source_check, report

NOTES = '''金箍棒ol离线正式版 v111

基于最新正式版 v110 构建。版本号111，版本名称3.87-offline.11。
沿用原包名、项目签名与 files/save 存档目录，支持覆盖安装同签名v110。
更新前请备份完整save目录；直接覆盖安装，不要卸载旧版或清除应用数据。
安装包不包含玩家存档。原正式版v110保留。

本版更新：
1. 九幽商店：11种材料按用途分为每份800—2000魂晶，数量、限购和上架权重不变。
2. 九幽宝图v4：12格加权奖盘；三种精华每阶10个、五法界魂箱每阶1个，移除经验密卷和仙缘果，加入两个圣母蟠桃格（首抽合计16%）。每张最多5抽，首抽不扣元宝，续抽每次20元宝；支持1—99张批量。已开始的旧盘保持原规则。
3. 猎魂之地：正逆塔首领及护卫四维在上一版基础上翻倍；游历按地图产出100/200/350/500魂力，四塔每分钟产出10/20/40/80魂力；守塔采用更高等级完整阵容；翻牌新增精魄石10/20个，合计60%。北京时间每周一零点重置双塔、地图、待翻牌并结算周榜；魂力余额、背包和已开启养成保留，未翻牌需换周前领取。
4. 仙盟秘境：每层5次探宝、三层累计15次，修复结算次数显示；八人敌阵按主角等级计算战力，后两层为首层2.2倍、5倍。
5. 太虚血战：80—99级组加入六档极高战力NPC各一名；已开赛名单保留，新赛程启用。
6. 精魄愈合：修复回血后额外播放零伤害普攻，保留回血、特效和真实攻击时序。
7. 天道轮回：修复叠加装备轮回报错，筛除不可回收目标，避免一键选择导致整批失败；原有合法装备返还规则保留。
8. 蟠桃大会：三名首领的群攻触发概率调整为20%，仅作用于本活动。
9. 游戏时钟：接入客户端连续计时与前台恢复校准，允许符合条件的跨重启离线间隔在30天内完整补算。异常系统日期差暂缓补算，不新增永久封锁；原有封锁和存档完整性保护保留。纯离线无法证明系统时间真实，30天是补时策略边界。

排除内容：九重天宫分层特殊商品、天星商品调价等九重天专属更改未纳入；九重天专属代码与配置逐字节保持正式v110版本。通用时钟修复仍作用于全游戏。

验证：实际安装包内玩法回归、Lua补丁编译与播放回归、离线运行时和旧存档副本升级。详细数量、哈希和证据见同名manifest.json及analysis/evidence/v111。
设备验收状态：见下方本次验证结果。物理手机或光速虚拟机逐玩法点击验收尚未完成。
'''


def main():
    checksum = digest(OUTPUT.read_bytes())
    source_check()
    assert digest(BASE.read_bytes()) == BASE_SHA
    records = {}
    for name in ('build-validation', 'protocol-validation', 'lua-validation',
                 'payload-save-validation', 'release-scope-validation'):
        data = json.loads((EVIDENCE / (name + '.json')).read_text())
        assert data['apk_sha256'] == checksum, name
        if name != 'build-validation':
            assert data['passed'] and not data.get('skipped', 0), name
        records[name] = data
    device_path = EVIDENCE / 'device-validation.json'
    device_ok = False
    if device_path.exists():
        device = json.loads(device_path.read_text())
        assert device['apk_sha256'] == checksum and device['passed']
        assert device['startup_branding_v111_verified']
        device_ok = True
        device_note = '专用ARM32 QA模拟器覆盖安装与原生冷启动验证通过。\n'
    else:
        unavailable = json.loads((EVIDENCE / 'device-environment-unavailable.json').read_text())
        assert unavailable['apk_sha256'] == checksum and unavailable['v111_installed'] is False
        device_note = ('本次未完成设备覆盖安装及冷启动验收：专用QA模拟器在安装v111前发生Android系统启动循环，'
                       '软件图形模式重试时模拟器进程退出。该限制不能由包内测试替代，详细日志已保留。\n')
    assert '\nOK\n' in (EVIDENCE / 'host-runtime-tests.log').read_text()
    for name in ('native-retry-validation', 'native-guard-validation'):
        data = json.loads((EVIDENCE / (name + '.json')).read_text())
        assert data['passed'] and data['native_source_sha256'] == records['build-validation']['native_source_sha256']
    metadata = records['build-validation']
    metadata.update(device_tested=device_ok, qa_upgrade_from_v110_verified=device_ok,
                    qa_cold_start_verified=device_ok, save_migration_verified=True,
                    protocol_tests=records['protocol-validation']['tests'],
                    evidence='analysis/evidence/v111', physical_device_tested=False,
                    device_validation_note=device_note.strip())
    OUTPUT.with_suffix('.manifest.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')
    notes = WORK / 'v111更新说明.txt'
    notes.write_text(NOTES + '\n本次验证结果：\n'
                     + str(metadata['protocol_tests']) + '项包内回归通过，零失败、零跳过；'
                     + '23项离线运行时测试、包内Lua及原生加载器检查、旧存档副本升级检查通过。\n'
                     + device_note)
    archive = WORK / (OUTPUT.name + '.zip')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for path in (OUTPUT, notes, OUTPUT.with_suffix('.apk.sha256'), OUTPUT.with_suffix('.manifest.json')):
            z.write(path, path.name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and digest(z.read(OUTPUT.name)) == checksum
    artifacts = [OUTPUT, OUTPUT.with_suffix('.apk.sha256'), OUTPUT.with_suffix('.manifest.json'), notes, archive]
    if OUTPUT.with_suffix('.apk.idsig').exists():
        artifacts.append(OUTPUT.with_suffix('.apk.idsig'))
    for source in artifacts:
        destination = ROOT / 'build' / source.name
        assert not destination.exists(), destination
    for source in artifacts:
        destination = ROOT / 'build' / source.name
        temporary = destination.with_name(destination.name + '.tmp')
        shutil.copy2(source, temporary)
        assert digest(source.read_bytes()) == digest(temporary.read_bytes())
        temporary.replace(destination)
    assert digest(BASE.read_bytes()) == BASE_SHA
    report('published-release', dict(published=True, apk_sha256=checksum, version_code=111,
        artifacts=['build/' + p.name for p in artifacts], baseline_v110_preserved=True,
        protocol_tests=metadata['protocol_tests'], device_tested=device_ok, physical_device_tested=False))
    print(ROOT / 'build' / OUTPUT.name)


if __name__ == '__main__':
    main()
