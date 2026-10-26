# NPC随机玩家资料与阵容查看说明

更新日期：2026-10-26。

两版已有 NPC 共 1,725 名，现在均有固定保存的随机玩家 ID、昵称、合法头像和角色资料，并可通过原版“其他玩家”入口查询、查看真实阵容。V1 的 240 名和 V2 的 1,485 名均已覆盖；等级、战力档、神仙选择和养成快照保持原设计。

## 使用入口与结果文件

游戏内打开好友／关注页面的“其他玩家”，默认浏览与自身同等级的 NPC。输入昵称或九位数字玩家 ID 搜索，点击结果中的名字，再选“查看阵容”。昵称支持部分文字匹配；玩家 ID 为精确匹配。

- [完整玩家资料目录](../analysis/npc_design/players/玩家资料目录.md)：全部 NPC 的 ID、名字、头像编号、等级、档位、VIP、战力及阵容。
- [资料数据库](../analysis/npc_design/players/catalog.json)：全部随机资料和原始阵容文件引用，供程序加载。
- [资料与阵容总表](../analysis/npc_design/players/overview.csv)：便于筛选和批量核对。
- [全量校验结果](../analysis/npc_design/players/validation.json)：唯一性、战力一致性与协议容量校验。
- [原阵容文件校验值](../analysis/npc_design/players/sources.json)：证明身份扩展未改写原始阵容。

可直接搜索的例子：

| 设计编号 | 玩家ID | 昵称 | 头像编号 | 等级 / 档位 | 战力 |
|---|---:|---|---:|---|---:|
| npc_v1_l01_t5_attack | 723317651 | 清霜瑶山 | 204 | 1 / T5 | 2,564 |
| npc_v1_l36_t3_magic | 792064051 | 落星清长 | 202 | 36 / T3 | 97,156 |
| npc_v2_l99_t1_attack | 733954731 | 栖鹤河明 | 201 | 99 / T1 | 3,367,402 |

## 随机资料规则

规则保存在 [npc_player_rules.json](../server_config/npc_player_rules.json)，生成器为 [build_npc_players.py](../analysis/tools/build_npc_players.py)。这是本地离线设计规则，不是恢复出的官方 NPC 分配算法。

每个稳定业务编号 `npc_id` 结合固定种子生成独立随机序列。玩家 ID 在 700000000—799999999 中抽取并检查重复；昵称由词库组合为四字中文并检查重复。全部 1,725 个 ID、昵称均唯一。保存后重启或重复查询不会换人；日常运行读取已保存的目录，不重新抽签。改变种子、词库或整批重新生成属于身份版本变更，已有引用需要同步迁移。

头像使用原客户端允许的八个编号：101—104、201—204，性别按头像组记录。八种头像均有分布，不强制平均；具体数量见校验文件。

| 资料 | 生成方式及约束 |
|---|---|
| 等级、战力、渡劫层数、流派 | 直接取原 NPC；等级和战力不随机改写 |
| VIP | T5：0—1；T4：0—3；T3：1—5；T2：3—8；T1：5—10，仅为虚构玩家的展示资料 |
| 天赋 | 从原版六种天赋中，按角色等级筛选已解锁项后随机选择 |
| 籍贯、性格、活跃时段、签名 | 从虚构世界背景词库中随机选择，保存于 `profile` |
| 帮派 | 未加入，`union_id=0`、`union_name=''` |
| 称号、宠物、洞府、灵阵 | 沿用原样本未配置状态，不借资料扩展添加属性加成 |

原客户端现有页面显示其支持的身份、头像、等级、VIP、天赋与阵容字段。籍贯、性格、活跃时段、签名完整保存在 JSON/CSV，并随查询附带 `npc_profile`，目前原版 UI 没有这些自定义字段的专用展示栏。

VIP 不发放元宝、充值奖励或每日权益。称号列表为空、佩戴称号为 0。查询成就时只从当前等级、VIP和实际养成状态推导可证明的记录，不伪造登录天数或历史胜负。

## 身份与旧编号兼容

资料库是覆盖两版快照的身份层：每条记录保存 `npc_id`、`version`、`legacy_role_id`、`source_file` 和 `profile`。原 V1/V2 JSON 中的九亿段角色编号保留为历史设计编号；应用运行时先通过 `npc_players.get()` 装配新身份。

直接查询支持新的随机 ID，也兼容 V1/V2 的旧 `role_id`。返回查看资料统一使用随机 ID，便于后续称号、成就查询指向同一名 NPC。

封神榜、逐鹿、蟠桃盛宴及渡劫继续使用已有活动对象编号处理战斗、队伍和历史记录，避免打乱既有存档。活动查看阵容时返回新的玩家 ID、昵称、头像、VIP，并以 `npc_scene_id` 附带原场景对象编号。活动的挑战对象池和难度抽样方式没有扩容；V2 全部玩家通过全局搜索入口开放查询。逐鹿队伍图标仍按原客户端协议显示领队神仙头像，查看玩家时才使用玩家头像。已保存的历史战报文字保留原记录，新记录使用新昵称。

```python
from network_redirect import npc_players

npc = npc_players.get('npc_v2_l99_t1_attack')
print(npc['player_profile'])
role = npc['role']  # 已装配随机身份，仍是真实阵容与养成
packet = npc_players.inspection(role['role_id'])
```

NPC 不创建登录账号，不写入真实玩家的 `roles` 表；遇到与本地角色 ID 冲突，搜索排除冲突对象，直接查询拒绝，不覆盖存档。

## 阵容查看协议与内容

复用原版协议，无需修改 APK：

| 协议 | 行为 |
|---|---|
| 1091 → 1092 | NPC 搜索；类型 1 查询指定等级，类型 2 查询名字或玩家 ID；每页 20 人，页码从 1 开始 |
| 1039 → 2998/event 11 | 查看 NPC 阵容与现有玩家资料 |
| 1078，flag=2 → 1077 | 查询目标 NPC 称号，返回其空称号列表 |
| 1067 → 1066 | 查询该 NPC 可证明的成就记录 |

查询必须经过登录验证，重复请求重用缓存回复，过期序号及无效参数拒绝。NPC 查询直接读取保存快照，避免触发玩家日常奖励或存档迁移。

阵容查看包括首发和替补、单仙等级/飞升/渡劫、实际四维与单仙战力、装备强化/进阶/星级/灵石、装备法术、精魄、觉醒星和助威神仙/助威法术。逐鹿查看遵循当前玩法的阵容人数上限。角色四维同时提供原始名称和客户端显示名称，保证神仙详情中的属性条可渲染。

同一份阵容由统一战力结算器复算。身份字段不改变阵容的 1.1 版战力；未装备库存仍留在原快照中，不冒充已装备物品，也不混入查询者背包。

## 生成和验证

在仓库根目录运行：

```bash
.runtime/venv/bin/python analysis/tools/build_npc_players.py
.runtime/venv/bin/python analysis/tools/build_npc_players.py --check
PYTHONPATH=.:tests .runtime/venv/bin/python -m unittest tests.test_npc_players tests.test_role_profile tests.test_activity_rank tests.test_activity_land tests.test_activity_party tests.test_activity_rape tests.test_cheer tests.test_npc_expansion
.runtime/venv/bin/python analysis/tools/build_npc_player_client_fixture.py
```

前两条只写入或核对设计资料，不打开真实存档。客户端夹具生成 `.runtime/npc-player-fixture.lua`，在已登录的原版 Lua 主线程执行；临时屏蔽发包并自动恢复，验证原生搜索处理与两版低/高等级阵容详情。

全量核验：1,725 名 NPC 身份唯一、头像合法；1,725 份阵容战力与原快照一致；全部查询包可编码，最大 27,091 字节，小于 32,768 字节协议限制。88 项相关自动化测试通过。原客户端验证记录见 [client_validation.json](../analysis/npc_design/players/client_validation.json)。

源码变更后需重启本地离线服务，新身份目录在进程中缓存。资料生成后再次运行 `--check` 可检查确定性；修改原阵容时须重新生成身份目录，避免总表中的战力摘要过时。
