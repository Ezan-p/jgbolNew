"""Publish the verified v112 test APK and its local distribution ZIP."""
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools import build_v112_test as build


def main():
    meta = json.loads((build.EVIDENCE / 'build-validation.json').read_text())
    sha = build.digest(build.OUTPUT.read_bytes())
    assert sha == meta['apk_sha256']
    validations = {}
    for name in ('scope', 'grant', 'lua', 'runtime', 'protocol'):
        data = json.loads((build.EVIDENCE / (name + '-validation.json')).read_text())
        assert data['passed'] and data['apk_sha256'] == sha, name
        assert not any(data.get(k) for k in ('errors', 'failures', 'skipped')), name
        validations[name] = data.get('tests', True)
    assert build.digest(build.BASE.read_bytes()) == build.BASE_SHA
    formal_sha = build.digest(build.FORMAL.read_bytes())
    # The separate formal release may be published while tests are running.
    # Require identical gameplay, and preserve that independently updated APK.
    with zipfile.ZipFile(build.FORMAL) as apk:
        import io
        with zipfile.ZipFile(io.BytesIO(apk.read('assets/offline/program.zip'))) as payload:
            for name, digest in meta['source_hashes'].items():
                if name not in ('offline_android/backend.py', 'network_redirect/login.html',
                                'offline_android/test_edition_v112.py'):
                    assert build.digest(payload.read(name)) == digest, name
    output = ROOT / 'build' / build.OUTPUT.name
    assert not output.exists(), 'Do not replace a published APK'
    for suffix in ('.apk', '.apk.idsig', '.apk.sha256', '.manifest.json'):
        source = build.OUTPUT.with_suffix(suffix)
        if source.exists():
            shutil.copy2(source, output.with_suffix(suffix))
    notes = output.with_name(output.stem + '使用说明.txt')
    notes.write_text(f'''金箍棒ol测试版 v112 · 2026-11-13更新整合

版本号112，版本名称3.87-test.112.1，登录页显示v112。
基于最新测试v111，整合当前工作区已实现的玩法、数值和客户端更新。

安装与存档
可覆盖同签名旧测试版v111/v110；先退出游戏并备份完整test-save-v106目录，再覆盖安装，不卸载、不清除数据。
沿用包名com.sygame.jingubang.test106、测试签名、18776端口及files/test-save-v106/game.sqlite3，与正式版共存。

本次新增存档补给
一至十阶九幽宝图（1431—1440）各追加500张，合计5000张。
碱水粽子1213、红豆粽子1214、咸肉粽子1215、五仁粽子1216各追加300个，合计1200个。
首次启动向固定测试账号v106_fixed_test一次性追加，不覆盖原库存；领取记录与道具原子保存。
重启、覆盖安装或消耗后均不重复领取，不自动补满。四种普通粽子不包括五星粽子1217。
保留原v108养成补给和v110一阶宝图500张的旧领取记录，旧补给已领不重发。
全新测试档仍先领取历史补给，因此新档一阶宝图为1000张（历史500＋本次500），其他九阶各500张、四粽子各300个。
APK不携带玩家数据库；补给在安装后首次启动时写入应用原测试存档。

整合内容
1. 九幽宝图v9十二格养成奖池：魂晶、三类经验丹、精魄石及各阶数量与概率调整，已开始旧盘保留。
2. 九幽冥仙恢复原表属性和初始技能；挂机魂晶为旧版6倍、首胜魂晶为旧版2倍。
3. 九幽商店v17：三种精华常驻，20魂晶/个、每日各限500个；其他材料和补天石货架调整。
4. 四种普通粽子各0.25%产出五星粽子；五星粽子可批量开启，元宝40%、大传世金卡30%、武器/防具各9%、法宝/被动各6%，移除大乘经。
5. 蛋莲月饼、五仁粽子移除仙币；仙晶改100个、6.5%概率。
6. 九重商会王母魂魄、五法界魂箱常驻，其余商品加权不重复抽四种，低级/高级单件权重4/1。
7. 八卦40级开放前两位，后六位60级消耗材料开启；正逆八卦助阵绑定神仙ID，换位跟随、下阵暂停。
8. 仙盟捐献每元宝获得10贡献，同步贡献余额、成员缓存与到账提示。
9. 修复等级卡升级奖励弹窗；1000魂元神石祈福固定奖励100元宝；仙灵店铺商品调整。
10. 太虚商店v5：三类精华、四/五星灵器、太古水晶、明心石、轮回舍利、无上石、补天石、神源水晶等11种商品重配价格和限购。
11. 太虚血战v8：排名元宝/圣母蟠桃/仙晶分别为第1名1500/200/20000，第2—3名800/100/15000，第4—10名500/50/10000，第11—20名300/10/5000；单场胜利仙晶100。
12. 血战支持各阶段退出确认与主动认输结算，取消退出继续战斗。
同时保留当前源码中的土地、蟠桃及兑换码等此前修复，原测试版十项更新延续。

验证
实际APK内模块完成{validations['protocol']}项玩法回归、{validations['grant']}项补给与真实v111测试档升级验证、{validations['runtime']}项测试版登录与网络时钟验证，零失败、零错误、零跳过。
已验证新档、旧档精确追加，所有10阶宝图和4种粽子实际协议使用、批量开粽子、请求重放、消耗后重启不补发、部分发奖失败及保存失败回滚、其他账号不变。
完整Lua编译、v112登录标识、背包批量使用、九幽输入和太虚认输等客户端回归通过。
原Android外壳、Java、原生库、资源和Python运行时沿用测试v111字节，仅更新版本清单、程序载荷和校验信息。
本轮未完成Android设备装机与触摸验收。

APK SHA-256：{sha}
验证证据：analysis/evidence/v112-test-20261113
''')
    with zipfile.ZipFile(output.with_suffix('.apk.zip'), 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in (output, notes, output.with_suffix('.apk.sha256'), output.with_suffix('.manifest.json')):
            archive.write(path, path.name)
    with zipfile.ZipFile(output.with_suffix('.apk.zip')) as archive:
        assert archive.testzip() is None and build.digest(archive.read(output.name)) == sha
    assert build.digest(build.BASE.read_bytes()) == build.BASE_SHA
    assert build.digest(build.FORMAL.read_bytes()) == formal_sha
    build.report('published-release', dict(published=True, apk=str(output.relative_to(ROOT)),
        zip=str(output.with_suffix('.apk.zip').relative_to(ROOT)), apk_sha256=sha,
        validations=validations, previous_test_preserved=True,
        current_formal_sha256=formal_sha, current_formal_gameplay_matches_snapshot=True))
    print(output)


if __name__ == '__main__':
    main()
