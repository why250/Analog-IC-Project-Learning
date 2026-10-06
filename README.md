# Analog IC Project Learning

面向熟练模拟 IC 工程师的 Virtuoso 实际工程研修课。以现有工程为教材，沿着 **设计意图 → 电路与模型 → testbench → 仿真证据 → 误差归因 → 设计判断** 学习。

第一站是 `cadence_verification` 中的 SAR ADC，随后学习基础整数 N PLL，Fractional-N/DSM 留作扩展。默认已掌握模拟电路与 Virtuoso 常规操作，ADC/PLL 的架构与模块电路按实际需求展开；每课围绕一个工程问题，完成一份可以在另一台电脑上继续的实验记录。

2026-10-04 已在服务器找到 AFE4404 反向工程，新增 [AFE 电路课程](courses/04-afe4404/README.md)：TIA、offset cancellation DAC、四相开关 RC、ADC、LED driver、bias/reference/LDO、时序与噪声预算。已只读核对关键 OA 连接与输入器件尺寸，提供 [21 张实际电路原图与结构说明](courses/04-afe4404/schematics.md)；模型、工作点与仿真仍待验证。从 [A00 接管](courses/04-afe4404/lessons/A00-project-map.md) 开始，原 SAR/PLL 进度保留。

## 从这里开始

2026-10-05 新增 [SAR ADC 完整开发设计教程（16 课）](courses/06-sar-development/README.md)：规格→Python/MATLAB 架构与预算→VA/RTL→模块电路与逐块替换→前仿→版图/PEX→实测。附可运行 Python 示例、模块 TB、结果归因和开发记录模板；系统模型与 PDK 可行性并行迭代。本次新证据是离线教学计算，没有新增 EDA 仿真。

AFE 续学按 [完整信号链结构路线](courses/04-afe4404/signal-chain-guide.md)：九篇主课配六篇结构课，提供 21 张真实电路图，当前从 [AMP_6 输入支路](courses/04-afe4404/lessons/A01a-tia-transistor-structure.md) 逐器件阅读。原图与静态连接已核对，工作点和性能仍待实验。

1. 阅读 [课程路线](COURSE.md)，了解每个阶段的工程产出。
2. 按 [环境与同步](docs/environment.md) 配置本机路径。
3. 开始 [第 01 课：接管 SAR ADC 工程，建立验证地图](courses/01-cadence-verification/lessons/01-project-map.md)，约 60–90 分钟。
4. 在 [第一课记录](notes/01-project-map.md) 填写观察，在 [续学入口](progress.md) 留下下一步。

2026-10-03 用户明确希望学习 SAR ADC 和基础 PLL 的电路。课程已调整为 **电路研修主线 9 课 + 验证实验 10 课**：SAR 架构、split CDAC、采样/自举、动态比较器、控制与预算；基础 PLL 架构、PFD/CP/filter/VCO/divider、环路动态、噪声与杂散。见 [电路课文](courses/00-circuit-foundations/README.md) 与 [实际模块地图](docs/circuit-map.md)。现有 verification 课文作为测量、归因和回归实验保留。

从 [完整课程目录](COURSE.md) 选择课文，从 [实验记录索引](notes/README.md) 保存学习过程。2026-10-03 已通过 SSH→服务器 bridge→独立 ADC 会话新运行一次比较器 nominal transient，Spectre 完成，详见 [运行记录](notes/2026-10-03-comparator-nominal.md)。学员学习、ADC 系统、自举开关和 PLL 实验仍待验证；课文齐全不代表学完或所有 TB 跑通。

## 仓库内容

ADC 系统学习新增 [Verilog-A 建模与逐电路替换](courses/05-adc-projects/lessons/A05-model-to-circuit.md) 和 [模型源码/新运行入口](models/adc_behavioral/README.md)：8 位教学闭环与级间残差模型已新运行；真实模块混合系统与完整 12 位流水线待验证。

ADS8681 / ADS1248 新增 [12 课逆向电路课程](courses/05-adc-projects/precision/README.md) 与 [37 张真实关键 schematic](courses/05-adc-projects/precision/schematics.md)，包括前端/PGA、CDAC/SC、升压/比较器和 reference。没有现成 TB 时按 [结构→理想实验→器件模块 TB](courses/05-adc-projects/precision/no-testbench.md) 推进；本轮无新仿真。

2026-10-04 新增 [真实 ADC 项目课程](courses/05-adc-projects/README.md)：基于服务器 `adc_projects` 的 8 位异步 SAR、12 位 Pipelined-SAR，以及 ADS8681/ADS1248 逆向库。包括实际架构、关键模块 TB、残差与数字合成、精密 ADC 研读课文；新工程仿真尚未执行。

可直接查看 [ADC 关键电路的 14 张原图](courses/05-adc-projects/schematics.md)，从 [自举开关逐器件分析](courses/05-adc-projects/lessons/A02a-bootstrap-structure.md) 开始。图像来自本轮实时只读 Virtuoso 导出，保留原始连接；器件工作点和性能待仿真。

学习各模块之前可先读 [关键 TB 与结果分析导读](courses/00-circuit-foundations/lessons/00-testbench-results-guide.md)，明确每个实验要回答的问题，以及波形和指标能支持的结论。

| 入口 | 用途 |
| --- | --- |
| [COURSE.md](COURSE.md) | 课程目标、顺序和验收产出 |
| [courses/](COURSE.md) | 电路主线与验证实验的完整课文 |
| [notes/](notes/README.md) | 各课学习记录、证据索引和未解决问题 |
| [progress.md](progress.md) | 跨电脑、跨会话续学的单一入口 |
| [docs/sources.md](docs/sources.md) | 原始工程定位、版本差异和校验值 |
| [docs/bridge.md](docs/bridge.md) | 使用 virtuoso-bridge-lite 辅助学习 |
| [docs/experiment-protocol.md](docs/experiment-protocol.md) | 运行身份、测量口径、阈值和通过/失败规则 |
| [AGENTS.md](AGENTS.md) | 后续 LLM 继续授课和维护课程的约定 |

GitHub 同步课文、笔记、小型结果摘要和自编脚本。Cadence 原始资料、PDK、OA 库和完整仿真结果保留在各自 EDA 环境；用资料校验值、相对路径和实验记录关联。换电脑后可以接着读课和写笔记，实际运行仿真还需要本地或远程 EDA 环境。

给下一次对话的起手提示：

> 请阅读 AGENTS.md、progress.md 和当前课的笔记，按熟练模拟 IC 工程师的水平继续授课。先让我对当前工程问题作出判断，再通过工程证据检验。每次只推进一个可验收的小任务，结束时更新续学入口。
