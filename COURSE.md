# 课程路线：SAR ADC、基础 PLL 与 AFE 电路

完整课文版本：2026-10-03。面向熟练模拟 IC 工程师，以真实模块结构、工作过程、设计取舍和独立 TB 为主线，随后建立系统测量、归因与回归能力。

每课采用相同节奏：提出工程问题 → 预测 → 检查配置/电路 → 最小实验 → 对照证据 → 记录设计判断。一课可拆成多次会话，每次只推进一项可验收的问题。先学电路，验证章节用于相应阶段的实验，不必把完整验证流程作为电路学习的先修课。

电路主线九课和原验证十课均已准备。**工程入口存在性、静态读取得到的结论与新运行结果分别标注；完整课文不代表所有实验已经跑通。**当前学习位置以 [progress.md](progress.md) 为准，执行规则见 [实验与证据规范](docs/experiment-protocol.md)。

## 电路研修主线（优先）

开发全流程配套：[SAR ADC 从规格到实测的 16 课完整教程](courses/06-sar-development/README.md)。01–05 建立规格、架构/预算、Python/MATLAB 与 VA/RTL；06–10 设计采样/CDAC/比较器/控制/reference；11–15 完成逐块替换、验证、版图/PEX 和实测；16 扩展 Pipelined-SAR。附 [可运行数值模型](scripts/sar_design_model.py) 与 [开发记录模板](notes/sar-development-template.md)。10 位贯穿例子为教学假设，实际原图与已有运行分别引用；本次没有新 EDA 仿真，学员与工艺设计验收仍逐项推进。

配套必读：[关键 testbench 的作用与结果分析](courses/00-circuit-foundations/lessons/00-testbench-results-guide.md)。逐项说明 SAR ADC/基础 PLL 的激励、观察量、测量口径、异常定位与设计判断，包含已新运行的比较器案例；其他模块保持待验证。

| 课次 | 结构与机制 | 模块实验 |
| --- | --- | --- |
| [S01 SAR 架构](courses/00-circuit-foundations/lessons/S01-sar-architecture.md) | 差分输入、电荷记忆、残差与逐位搜索 | 一次转换的电荷与时序 |
| [S02 CDAC](courses/00-circuit-foundations/lessons/S02-cdac.md) | 两节点电荷守恒、split bridge、位权、reference mux | 单位权、进位、桥接扰动与建立 |
| [S03 采样与自举](courses/00-circuit-foundations/lessons/S03-sampling-bootstrap.md) | TG、自举预充电/采样/恢复、实际 PMOS 实现 | 独立 TB、残差/pedestal、失真和端间应力 |
| [S04 比较器](courses/00-circuit-foundations/lessons/S04-comparator.md) | 动态锁存核、reset/evaluate、再生、SR latch | 判决时间、offset/noise、memory 与 kickback |
| [S05 控制与预算](courses/00-circuit-foundations/lessons/S05-sar-timing-budget.md) | 每位路径、采样窗、模块噪声与负载取舍 | 时序闭合及一次系统变更 |
| [P01 基础 PLL](courses/00-circuit-foundations/lessons/P01-pll-architecture.md) | 整数 N、环路方向、捕获与锁定 | 固定 N 的初始环路 |
| [P02 PLL 电路模块](courses/00-circuit-foundations/lessons/P02-pll-block-circuits.md) | PFD reset、CP 镜像与开关、filter、VCO、divider | 各模块特性与参数提取 |
| [P03 环路动态](courses/00-circuit-foundations/lessons/P03-pll-loop-dynamics.md) | Kpd/Kvco 单位、带宽、阻尼、稳定性与延迟 | 小相位阶跃、参数改变、启动 |
| [P04 PLL 噪声](courses/00-circuit-foundations/lessons/P04-pll-noise.md) | 噪声传递、CP 电荷→ripple→reference spur | 噪声预算、spur 对照与 jitter |

推荐顺序为工程接管→S01–S05→P01–P04，已有比较器 TB 可先用于工具链验证。随后选择以下验证实验。模块身份见 [电路地图](docs/circuit-map.md)，每项独立实验用 [模块记录模板](notes/circuit-lab-template.md)。PLL 教材原含 fractional-N，基础课程先固定整数 N 或采用注明边界的行为环路，再接实际模块；实际 PLL 模块层级尚待读取。

## 第一单元：SAR ADC 验证工程

教材：`adc_verification_v5.0_001`。从已有静态工程地图进入新 nominal 时序，再建立可信指标、定位机制并形成回归计划。

| 课次 | 核心问题 | 实验与验收产出 |
| --- | --- | --- |
| [01 接管工程](courses/01-cadence-verification/lessons/01-project-map.md) | 这个 testbench 到底验证了什么？ | 库/视图地图、时钟和采样关系、模型边界、环境阻塞点 |
| [02 建立可复现基线](courses/01-cadence-verification/lessons/02-nominal-baseline.md) | 如何证明本机结果来自当前配置？ | 新网表身份、两段采样/十次比较、稳定码相位、启动区间 |
| [03 审计动态指标](courses/01-cadence-verification/lessons/03-dynamic-metrics.md) | ENOB/SNDR 是设计性能还是测量设置的产物？ | bus 解码、真实幅度、窗口/FFT、同数据交叉核验 |
| [04 从系统定位到模块](courses/01-cadence-verification/lessons/04-error-attribution.md) | 哪个非理想因素主导误差？ | 采样/建立、CDAC 权重与静态线性、比较器机制的受控实验 |
| [05 噪声、失调与统计验证](courses/01-cadence-verification/lessons/05-noise-statistics.md) | 单点通过能说明多少？ | 噪声/失配/PVT 分离，种子、分布、置信区间和预算 |
| [06 制定回归计划](courses/01-cadence-verification/lessons/06-regression-plan.md) | 哪些测试足以支持一次设计变更？ | 现有 plan 审计、需求覆盖矩阵、最小回归与 ADC 评审 |

第一课附 [采样控制入口续篇](courses/01-cadence-verification/lessons/01a-sampling-entry.md)，已据当前静态控制链解释 12 个内部周期，波形检验接第 02 课。

阶段结业：提交一份 ADC 工程评审，回答“可信的指标有哪些、由什么配置支持、尚未覆盖什么、下一项最有价值的实验是什么”。不以跑完全部角落作为唯一完成标准。

## 第二单元验证实验：PLL 与 Fractional-N 扩展

教材：`pll_verification_ws_v1.0_001`。已静态核实 `pll_sim` 的旧 AMS 状态与 config 入口，当前工具支持、规格数值及实际绑定待第 07 课审计。

| 课次 | 核心问题 | 预期产出 |
| --- | --- | --- |
| [07 规格到验证计划](courses/02-pll-verification/lessons/07-spec-model-map.md) | 环路和混合信号模型分别承担什么？ | 规格追溯、config/AMS 入口、模拟数字与模型边界 |
| [08 启动与锁定](courses/02-pll-verification/lessons/08-startup-lock.md) | “锁住了”如何量化和复现？ | 频率/相位/保持判据、启动时间线、初态与重调谐对照 |
| [09 噪声、杂散与模型精度](courses/02-pll-verification/lessons/09-noise-spurs.md) | 哪些结论必须提升模型精度才能成立？ | 分数序列、spur 对照、噪声密度/积分 jitter、分析适用性 |

阶段结业：提交 PLL 验证评审，明确目标输出端、锁定证据、噪声与杂散口径，以及行为/晶体管/提取模型的适用范围。

## 新增单元：AFE4404 反向工程电路（2026-10-04）

[AFE4404 完整课程](courses/04-afe4404/README.md) 有九篇主课，依次为 A00 工程接管、A01 TIA、A02 offset cancellation DAC、A03 四相 switched RC、A04 ADC/码格式、A05 LED driver、A06 bias/reference/LDO、A07 timing、A08 noise 与设计变更。后续新增六篇晶体管与接口结构课，按 [完整信号链路线](courses/04-afe4404/signal-chain-guide.md) 学习，配有 [记录模板](notes/afe4404-lab-template.md)。

教材为服务器 AFE4404 原包与五个 HIX_1907151* OA 库，入口 HIX_1907151TOP/TOP_HIER/schematic，见 [工程地图](docs/afe4404-map.md)。已实时只读确认 TIA/反馈、滤波后的 VOL_GEN_1/AMP_BLOCK、ADC 与 DAC_1 返回、TX 端口链，提供 [21 张原图](courses/04-afe4404/schematics.md)。工艺模型、独立 TB、转换算法与新仿真仍待验证。课程先读实际结构，再建独立模块实验；公开产品规格与反向工程实测分别记录，不能把 SAR 的架构、供电或 TB 直接套到 AFE。

## 综合练习

[A05：先行为建模、再逐模块替换电路](courses/05-adc-projects/lessons/A05-model-to-circuit.md) 用 8 位异步 SAR 验证八次决策/握手，用 Pipelined-SAR 研究残差、编码和样本对齐。模块化教学 VA 与四次新 Spectre 检查已准备，完整两级系统/原电路替换仍待执行。

ADS8681/ADS1248 精密 ADC 扩展现已形成 [两套完整课文，共 12 课](courses/05-adc-projects/precision/README.md)，配 [37 张实际原图](courses/05-adc-projects/precision/schematics.md)。ADS8681 R01–R06 学实际路径、前端反馈、SC/CDAC、升压与锁存、参考及模块 TB；ADS1248 D01–D06 学输入链、PGA、SC、多级量化、reference/激励与低频结果。无现成 TB 时先闭合控制/模型边界，再分模块实验；所有新晶体管实验待执行。

新增实战路线：[真实 ADC 项目课程](courses/05-adc-projects/README.md)。A01–A02 用 8 位异步 SAR 贯通实际自举采样、CDAC、比较器与异步握手，配套 S02–S05；A03 学 12 位 Pipelined-SAR 的级间残差与码合成；A04 研读 ADS8681/ADS1248 逆向模块。四份课文及项目入口已准备，工程证据和新运行状态单独记录。基础 PLL 仍按 P01–P04 进行，精密 ADC 扩展可后选。

[10 设计变更与最小回归](courses/03-capstone/lessons/10-design-change.md)：选择 ADC 或 PLL 中一个已定位的瓶颈，提出设计变更，预测收益与代价，再用最小回归验证。提交同条件的前后比较、误差范围、不可退化项、恢复副本和跨电脑复现步骤。

## 研修顺序与通过方式

电路主线优先。验证实验中 01–03 建立可信数据链，04–06 做机制与评审；PLL 07 的配置地图先于 08 的锁定，08 的稳态区间先于 09 的噪声/杂散。第 10 课选一个单元完成一次实际变更，另一个单元的未运行项保持未执行。

每课完成需要课文指定的证据与学员设计判断，记录在 [各课笔记](notes/README.md)。实验受工具/模型限制时允许交付已验证的部分和明确的阻塞，不将计划当结果。结课要求至少一条实际系统比较和完整的假设—干预—证据—判断链。

具体节点、版本相关操作和求解器选项在运行前查本机文档与新网表；发现版本差异时更新 [资料索引](docs/sources.md)。
