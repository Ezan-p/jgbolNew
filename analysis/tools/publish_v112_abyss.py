"""Publish verified formal v112 using the user's existing simple filenames."""
import json
from pathlib import Path
import re
import shutil
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from analysis.tools.build_v112_abyss import WORK,EVIDENCE,BASE,BASE_SHA,OUTPUT,digest,report


def main():
    sha=digest(OUTPUT.read_bytes())
    records={name:json.loads((EVIDENCE/(name+'.json')).read_text()) for name in (
        'build-validation','scope-validation','protocol-validation','lua-validation','payload-save-validation')}
    assert all(r['apk_sha256']==sha for r in records.values())
    assert all(r['passed'] for name,r in records.items() if name!='build-validation')
    protocol=records['protocol-validation']
    assert protocol['failures']==protocol['errors']==protocol['skipped']==0
    assert records['lua-validation']['abyss_shop_batch']
    assert records['payload-save-validation']['previous_v112_to_new_v112_all_tables_equal']
    assert digest(BASE.read_bytes())==BASE_SHA
    public=ROOT/'build'; destination=public/OUTPUT.name
    assert digest(destination.read_bytes())==BASE_SHA
    document=ROOT/'docs/v112内容整合与验证说明.md'
    old_document=document.read_text()
    updates=re.findall(r'^\d+\. .*$',old_document,re.M)
    assert len(updates)==12
    updates[0]='1. 九幽宝图v10十二格养成奖池：魂晶首抽28%、五法界魂箱7%、明心转生石1%、伏心转生石7%；其余奖励数量与概率沿用已有规则，已开始旧盘保留。'
    updates[2]='3. 九幽商店v18：全部8种材料加权无放回抽6种，取消精华常驻；三种精华、轮回舍利、伏心转生石权重各40，明心转生石20，无上转生石3，补天石5。价格与限购保持原规则；精魄石、神装灵器、神源水晶继续不入池。'
    updates.append('13. 九幽商店六格均支持批量兑换，单次上限为100份、当日剩余限购及余额可购数的最小值；确认时重新校验余额、限购、货架日期和版本。兑换后继续显示单份数量，精华可分5批各100个买满当日500个。')
    bullets='\n'.join(updates)
    archive=public/'archive/v112-before-abyss-20261114'
    archive.mkdir(parents=True,exist_ok=False)
    preserved={}
    for path in [*public.glob('金箍棒ol离线正式版v112*'),public/'v112更新说明.txt',document]:
        if path.is_file():
            shutil.copy2(path,archive/path.name)
            preserved[path.name]=digest(path.read_bytes())
    validation=(f"本轮实际APK内{protocol['tests']}项九幽、宝图、配置、太虚兼容及Android运行时回归最终通过，零失败、零错误、零跳过。"
        '全部生成Lua编译、v112登录标识及九幽/太虚客户端回归通过；批量专项先复现原版限制，再验证六格、100份上限、余额与限购约束、旧窗口拒绝及单份数量显示。'
        'v111→新v112→重启存档迁移通过；上一批v112→新v112→重启所有账号数据表逐值一致。'
        '签名、对齐、载荷哈希和更新范围核对通过。')
    if protocol['environment_recheck_test_ids']:
        validation+='本机端口受沙箱限制的项目在允许回环端口的环境复测通过，首次失败与复测记录保留。'
    limitation='本轮未进行Android装机、物理手机或光速虚拟机实机验收。上一批v112的1387项完整回归为历史记录，不计入本轮专项测试数量。'
    migration=('九幽商店首次访问按v18重建货架并清空旧限购，已有魂晶、库存和养成保留；'
        '已开始宝图保留原奖池及剩余付费次数，未开始的旧预览重新打开后使用v10。'
        '幻境商店、同周血战及其他既有玩法沿用上一批v112规则。')
    note=WORK/'v112更新说明.txt'
    note.write_text(f'''金箍棒ol离线正式版 v112 · 2026-11-14

版本号112；版本名称3.87-offline.12；登录页v112；安装包名称金箍棒ol离线正式版v112.apk。
沿用正式包名com.sygame.jingubang.p360、原签名、18770端口及files/save目录。
支持覆盖同签名正式v112/v111/v110。先退出游戏并备份完整save目录，再覆盖安装；不要卸载或清除数据。
ARM32（armeabi-v7a），最低Android API21。APK不含玩家数据库或测试版自动补给，原100个兑换码及领取记录保留。

当前整合内容（本轮更新第1、3、13项）
{bullets}

存档迁移
{migration}

验证
{validation}
{limitation}

APK SHA-256：{sha}
证据：analysis/evidence/v112-abyss-20261114。
上一批正式v112及说明已归档：build/archive/v112-before-abyss-20261114。
''')
    meta=records['build-validation']
    meta['verification']=dict(protocol_tests=protocol['tests'],lua_verified=True,
        abyss_shop_batch_verified=True,old_save_compatibility_verified=True,
        device_verified=False,physical_device_tested=False,
        baseline_full_regression_tests=1387,baseline_evidence='analysis/evidence/v112-taixu-20261113')
    OUTPUT.with_suffix('.manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    distribution=OUTPUT.with_suffix('.apk.zip')
    with zipfile.ZipFile(distribution,'w',zipfile.ZIP_DEFLATED) as z:
        for path in (OUTPUT,OUTPUT.with_suffix('.apk.sha256'),OUTPUT.with_suffix('.manifest.json'),note):
            z.write(path,path.name)
    with zipfile.ZipFile(distribution) as z:
        assert z.testzip() is None and digest(z.read(OUTPUT.name))==sha
        assert not any('三项更新' in n for n in z.namelist())
    for path in (OUTPUT,OUTPUT.with_suffix('.apk.sha256'),OUTPUT.with_suffix('.manifest.json'),
                 OUTPUT.with_suffix('.apk.idsig'),distribution,note):
        shutil.copy2(path,public/path.name)
    assert digest(destination.read_bytes())==sha
    assert all(digest((archive/name).read_bytes())==h for name,h in preserved.items())
    for path in Path('/private/tmp').glob('jgbol-v112-abyss-*.log'):
        shutil.copy2(path,EVIDENCE/path.name.removeprefix('jgbol-v112-abyss-'))
    document.write_text(f'''# 离线正式版v112内容整合与验证说明

更新日期：2026-11-14。版本号112，版本名称`3.87-offline.12`，登录页v112。

下载：[正式APK](../build/{OUTPUT.name})、[ZIP分发包](../build/{distribution.name})、[更新说明](../build/{note.name})。

## 更新范围

保留此前正式v112全部更新，本轮调整九幽宝图、商店上架，并补齐六格批量兑换。当前内容如下：

{bullets}

## 安装与存档

沿用正式包名、原签名及`files/save`目录，可覆盖同签名正式v112/v111/v110。先退出游戏并备份完整save目录，覆盖安装，不卸载、不清除数据。APK不含玩家数据库或测试版自动补给，原100个兑换码保留。

{migration}

相对上一批正式v112，仅修改`abyss_client.lua`、`activity.py`、`activity_abyss.py`、`activity_rules.json`及生成的客户端Lua和载荷清单。活动配置差异仅限宝图权重/版本与九幽商店货架/版本；Android版本清单、原生引擎、Java、游戏资源、Python运行时及其他载荷逐字节保留。

## 验证结果

{validation}

{limitation}

APK SHA-256：`{sha}`。

本轮[构建与验证证据](../analysis/evidence/v112-abyss-20261114)，脚本为`analysis/tools/build_v112_abyss.py`、`verify_v112_abyss.py`及`publish_v112_abyss.py`。上一批APK、附件和说明见[历史归档](../build/archive/v112-before-abyss-20261114)，[上一批验证记录](../analysis/evidence/v112-taixu-20261113)保留。
''')
    for relative in ('docs/九幽商店材料奖池设计与明细.md','docs/九幽宝图产出分析.md'):
        path=ROOT/relative
        with path.open('a') as f:
            f.write('\n\n2026-11-14发布：当前规则已整合进离线正式v112；本轮封装、实际APK专项验证及安装说明见[v112内容整合与验证说明](v112内容整合与验证说明.md)。此前“未重建APK”记录对应当时的源码验证范围。\n')
    report('published-release',dict(published=True,apk_sha256=sha,apk_bytes=destination.stat().st_size,
        zip_sha256=digest((public/distribution.name).read_bytes()),version_code=112,
        version_name='3.87-offline.12',feature_groups=13,packaged_protocol_tests=protocol['tests'],
        device_verified=False,previous_v112_archived=True,archive_sha256=preserved,
        downloads=[str((public/p.name).relative_to(ROOT)) for p in (OUTPUT,distribution)]))
    print('Published',destination,sha)


if __name__=='__main__':
    main()
