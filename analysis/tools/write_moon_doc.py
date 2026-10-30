"""Generate exact Mid-Autumn reward tables from the runtime configuration."""
from fractions import Fraction
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from network_redirect import activity_moon as moon, summon


def percent(value):
    value=Fraction(value)
    if value.denominator==1:return f'{value.numerator}%'
    if 1000000%value.denominator==0:return f'{float(value):g}%'
    return f'{value.numerator}/{value.denominator}%（约{float(value):.8f}%）'


def main():
    r=moon.load_rules()
    names={int(x['Ftype_id']):x['name'] for x in summon.rows('item_name.csv')}
    skills={int(x['type_id']):x['name'] for x in summon.rows('skill_name.csv')}
    def name(p):
        typ,tid,_,_=p
        return {11:'元宝',12:'银两'}.get(typ) or (skills if typ==6 else names)[tid]
    lines=['''# 缘聚中秋离线活动实现说明

2026-10-30 更新：四种月饼与四种粽子均支持在制作按钮中选择数量，一次制作1～min(可用材料、当日剩余额度、100)个。每个成品仍消耗通用材料15个和对应专用材料15个；每日额度及个人累计按实际制作数量推进，批量跨过多个10个门槛会一次发齐全部蟠桃奖励。面粉、粽叶改为2／3／4个各1/3，其他材料概率与成品奖池不变。

版本：`2026-10-31-red-bean-essence-20`。本说明对应用户参考图落地后的离线实现，概率、图中未指定的数量和候选范围均为本次合理补充，**不是原服官方概率**。旧《四种月饼奖励池设计说明》为历史方案，当前以本文与 `server_config/moon_rules.json` 为准。

## 1. 常驻与玩法流程

缘聚中秋现为常驻活动。`activity_rules.json` 的 `seasonal_games.moon.enabled=true` 时开放，后端不再依据旧 `start_time/end_time` 判断截止；客户端移除“活动剩余时间”图样和递归倒计时，显示“常驻开放”。手动关闭开关后停止制作和材料产出，背包中已经获得的月饼仍可开启。

1. 在旅途、天命之战或蟠桃会取得材料。
2. 用面粉15个和指定馅料15个制作对应月饼1个，制作成功率100%，不会随机变成其他月饼。
3. 在背包使用月饼，每个独立抽取一个具体奖励；随机结果在本机后端产生，随后发送到账结果和背包更新。
4. 四种月饼共用每日100次制作上限，北京时间00:00重置；材料、成品和累计制作进度不随换日清空。开启月饼不占制作次数。

首次查询活动状态时，新角色获得面粉60个、紫薯／红豆／桂花／蛋莲馅料各15个，足够四种月饼各制作一次。每角色只发一次，标记为 `moon:permanent`；旧存档已有任何 `moon:开始时间` 领取记录时视作已领取，不补发、不回收原有材料。重启、重复查询、修改旧活动起止时间均不重复赠送。

| 成品 | 成品ID | 配方 | 产量 |
|---|---:|---|---:|
| 紫薯月饼 | 1130 | 面粉1134×15＋紫薯馅料1135×15 | 1 |
| 红豆月饼 | 1131 | 面粉1134×15＋红豆馅料1136×15 | 1 |
| 桂花月饼 | 1132 | 面粉1134×15＋桂花馅料1137×15 | 1 |
| 蛋莲月饼 | 1133 | 面粉1134×15＋蛋莲馅料1138×15 | 1 |

沿用已有离线累计赠礼：**个人累计每制作10个月饼，额外得到普通蟠桃1001×10**，在第10、20、30……次制作时直接发放。不按自然日清零，也不是全服随机送礼。界面提示已改为个人累计进度。此项与月饼开箱独立，不纳入下列奖池100%的分母；紫薯等月饼不会因为额外赠礼而改变本池概率。

## 2. 材料随机掉落

本次明确采用“四种馅料分别独立判定”的规则：**每次有效结算先抽面粉，再对四种馅料各抽一次**。四种馅料可同时掉落，不是四选一，也不是总计最多2个。

| 材料／ID | 0个 | 1个 | 2个 | 3个 | 4个 | 每次长期期望 |
|---|---:|---:|---:|---:|---:|---:|
| 面粉1134 | 0% | 0% | 1/3 | 1/3 | 1/3 | 3个 |
| 紫薯馅料1135 | 10% | 70% | 20% | 0% | 0% | 1.1个 |
| 红豆馅料1136 | 10% | 70% | 20% | 0% | 0% | 1.1个 |
| 桂花馅料1137 | 10% | 70% | 20% | 0% | 0% | 1.1个 |
| 蛋莲馅料1138 | 10% | 70% | 20% | 0% | 0% | 1.1个 |

面粉2／3／4个三档各约33.333333%，按2026-10-30用户要求调整。馅料0／1／2个对应整数票号0—9／10—79／80—99；面粉票号0／1／2分别对应2／3／4个。0个不创建背包条目、不显示零数量奖励。

| 来源 | 触发单位 | 到账／显示 | 不产出的情况 |
|---|---|---|---|
| 普通旅途、精英旅途 | 每一场服务端判定胜利 | 关卡奖励，材料直接入包 | 战败、非法关卡、资源不足 |
| 普通／精英扫荡 | 每次成功扫荡中的每一场分别随机 | 批次按逐场结果结算 | 未解锁、不满足扫荡条件、无效批次 |
| 天命之战 | 每一关服务端判定胜利 | 即时掉落事件22，直接入包；不占用每三关银两领取流程 | 战败、错误关数／阶段、重复领奖 |
| 蟠桃会 | 每次有效免费或付费挑战 | 战斗奖励直接入包 | 非开放时段、挑战次数不足、费用不足等无效请求 |

蟠桃会沿用其参与挑战结算方式，挑战完成即可获材料，不要求击杀高血量Boss。查询界面、心跳、打开背包、查看战报不触发材料抽取。未增加其他玩法的材料产出，未启用月饼成品直接掉落。

每次有效结算总计面粉2—4个，四种馅料合计0—8个；长期均值为面粉3、馅料4.4，总材料7.4个。100次结算期望获得面粉300、各馅料110。面粉由四个配方共用，长期总制作产能约为每次3/15个月饼；“每种馅料都有掉落”不代表四个配方都能同时消耗同一份面粉。期望值不是短期保底。

## 3. 开箱的共同规则

每个池总权重10000。先按组权重抽一个组，再从该组明确列出的候选中等概率抽一个，固定发放表中数量。单候选组不需要第二次抽取。**最终概率＝组权重÷10000÷该组候选数**。下表既给组概率，也给每个具体候选的最终概率，重复出现的组概率不能逐行相加；所有“具体候选最终概率”合计100%。

无空奖、无额外元宝费用、无十连保底、无动态概率、无累计必出。连续开启N个独立抽N次，允许重复；展示时才合并同种同等级奖励。后端每次接受同一所选背包堆叠中的1—100个月饼，原客户端单次／批量入口沿用原有交互。旧四项固定奖励不再叠加发放。

对象类型5为道具／装备，6为法术，11为元宝，12为银两；货币的模板ID为0。所有成品、灵石、法术的初始等级均为1。数量为中奖后的固定值，不是在1到该数值之间再随机。

| 月饼 | 奖励组数 | 具体结果数 | 小传世金卡 | 大传世金卡 | 最终概率合计 |
|---|---:|---:|---:|---:|---:|
''']
    for tid,pool in r['pools'].items():
        groups=pool['groups'];lines.append(f"| {pool['name']}／{tid} | {len(groups)} | {sum(len(g['candidates']) for g in groups)} | 0.45% | 0.05% | 100% |\n")
    notes={
    '1130':'紫薯侧重日常消耗和乾坤袋。包子为1022、仙丹为1023，均为正常大份道具，中奖各2个，包子不使用小包子1020替代。四种乾坤袋发放的是完整袋子，不在月饼开奖时继续开袋。',
    '1131':'红豆按图包含一级灵石×2、三种精华×20、四／五星灵器、四档水晶、重铸符、五星碎片×5及稀有五星武器／防具。普通五星成品白名单取自通用五星武器碎片6002和防具碎片6003的合成候选，共10种，各0.01%，合计0.1%。不含五星法宝成品；五星法宝以6004碎片参与。四／五星灵器1313／1314是材料，不是装备。',
    '1132':'桂花的“四星及以下法术”采用实际可用的2—4星法术共34种：二星2种、三星11种、四星21种。1星表中的普通攻击、战斗基础效果、弹道、追踪和内部占位技能不作为背包法术奖励。五星主动法术11种共0.5%，不含五星被动成品；五星被动以6005通用碎片×5参与。五法界魂箱1249每次5个，按图中数量发放。',
    '1133':'蛋莲银两分为5万、15万、50万三档，概率30%、25%、10%；元宝20／50／100／200四档，概率18%、7%、2.5%、0.5%。仙晶1366和仙币1361各次20个，作为背包道具到账，沿用对应玩法的消费逻辑。'}
    for section,(tid,pool) in enumerate(r['pools'].items(),4):
        lines.append(f"\n## {section}. {pool['name']}完整奖励池\n\n{notes[tid]}\n\n")
        lines.append('| 组 | 具体奖励 | 对象类型／模板ID | 中奖数量 | 组权重 | 整组概率 | 候选数 | 该候选最终概率 |\n|---|---|---|---:|---:|---:|---:|---:|\n')
        total=Fraction(0)
        for index,g in enumerate(pool['groups'],1):
            for p in g['candidates']:
                final=Fraction(g['weight'],100*len(g['candidates']));total+=final
                lines.append(f"| {index:02} | {name(p)} | {p[0]}／{p[1]} | {p[2]:,} | {g['weight']} | {percent(Fraction(g['weight'],100))} | {len(g['candidates'])} | {percent(final)} |\n")
        assert total==100
        lines.append('\n所有具体候选最终概率精确合计100%；循环小数以分数表示的概率为准。\n')
    lines.append('''
## 8. 稀有奖励、后续使用与收益口径

- 小传世金卡为1156“传世金卡（小）”，每次1张，各池0.45%；大传世金卡为1152“传世金卡”，每次1张，各池0.05%。两类合计0.5%，小卡概率为大卡的9倍；约222.22次／2000次的倒数仅表示长期频率，不是承诺在该次数内获得。
- 金卡中奖时只发到背包，不自动使用、不自动增加充值额度或元宝；之后主动使用会执行当前金卡系统的原有规则。详见[金卡充值系统实现说明](金卡充值系统实现说明.md)。
- 紫薯四种袋子合计19.5%；其中VIP乾坤袋1%。月饼抽中VIP袋没有额外VIP条件，后续开袋仍受该道具现有使用要求约束。
- 红豆五星碎片三种各0.3%，合计0.9%，每次5片；五星武器／防具成品合计0.1%，每件具体装备0.01%。
- 桂花五星被动碎片0.5%，每次5片；五星主动法术成品合计0.5%，11种等概率，每种为1/22%≈0.04545455%。
- 乾坤袋、五法界魂箱、装备／法术碎片、金卡后续的开启、合成或使用不属于本次月饼抽奖，不把后续可能得到的奖品重复算入本池。

| 月饼 | 每个直接元宝期望 | 每个直接银两期望 | 其他重点期望 |
|---|---:|---:|---|
''')
    for tid,pool in r['pools'].items():
        gold=silver=Fraction(0)
        for g in pool['groups']:
            for p in g['candidates']:
                value=Fraction(g['weight']*p[2],10000*len(g['candidates']))
                if p[0]==11:gold+=value
                if p[0]==12:silver+=value
        more={'1130':'包子0.4个、仙丹0.36个','1131':'三类五星碎片合计0.045片','1132':'蟠桃2个、五法界魂箱0.15个','1133':'仙晶0.7个、仙币0.6个'}[tid]
        lines.append(f"| {pool['name']} | {float(gold):g} | {float(silver):g} | {more} |\n")
    lines.append('''
以上不计累计制作赠礼，不把金卡或其他道具折算为元宝，也不计其后续使用奖励。

## 9. 离线结算、存档和失败保护

随机源为Python `secrets.randbelow`，来自本机操作系统，不依赖公网或官方活动服务器，不使用固定日期、胜场轮换或角色名作为抽奖结果。四个奖池和材料规则加载在本地服务中。

- 制作、掉落、开箱均由后端判断并在角色副本中操作，客户端不能指定奖品、数量或结果。完成响应编码后统一保存；业务拒绝、发奖异常、协议编码异常不提交半份结果。
- 开箱严格校验所选库存ID、月饼类型、数量、等级、目标、锁定和占用标记；只扣所选堆叠，不从同类其他堆叠偷偷扣除。材料合成沿用未锁定且未被占用材料的合并消耗规则。
- 普通材料正常堆叠；装备、一级灵石和法术按独立库存ID发放。法术沿用项目原有`attach_type=6,count=0`实例表示，奖励弹窗的中奖数量仍为1；两颗一级灵石不会变成一颗二级灵石。
- 元宝、银两到账前验证不超过协议有符号32位上限2147483647；超限整次开箱拒绝，不扣月饼。
- 同一会话、同序号、同报文重传复用原响应，不再次随机、不重复扣除或发奖；同序号更换内容被拒绝。请求缓存不宣称跨服务重启永久有效。已消耗库存、余额和制作进度随角色存档保留。
- 关闭游戏期间没有自动战斗或挂机材料产出；这里的“离线”指不依赖远端官方服务，仍须运行本地游戏后端。
- 后续粽叶飘香已同步为同样的四池概率与数量、制作规则；两活动独立抽取材料和开箱结果，并各自累计制作进度。详见[粽叶飘香说明](粽叶飘香离线活动实现说明.md)。

## 10. 配置与接入文件

| 文件 | 作用 |
|---|---|
| [`moon_rules.json`](../server_config/moon_rules.json) | 四池分组、完整候选ID、数量、整数权重、材料分布 |
| [`activity_moon.py`](../network_redirect/activity_moon.py)、[`activity_food.py`](../network_redirect/activity_food.py) | 配置校验、本机抽奖、两活动共用的逐个开奖、指定堆叠扣除、类型化发奖 |
| [`activity_seasonal.py`](../network_redirect/activity_seasonal.py) | 常驻开关、一次性材料迁移、旅途掉落入口、制作和累计赠礼、月饼使用分发 |
| [`activity_party.py`](../network_redirect/activity_party.py) | 蟠桃会每次有效挑战材料结算 |
| [`activity_duty.py`](../network_redirect/activity_duty.py) | 天命每关胜利材料即时到账 |
| [`activity.py`](../network_redirect/activity.py) | 加载并校验中秋独立规则；旧固定配置只保留历史五星粽子1217 |
| [`moon_client.lua`](../network_redirect/moon_client.lua) | 原生界面常驻、删除倒计时图样及递归更新、制作开关和个人累计文案 |
| [`summon.py`](../network_redirect/summon.py)、[`summon_client.js`](../network_redirect/summon_client.js) | 安装和撤销Lua适配 |
| [`test_activity_moon.py`](../tests/test_activity_moon.py) | 概率全区间、108个候选实际到账、掉落来源、存档和异常回滚 |
| [`verify_moon_client.py`](../analysis/tools/verify_moon_client.py) | 原生Cocos客户端隔离验证与界面截图 |
| [`write_moon_doc.py`](../analysis/tools/write_moon_doc.py) | 从实际配置重新生成本文精确奖励表 |

`reward/candidates`规格为`[对象类型, 模板ID, 数量, 等级]`。奖池总权重必须为10000，禁止无效道具、重复候选、零数量或直接返回月饼及其原料。更改概率或数量后重启本地服务加载；既有库存不会追溯重抽。客户端常驻适配需重新连接离线注入或重新启动游戏。

沿用协议：活动状态 `1205 flag=0 → 47.midautumn_data`；进度查询 `1333 flag=0`；制作 `1333 flag=1,src_type=1135..1138 → 178`；背包开启 `1051 → 21.attach_list`。材料随原有战斗和背包同步到账，不新增客户端开奖协议。

## 11. 验证与复现

本次后端共188项通过（中秋专项13项、共享活动61项、天命37项、蟠桃会15项、旅途36项、召唤／注入26项）；原生客户端14项通过。后端使用临时SQLite存档验证，不修改真实账号。专项覆盖四池全部40000个组选择票号、各馅料100个票号和面粉三档、108个候选经真实1051协议逐项到账、批量独立抽取、装备／法术／灵石实例、非法请求、重传不重抽、发奖及编码失败回滚、余额上限、常驻开关、逐场扫荡、天命胜负和蟠桃会参与掉落。

客户端验证在已运行的原生Cocos游戏内创建隔离界面，替换库存读取并拦截所有游戏发送请求；验证后恢复原模块与界面。核对常驻提示、隐藏旧倒计时图样、不再递归计时、历史过期日期下的制作、四配方请求、开关、个人累计提示、四个月饼背包使用和奖励展示。

```sh
.runtime/venv/bin/python -m unittest discover -s tests -p 'test_activity_moon.py'
.runtime/venv/bin/python -m unittest discover -s tests -p 'test_activity.py'
.runtime/venv/bin/python -m unittest discover -s tests -p 'test_activity_duty.py'
.runtime/venv/bin/python -m unittest discover -s tests -p 'test_activity_party.py'
.runtime/venv/bin/python -m unittest discover -s tests -p 'test_journey.py'
.runtime/venv/bin/python -m unittest discover -s tests -p 'test_summon.py'
.runtime/venv/bin/python analysis/tools/verify_moon_client.py
.runtime/venv/bin/python analysis/tools/write_moon_doc.py
```

执行记录见[后端测试记录](../analysis/evidence/moon/backend_tests.log)、[原生客户端验证](../analysis/evidence/moon/client_validation.json)、[活动界面截图](../analysis/evidence/moon/main.png)。测试只验证当前实现和明确配置，不以少量随机样本反推或宣称官方概率。
''')
    path=ROOT/'docs/缘聚中秋离线活动实现说明.md';path.write_text(''.join(lines));print(path)


if __name__=='__main__':main()
