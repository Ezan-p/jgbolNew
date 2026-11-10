"""Publish the fully checked isolated test artifact, preserving previous packages."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from analysis.tools.build_v111_test import WORK,EVIDENCE,APK,BASE,BASE_SHA,PREVIOUS,PREVIOUS_SHA,digest

NOTES='''金箍棒ol测试版 v111
版本号：111；版本名称：3.87-test.111.1。

安装与存档
沿用测试版独立包名com.sygame.jingubang.test106、原测试签名、18776端口与files/test-save-v106存档目录，可覆盖安装此前v106/v108/v110测试版及v110九幽宝图500版，与正式版共存。
先备份完整测试版存档目录，再覆盖安装；不要卸载旧测试版或清除数据。正式版存档不会自动迁入测试版。
保留固定测试账号和既有一次性养成补给。沿用500张一阶九幽宝图补给：未领取的旧档及新档按既有规则领取一次，已领取或已消耗的不补发。APK不含玩家数据库。

相对正式v111纳入的更新（截至2026-11-10）
1. 救悟空／十万猴急关闭入口及活动操作，停止新增活动珠、充值额度和特权邮件；保留已有道具、邮件、活动存档。
2. 游戏时钟接入多来源HTTPS校准，统一北京时间显示、周末判断和前台恢复校准。断网同次设备启动继续连续计时；跨设备重启的离线间隔待联网确认；未来结算记录不会因回拨重复领奖。保留时间完整性保护与已有处罚，新增联网确认的改时间异常检测。联网校时不上传角色存档。
3. 灵宠仙地三目标分别记录两类挑战，每日六个组合；3次普通额度用完后可用3次付费额度，付费100元宝/次。修复完成状态、跨日页面、第六次挑战和奖励预览/结算同步。
4. 灵兽试炼每次满血挑战，须击杀首领才通关；失败伤害不累计；旧部分伤害不折算为通关。
5. 试炼点赞20元宝/次，每天最多3次，每次四维+5%，上限15%；补齐扣费确认、余额和次数提示、按钮状态及防连点。
6. 试炼每层领奖增加3次领养机会，四层共12次；领养仅周六、周日开放。
7. 宠物商店每天固定下品符、中品符、驯养丹3格，再从6种候选中加权抽3格。驯养丹5颗/份限3份，三种升星材料各限5份，宝箱限1份；增加货架持久化及过期页面校验。
8. 驯养宝箱每箱独立产出10/15/20颗驯养丹，概率30%/50%/20%；每批1—15箱。修复新角色未初始化其他活动时开箱与背包同步。
9. 仙盟宝库16种候选、每天8格，新增精华礼包、驯养宝箱、乾坤符箓礼包、圣母蟠桃和两档银两，调整商品数量、贡献价格及限购，移除直接精魄石和三种精华。
10. 西天取经经书刷新只随机第2—5档，概率60%/25%/12%/3%，可重复、可降档、无保底；第5档停止刷新，界面提示同步。
11. 洞府红尘劫两阶段采用60级3人、100级5人固定阵容，面板战力305598/1748010；预览与实战共用数值并接入修炼。规模1需三建筑11级，规模2取消额外建筑等级检查，修复升级后阶段刷新与满级挑战入口。
12. 洞府常驻商店：仙木100/1000币/限20份，修炼果5/1000币/限10份，宠物转换丹1/5000币/限1份，驯养丹5/1000币/限10份。限时栏11选3，加入天仙令1/2000币/限1份，替换原三种升星材料。
13. 宠物融合概率预览体现已有星级保底；幻化成长限制在目标类型、品质和星级合法范围，修复越界记忆及九星加成；隐藏未实现技能按钮。
14. 中秋、端午北京时间每周一00:00刷新制作进度和赠料资格。各自剩余材料（含锁定）合计10:1邮件返还普通蟠桃，向下取整、尾数清空；成品和已获奖励保留；旧档首次建立基线不立即回收。
15. 东海撒网新增菩提祖师魂魄、五法界魂箱、东华大帝魂魄各1个、各1%；小包子概率17%降至14%；移除概率预览弹窗及点击热区。
16. 九幽宝图v5：新盘12种不同奖品，各按宝图每阶1个发放；三种精华各17%，四星灵器/圣母蟠桃/轮回舍利各10%，界魂箱9%，五星灵器/太古水晶/补天石/明心石/无上石各2%（未移除格子的首抽概率）；已开始旧盘沿用原规则。
17. 猎魂翻牌精魄石10/20个初始权重20%/15%，黄色精魄55%、紫碎8%、紫精魄2%；普通5牌最多2张石，冥界3牌最多1张石，封顶后余类重新归一化并打乱；扫荡追加精魄石5个。
18. 太虚血战第1/2—3/4—10/11—20名奖励改为元宝1000/500/300/150、圣母蟠桃200/100/50/10，仙晶沿用10000/8000/5000/3000。
19. 精华礼包采用11月10日最终规则：随机一种白虎/玄武/青龙精华，各1/3；数量20/50/100，概率80%/15%/5%，批量每包独立抽取。此前固定10个方案已替换。
20. 新奖励按原表不可堆叠规则独立发放；旧叠加装备迁移为独立实例，原件保留养成及关联，额外件为未养成装备，保留锁定。
21. 九幽商店采用11月10日v11规则：三种精华每份100、1000魂晶、每日限5份，其余8种商品及上架权重不变；版本迁移刷新旧货架并清空旧限购，保留库存与魂晶。

沿用正式v111已包含的玩法更新。九重天分层特殊商品仅有设计，本包未纳入；其专属代码、配置与正式v111逐字节一致。
本次另适配测试账号入口的network_time参数，多账号共用同一时钟，保持原补给领取标记。
'''


def main():
    subprocess.run([sys.executable,str(ROOT/'analysis/tools/verify_v111_test_scope.py')],check=True)
    meta=json.loads((EVIDENCE/'build-validation.json').read_text());sha=meta['apk_sha256']
    assert sha==digest(APK.read_bytes())
    reports={}
    for name in ('packaged-targeted','packaged-additional','lua','grant','upgrade','runtime','scope'):
        filename=name+'.json' if name.startswith('packaged-') else name+'-validation.json'
        report=json.loads((EVIDENCE/filename).read_text())
        assert report['passed'] and report['apk_sha256']==sha,name
        assert not any(report.get(k,0) for k in ('errors','failures','skipped')),name
        reports[name]=report
    all_ids=[]
    for name in ('packaged-targeted','packaged-additional'):
        assert reports[name]['tests']==len(reports[name]['test_ids'])
        assert len(set(reports[name]['test_ids']))==reports[name]['tests']
        all_ids+=reports[name]['test_ids']
    ids=sorted(set(all_ids))
    merged=dict(passed=True,apk_sha256=sha,tests=len(ids),errors=0,failures=0,skipped=0,
        test_ids=ids,suites=sorted(set(reports['packaged-targeted']['suites']+reports['packaged-additional']['suites'])),
        validation_mode='actual immutable APK payload',
        excluded_initial_runs=['protocol-shard-0.log','protocol-shard-1.log','protocol-shard-2.log'],
        exclusion_reason='Initial runner import order selected live workspace code; later concurrent edits changed that workspace. These runs are not counted.')
    (EVIDENCE/'protocol-validation.json').write_text(json.dumps(merged,indent=2)+'\n')
    device=json.loads((EVIDENCE/'device-validation.json').read_text())
    assert device['apk_sha256']==sha
    total=len(ids)+reports['grant']['tests']+reports['runtime']['tests']
    notes=NOTES+f'\n本次验证\n实际APK解包载荷的玩法与客户端回归{len(ids)}项、测试补给6项、运行时2项，共{total}项通过，零失败、零错误、零跳过；重复用例已去重。\n完整Lua5.1编译、登录前v111标识、真实旧测试包生成的临时存档升级与重启、装备迁移、联网时钟接入、补给防重复、签名及对齐检查通过。\n初轮回归脚本导入了工作区源码，期间工作区出现后续修改，因此初轮结果不计入上述数量。最终回归使用已生成APK的固定载荷；旧点赞测试残血预期已按本次满血挑战规则修正并重测通过。\n本包按本次确认的21项更新冻结；打包期间新增的九重天等后续工作区改动未纳入，相关文件清单见scope-validation.json。\n设备验收：{device["note"]}\n未完成物理手机或光速虚拟机逐玩法触摸验收。\nAPK SHA-256：{sha}\n'
    output=ROOT/'build'/APK.name
    assert not output.exists(),'Refusing to replace an existing published test APK'
    verification=dict(tests=total,protocol_tests=len(ids),failures=0,errors=0,skipped=0,lua_passed=True,
        actual_packaged_tests=len(ids),
        test_save_upgrade_passed=True,runtime_passed=True,device_verified=device['passed'],physical_device_test=False)
    meta['verification']=verification
    text=json.dumps(meta,ensure_ascii=False,indent=2)+'\n'
    APK.with_suffix('.manifest.json').write_text(text)
    note=output.with_name(output.stem+'使用说明.txt');note.write_text(notes)
    for suffix in ('.apk','.apk.sha256','.manifest.json','.apk.idsig'):
        shutil.copy2(APK.with_suffix(suffix),output.with_suffix(suffix))
    archive=output.with_suffix('.apk.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in (output,note,output.with_suffix('.manifest.json'),output.with_suffix('.apk.sha256')):z.write(p,p.name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and digest(z.read(output.name))==sha
    assert digest(output.read_bytes())==sha
    assert digest(BASE.read_bytes())==BASE_SHA and digest(PREVIOUS.read_bytes())==PREVIOUS_SHA
    report=dict(published=True,apk=str(output.relative_to(ROOT)),apk_sha256=sha,archive=str(archive.relative_to(ROOT)),notes=str(note.relative_to(ROOT)),baselines_preserved=True,**verification)
    (EVIDENCE/'published-release.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
