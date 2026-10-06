# 实验记录索引

新增 [2026-10-05 SAR 开发设计教程与离线计算记录](2026-10-05-sar-development.md)，对应 [16 课完整教程](../courses/06-sar-development/README.md)、[设计记录模板](sar-development-template.md) 与 [Python 数值结果](evidence/2026-10-05-sar-design-model/summary.json)。课文/数值例子已准备；本次无新 EDA，学员验收与真实工艺闭合待执行。

新增 [ADC Verilog-A 基线与逐模块替换记录](2026-10-04-adc-modeling.md)，包括新 8 位行为系统、超时反例、残差放大器与输出 bus 波形验收。实际混合系统/完整 12 位流水线未运行。

新增 [ADS8681 / ADS1248 结构课程与无 TB 路线记录](2026-10-04-precision-adc.md)，配 [专用模块记录模板](precision-adc-lab-template.md)。37 张原图与 12 课课文准备完成，所有本项目新仿真待执行。

AFE 完整链路续篇：[2026-10-04 信号链结构课程](2026-10-04-afe4404-signal-chain.md)，对应 [九篇主课与六篇结构课](../courses/04-afe4404/signal-chain-guide.md)、[21 张原图](../courses/04-afe4404/schematics.md) 和 [最新 live 连接/hash](evidence/2026-10-04-afe4404-signal-chain.json)。学员理解、模型和 AFE 仿真仍待验收。

ADC 实际电路图：[2026-10-04 只读结构与原图](2026-10-04-adc-schematics.md)，对应 [14 张原图目录](../courses/05-adc-projects/schematics.md) 和 [live 连接/hash](evidence/2026-10-04-adc-schematics.json)。本项建立独立会话，尚未新仿真。

新增实战路线：[2026-10-04 adc_projects 接管与课程](2026-10-04-adc-projects.md)，对应 [四工程课文](../courses/05-adc-projects/README.md) 和 [资料/静态结构证据](evidence/2026-10-04-adc-projects.json)。已有导出复核，尚未新仿真。

2026-10-04 补充 [关键 TB 的用途与结果分析记录](2026-10-04-testbench-guide.md)，对应 [导读课文](../courses/00-circuit-foundations/lessons/00-testbench-results-guide.md) 和 [保存配置/只读结构证据](evidence/2026-10-04-testbench-guide.json)。本项没有新仿真。

表格是记录模板，状态均由实际学习和运行更新；课文编写完成不代表学员已经完成该课。共享规则见 [实验与证据规范](../docs/experiment-protocol.md)，当前续学位置见 [progress.md](../progress.md)。

AFE 新分支：[2026-10-04 定位与建课](2026-10-04-afe4404-discovery.md)、[九课入口](../courses/04-afe4404/README.md)、[AFE 模块记录模板](afe4404-lab-template.md)。文件系统和部分产品资料已核对，OA 连接、AFE 模型/仿真与学员学习未执行；不覆盖以下 SAR/PLL 记录。

随后新增 [关键原图与实际连接记录](2026-10-04-afe4404-schematics.md)：独立 afe_course 会话只读追踪 TIA/反馈，导出 13 张完整原图和输入级局部图，见 [读图入口](../courses/04-afe4404/schematics.md)。OA 静态连接已有证据，模型/工作点、新仿真与学员理解仍待验收。

| 课次 | 记录 | 当前证据状态 |
| --- | --- | --- |
| 01 | [工程地图与采样入口](01-project-map.md) | 有 2026-10-01 环境和静态读取，尚无新仿真 |
| 02 | [Nominal 基线](02-nominal-baseline.md) | 模板，未执行 |
| 03 | [动态指标](03-dynamic-metrics.md) | 模板，未执行 |
| 04 | [误差归因](04-error-attribution.md) | 模板，未执行 |
| 05 | [噪声与统计](05-noise-statistics.md) | 模板，未执行 |
| 06 | [回归计划与 ADC 评审](06-regression-plan.md) | 模板，未执行 |
| 07 | [PLL 规格与模型地图](07-spec-model-map.md) | 入口存在性已查，内容审计未执行 |
| 08 | [PLL 启动与锁定](08-startup-lock.md) | 模板，未执行 |
| 09 | [PLL 噪声与杂散](09-noise-spurs.md) | 模板，未执行 |
| 10 | [设计变更](10-design-change.md) | 模板，未执行 |

每次追加带日期的会话，保留原预测和后续修正。为每个实测值绑定条件、run ID 和测量定义；不覆盖另一台机器的记录。

小型证据：[2026-10-01 环境与控制链](evidence/2026-10-01-environment.json)、[2026-10-03 完整课入口检查](evidence/2026-10-03-course-entries.json)。

电路主线 S01–S05/P01–P04 用 [模块记录模板](circuit-lab-template.md) 新建记录。首个模块记录：[2026-10-03 比较器 nominal transient](2026-10-03-comparator-nominal.md)，对应 [电路与运行证据](evidence/2026-10-03-circuit-modules.json)。这是一个比较器新运行，ADC 系统 nominal 第 02 课仍未执行。

续篇：[2026-10-04 比较器小差分与判决时间](2026-10-04-comparator-delay.md)，对应 [测量 JSON](evidence/2026-10-04-comparator-delay.json) 与 [新波形图](evidence/2026-10-04-comparator-delay.png)。四点 nominal 动态核检查完成，学员掌握与统计/系统实验仍待验证。
