"""Publish the verified v110 test refresh alongside all existing releases."""
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.build_v110_test_refresh import APK, BASE, BASE_SHA, PREVIOUS, PREVIOUS_SHA, EVIDENCE, digest, report

UPDATES = '''1. 新增等级卡：每张主角升1级，保留修为及正常升级奖励，最高99级；仅通过10／20／50张三档激活码礼包获取，每账号每档一次。
2. 蟠桃大会前十名NPC采用封神榜初始第11—20名完整模板，伤害分十档，每档每日从5个固定值选1个，总范围7915万—1.177亿。
3. 蟠桃大会日榜：1—5名圣母蟠桃150，6—10名100，11—20名50，21—50名普通蟠桃200；沿用13:00后邮件结算与防重复。
4. 九重商会移除两种密卷，低级池7种，除魂缘丹外限兑5份，魂缘丹限1份，超级召唤符100天星；调整高级商品价格，保留已有购买记录。
5. 仙盟宝库精华礼包每份1个，200贡献，每次刷新限购3份，上架权重保持5。
6. 中秋、端午页面显示每秒更新的周刷新倒计时，截止北京时间下周一00:00，跨周自动切换。
7. 太虚血战四个等级组各固定最强15名NPC，另外4名普通NPC分段抽取；已开赛名单保留，新届采用新规则。
8. 幻境商店每日固定三种精华及近古水晶，另外加权抽2种，全部单件出售。精华20仙晶／限100件，近古水晶100仙晶／限10件；其余价格、限兑及低概率上架按新配置执行。
9. 升阶宝箱三种精华每次10个，其他材料1个；五星灵器／远古水晶／太古水晶各5%，其余六项各17/120，逐箱独立抽取。
10. 猎魂宝箱固定精魄石10个，再抽一项：紫色精魄碎片1个5%；精魄石10或20个、白虎／玄武／青龙精华各10个，这五项各19%。'''


def main():
    meta = json.loads((EVIDENCE / 'build-validation.json').read_text())
    checksum = digest(APK.read_bytes())
    assert checksum == meta['apk_sha256']
    results = {}
    for name in ('protocol', 'lua', 'grant', 'runtime', 'upgrade', 'scope'):
        data = json.loads((EVIDENCE / (name + '-validation.json')).read_text())
        assert data['passed'] and data['apk_sha256'] == checksum, name
        assert not any(data.get(k) for k in ('failures', 'errors', 'skipped')), name
        results[name] = data
    device = json.loads((EVIDENCE / 'device-validation.json').read_text())
    assert device['apk_sha256'] == checksum
    assert digest(BASE.read_bytes()) == BASE_SHA and digest(PREVIOUS.read_bytes()) == PREVIOUS_SHA
    output = ROOT / 'build' / APK.name
    assert not output.exists(), 'Keep existing published artifacts'
    tests = sum(results[k]['tests'] for k in ('protocol', 'grant', 'runtime'))
    status = ('独立Android 6 ARM32 QA模拟器覆盖安装通过；安装前后完整测试存档字节一致，APK回读哈希及新程序、原生引擎启动就绪检查通过。'
              if device['passed'] else '本轮设备安装启动验收未完成：' + device.get('environment_diagnosis', device.get('reason', device['status'])))
    notes = f'''金箍棒ol测试版 v110 · 2026-11-10整合更新

Android版本号110；版本名3.87-test.110.1；登录页显示v110。
以2026-11-10最新版正式v111玩法载荷为基础，纳入以下10项后续更新，并沿用v110测试版独立运行外壳。正式v111已有的21项整合更新全部保留。

本次10项更新
{UPDATES}

安装与存档
直接覆盖同签名v110测试版（包括九幽宝图500版）；不要卸载、清除数据。
包名com.sygame.jingubang.test106、测试签名、端口18776及files/test-save-v106存档目录不变，与正式版独立。
更新前退出游戏，备份完整test-save-v106目录（含数据库、时钟及保护密钥等同代文件）。APK不含玩家数据库，不导入正式版进度。
本包Android版本号仍为110；已装测试版v111的设备不能按普通覆盖安装降级至本包，不建议卸载以规避版本检查。
原v110／v111及正式版分发文件全部保留，本次另存新文件。

测试补给
沿用原养成补给修订108及领取标记，不开启新一轮补给。
沿用一次性500张一阶九幽宝图：未领旧档或新档按既有规则领一次；已领取、已消耗均不补发。
等级卡不自动赠送，只能兑换礼包后入包；10张码7KIEGUOTCKQN、20张码K1MJI3166RT4、50张码CUTWP96BZCKY。
三档各限一次，兑换不会自动使用；99级仍可领卡但不可继续升级。

规则迁移
保留既有角色养成、库存、货币及已领取记录。商店更新按各模块规则迁移货架和购买额度；已开赛血战保留本届名单，历史蟠桃排名邮件不重发。
联网校时、装备实例拆分、活动周刷新及九幽商店迁移沿用最新版正式v111规则，详见docs/v111_20261110整合更新与验证.md。
九重天宫分层特殊商品仍为设计稿，本包未实施。

验证
实际APK解包执行{results['protocol']['tests']}项去重玩法回归、6项补给及2项测试运行时回归，共{tests}项通过；零失败、零错误、零跳过。
初轮1项HTTP登录测试因沙箱禁止监听本机端口而报权限错误；已在允许临时端口的环境中使用同一APK模块单独复核通过，不重复计数。原日志与复核结果均保留。
完整Lua5.1编译、v110标识、客户端回归、真实旧测试包生成的临时存档升级／重启、补给防重复、10项功能范围、生成补丁一致性、签名与对齐检查通过。
{status}
未进行物理手机、光速虚拟机和全部玩法逐项触摸验收。
ARM32（armeabi-v7a），最低Android API21；需支持32位ARM应用。
证据目录：analysis/evidence/v110-test-refresh-20261110。
APK SHA-256：{checksum}
'''
    note = output.with_name(output.stem + '使用说明.txt')
    for suffix in ('.apk', '.apk.sha256', '.apk.idsig'):
        shutil.copy2(APK.with_suffix(suffix), output.with_suffix(suffix))
    note.write_text(notes)
    meta['verification'] = dict(tests=tests, gameplay_tests=results['protocol']['tests'],
        failures=0, errors=0, skipped=0, lua=True, upgrade=True, scope=True,
        device_verified=device['passed'], device_status=device['status'], physical_device_tested=False)
    output.with_suffix('.manifest.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n')
    supplies = ROOT / 'build/金箍棒ol测试版-v110沿用补给清单.json'
    archive = output.with_suffix('.apk.zip')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for path in (output, output.with_suffix('.apk.sha256'), output.with_suffix('.manifest.json'), note, supplies):
            z.write(path, path.name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and digest(z.read(output.name)) == checksum
    assert digest(output.read_bytes()) == checksum
    report('published-release', dict(published=True, apk=str(output.relative_to(ROOT)),
        archive=str(archive.relative_to(ROOT)), apk_sha256=checksum, tests=tests,
        device_verified=device['passed'], originals_preserved=True))
    doc = ROOT / 'docs/v110测试版20261110整合更新与验证.md'
    assert not doc.exists()
    doc.write_text('# v110测试版2026-11-10整合更新与验证\n\n'
        f'已打包：[APK](../build/{output.name})， [ZIP分发包](../build/{archive.name})。\n\n'
        + notes + '\n构建：`analysis/tools/build_v110_test_refresh.py`；包内回归：`analysis/tools/verify_v110_test_refresh.py`；发布：`analysis/tools/publish_v110_test_refresh.py`。\n')
    print(output)
    print('Verified tests:', tests, 'Device:', device['passed'])


if __name__ == '__main__':
    main()
