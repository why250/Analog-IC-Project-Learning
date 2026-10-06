# AFE4404 反向工程电路研修

建课日期：2026-10-04。教材已在服务器定位，本单元有九篇主课、六篇结构课和实验记录模板；**已只读核对关键 OA 连接与保存参数，可查看 21 张原图；没有生成新网表或运行 AFE 仿真。** 学员结构理解待反馈。原 SAR ADC/PLL 记录保留，AFE 是新增学习分支。

用户希望完整理解信号链上的关键电路，最新入口为 [完整信号链结构路线](signal-chain-guide.md)。先按实际连接学习输入、TIA/反馈、DAC、滤波/保持、VOL_GEN_1 与 AMP_BLOCK、ADC/返回 DAC 和读出，再配套 TX、偏置、参考、供电及时序。当前读图课为 [A01a 输入与偏置](lessons/A01a-tia-transistor-structure.md)。

项目来自共享盘 `Analog-IC/AFE/E031.AFE电路，模拟前端芯片，AFE4404/`，来源由服务器项目 README 记载。原包为 `originals/afe4404.7z`，包含五个 `HIX_1907151*` OA 库，配有 TI AFE4404 Rev. D 数据手册与 `gf018hv_green` OA 工艺库。反向工程与公开产品的功能对应关系需要逐项证明，不能认定还原工程就是厂商的完整原始实现。

机器路径从 `config/local.env` 的 `AFE4404_ROOT`、`AFE4404_WORKSPACE`、`AFE4404_PDK_ROOT` 获取。资料身份与入口见 [工程地图](../../docs/afe4404-map.md)，新检查证据见 [JSON](../../notes/evidence/2026-10-04-afe4404-discovery.json)。

## 课程顺序

| 课次 | 一个核心问题 | 实际候选入口 | 验收产出 |
| --- | --- | --- | --- |
| [A00 接管与功能映射](lessons/A00-project-map.md) | 哪条连接链才是光电接收链？ | TOP_HIER / TOP_FLAT | 一条有实际连接证据的 INP/INM → 接收链地图 |
| [A01 TIA](lessons/A01-tia.md) | 增大 Rf 为什么可能降低脉冲测量质量？ | AMP_* / RES_ADJ_* / CAP_SWITCH_* | 增益、摆幅与建立的单变量比较 |
| [A02 Offset cancellation DAC](lessons/A02-offset-dac.md) | 为什么数字相减不能替代输入 DC 消除？ | DAC_* / DAC_CELL_* / DEC_* | 电流方向、码步与 TIA headroom |
| [A03 开关 RC 滤波与保持](lessons/A03-switched-rc.md) | 相邻相位怎样相互污染？ | SWITCHED_RC_FILTER / SWITCH_* / BUF_* | 建立、hold droop 或交接残差 |
| [A04 ADC 与读出码](lessons/A04-adc.md) | 24-bit 输出代表多少模拟信息？ | ADC_1 / ADC_CELL_1 / COMP_1 | ADC 架构证据和有符号码映射 |
| [A05 LED 驱动](lessons/A05-led-driver.md) | LED 电流何时随端电压失真？ | AMP_5 / SWITCH_BLOCK / SWITCH_CELL_1 | 电流码步、compliance 与脉冲电荷 |
| [A06 偏置、参考与 LDO](lessons/A06-bias-reference-ldo.md) | 电源扰动从哪条路径进入信号？ | BIAS_* / VREF_1 / VOL_GEN_* / LDO_* | 一个模块的启动或供电敏感性 |
| [A07 时序与配置](lessons/A07-timing-control.md) | 采样、保持、复位、转换如何交接？ | CTRL_* / COUNT_4B_1 / FREQ_* / OSC_* | 一个 PRF 周期的事件表与相位身份 |
| [A08 噪声预算与设计变更](lessons/A08-noise-design-review.md) | 哪项改动值得付出功耗和时间？ | 经 A00 确认的接收链 | 一项同条件前后比较及最小回归 |

表中入口除 TOP 外均在 `HIX_1907151SUB`，TOP 在 `HIX_1907151TOP`。初始功能分类为候选。随后已完成 [关键电路只读核对与原图导出](schematics.md)：实际 TIA 为 AMP_6，反馈为 RC_CELL_2，DAC_2 接 TIA 输入，输出接 SWITCHED_RC_FILTER；TX 路径为 AMP_5 + SWITCH_BLOCK。DRIVER_1/2 实际为 I/O 驱动，A05 应从已确认 TX 入口继续。模型、工作点与新仿真仍未验证，A01–A08 的方案不能当成实测结论。

## 学习方式

按“问题—预测—实验—证据—设计判断”推进，每次只验收一项。先读电路，再建独立 TB。第一课只读检查，不运行全芯片。修改前保留可恢复副本，实验库不得覆盖这五个来源库；复制后检查层级仍指向哪些源 cell。

没有模型时仍可做连接分析、反馈方向、电荷守恒与时序推导；理想或行为实验应单独标明，不用于验收工艺噪声、offset、PVT 或产品性能。通用规范见 [实验协议](../../docs/experiment-protocol.md)。

从 [完整结构路线](signal-chain-guide.md) 和 [真实电路原图](schematics.md) 开始，在 [AFE 记录模板](../../notes/afe4404-lab-template.md) 保存预测与证据。初始 [建课笔记](../../notes/2026-10-04-afe4404-discovery.md) 与 [首批原图记录](../../notes/2026-10-04-afe4404-schematics.md) 保留，最新为 [完整链路建课记录](../../notes/2026-10-04-afe4404-signal-chain.md)。下一项操作是在 A01a 解释 AMP_6 的输入支路电流，并查明 P15751_G 的驱动与输入 NMOS 工作区，学员理解待验收。
