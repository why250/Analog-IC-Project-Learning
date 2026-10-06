# AFE4404：资料身份与候选电路地图

检查日期：2026-10-04。初查方法为 Windows → SSH → 服务器文件系统，以及 Poppler 提取数据手册文字；数据手册第 14 页 Figure 23 已渲染并查看。下列初查保留当时范围；同日后续已连接独立 AFE Virtuoso 会话，实际 OA 连接与原图见本页末尾更新。没有 AFE 新仿真。

## 路径与原包

| 本机配置变量 | 本次服务器位置 |
| --- | --- |
| AFE4404_ROOT | `/home/userone/AAAIC/afe_projects/afe4404` |
| AFE4404_WORKSPACE | `/home/userone/AAAIC/workspaces/afe4404` |
| AFE4404_PDK_ROOT | `/home/userone/AAAIC/pdks/gf018hv_green` |

操作时从 `config/local.env` 读取，不把此机器路径写死在新脚本里。

| 相对 AFE4404_ROOT 的文件 | 本次重新计算的 SHA-256 |
| --- | --- |
| originals/afe4404.7z | `e21f8ec458ab36723817ce742423bcf755628b68be3da3165d69d2c5e88d42b2` |
| docs/afe4404.pdf | `6704bbac93ec071ab807387bcc8f3cfc389d6efab8ff42774f0a8d34faaab8e4` |

来源 README 记载原包曾通过完整性检查、解出 2,985 个文件。本轮只重新计算 hash，没有重做 7z 完整性测试或原包逐文件比较。解包工作库可能与原包有差异，不能因原包 hash 稳定而认定工作库未变。选定 SUB/TOP schematic 的当前 hash 与工作区 cds.lib hash 已存入 [证据 JSON](../notes/evidence/2026-10-04-afe4404-discovery.json)。

## 本次文件系统事实

| Library | Cell 目录数 | schematic 数 | 观察 |
| --- | --- | --- | --- |
| HIX_1907151DEV | 13 | 0 | 13 个 symbol，12 个 spectre view，8 个 layout view |
| HIX_1907151INT | 115 | 115 | 以 INV/NAND/TRIGATE 等命名的原理图 |
| HIX_1907151LIB | 134 | 134 | 以 BUF/逻辑组合等命名的原理图 |
| HIX_1907151SUB | 136 | 136 | 模拟与控制模块候选 |
| HIX_1907151TOP | 2 | 2 | TOP_HIER、TOP_FLAT |

合计 400 个 cell 目录、387 个 schematic 文件。上述五库未找到名为 `maestro`、`adexl`、`config` 或 `veriloga` 的 view 目录；不代表其他位置不存在仿真配置。

工作区 cds.lib 保存值定义了五库、gf018hv_green 及 IC251 标准库。它们指向服务器实际目录；实时会话 readPath、技术库绑定和 CDF 回调仍未核对。`DEV/nmos_3p3_EX/spectre` 等 view 内存在 symbol.oa/master.tag，**spectre view 存在不等于完整器件模型已经提供**。本轮递归搜索 AFE4404_PDK_ROOT 未发现后缀为 .scs/.lib/.sp 的文件；其他后缀、站点模型目录和加密模型仍待审计。

## 功能与入口：当前只作候选映射

| 公开功能 | 候选 library/cell/view | 需要补的工程证据 |
| --- | --- | --- |
| 芯片顶层 | HIX_1907151TOP/TOP_HIER/schematic、TOP_FLAT/schematic | 端口、层级引用及两顶层的一致性 |
| TIA / buffer | HIX_1907151SUB/AMP_BLOCK、AMP_1–AMP_7、BUF_BLOCK、BUF_1–BUF_6 | INP/INM、闭环反馈、输出共模和所驱动负载 |
| 可调反馈 / 电容 | 同库 RES_ADJ_1–RES_ADJ_8 及变体、CAP_SWITCH_1–CAP_SWITCH_5 | 编码、等效 R/C、实际连接位置 |
| Offset / LED 电流 DAC | 同库 DAC_1–DAC_3、DAC_CELL_1–DAC_CELL_3 及变体 | 哪个接 TIA 输入，哪个接 TX 路径，电流方向 |
| 分相采样 | 同库 SWITCHED_RC_FILTER、SWITCH_BLOCK、RC_SWITCH、SWITCH_* | 相位选择、采样电容、buffer 输入与复位节点 |
| ADC | 同库 ADC_1、ADC_CELL_1、COMP_1 | 架构、量化/计数/反馈机制、输出码宽 |
| LED 驱动 | 同库 DRIVER_1、DRIVER_2 | TX1–TX3 连接、控制码、输出支路 |
| 供电与参考 | 同库 BIAS_1–BIAS_4、LDO_1、LDO_2、VREF_1、VOL_GEN_1–VOL_GEN_4 | 电源域、参考用途、startup、负载 |
| 时序 / 时钟 | 同库 CTRL_1–CTRL_7、COUNT_4B_1、FREQ_BLOCK_1、FREQ_DIV_1/2、OSC_1–OSC_3 | 控制位含义、采样/转换事件、reset 与 ADC_RDY |

除 TOP 行外，候选 cell 的 view 都是 schematic。表格不宣称已确认任何实例路径；例如 DAC_1 不能仅凭名字分配为 offset DAC。

## 数据手册已审阅范围

TI `SBAS689D`，2016-12 Rev. D。第 1 页确认光学生物传感用途、三 LED、单 photodiode、I²C 与可编程 TIA。第 13–19 页核对以下公开产品事实：

- 第 13–15 页：一 PRF 周期产生四组数据，四路滤波器分相采样，再经 buffer/ADC 转换。Figure 23 为简化单端画法，文字明确接收链为全差分；不能照图误认实际电路单端。
- 第 14、16 页：差分跨阻为 2Rf，Rf 范围 10 kΩ–2 MΩ；RfCf 建议约为采样/LED 脉宽的 1/5 或更小。该建议不是任意精度下的建立验收阈值。
- 第 15 页：2-LED 模式为 LED2 → Ambient2 → LED1 → Ambient1；3-LED 模式为 LED2 → LED3 → LED1 → Ambient。
- 第 16 页：LED 电流为 6-bit 控制，默认 0–50 mA，63 个等步长间隔；加倍模式可达约 100 mA，高码饱和精度受限。
- 第 17–18 页：每相可独立设置 TIA 输入 offset cancellation current，支持极性选择；输入 DC 消除与数字 ambient 相减作用位置不同。
- 第 19 页：22-bit ADC 表示通过 24-bit 二补码寄存器读出，bits 23/22 作符号扩展；TIA 差分工作范围 ±1 V，ADC 满量程 ±1.2 V。

这些是**产品资料值**，不是 HIX 还原电路的保存参数或实测性能。详细寄存器位、noise 表格、完整时序约束、版图及后仿真尚未审阅。课程中的等效模型与实验设计为原创推导，未指定的 R/C、阈值、负载由独立实验事先选定并记录。

## 同日后续：实际 OA 连接与原图

独立 `afe_course` 会话身份和实时 TOP/SUB/DEV/PDK readPath 已核对。以 read 模式打开原理图，读取关键 terminal/net 与保存尺寸，导出 13 张完整原图和 AMP_6 输入局部图。来源 schematic 的导出前后 SHA-256 相同；未生成新网表或运行仿真。

| 路径 | 实际结构证据 |
| --- | --- |
| 接收输入 | INP/INM 经 N15955/N15954 的 D/S 接 net707/net708，连 MI499/AMP_6 的 VP/VM；开关导通条件待查 |
| TIA 反馈 | AMP_6 的 VOP/VOM 经 MI336/MI337 的 RC_CELL_2 返回输入；RC_CELL_2 内 RES_ADJ_3 与 CAP_SWITCH_5 并联 |
| 输入取消路径 | MI495/DAC_2 的 VO1/VO2 接 net707/net708；电流方向和码步待测 |
| TIA 后级 | MI311/SWITCHED_RC_FILTER 的 VIN1/VIN2 接 net713/net714 |
| TX 路径 | MI152/AMP_5 与 MI341/SWITCH_BLOCK 经 net770/net830 相连，后者接 TX1/TX2/TX3；DRIVER_1/2 实际用于 I/O，更正初查名称候选 |
| ADC | ADC_1 含 17 个 ADC_CELL_1、15 路输出 buffer，局部 Z<14:0>；完整转换机制和产品 22/24-bit 的对应待证明 |

查看 [真实电路原图与读图说明](../courses/04-afe4404/schematics.md) 和 [本地图册](../courses/04-afe4404/schematic-gallery.html)。证据为 [连接/尺寸摘要](../notes/evidence/2026-10-04-afe4404-connectivity.json)、[原图与 hash 清单](../notes/evidence/2026-10-04-afe4404-schematics.json)，操作记录见 [只读结构笔记](../notes/2026-10-04-afe4404-schematics.md)。

## 完整信号链续篇

用户随后要求完整理解信号链关键电路，新只读补查确认 FILTER→顶层交接开关→VOL_GEN_1→AMP_BLOCK→ADC_1，以及 ADC 输出总线→DAC_1→AMP_BLOCK 返回路径。ADC 局部总线还接 COUNT_4B_1 和 MX21_15BX4；完整转换算法、位序、最终接口和相位待验证。

路线扩为 [九篇主课与六篇结构课](../courses/04-afe4404/signal-chain-guide.md)，原图现有 21 张。新增来源 hash、连接、存储电容/输入支路保存参数与七张图的 hash 见 [最新 JSON](../notes/evidence/2026-10-04-afe4404-signal-chain.json)，记录见 [完整链路建课](../notes/2026-10-04-afe4404-signal-chain.md)。所有来源 hash 在读取及对应导出前后相同，无新仿真。

下一项操作：接学员对输入驱动 NMOS 的预测，在 A01a 的明确假设下推导 P15738/P15737 电流方向，并继续查 P15751_G 的驱动与 bias/enable。模型初始化、工作点与新仿真仍待验证。
