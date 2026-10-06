# AFE4404：关键电路原图与结构学习入口

本页对应 2026-10-04 新读取的真实 OA 原理图。**已核对静态连接与保存参数；没有运行 AFE 仿真，学员预测与结构理解仍待反馈。** 图片由 Virtuoso 原生导出，没有重画器件或补造连接。

同日按完整信号链学习要求补查，新增 7 张原图，当前共 21 张。结构课顺序见 [完整路线](signal-chain-guide.md)，最新连接见 [信号链 JSON](../../notes/evidence/2026-10-04-afe4404-signal-chain.json)。

可以从 [交互图册](schematic-gallery.html) 选择模块、缩放与拖动，也可直接点击下表 PNG。图册 HTML 已做脚本语法和资源路径检查；内置浏览器限制 file 协议，交互操作尚未通过浏览器实测。单张原图和本页不依赖图册交互。

## 实际原图目录

除 TOP_HIER 外，library 均为 `HIX_1907151SUB`，view 均为 `schematic`。来源图上的部分器件标签本来就重叠；解释连接与尺寸时以 [结构化摘要](../../notes/evidence/2026-10-04-afe4404-connectivity.json) 为准。图片包含全部来源实例，不因标有 UNUSED 就删除它们。

| 看什么 | 原图 | 静态结构证据 / 学习问题 |
| --- | --- | --- |
| TIA 输入级 | [AMP_6 局部放大](../../notes/evidence/afe4404/AMP_6_input.png) | P15737/P15738 的 PMOS 输入对，共源 net73；旁路输入支路怎样工作？ |
| TIA 全电路 | [AMP_6](../../notes/evidence/afe4404/AMP_6.png) | 173 个实例；输入、偏置、输出、调整与 UNUSED 区如何区分？ |
| 外部反馈 | [RC_CELL_2](../../notes/evidence/afe4404/RC_CELL_2.png) | RES_ADJ_3 与 CAP_SWITCH_5 并联于 PLUS/MINUS |
| 反馈电容支路 | [CAP_SWITCH_5](../../notes/evidence/afe4404/CAP_SWITCH_5.png) | 5 个 MIM 电容和 6 个 NMOS 实例；配置不同会接入哪些电容？ |
| 反馈电阻选择 | [RES_ADJ_3](../../notes/evidence/afe4404/RES_ADJ_3.png) | 8 个 RES_ADJ_8 及变体；等效 Rf 仍需下降一层 |
| 分相 RC 滤波 | [SWITCHED_RC_FILTER](../../notes/evidence/afe4404/SWITCHED_RC_FILTER.png) | 32 个电阻、8 个电容类实例、32 个 switch 子块及 CTRL_7 |
| 输入 DAC | [DAC_2](../../notes/evidence/afe4404/DAC_2.png) | VO1/VO2 与 TIA 输入同节点，内部 15 个 DAC_CELL_2 |
| DAC 单元 | [DAC_CELL_2](../../notes/evidence/afe4404/DAC_CELL_2.png) | 电流选择、bias 与输出端，实际电流方向未测 |
| ADC 阵列 | [ADC_1](../../notes/evidence/afe4404/ADC_1.png) | 17 个 ADC_CELL_1，15 路输出 buffer，Z<14:0> |
| ADC 单元 | [ADC_CELL_1](../../notes/evidence/afe4404/ADC_CELL_1.png) | 输入选择、两只电容、交叉耦合与输出支路；完整转换机制待查 |
| 滤波后接口 | [VOL_GEN_1](../../notes/evidence/afe4404/VOL_GEN_1.png) | 顶层 MI199/MI188，输入与 VO 反馈的 PMOS 支路，共模参考与双供电域 |
| 转换前模拟模块 | [AMP_BLOCK](../../notes/evidence/afe4404/AMP_BLOCK.png) | AMP_1、两个 AMP_2、AMP_3 与开关 RC/电容，接信号和 DAC 返回 |
| 输出到 ADC 的放大器 | [AMP_1](../../notes/evidence/afe4404/AMP_1.png) | AMP_BLOCK 的 MI83，VOP/VOM 接 VO1_1/VO1_2 |
| 电容网络中的放大器 | [AMP_2](../../notes/evidence/afe4404/AMP_2.png) | AMP_BLOCK 的 MI3/MI5，固定相位与电荷状态待证明 |
| 多端输出放大模块 | [AMP_3](../../notes/evidence/afe4404/AMP_3.png) | AMP_BLOCK 的 MI315，含 AMP_7 与 CAP_SWITCH_4 子块 |
| 数字返回 DAC | [DAC_1](../../notes/evidence/afe4404/DAC_1.png) | A 接 ADC 输出总线，VO1/VO2 返回 AMP_BLOCK.VI2，完整更新算法待查 |
| 读出状态入口 | [COUNT_4B_1](../../notes/evidence/afe4404/COUNT_4B_1.png) | D 接局部 ADC 总线，CP/CPN 与 Q/QN/SUM，最终格式待追踪 |
| LDO | [LDO_1](../../notes/evidence/afe4404/LDO_1.png) | 62 个实例，参考、负载和稳定性未验证 |
| TX 模拟环路 | [AMP_5](../../notes/evidence/afe4404/AMP_5.png) | 顶层 MI152，连 net770/net830 与 TX_SUP |
| TX 开关阵列 | [SWITCH_BLOCK](../../notes/evidence/afe4404/SWITCH_BLOCK.png) | 顶层 MI341 接 TX1/TX2/TX3，内有 64 个 SWITCH_CELL_1 |
| 层级总览 | [TOP_HIER](../../notes/evidence/afe4404/TOP_HIER.png) | library=HIX_1907151TOP，226 个实例、363 个端口，很多是暴露内部节点 |

## 第一项结构学习：TIA 的输入与反馈

先预测：这一条反馈是连续时间 R∥C、周期性 switched-capacitor，还是组合？本轮问题已提出，尚无学员回答。以下记录实际连接，不能将助教发现记作学员掌握。

顶层 `INP` 经 `N15955.D/S` 接 `net707`，`INM` 经 `N15954.D/S` 接 `net708`。它们分别连接 `MI499 → AMP_6` 的 VP、VM。这里“经 D/S”描述静态连接，不保证该 NMOS 在某个控制条件下必然导通；enable 和输入路径导通状态待核对。

| TOP_HIER 实例 | Master | 已读 terminal/net |
| --- | --- | --- |
| N15955 | gf018hv_green/nmos_3p3 | D=INP，S=net707，G=X21176_ZN |
| N15954 | gf018hv_green/nmos_3p3 | D=INM，S=net708，G=X21176_ZN |
| MI499 | HIX_1907151SUB/AMP_6 | VP=net707，VM=net708，VOP=net713，VOM=net714 |
| MI336 | HIX_1907151SUB/RC_CELL_2 | PLUS=net713，MINUS=net708 |
| MI337 | HIX_1907151SUB/RC_CELL_2 | PLUS=net714，MINUS=net707 |
| MI495 | HIX_1907151SUB/DAC_2 | VO1=net707，VO2=net708 |
| MI311 | HIX_1907151SUB/SWITCHED_RC_FILTER | VIN1=net713，VIN2=net714 |

可见输出各经一组 RC 返回相反编号的输入侧。RC_CELL_2 内 `MI334 → RES_ADJ_3` 和 `MI316 → CAP_SWITCH_5` 跨同一 PLUS/MINUS，是实际并联的电阻/电容可配置网络。CAP_SWITCH_5 有一只直接跨 PLUS/MINUS 的电容，其余支路有开关。不能因为名字包含 SWITCH 就认定这里采用周期性电荷转移的 SC 积分；先查 gate 控制及相位，再判断时间行为。

输入 DAC 与 TIA 输入共节点，支持将 DAC_2 作为 cancellation 路径候选；真正的码到电流、极性和 headroom 效果仍需模型、工作点和实验。输出已接 switched RC，故此处 AMP_6 作为接收 TIA 的功能对应由连接支持，超过了此前仅凭 cell 名的判断。

## 第二层：看输入对，而不猜工作点

[输入级放大图](../../notes/evidence/afe4404/AMP_6_input.png) 是原 CAD 的局部导出，周围电路超出视野；完整连接以 AMP_6 全图和摘要为准。

| AMP_6 器件 | 连接 | 文件保存的几何参数 |
| --- | --- | --- |
| P15738 | G=VP，S=net73，D=net79 | totalW=448 µm，fingerW=14 µm，nf=32，L=2 µm，m=1 |
| P15737 | G=VM，S=net73，D=net78 | 同上 |
| P15448 | G=VP，S=net83，D=net89 | totalW=10 µm，fingerW=5 µm，nf=2，L=0.6 µm，m=1 |
| P15446 | G=VM，S=net83，D=net87 | 同上 |
| N15838 | G=VP，S=net79，D=net71 | totalW=213.6 µm，nf=12，L=8 µm |
| N15836 | G=VM，S=net71，D=net78 | 同上 |

两组 PMOS 都接 VP/VM，不能把全部输入作用简化为一对 MOS。相连的 NMOS 也由输入驱动，且 D/S 静态标注不对称；需要继续分析偏置、局部反馈与工作区，不能根据图形直接给出教科书拓扑名称。

这些是新只读查询返回的**保存尺寸/CDF 值**，不是实测 gm、Id、offset 或噪声。较大面积可能是输入噪声/失配取舍的一部分，但还需有效宽度、工作点和模型证明。totalW 与 nf 已分别记录，不能未经 CDF 语义核实就再次乘 nf。

## 读图之后怎样继续

下一项只验收一个问题：按 [A01a](lessons/A01a-tia-transistor-structure.md) 沿 P15737/P15738 的源、漏和相连 NMOS 追到偏置与下一级，解释差分电流怎样形成并传递。随后按 [完整路线](signal-chain-guide.md) 分析共模反馈、补偿、接口与转换；增益、相位裕度、noise 和动态建立用独立 TB 逐项验证。

本轮没有完成这一晶体管机制课的学员验收。连接证据可进入 [A01](lessons/A01-tia.md)，仿真准备仍需审计模型。导出身份、原图 hash、source hash 和窗口记录见 [图像清单](../../notes/evidence/2026-10-04-afe4404-schematics.json)；来源 OA 与完整读取 JSON 留服务器。
