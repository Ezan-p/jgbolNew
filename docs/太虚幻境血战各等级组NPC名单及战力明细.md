# 太虚幻境血战各等级组NPC名单及战力明细

生成日期：2026-11-10。配置版本：`offline-taixu-6`。本文对应调整后的新赛程名单。

## 1. 名单范围与战力口径

本文列出四个等级组共76个NPC席位：每组固定最强15名，共60名；另列2026-11-09赛周各组抽取的4名普通NPC，共16名。每个组另有玩家本人，合计20名参赛者；玩家战力随账号变化，未列入NPC表。

样本赛周为**北京时间2026-11-09 00:00至2026-11-16 00:00之前**。前15名在本地NPC库不变时不随赛周更换；第16—19名仅代表该赛周抽样结果。已开赛旧档保留原名单，正常跨周后再按新规则生成，不能用本表反推旧档一定已有这些对手。

- **初始名次**：新届冲榜开始时的NPC位置，不是最终排名。玩家初始第20名；比赛后继续按积分、赛事血量更新排名。
- **角色等级**：分组依据，四组分别是50—59、60—69、70—79、80—99级；不是神仙等级。
- **目录／榜单战力**：正式NPC资料中的 `role_combat_power`，当前用于血战选人与榜单显示。
- **当前实际战力**：通过 `npc_players.get()` 加载完整养成并使用当前引擎重算得到，等于八名上阵神仙战力之和。该值是阵容指标，不代表任何一场战斗必胜。
- **差值**：实际战力减目录战力。部分普通NPC目录留有少量历史差异；四组全部候选已重算核对，前15名身份与顺序均一致。本次没有改写共享NPC库。
- **T／E档和倾向**：沿用本地设计标记；T为普通设计档、E为极高战力档，倾向表示设计侧重。各组前15名按战力选取，不按档位分配固定名额。
- **玩家ID**：阵容查看、挑战与战报使用的正式身份；附录另列内部NPC编号和原始阵容文件。

## 2. 四组概览

| 等级组 | 正式候选数 | 第1名／实际战力 | 第15名／实际战力 | 前15名战力合计 | 前15名平均战力 |
| --- | --- | --- | --- | --- | --- |
| 50—59级（组4） | 165 | 隐泉雨松／642,308 | 栖鹤鹤长／482,714 | 7,921,864 | 528,124.27 |
| 60—69级（组5） | 180 | 问道河长／1,281,223 | 踏雪云清／921,167 | 15,218,435 | 1,014,562.33 |
| 70—79级（组6） | 165 | 朝露山琴／1,561,732 | 远山苍长／1,085,263 | 17,929,943 | 1,195,329.53 |
| 80—99级（组7） | 445 | 太初劫锋／45,077,029 | 玉衡守真／28,053,194 | 490,196,700 | 32,679,780.00 |

最高组当前最强15名全部为99级E1档NPC；其余三组的最强15名均为本组普通T1档NPC。以下所有战力均给出整数原值，避免以“万”取整掩盖差异。

## 3. 50—59级组完整名单（内部组号4）

### 3.1 固定最强15名

| 初始名次 | NPC姓名 | 角色等级 | 设计档 | 倾向 | 目录／榜单战力 | 当前实际战力 | 差值 | 正式玩家ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 隐泉雨松 | 50 | T1 | 攻击 | 642,308 | 642,308 | 0 | `718527076` |
| 2 | 寒江鹤青 | 59 | T1 | 攻击 | 628,216 | 628,216 | 0 | `782696994` |
| 3 | 凌波竹鹤 | 58 | T1 | 攻击 | 588,425 | 588,425 | 0 | `772701571` |
| 4 | 浮岚雨霜 | 52 | T1 | 攻击 | 546,645 | 546,645 | 0 | `713504617` |
| 5 | 寒江雪苍 | 56 | T1 | 生存 | 538,662 | 538,662 | 0 | `751412591` |
| 6 | 隐泉川空 | 58 | T1 | 生存 | 521,491 | 521,491 | 0 | `752651595` |
| 7 | 观海苍剑 | 58 | T1 | 法术 | 512,474 | 512,474 | 0 | `788288266` |
| 8 | 踏雪花松 | 59 | T1 | 法术 | 505,648 | 505,648 | 0 | `742449378` |
| 9 | 寒江长星 | 54 | T1 | 攻击 | 503,671 | 503,671 | 0 | `756125867` |
| 10 | 观海松川 | 56 | T1 | 攻击 | 495,995 | 495,995 | 0 | `743062440` |
| 11 | 观海河玉 | 53 | T1 | 攻击 | 491,164 | 491,164 | 0 | `775532453` |
| 12 | 望月瑶水 | 57 | T1 | 攻击 | 490,716 | 490,716 | 0 | `729827923` |
| 13 | 寻仙清月 | 50 | T1 | 攻击 | 489,993 | 489,993 | 0 | `744637678` |
| 14 | 流霞明岚 | 59 | T1 | 生存 | 483,742 | 483,742 | 0 | `726088256` |
| 15 | 栖鹤鹤长 | 55 | T1 | 攻击 | 482,714 | 482,714 | 0 | `711241713` |

### 3.2 本赛周普通NPC补充席位

以下4名来自排除固定前15名后的普通T档池，按战力分成4段，每段抽取1名。新赛周可能更换。

| 初始名次 | NPC姓名 | 角色等级 | 设计档 | 倾向 | 目录／榜单战力 | 当前实际战力 | 差值 | 正式玩家ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 16 | 流霞清风 | 56 | T1 | 法术 | 456,285 | 456,285 | 0 | `772127433` |
| 17 | 落星竹剑 | 53 | T3 | 生存 | 150,569 | 150,569 | 0 | `735737935` |
| 18 | 云溪竹瑶 | 55 | T4 | 攻击 | 96,039 | 96,039 | 0 | `706577896` |
| 19 | 清霜青霜 | 50 | T4 | 法术 | 65,127 | 65,127 | 0 | `737412328` |

### 3.3 身份与阵容来源对照

名次与本组上表一一对应。来源链接为只读原始设计快照；同一聚合文件内用内部NPC编号定位具体角色。

| 初始名次 | NPC姓名 | 内部NPC编号 | 原始阵容来源 |
| --- | --- | --- | --- |
| 1 | 隐泉雨松 | `npc_v1_l50_t1_attack` | [analysis/npc_design/v1/catalog.json](../analysis/npc_design/v1/catalog.json) |
| 2 | 寒江鹤青 | `npc_v2_l59_t1_attack` | [analysis/npc_design/v2/levels/level_59.json](../analysis/npc_design/v2/levels/level_59.json) |
| 3 | 凌波竹鹤 | `npc_v2_l58_t1_attack` | [analysis/npc_design/v2/levels/level_58.json](../analysis/npc_design/v2/levels/level_58.json) |
| 4 | 浮岚雨霜 | `npc_v2_l52_t1_attack` | [analysis/npc_design/v2/levels/level_52.json](../analysis/npc_design/v2/levels/level_52.json) |
| 5 | 寒江雪苍 | `npc_v2_l56_t1_endurance` | [analysis/npc_design/v2/levels/level_56.json](../analysis/npc_design/v2/levels/level_56.json) |
| 6 | 隐泉川空 | `npc_v2_l58_t1_endurance` | [analysis/npc_design/v2/levels/level_58.json](../analysis/npc_design/v2/levels/level_58.json) |
| 7 | 观海苍剑 | `npc_v2_l58_t1_magic` | [analysis/npc_design/v2/levels/level_58.json](../analysis/npc_design/v2/levels/level_58.json) |
| 8 | 踏雪花松 | `npc_v2_l59_t1_magic` | [analysis/npc_design/v2/levels/level_59.json](../analysis/npc_design/v2/levels/level_59.json) |
| 9 | 寒江长星 | `npc_v2_l54_t1_attack` | [analysis/npc_design/v2/levels/level_54.json](../analysis/npc_design/v2/levels/level_54.json) |
| 10 | 观海松川 | `npc_v2_l56_t1_attack` | [analysis/npc_design/v2/levels/level_56.json](../analysis/npc_design/v2/levels/level_56.json) |
| 11 | 观海河玉 | `npc_v2_l53_t1_attack` | [analysis/npc_design/v2/levels/level_53.json](../analysis/npc_design/v2/levels/level_53.json) |
| 12 | 望月瑶水 | `npc_v2_l57_t1_attack` | [analysis/npc_design/v2/levels/level_57.json](../analysis/npc_design/v2/levels/level_57.json) |
| 13 | 寻仙清月 | `npc_v2_l50_t1_attack` | [analysis/npc_design/v2/levels/level_50.json](../analysis/npc_design/v2/levels/level_50.json) |
| 14 | 流霞明岚 | `npc_v2_l59_t1_endurance` | [analysis/npc_design/v2/levels/level_59.json](../analysis/npc_design/v2/levels/level_59.json) |
| 15 | 栖鹤鹤长 | `npc_v2_l55_t1_attack` | [analysis/npc_design/v2/levels/level_55.json](../analysis/npc_design/v2/levels/level_55.json) |
| 16 | 流霞清风 | `npc_v2_l56_t1_magic` | [analysis/npc_design/v2/levels/level_56.json](../analysis/npc_design/v2/levels/level_56.json) |
| 17 | 落星竹剑 | `npc_v2_l53_t3_endurance` | [analysis/npc_design/v2/levels/level_53.json](../analysis/npc_design/v2/levels/level_53.json) |
| 18 | 云溪竹瑶 | `npc_v2_l55_t4_attack` | [analysis/npc_design/v2/levels/level_55.json](../analysis/npc_design/v2/levels/level_55.json) |
| 19 | 清霜青霜 | `npc_v2_l50_t4_magic` | [analysis/npc_design/v2/levels/level_50.json](../analysis/npc_design/v2/levels/level_50.json) |

## 4. 60—69级组完整名单（内部组号5）

### 4.1 固定最强15名

| 初始名次 | NPC姓名 | 角色等级 | 设计档 | 倾向 | 目录／榜单战力 | 当前实际战力 | 差值 | 正式玩家ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 问道河长 | 65 | T1 | 攻击 | 1,281,223 | 1,281,223 | 0 | `711150473` |
| 2 | 观海星秋 | 60 | T1 | 攻击 | 1,197,265 | 1,197,258 | -7 | `785968658` |
| 3 | 寒江玄川 | 69 | T1 | 攻击 | 1,141,419 | 1,141,417 | -2 | `766682553` |
| 4 | 松间瑶海 | 66 | T1 | 攻击 | 1,067,566 | 1,067,560 | -6 | `732404537` |
| 5 | 长歌山松 | 68 | T1 | 攻击 | 1,001,307 | 1,001,303 | -4 | `745864108` |
| 6 | 青云苍松 | 67 | T1 | 攻击 | 987,986 | 987,986 | 0 | `772971343` |
| 7 | 朝露归水 | 63 | T1 | 攻击 | 982,431 | 982,431 | 0 | `795319500` |
| 8 | 观海山水 | 67 | T1 | 法术 | 973,427 | 973,422 | -5 | `765080855` |
| 9 | 望月鹤风 | 69 | T1 | 法术 | 965,337 | 965,328 | -9 | `781818573` |
| 10 | 长歌云岚 | 61 | T1 | 攻击 | 950,099 | 950,099 | 0 | `711466373` |
| 11 | 远山竹长 | 63 | T1 | 生存 | 942,131 | 942,129 | -2 | `790221365` |
| 12 | 清霜秋云 | 66 | T1 | 生存 | 941,476 | 941,472 | -4 | `797516611` |
| 13 | 松间霜山 | 64 | T1 | 攻击 | 934,944 | 934,940 | -4 | `772997173` |
| 14 | 寒江青雨 | 65 | T1 | 攻击 | 930,703 | 930,700 | -3 | `741377990` |
| 15 | 踏雪云清 | 68 | T1 | 生存 | 921,178 | 921,167 | -11 | `737259034` |

### 4.2 本赛周普通NPC补充席位

以下4名来自排除固定前15名后的普通T档池，按战力分成4段，每段抽取1名。新赛周可能更换。

| 初始名次 | NPC姓名 | 角色等级 | 设计档 | 倾向 | 目录／榜单战力 | 当前实际战力 | 差值 | 正式玩家ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 16 | 问道川花 | 67 | T2 | 生存 | 428,932 | 428,932 | 0 | `763632431` |
| 17 | 问道玄秋 | 65 | T3 | 生存 | 215,168 | 215,168 | 0 | `792036961` |
| 18 | 长歌归秋 | 65 | T4 | 生存 | 87,350 | 87,350 | 0 | `761116800` |
| 19 | 凌波云清 | 65 | T5 | 法术 | 34,721 | 34,721 | 0 | `718730444` |

### 4.3 身份与阵容来源对照

名次与本组上表一一对应。来源链接为只读原始设计快照；同一聚合文件内用内部NPC编号定位具体角色。

| 初始名次 | NPC姓名 | 内部NPC编号 | 原始阵容来源 |
| --- | --- | --- | --- |
| 1 | 问道河长 | `npc_v1_l65_t1_attack` | [analysis/npc_design/v1/catalog.json](../analysis/npc_design/v1/catalog.json) |
| 2 | 观海星秋 | `npc_v1_l60_t1_attack` | [analysis/npc_design/v1/catalog.json](../analysis/npc_design/v1/catalog.json) |
| 3 | 寒江玄川 | `npc_v2_l69_t1_attack` | [analysis/npc_design/v2/levels/level_69.json](../analysis/npc_design/v2/levels/level_69.json) |
| 4 | 松间瑶海 | `npc_v2_l66_t1_attack` | [analysis/npc_design/v2/levels/level_66.json](../analysis/npc_design/v2/levels/level_66.json) |
| 5 | 长歌山松 | `npc_v2_l68_t1_attack` | [analysis/npc_design/v2/levels/level_68.json](../analysis/npc_design/v2/levels/level_68.json) |
| 6 | 青云苍松 | `npc_v2_l67_t1_attack` | [analysis/npc_design/v2/levels/level_67.json](../analysis/npc_design/v2/levels/level_67.json) |
| 7 | 朝露归水 | `npc_v2_l63_t1_attack` | [analysis/npc_design/v2/levels/level_63.json](../analysis/npc_design/v2/levels/level_63.json) |
| 8 | 观海山水 | `npc_v2_l67_t1_magic` | [analysis/npc_design/v2/levels/level_67.json](../analysis/npc_design/v2/levels/level_67.json) |
| 9 | 望月鹤风 | `npc_v2_l69_t1_magic` | [analysis/npc_design/v2/levels/level_69.json](../analysis/npc_design/v2/levels/level_69.json) |
| 10 | 长歌云岚 | `npc_v2_l61_t1_attack` | [analysis/npc_design/v2/levels/level_61.json](../analysis/npc_design/v2/levels/level_61.json) |
| 11 | 远山竹长 | `npc_v2_l63_t1_endurance` | [analysis/npc_design/v2/levels/level_63.json](../analysis/npc_design/v2/levels/level_63.json) |
| 12 | 清霜秋云 | `npc_v2_l66_t1_endurance` | [analysis/npc_design/v2/levels/level_66.json](../analysis/npc_design/v2/levels/level_66.json) |
| 13 | 松间霜山 | `npc_v2_l64_t1_attack` | [analysis/npc_design/v2/levels/level_64.json](../analysis/npc_design/v2/levels/level_64.json) |
| 14 | 寒江青雨 | `npc_v2_l65_t1_attack` | [analysis/npc_design/v2/levels/level_65.json](../analysis/npc_design/v2/levels/level_65.json) |
| 15 | 踏雪云清 | `npc_v2_l68_t1_endurance` | [analysis/npc_design/v2/levels/level_68.json](../analysis/npc_design/v2/levels/level_68.json) |
| 16 | 问道川花 | `npc_v2_l67_t2_endurance` | [analysis/npc_design/v2/levels/level_67.json](../analysis/npc_design/v2/levels/level_67.json) |
| 17 | 问道玄秋 | `npc_v2_l65_t3_endurance` | [analysis/npc_design/v2/levels/level_65.json](../analysis/npc_design/v2/levels/level_65.json) |
| 18 | 长歌归秋 | `npc_v1_l65_t4_endurance` | [analysis/npc_design/v1/catalog.json](../analysis/npc_design/v1/catalog.json) |
| 19 | 凌波云清 | `npc_v2_l65_t5_magic` | [analysis/npc_design/v2/levels/level_65.json](../analysis/npc_design/v2/levels/level_65.json) |

## 5. 70—79级组完整名单（内部组号6）

### 5.1 固定最强15名

| 初始名次 | NPC姓名 | 角色等级 | 设计档 | 倾向 | 目录／榜单战力 | 当前实际战力 | 差值 | 正式玩家ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 朝露山琴 | 70 | T1 | 攻击 | 1,561,737 | 1,561,732 | -5 | `716380367` |
| 2 | 醉竹玉琴 | 76 | T1 | 攻击 | 1,298,345 | 1,298,343 | -2 | `765298766` |
| 3 | 云溪清雨 | 79 | T1 | 攻击 | 1,292,963 | 1,292,962 | -1 | `772462451` |
| 4 | 听雨星海 | 78 | T1 | 攻击 | 1,255,040 | 1,255,032 | -8 | `719657834` |
| 5 | 醉竹山松 | 74 | T1 | 攻击 | 1,198,112 | 1,198,103 | -9 | `703811439` |
| 6 | 醉竹岚长 | 72 | T1 | 攻击 | 1,173,090 | 1,173,082 | -8 | `716259545` |
| 7 | 凌波剑水 | 75 | T1 | 攻击 | 1,172,362 | 1,172,361 | -1 | `786886184` |
| 8 | 观海水长 | 76 | T1 | 生存 | 1,160,726 | 1,160,723 | -3 | `713952469` |
| 9 | 朝露岚归 | 70 | T1 | 攻击 | 1,157,566 | 1,157,566 | 0 | `798895414` |
| 10 | 松间雪川 | 73 | T1 | 攻击 | 1,138,338 | 1,138,332 | -6 | `768975930` |
| 11 | 松间雪月 | 75 | T1 | 法术 | 1,125,009 | 1,125,008 | -1 | `725547561` |
| 12 | 落星长琴 | 75 | T1 | 生存 | 1,109,295 | 1,109,284 | -11 | `722904837` |
| 13 | 长歌水秋 | 77 | T1 | 攻击 | 1,102,174 | 1,102,171 | -3 | `777056327` |
| 14 | 清霜河月 | 79 | T1 | 法术 | 1,099,987 | 1,099,981 | -6 | `750607158` |
| 15 | 远山苍长 | 71 | T1 | 攻击 | 1,085,266 | 1,085,263 | -3 | `763380605` |

### 5.2 本赛周普通NPC补充席位

以下4名来自排除固定前15名后的普通T档池，按战力分成4段，每段抽取1名。新赛周可能更换。

| 初始名次 | NPC姓名 | 角色等级 | 设计档 | 倾向 | 目录／榜单战力 | 当前实际战力 | 差值 | 正式玩家ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 16 | 流霞鹤月 | 73 | T1 | 法术 | 987,066 | 987,060 | -6 | `797872385` |
| 17 | 飞白雨川 | 77 | T3 | 法术 | 237,875 | 237,873 | -2 | `709465928` |
| 18 | 清霜月风 | 74 | T4 | 攻击 | 102,385 | 102,385 | 0 | `783522304` |
| 19 | 临风长明 | 76 | T5 | 法术 | 42,565 | 42,565 | 0 | `710891652` |

### 5.3 身份与阵容来源对照

名次与本组上表一一对应。来源链接为只读原始设计快照；同一聚合文件内用内部NPC编号定位具体角色。

| 初始名次 | NPC姓名 | 内部NPC编号 | 原始阵容来源 |
| --- | --- | --- | --- |
| 1 | 朝露山琴 | `npc_v1_l70_t1_attack` | [analysis/npc_design/v1/catalog.json](../analysis/npc_design/v1/catalog.json) |
| 2 | 醉竹玉琴 | `npc_v2_l76_t1_attack` | [analysis/npc_design/v2/levels/level_76.json](../analysis/npc_design/v2/levels/level_76.json) |
| 3 | 云溪清雨 | `npc_v2_l79_t1_attack` | [analysis/npc_design/v2/levels/level_79.json](../analysis/npc_design/v2/levels/level_79.json) |
| 4 | 听雨星海 | `npc_v2_l78_t1_attack` | [analysis/npc_design/v2/levels/level_78.json](../analysis/npc_design/v2/levels/level_78.json) |
| 5 | 醉竹山松 | `npc_v2_l74_t1_attack` | [analysis/npc_design/v2/levels/level_74.json](../analysis/npc_design/v2/levels/level_74.json) |
| 6 | 醉竹岚长 | `npc_v2_l72_t1_attack` | [analysis/npc_design/v2/levels/level_72.json](../analysis/npc_design/v2/levels/level_72.json) |
| 7 | 凌波剑水 | `npc_v2_l75_t1_attack` | [analysis/npc_design/v2/levels/level_75.json](../analysis/npc_design/v2/levels/level_75.json) |
| 8 | 观海水长 | `npc_v2_l76_t1_endurance` | [analysis/npc_design/v2/levels/level_76.json](../analysis/npc_design/v2/levels/level_76.json) |
| 9 | 朝露岚归 | `npc_v2_l70_t1_attack` | [analysis/npc_design/v2/levels/level_70.json](../analysis/npc_design/v2/levels/level_70.json) |
| 10 | 松间雪川 | `npc_v2_l73_t1_attack` | [analysis/npc_design/v2/levels/level_73.json](../analysis/npc_design/v2/levels/level_73.json) |
| 11 | 松间雪月 | `npc_v2_l75_t1_magic` | [analysis/npc_design/v2/levels/level_75.json](../analysis/npc_design/v2/levels/level_75.json) |
| 12 | 落星长琴 | `npc_v2_l75_t1_endurance` | [analysis/npc_design/v2/levels/level_75.json](../analysis/npc_design/v2/levels/level_75.json) |
| 13 | 长歌水秋 | `npc_v2_l77_t1_attack` | [analysis/npc_design/v2/levels/level_77.json](../analysis/npc_design/v2/levels/level_77.json) |
| 14 | 清霜河月 | `npc_v2_l79_t1_magic` | [analysis/npc_design/v2/levels/level_79.json](../analysis/npc_design/v2/levels/level_79.json) |
| 15 | 远山苍长 | `npc_v2_l71_t1_attack` | [analysis/npc_design/v2/levels/level_71.json](../analysis/npc_design/v2/levels/level_71.json) |
| 16 | 流霞鹤月 | `npc_v2_l73_t1_magic` | [analysis/npc_design/v2/levels/level_73.json](../analysis/npc_design/v2/levels/level_73.json) |
| 17 | 飞白雨川 | `npc_v2_l77_t3_magic` | [analysis/npc_design/v2/levels/level_77.json](../analysis/npc_design/v2/levels/level_77.json) |
| 18 | 清霜月风 | `npc_v2_l74_t4_attack` | [analysis/npc_design/v2/levels/level_74.json](../analysis/npc_design/v2/levels/level_74.json) |
| 19 | 临风长明 | `npc_v2_l76_t5_magic` | [analysis/npc_design/v2/levels/level_76.json](../analysis/npc_design/v2/levels/level_76.json) |

## 6. 80—99级组完整名单（内部组号7）

### 6.1 固定最强15名

| 初始名次 | NPC姓名 | 角色等级 | 设计档 | 倾向 | 目录／榜单战力 | 当前实际战力 | 差值 | 正式玩家ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 太初劫锋 | 99 | E1 | 攻击 | 45,077,029 | 45,077,029 | 0 | `776294836` |
| 2 | 灵墟守真 | 99 | E1 | assault | 35,851,975 | 35,851,975 | 0 | `719714127` |
| 3 | 玉衡问剑 | 99 | E1 | assault | 35,718,182 | 35,718,182 | 0 | `778136261` |
| 4 | 玉衡归云 | 99 | E1 | counter | 33,868,813 | 33,868,813 | 0 | `709042817` |
| 5 | 灵墟观海 | 99 | E1 | sustain | 33,144,362 | 33,144,362 | 0 | `794978414` |
| 6 | 玉衡逐星 | 99 | E1 | sustain | 32,888,808 | 32,888,808 | 0 | `737182431` |
| 7 | 玉衡临风 | 99 | E1 | assault | 32,369,054 | 32,369,054 | 0 | `776564311` |
| 8 | 灵墟归云 | 99 | E1 | hybrid | 31,932,931 | 31,932,931 | 0 | `777837872` |
| 9 | 灵墟临风 | 99 | E1 | counter | 31,721,589 | 31,721,589 | 0 | `739843162` |
| 10 | 玉衡听澜 | 99 | E1 | spell | 31,565,968 | 31,565,968 | 0 | `740385499` |
| 11 | 灵墟破晓 | 99 | E1 | reserve | 30,712,953 | 30,712,953 | 0 | `719509246` |
| 12 | 玉衡观海 | 99 | E1 | spell | 29,885,215 | 29,885,215 | 0 | `727832872` |
| 13 | 永劫太玄 | 99 | E1 | 生存 | 29,300,538 | 29,300,538 | 0 | `774623031` |
| 14 | 灵墟渡厄 | 99 | E1 | spell | 28,106,089 | 28,106,089 | 0 | `797278848` |
| 15 | 玉衡守真 | 99 | E1 | hybrid | 28,053,194 | 28,053,194 | 0 | `777606552` |

### 6.2 本赛周普通NPC补充席位

以下4名来自排除固定前15名后的普通T档池，按战力分成4段，每段抽取1名。新赛周可能更换。

| 初始名次 | NPC姓名 | 角色等级 | 设计档 | 倾向 | 目录／榜单战力 | 当前实际战力 | 差值 | 正式玩家ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 16 | 渡川清长 | 89 | T1 | 攻击 | 1,529,587 | 1,529,582 | -5 | `786122884` |
| 17 | 隐泉河川 | 90 | T3 | 生存 | 252,627 | 252,627 | 0 | `719660036` |
| 18 | 栖鹤琴剑 | 82 | T4 | 生存 | 95,908 | 95,908 | 0 | `773939770` |
| 19 | 醉竹云月 | 99 | T5 | 法术 | 20,430 | 20,430 | 0 | `789577608` |

### 6.3 身份与阵容来源对照

名次与本组上表一一对应。来源链接为只读原始设计快照；同一聚合文件内用内部NPC编号定位具体角色。

| 初始名次 | NPC姓名 | 内部NPC编号 | 原始阵容来源 |
| --- | --- | --- | --- |
| 1 | 太初劫锋 | `npc_extreme_p6_attack` | [analysis/npc_design/extreme/catalog.json](../analysis/npc_design/extreme/catalog.json) |
| 2 | 灵墟守真 | `npc_extreme100_085` | [analysis/npc_design/extreme_expansion/npcs/npc_extreme100_085.json](../analysis/npc_design/extreme_expansion/npcs/npc_extreme100_085.json) |
| 3 | 玉衡问剑 | `npc_extreme100_091` | [analysis/npc_design/extreme_expansion/npcs/npc_extreme100_091.json](../analysis/npc_design/extreme_expansion/npcs/npc_extreme100_091.json) |
| 4 | 玉衡归云 | `npc_extreme100_099` | [analysis/npc_design/extreme_expansion/npcs/npc_extreme100_099.json](../analysis/npc_design/extreme_expansion/npcs/npc_extreme100_099.json) |
| 5 | 灵墟观海 | `npc_extreme100_088` | [analysis/npc_design/extreme_expansion/npcs/npc_extreme100_088.json](../analysis/npc_design/extreme_expansion/npcs/npc_extreme100_088.json) |
| 6 | 玉衡逐星 | `npc_extreme100_094` | [analysis/npc_design/extreme_expansion/npcs/npc_extreme100_094.json](../analysis/npc_design/extreme_expansion/npcs/npc_extreme100_094.json) |
| 7 | 玉衡临风 | `npc_extreme100_097` | [analysis/npc_design/extreme_expansion/npcs/npc_extreme100_097.json](../analysis/npc_design/extreme_expansion/npcs/npc_extreme100_097.json) |
| 8 | 灵墟归云 | `npc_extreme100_089` | [analysis/npc_design/extreme_expansion/npcs/npc_extreme100_089.json](../analysis/npc_design/extreme_expansion/npcs/npc_extreme100_089.json) |
| 9 | 灵墟临风 | `npc_extreme100_087` | [analysis/npc_design/extreme_expansion/npcs/npc_extreme100_087.json](../analysis/npc_design/extreme_expansion/npcs/npc_extreme100_087.json) |
| 10 | 玉衡听澜 | `npc_extreme100_092` | [analysis/npc_design/extreme_expansion/npcs/npc_extreme100_092.json](../analysis/npc_design/extreme_expansion/npcs/npc_extreme100_092.json) |
| 11 | 灵墟破晓 | `npc_extreme100_090` | [analysis/npc_design/extreme_expansion/npcs/npc_extreme100_090.json](../analysis/npc_design/extreme_expansion/npcs/npc_extreme100_090.json) |
| 12 | 玉衡观海 | `npc_extreme100_098` | [analysis/npc_design/extreme_expansion/npcs/npc_extreme100_098.json](../analysis/npc_design/extreme_expansion/npcs/npc_extreme100_098.json) |
| 13 | 永劫太玄 | `npc_extreme_p6_endurance` | [analysis/npc_design/extreme/catalog.json](../analysis/npc_design/extreme/catalog.json) |
| 14 | 灵墟渡厄 | `npc_extreme100_086` | [analysis/npc_design/extreme_expansion/npcs/npc_extreme100_086.json](../analysis/npc_design/extreme_expansion/npcs/npc_extreme100_086.json) |
| 15 | 玉衡守真 | `npc_extreme100_095` | [analysis/npc_design/extreme_expansion/npcs/npc_extreme100_095.json](../analysis/npc_design/extreme_expansion/npcs/npc_extreme100_095.json) |
| 16 | 渡川清长 | `npc_v2_l89_t1_attack` | [analysis/npc_design/v2/levels/level_89.json](../analysis/npc_design/v2/levels/level_89.json) |
| 17 | 隐泉河川 | `npc_v2_l90_t3_endurance` | [analysis/npc_design/v2/levels/level_90.json](../analysis/npc_design/v2/levels/level_90.json) |
| 18 | 栖鹤琴剑 | `npc_v2_l82_t4_endurance` | [analysis/npc_design/v2/levels/level_82.json](../analysis/npc_design/v2/levels/level_82.json) |
| 19 | 醉竹云月 | `npc_v2_l99_t5_magic` | [analysis/npc_design/v2/levels/level_99.json](../analysis/npc_design/v2/levels/level_99.json) |

## 7. 名单生成、核对与复现

各组先筛选正式角色等级范围，再按 `(role_combat_power, npc_id)` 降序保留最强15名；同战力按内部NPC编号降序排列。其余4席从排除这15名后的普通T档池中按战力升序分段，并按 `SHA-256(赛周起始日:组号:npc_id)` 选取每段哈希最小者。最后把19名按战力排为初始榜单，使用现有真实身份与完整阵容参与战斗。

本次文档生成逐一校验76个席位与当前选人函数一致、实际战力与当前NPC装载器重算结果一致，并核对每名NPC恰有8名上阵神仙且其战力之和等于实际战力。此前相关56项后端回归和52周×4组名单审计均通过；本表未新增战斗胜率或伤害推测。

- [当前玩法说明](太虚幻境血战离线玩法说明.md)
- [历劫与血战实现说明](太虚幻境历劫与血战离线实现说明.md)
- [完整机器可读名单、实际战力与目录差异](../analysis/evidence/taixu/arena_top15_roster.json)
- [名单审计脚本](../analysis/tools/audit_arena_roster.py)
- [56项测试日志](../analysis/evidence/taixu/arena_top15_tests.log)
- [选人实现](../network_redirect/activity_arena.py)、[配置](../server_config/taixu_rules.json)、[NPC资料装载器](../network_redirect/npc_players.py)

重新核对当前设计库并导出样本名单：

```sh
.runtime/venv/bin/python analysis/tools/audit_arena_roster.py
```

审计脚本的样本赛周当前固定为2026-11-09；改动NPC设计库后应重新核对并更新本文，不应将未来生成的不同名单当作本表所记录版本。
