# SAR ADC 与基础 PLL：电路研修主线

SAR 开发配套：[从规格、预算、建模到电路/版图/实测的完整 16 课](../06-sar-development/README.md)，附 Python 计算与模块设计方法。先读 01–04 可建立系统预算，再把本目录 S02–S05 的具体结构放入模块设计和逐块替换流程；PLL 原学习顺序保留。

实验导读：[关键 testbench 的作用与结果分析](lessons/00-testbench-results-guide.md)。覆盖现有 SAR TB 的真实 DUT/激励/观察路径、比较器新运行的完整分析，以及待执行的基础 PLL 模块与环路实验。

读者是熟练模拟 IC 工程师。重点是理解结构、时序与设计取舍，并能在真实 Virtuoso 工程中验证。每课包含完整的机制说明和待执行实验；实验的通过状态以 [progress](../../progress.md) 与运行记录为准。

| 顺序 | 课文 | 核心产出 |
| --- | --- | --- |
| S01 | [SAR 架构与电荷流](lessons/S01-sar-architecture.md) | 一次转换的电荷、残差和时序图 |
| S02 | [CDAC 与 split 权重](lessons/S02-cdac.md) | 从实际连接推导十个位权，预测桥接误差 |
| S03 | [采样开关与自举](lessons/S03-sampling-bootstrap.md) | 分相导通表、建立误差、Vgs/Vgd/Vgb 轨迹 |
| S04 | [动态比较器](lessons/S04-comparator.md) | reset/evaluate/再生路径、判决时间与 kickback |
| S05 | [SAR 控制与系统预算](lessons/S05-sar-timing-budget.md) | 每位时间预算、有效码时刻、模块指标分配 |
| P01 | [基础整数 N PLL](lessons/P01-pll-architecture.md) | 环路方向、频率关系、锁定条件 |
| P02 | [PLL 各模块电路](lessons/P02-pll-block-circuits.md) | PFD/CP/filter/VCO/divider 的结构与模块 TB |
| P03 | [环路动态与稳定性](lessons/P03-pll-loop-dynamics.md) | 单位一致的环路模型、稳定性和启动实验 |
| P04 | [基础噪声与杂散](lessons/P04-pll-noise.md) | 噪声传递、reference spur 与 jitter 的证据 |

顺序建议：先完成工程接管，再按 S01→S02→S03→S04→S05 学 ADC；其中比较器已有 TB，可先用 S04 跑通工具链。随后按 P01→P04 学基础 PLL。现有 verification 章节作为相应阶段的测量与回归实验，不要求先学完验证方法才开始看电路。Fractional-N/DSM 放在基础 PLL 之后选修。

每次会话只验收一个问题。使用 [模块实验记录模板](../../notes/circuit-lab-template.md)，记录预测、配置、运行身份、波形和判断。不同 TB 的 DUT 名称可能不同，必须先核对 master 与新网表。工程缺少模块 TB 时建立独立工作副本，不能把理想模型测试当成晶体管模块性能。

本轮模块身份与局限见 [实际电路地图](../../docs/circuit-map.md)。概念图和公式是教学推导；它们不代表已完成设计或新仿真通过。

实际晶体管链的补充教材：[真实 ADC 项目课程](../05-adc-projects/README.md)。8 位异步 SAR 的 BOOSTRAP 确实接入已导出的采样路径，已有独立采样 TB，可接 S03 的实际开关学习；其 PDK/时序与当前 GPDK045 工程不同，不能复用现有比较器性能数值。

已执行的电路实验：[S04 reset/evaluate 与保持输出](lessons/S04a-reset-evaluate-evidence.md)，包含 2026-10-04 四个小差分输入的新 nominal 波形与测量口径。
