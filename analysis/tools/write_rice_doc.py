"""Generate complete Dragon Boat probabilities from the shared runtime pools."""
from fractions import Fraction
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from network_redirect import activity, activity_rice as rice, summon
from write_moon_doc import percent


def main():
    shared=activity.load_rules();rules=shared['moon_rules']
    names={int(x['Ftype_id']):x['name'] for x in summon.rows('item_name.csv')}
    skills={int(x['type_id']):x['name'] for x in summon.rows('skill_name.csv')}
    def name(p):return {11:'元宝',12:'银两'}.get(p[0]) or (skills if p[0]==6 else names)[p[1]]
    lines=['''# 粽叶飘香离线活动实现说明

2026-10-30 更新：四种月饼与四种粽子均支持在制作按钮中选择数量，一次制作1～min(可用材料、当日剩余额度、100)个。每个成品仍消耗通用材料15个和对应专用材料15个；每日额度及个人累计按实际制作数量推进，批量跨过多个10个门槛会一次发齐全部蟠桃奖励。面粉、粽叶改为2／3／4个各1/3，其他材料概率与成品奖池不变。

实现日期：2026-10-27（北京时间）。本次依据用户参考图实现，并严格沿用[缘聚中秋](缘聚中秋离线活动实现说明.md)的四个奖励池、数量、概率和制作规则。当前共享奖池版本为 `2026-10-31-red-bean-essence-20`。以下为本地离线规则，不是原服官方概率。

## 1. 与缘聚中秋的对应关系

| 粽子／ID | 对应月饼／ID | 奖励主题 | 奖励组数 | 具体结果数 |
|---|---|---|---:|---:|
| 碱水粽子1213 | 紫薯月饼1130 | 日常道具、乾坤袋、货币、金卡 | 11 | 11 |
| 红豆粽子1214 | 红豆月饼1131 | 装备材料、五星碎片、稀有成品、货币、金卡 | 21 | 30 |
| 咸肉粽子1215 | 桂花月饼1132 | 养成、召唤、法术、货币、金卡 | 15 | 56 |
| 五仁粽子1216 | 蛋莲月饼1133 | 三档银两、四档元宝、仙晶、仙币、金卡 | 11 | 11 |

两个活动直接读取同一份 `server_config/moon_rules.json`，粽子通过固定ID映射选择对应池；不另复制一套容易发生偏差的奖励配置。四池合计108个具体结果，**每个池最终概率均为100%**。

共用的是概率和数量，随机结果与进度各自独立：粽叶／糯米不会复制面粉／馅料的数量，开粽子也不会复用开月饼的奖品。每次都重新调用本机随机源，无相同种子初始化、固定轮换或“同一场两个活动必须同结果”的规则。

## 2. 常驻、赠料、配方和累计赠礼

`seasonal_games.rice.enabled=true` 时常驻开放，不再受历史 `start_time/end_time` 限制。原生界面取消旧倒计时图样和递归计时器，显示“常驻开放”。关闭粽子开关只关闭粽子材料和制作，不影响月饼；已有粽子仍可从背包开启。

| 配方序号 | 成品／ID | 消耗 | 确定产量 |
|---:|---|---|---:|
| 1 | 碱水粽子1213 | 飘香粽叶1208×15＋碱水糯米1209×15 | 1 |
| 2 | 红豆粽子1214 | 飘香粽叶1208×15＋红豆糯米1210×15 | 1 |
| 3 | 咸肉粽子1215 | 飘香粽叶1208×15＋咸肉糯米1211×15 | 1 |
| 4 | 五仁粽子1216 | 飘香粽叶1208×15＋五仁糯米1212×15 | 1 |

合法制作成功率100%，不随机改变品种。粽子原协议携带两个真实材料库存ID；后端确认两者属于该配方、未锁定／占用且各有15个，**只扣实际选中的两份库存**，不会改扣同类其他堆叠。

- 首次查询活动，新角色获飘香粽叶60、四种糯米各15，足够四种各做1个。标记 `rice:permanent`，每角色仅一次；重复查询、重启、修改旧活动日期不重发。
- 旧存档已有任意 `rice:开始时间` 领取标记时视为已经领取，保留原材料和成品，不补发、不回收。粽子赠料标记与月饼标记相互独立。
- 四种粽子合计每天最多制作100次，北京时间00:00刷新。月饼另有独立的100次额度，不互相占用。开启成品不消耗制作次数，材料和成品不在换日时清空。
- **个人每累计制作10个粽子，额外得到普通蟠桃1001×10**，第10、20、30……次制作即时发放。沿用月饼的赠礼门槛和数量，但用独立的 `rice_count`；月饼制作不会推进粽子累计，反之亦然。
- 累计进度跨日、重启保留。旧版未存可信的粽子终身制作总数，新字段首次建立为0，从升级后的成功制作开始累计，不据旧广播或背包库存猜测历史次数、追补奖励。

原版文案中的“制作时随机出现五星粽子”不属于此次四种粽子与四种月饼相同的机制，因此本次普通制作仍不生成1217。已持有的**五星粽子1217**继续保留原兼容规则：每个固定开出圣母蟠桃1343×1，可正常使用和展示；它不属于四个随机奖池。活动页旧的五星粽子概率提示已替换为个人累计赠礼说明。

## 3. 材料来源和独立概率

| 材料／ID | 掉0个 | 掉1个 | 掉2个 | 掉3个 | 掉4个 | 单次期望 |
|---|---:|---:|---:|---:|---:|---:|
| 飘香粽叶1208 | 0% | 0% | 1/3 | 1/3 | 1/3 | 3个 |
| 碱水糯米1209 | 10% | 70% | 20% | 0% | 0% | 1.1个 |
| 红豆糯米1210 | 10% | 70% | 20% | 0% | 0% | 1.1个 |
| 咸肉糯米1211 | 10% | 70% | 20% | 0% | 0% | 1.1个 |
| 五仁糯米1212 | 10% | 70% | 20% | 0% | 0% | 1.1个 |

粽叶2／3／4个三档各约33.333333%，按2026-10-30用户要求调整，与面粉完全一致。四种糯米每次**分别**独立判定；不是四选一，也不是四种合计最多2个。每次有效结算粽叶2—4个，糯米总计0—8个；抽中0个时不创建零数量物品。

| 来源 | 何时抽取 | 到账方式 |
|---|---|---|
| 普通／精英旅途 | 每场服务端判定胜利 | 与关卡掉落一同入包并显示 |
| 普通／精英扫荡 | 批次中每场分别抽取 | 每场结果汇总，整批失败时全部回滚 |
| 天命之战 | 每一关胜利 | 即时掉落事件22；不影响该玩法原有奖励领取阶段 |
| 蟠桃会 | 每次有效免费／付费挑战结算 | 与参与奖励一起入包；不要求击杀Boss |

旅途和天命战败不掉；无效请求、次数／资源不足、查询、心跳、查看背包或战报不抽取。未增加成品直接掉落或关闭游戏期间自动产料。

两个活动同时开放时，每次有效结算有**10次独立数量抽取**：粽叶1次＋四种糯米4次，面粉1次＋四种馅料4次。可同时获得两套材料，也可粽子糯米全部0而月饼馅料全部2。以碱水糯米和紫薯馅料为例，两者同为1个的概率为70%×70%=49%，同为2个为4%；不会因其中一项抽中2个而固定另一项也为2个。

每100次结算，粽子材料长期期望为粽叶300、四种糯米各110。月饼另行获得自己的材料，两套期望相同。粽叶由四配方共用，长期总制作产能约3/15个粽子／次，不是每种各3/15个；期望值不是短期保证。

## 4. 开箱与概率口径

每消耗1个粽子，先按总权重10000抽一个奖励组，再从该组中等概率抽一个具体候选。单候选组直接发奖。**指定候选最终概率＝组权重÷10000÷候选数**。固定发放表中数量，不在1到该数量之间再随机。

无空奖、额外收费、VIP开奖门槛、十连保底、动态概率或累计必出。后端支持单个所选库存堆叠中1—100个粽子一次使用；批量逐个独立抽取，最后合并同类同等级的展示条目，不能把“一次抽到的结果×开启数量”当作批量开奖。原生背包使用／批量入口沿用客户端原交互。

表中类型5为道具／装备，6为法术，11为元宝，12为银两；货币模板ID为0。所有成品、法术、灵石初始等级为1。整组概率会在同组多行中重复显示，不能逐行相加；逐行相加的是“该候选最终概率”。
''']
    notes={1213:'日常消耗池。包子1022×2、仙丹1023×2；乾坤袋作为完整道具发到背包。',
           1214:'装备池。三类一级灵石每次2颗，三类精华每次20个，三类五星碎片每次5片。五星武器／防具成品采用普通通用碎片的10种合成候选，总概率0.1%，每种0.01%。四／五星灵器为材料，不是装备成品。',
           1215:'养成与法术池。2—4星法术共34种，不发普通攻击及内部占位技能。五星主动法术11种合计0.5%；五星被动以6005碎片×5提供，不发五星被动成品。五法界魂箱每次5个。',
           1216:'财富池。银两三档，元宝四档；仙晶1366和仙币1361每次20个，作为背包道具，沿用对应玩法的消费方式。'}
    for section,(tid,mid) in enumerate(rice.FOOD_POOLS.items(),5):
        pool=rules['pools'][str(mid)]
        lines.append(f'\n## {section}. {names[tid]}完整奖励池\n\n{notes[tid]}与{names[mid]}每一项数量、概率相同。\n\n')
        lines.append('| 组 | 具体奖励 | 对象类型／模板ID | 中奖数量 | 组权重 | 整组概率 | 候选数 | 该候选最终概率 |\n|---|---|---|---:|---:|---:|---:|---:|\n')
        total=Fraction(0)
        for index,g in enumerate(pool['groups'],1):
            for p in g['candidates']:
                chance=Fraction(g['weight'],100*len(g['candidates']));total+=chance
                lines.append(f"| {index:02} | {name(p)} | {p[0]}／{p[1]} | {p[2]:,} | {g['weight']} | {percent(Fraction(g['weight'],100))} | {len(g['candidates'])} | {percent(chance)} |\n")
        assert total==100
        lines.append('\n该池所有具体候选最终概率精确合计100%；循环小数以表内分数为准。\n')
    lines.append('''
## 9. 稀有奖励和后续使用

- 每池小传世金卡1156×1为0.45%，大传世金卡1152×1为0.05%，合计0.5%。中奖只发金卡，不自动使用或增加充值进度；后续主动使用沿用[金卡系统](金卡充值系统实现说明.md)。
- 红豆粽子：三类五星碎片各0.3%，合计0.9%；10种普通五星武器／防具成品合计0.1%。不发五星法宝成品，五星法宝通过碎片6004参与。
- 咸肉粽子：五星被动碎片×5为0.5%；五星主动成品总计0.5%，每种为1/22%≈0.04545455%。
- 碱水粽子的四种乾坤袋合计19.5%，其中VIP乾坤袋1%。抽中袋子无需VIP，后续开袋仍遵守该道具的现有要求。
- 乾坤袋、五法界魂箱、碎片和金卡的后续使用／合成另行结算，不重复计入粽子本轮100%奖池，不在粽子开奖时自动打开。
- 个人累计制作赠送的蟠桃独立于开箱，不改变四个奖池概率。连续获得重复奖励是独立抽样允许的正常情况。

| 粽子 | 每个直接元宝期望 | 每个直接银两期望 | 其他重点期望 |
|---|---:|---:|---|
''')
    for tid,mid in rice.FOOD_POOLS.items():
        sums={11:Fraction(0),12:Fraction(0)}
        for g in rules['pools'][str(mid)]['groups']:
            for p in g['candidates']:
                if p[0] in sums:sums[p[0]]+=Fraction(g['weight']*p[2],10000*len(g['candidates']))
        more={1213:'包子0.4个，仙丹0.36个',1214:'三类五星碎片合计0.045片',1215:'蟠桃2个，五法界魂箱0.15个',1216:'仙晶0.7个，仙币0.6个'}[tid]
        lines.append(f'| {names[tid]} | {float(sums[11]):g} | {float(sums[12]):g} | {more} |\n')
    lines.append('''
上述期望不折算金卡或容器价值，不含累计制作赠礼。

## 10. 离线结算和数据保护

随机源是Python `secrets.randbelow`，来自本机操作系统，不依赖公网或官方服务器。两个活动各自调用随机函数，仅共用静态奖池；关闭一个活动不会触发该活动的任何材料抽取，也不会关闭另一个活动。

制作、战斗掉落、使用均在后端角色副本上完成，校验及响应编码成功后再提交存档。每次开箱严格验证类型、库存ID、数量、等级、目标及锁定／占用状态，只扣指定堆叠。数量错误、材料不足、发奖错误、响应编码失败、货币超过2147483647时不提交消耗或部分奖励。

材料允许正常堆叠；装备、一级灵石和法术分别建立独立库存ID。两颗一级灵石保持两颗1级物品，不合并成2级；法术沿用现有实例表示，背包数据中的`count=0`并不表示发奖0个，奖励数量仍为1。

同一会话、同序号、同报文重传使用已缓存的响应，不再次抽取或发奖；相同序号换内容会被拒绝。请求缓存不保证跨服务重启继续存在，已经提交的库存、货币和累计进度由SQLite保存。所有正常游戏操作仍需要本地后端运行；关闭程序期间不会凭空生成战斗掉落。

原客户端对月饼有专门的开箱展示分支，对粽子没有同样的分支。本次补上1213—1217成功使用后的背包单元更新和原生奖励弹窗，展示服务端 `attach_list`；展示回调不重新抽奖、不发业务请求、不自行给角色加资源。其他道具和月饼仍交给原有回调处理。

## 11. 接入与配置

| 文件 | 作用 |
|---|---|
| [`moon_rules.json`](../server_config/moon_rules.json) | 两活动共用的108项奖励和材料数量分布 |
| [`activity_rice.py`](../network_redirect/activity_rice.py) | 四种粽子映射、独立随机调用、独立累计进度、客户端参数 |
| [`activity_food.py`](../network_redirect/activity_food.py) | 共用加权抽取、材料数量抽取、逐个开箱、指定堆叠扣除与发奖 |
| [`activity_moon.py`](../network_redirect/activity_moon.py) | 保留月饼入口与概率校验，调用相同共用机制 |
| [`activity_seasonal.py`](../network_redirect/activity_seasonal.py) | 两活动独立材料结算、常驻、赠料迁移、配方、累计赠礼 |
| [`activity_duty.py`](../network_redirect/activity_duty.py)、[`activity_party.py`](../network_redirect/activity_party.py) | 天命与蟠桃会使用统一的双活动材料入口 |
| [`activity_rules.json`](../server_config/activity_rules.json) | 独立开关；共用制作上限、累计赠礼数值；仅保留1217兼容固定奖励 |
| [`rice_client.lua`](../network_redirect/rice_client.lua) | 常驻界面、个人累计提示、取消倒计时、粽子开奖展示 |
| [`summon.py`](../network_redirect/summon.py)、[`summon_client.js`](../network_redirect/summon_client.js) | 安装和撤销客户端适配 |
| [`test_activity_rice.py`](../tests/test_activity_rice.py) | 108个候选实际到账、概率区间、双活动独立性及异常保护 |
| [`verify_rice_client.py`](../analysis/tools/verify_rice_client.py) | 原生Cocos隔离验证与截图 |
| [`write_rice_doc.py`](../analysis/tools/write_rice_doc.py) | 从实际奖池重新生成本文完整奖励表 |

为保持两个活动完全一致，粽子沿用 `seasonal_craft_daily_limit=100`、`seasonal_moon_bonus_every=10`、`seasonal_moon_bonus=[[5,1001,10,1]]`；最后两个键虽保留历史moon名称，现作为两活动共用数值，**进度并不共用**。每日计数分别为 `rice:日期`、`moon:日期`，终身计数分别为 `rice_count`、`moon_count`。

旧的 `seasonal_travel_material_count` 固定轮换配置和1213—1216固定开箱奖励已删除，避免与随机奖池并行。共享奖池校验禁止直接发两活动的成品和原料，避免自我生成开箱材料。

协议保持原版：状态 `1205 flag=0 → 47.dragon_boat_info`；制作 `1126 compose_type=1..4,material_count=2,material_list=[{id},{id}] → 126`；使用 `1051 → 21.attach_list`。状态附加常驻开关及 `rice_count/cur_process/left_process`，制作响应附加 `local_rice_progress`。无须替换APK资源，重新启动本地离线游戏即可加载新代码、配置和Lua适配。

## 12. 验证与复现

本次共207项后端测试通过（粽子专项13项、月饼回归13项、共享活动／蟠桃会／旅途／召唤138项、天命43项）；原生客户端16项通过。后端验证使用临时SQLite账号，覆盖：四池40000个组权重票号、108个候选真实1051协议到账、独立材料数量区间、两个活动同时掉落的不同结果、独立开关、批量100次、独立累计及每日上限、指定库存消耗、旧存档迁移、重传、重启、超限／异常回滚、旅途／扫荡／天命／蟠桃会来源与历史五星粽子。

原生Cocos验证使用临时界面并拦截游戏发送，核对四个配方、常驻和历史过期日期、关闭开关、累计赠礼、四粽子背包入口、随机奖励弹窗、历史五星粽子和月饼原有回调。结束后恢复原界面及模块，没有修改真实账号资源；截图已进行目视检查。

```sh
.runtime/venv/bin/python -m unittest discover -s tests -p 'test_activity_rice.py'
.runtime/venv/bin/python -m unittest discover -s tests -p 'test_activity_moon.py'
PYTHONPATH=tests .runtime/venv/bin/python -m unittest test_activity test_activity_party test_journey test_summon
.runtime/venv/bin/python -m unittest discover -s tests -p 'test_activity_duty.py'
.runtime/venv/bin/python analysis/tools/verify_rice_client.py
.runtime/venv/bin/python analysis/tools/write_rice_doc.py
```

证据：[粽子后端专项](../analysis/evidence/rice/backend_tests.log)、[月饼回归](../analysis/evidence/rice/moon_regression.log)、[共享活动／旅途／召唤回归](../analysis/evidence/rice/shared_regression.log)、[天命回归](../analysis/evidence/rice/duty_regression.log)、[客户端检查](../analysis/evidence/rice/client_validation.json)、[活动截图](../analysis/evidence/rice/main.png)。概率以配置中的精确权重为准，不能根据少量实际开箱样本反推固定轮换或保底。
''')
    path=ROOT/'docs/粽叶飘香离线活动实现说明.md';path.write_text(''.join(lines));print(path)


if __name__=='__main__':main()
