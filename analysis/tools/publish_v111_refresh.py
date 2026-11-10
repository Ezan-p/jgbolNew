"""Publish refreshed v111 only after exact-package validation; preserve original."""
import json
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v111_refresh import (
    WORK, EVIDENCE, ARCHIVE, OUTPUT, BASE, BASE_SHA, NAME, digest, report, source_check)

NOTES = '''金箍棒ol离线正式版 v111 · 2026-11-10整合更新

版本号111，版本名称3.87-offline.11。原包名、签名、files/save目录不变。
支持覆盖安装同签名旧v111及v110。更新前退出游戏并备份完整同代save目录，
直接覆盖安装，不卸载、不清除应用数据。APK不含玩家存档。
旧v111完整分发文件已保存在build/archive/v111-before-refresh-20261110。

相对2026-11-09正式v111的更新：
1. 关闭救悟空／十万猴急入口及新增活动奖励、充值赠珠和特权邮件；保留已有道具、邮件和存档。
2. 联网校准北京时间：多源HTTPS确认，启动、前台恢复及运行期间校时；断网同次启动继续计时，跨设备重启收益待联网确认。可信联网补时不受旧30天上限限制；未来结算记录不重复刷新，联网确认的改时异常进入原TIME-001保护，既有处罚不自动解除。业务和存档仍在本机，校时不上传账号或存档。
3. 灵宠仙地三个任务目标分别记录两种模式，每日共六种挑战；先用3次普通额度，再用3次付费额度，付费100元宝／次。修复第六次挑战阻挡、已挑战提示、跨日页面和奖励展示。
4. 灵兽试炼每次满血挑战，必须击杀首领才通关；回合耗尽未击杀判负，失败伤害不累计，保留旧档已确认通关和领奖进度。
5. 试炼点赞每次20元宝，每日3次，每次四维增加5%，最多15%；增加扣费确认及次数、增益、余额和按钮状态同步。
6. 试炼每通关并领取一层奖励增加3次领养，四层累计12次；领养仅周六、周日开放，领奖后即时同步次数。
7. 宠物商店固定下品符、中品符、驯养丹三格，另外从上品符、神品符、妖王丹、仙气灵、神元精、驯养宝箱中加权抽三种，每天六格不重复。驯养丹每份5颗限购3份，升星材料各5份，宝箱1份；镇魂符额度随累计声望增长。旧页面不能误买跨日新商品。
8. 驯养宝箱每箱独立抽取10／15／20颗驯养丹，概率30%／50%／20%，每批1—15箱。修复开箱依赖其他活动初始化及背包同步。
9. 仙盟宝库候选改为16项、每天8格，重配商品数量、贡献价格和限购；新增精华礼包、驯养宝箱、乾坤符箓礼包、圣母蟠桃，银两10万／50万两档，移除直接精魄石和三种精华；保留已用购买额度。
10. 西天取经刷新仅在第2—5档独立随机，概率60%／25%／12%／3%，可重复、可降档、无保底；最高档停止刷新，更新界面说明。
11. 洞府红尘劫改为60级三人／100级五人固定阵容，预览战力305598／1748010，预览与实战一致。第一阶段三座主建筑11级，第二阶段不额外检查建筑等级；修复升级后阶段刷新与满规模入口。
12. 洞府常驻店为仙木100／修炼果5／宠物转换丹1／驯养丹5，价格1000／1000／5000／1000仙币，限购20／10／1／10份。限时池11项每日加权抽3项，包含天仙令1个（2000仙币、限购1、低权重）；下架蟠桃及限时升星材料。
13. 宠物融合预览与实际星级保底一致，1—6星最低品质3、7—9星最低品质4；幻化成长限制在目标类型、品质、星级范围，修正越界记忆，避免九星重复加成。隐藏未实现的洞府宠物技能按钮。
14. 中秋、端午每周一北京时间0点刷新制作累计与赠料资格；各活动剩余五种材料含锁定材料合计按10:1邮件换普通蟠桃，向下取整并清空尾数；成品与已获奖励保留。旧档首次迁移不立即回收，界面及在线跨周同步更新。
15. 东海撒网新增菩提祖师魂魄1、五法界魂箱1、东华大帝魂魄1，各1%；小包子17%降至14%；移除概率预览弹窗和触摸热区。
16. 九幽宝图v5：所有奖品每阶1个，第二个蟠桃格改四星灵器；首抽三种精华各17%，四星灵器／圣母蟠桃／轮回舍利各10%，界魂箱9%，五星灵器／太古水晶／补天石／明心石／无上石各2%。旧已开始奖盘保留。
17. 猎魂翻牌初始权重为精魄石10个20%、20个15%、黄色精魄55%、紫碎片8%、紫精魄2%；普通5牌最多2张精魄石、冥界3牌最多1张，达到上限后重分配其他类别权重并打乱牌序。扫荡增加精魄石5个。
18. 太虚血战排名元宝／圣母蟠桃／仙晶：第1名1000／200／10000，第2—3名500／100／8000，第4—10名300／50／5000，第11—20名150／10／3000。
19. 精华礼包采用11月10日最终规则：三种精华各1/3，数量20／50／100个，概率80%／15%／5%；批量每包独立抽取，替代中间版本的固定10个。
20. 不可堆叠物品按独立ID发放；旧叠加装备拆分，原件保留养成与装备关联，额外件恢复未养成状态并保留锁定。
21. 九幽商店采用v11最终规则：三种精华每份100个、1000魂晶、每种每日5份，上架日最多500个；其余8种商品及上架权重不变。版本迁移刷新旧货架和限购，保留库存及魂晶。

旧v111原有更新继续保留。此前清单之外的九重天分层特殊商品未纳入本次，九重天专属代码和配置保持原包字节。
本轮仅替换程序载荷及其校验配置，游戏引擎、客户端资源、Python运行时、Java桥和原生库保持旧v111原字节。
因版本号相同，请通过本文件日期及同名sha256文件区分新旧包。
'''


def main():
    source_check(check_worktree=False)
    checksum = digest(OUTPUT.read_bytes())
    records = {}
    for name in ('build-validation', 'protocol-validation', 'lua-validation',
                 'payload-save-validation', 'release-scope-validation', 'packaging-validation',
                 'native-guard-validation', 'native-retry-validation'):
        record = json.loads((EVIDENCE / (name + '.json')).read_text())
        assert record['apk_sha256'] == checksum
        if name != 'build-validation':
            assert record['passed'] and not record.get('skipped', 0), name
        records[name] = record
    device = json.loads((EVIDENCE / 'device-validation.json').read_text())
    assert device['apk_sha256'] == checksum
    assert device['passed'] or device.get('status') == 'environment_unavailable'
    if device['passed']:
        assert device.get('screenshot_reviewed') and device.get('startup_branding_v111_verified')
    metadata = records['build-validation']
    metadata.update(protocol_tests=records['protocol-validation']['tests'],
                    save_migration_verified=True, device_tested=device['passed'],
                    physical_device_tested=False, evidence=str(EVIDENCE.relative_to(ROOT)),
                    device_validation_note=device['summary'])
    OUTPUT.with_suffix('.manifest.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')
    note = WORK / 'v111更新说明.txt'
    note.write_text(NOTES + '\n本次验证：\n' + str(metadata['protocol_tests']) +
                   '项不同包内回归通过，零失败、零跳过；完整Lua编译、旧存档副本升级及重启、打包隔离验证通过。\n' +
                   device['summary'] + '\n物理手机及光速虚拟机逐玩法验收未完成。\n')
    archive = WORK / (NAME + '.zip')
    artifacts = [OUTPUT, OUTPUT.with_suffix('.apk.sha256'), OUTPUT.with_suffix('.manifest.json'), note]
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for path in artifacts:
            z.write(path, path.name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and digest(z.read(NAME)) == checksum
    artifacts += [archive, OUTPUT.with_suffix('.apk.idsig')]
    backup = json.loads((EVIDENCE / 'original-release-backup.json').read_text())['files']
    for path in artifacts:
        target = ROOT / 'build' / path.name
        assert target.is_file() and digest(target.read_bytes()) == backup[path.name], target
        assert digest((ARCHIVE / path.name).read_bytes()) == backup[path.name]
    for path in artifacts:
        target = ROOT / 'build' / path.name
        temporary = target.with_name(target.name + '.refresh-tmp')
        shutil.copy2(path, temporary)
        assert digest(temporary.read_bytes()) == digest(path.read_bytes())
        temporary.replace(target)
    assert digest(BASE.read_bytes()) == BASE_SHA
    report('published-release', dict(published=True, apk_sha256=checksum, version_code=111,
        revision='2026-11-10', artifacts=['build/' + p.name for p in artifacts],
        old_release_backup=str(ARCHIVE.relative_to(ROOT)), protocol_tests=metadata['protocol_tests'],
        device_tested=device['passed'], physical_device_tested=False))
    print(ROOT / 'build' / NAME)


if __name__ == '__main__':
    main()
