# 真实 ADC 项目课程：异步 SAR、Pipelined-SAR 与精密 ADC

完整开发方法见 [SAR ADC 开发设计 16 课](../06-sar-development/README.md)：把这里的实际原图/接口和 A05 混合替换接入规格、预算、前后仿与实测流程。贯穿数值案例独立于本工程参数，不代替 PDK 设计或作者结果复现。

新增 [A05：Verilog-A 模块建模与逐电路替换](lessons/A05-model-to-circuit.md)，附 [可复现源码与新运行](../../models/adc_behavioral/README.md)。8 位教学闭环的新五样本/超时检查和残差模型增益/限幅检查完成；原 OA 混合系统与完整 12 位流水线仍待验证。

新增 [ADS8681 / ADS1248 逆向电路完整课程（12 课）](precision/README.md)：[37 张关键电路原图](precision/schematics.md)，逐模块学习前端/PGA、CDAC/SC、升压/比较器、reference/bias 与低频误差，并说明 [没有 TB 时怎样建立实验](precision/no-testbench.md)。本轮已实时核对两套顶层与选定模块，没有新仿真。

看实际电路：[14 张关键 schematic 原图](schematics.md)，包含自举开关、动态比较器、CDAC 开关/阵列、异步控制和级间增益增强放大器。首项逐器件学习：[BOOSTRAP 的 MOS 电容与浮置节点](lessons/A02a-bootstrap-structure.md)。本轮已实时只读检查，性能仍待仿真。

这条路线使用服务器 `ADC_PROJECTS_ROOT` 中的四个工程，补充 [电路主线](../00-circuit-foundations/README.md)。默认先学 8 位异步 SAR 的完整晶体管信号链，再学 Pipelined-SAR 的残差放大与数字对齐；ADS8681/ADS1248 作为精密 ADC 扩展。基础 PLL 仍按 P01–P04 展开，不被本路线替代。

2026-10-04 接管阶段核实四个工程、14 个库、原包和关键 cell/view，复核先前 bridge 导出及选定文件哈希；该次没有 live OA 读取，详见 [接管证据](../../notes/evidence/2026-10-04-adc-projects.json) 与 [接管记录](../../notes/2026-10-04-adc-projects.md)。随后查看电路图的独立会话已实时读取 14 个关键 cell，见 [新原图与连接证据](../../notes/evidence/2026-10-04-adc-schematics.json)。两阶段均无新网表或仿真。作者报告值是待复现目标，不作为当前成绩。

## 工程选择

| 工程目录 | 实际入口 | 适合学习的机制 | 当前边界 |
| --- | --- | --- | --- |
| `async_sar_8bit_40MSps` | `8_bit_sar_adc/8bit_SAR_ADC_test` → `SAR_ADC` | 实际自举采样、Vcm-based CDAC、动态比较器、异步握手与码输出 | 21 个 cell 目录；前仿基线待运行 |
| `pipelined_sar_12bit_100MSps` | `Pipe_SAR/Pi-SAR_amp` | 两级量化、残差传递、gain boosting、冗余与数字对齐 | 46 个 cell 目录；名称中的 #2d/#2e 是文件夹编码，OA 名称以导出核对 |
| `ads8681_reverse_engineering` | `HIX_2012210_TOP/TOP_HIER` | 精密 SAR 的前端、reference、采样与比较器 | 顶层/PGA/SC/SAR/COMP 已选读；模型与时序待验证 |
| `ads1248_reverse_engineering` | `HIX_2012180TOP/TOP_HIER` | ΔΣ、PGA、SC 电路、低频噪声与参考 | INPUT_MUX→PGA→SC→AMP→COMP 已追踪；阶数/滤波/模型待验证 |

`cadence_verification` 适合已有 ADE 工具链、测量表达式和受控回归；8 位异步 SAR 适合把自举—CDAC—比较器—逻辑的真实连接贯通。两个工程的比较器、PDK、位数和时序不同，已有 10 位工程的 190/198 ps 结果不能移植到这里。

## 课文与验收顺序

| 单元 | 课文 | 本次只验收一个问题的建议 | 最终产物 |
| --- | --- | --- | --- |
| A01 | [8 位异步 SAR：架构与电荷](lessons/A01-async-sar-architecture.md) | 七组受控电容为何对应八次判决？ | 参考域、位权、极性、一次转换事件图 |
| A02.1 | [实际模块 TB 与结果分析](lessons/A02-module-testbenches.md) | `BOOSTRAP_test` 能否在 2 pF 上完成采样？ | 分相图、held error、端间电压轨迹 |
| A02.2 | 同上：比较器 | 小过驱动下多长时间产生可用决定？ | 极性与延迟、复位、共模/负载边界 |
| A02.3 | 同上：CDAC/reference | 切换的电压步幅正确，且在下次比较前建立吗？ | 单 bit 曲线、共模、reference 动态 |
| A02.4 | 同上：异步环路与系统 | 八次判决能否正确终止，并给出一个稳定码？ | 短 DC 基线、有效码采样，随后相干 FFT |
| A03.1 | [Pipelined-SAR：残差与数字合成](lessons/A03-pipelined-sar.md) | 第一级残差怎样进入第二级？ | 实际级间传递、输出极性与 range |
| A03.2 | 同上：放大器/冗余 | 长窗与短窗误差分别由什么主导？ | 增益/动态建立、辅助环路、数字延迟对齐 |
| A04 | [精密 ADC 逆向电路研读](lessons/A04-precision-adc.md) | 一条选定模拟链究竟有哪些可见模块？ | 层级功能图、可运行子模块 TB、模型限制 |

各单元包含机制、工程入口、预测问题、最小实验和结果分析；未运行的项目均保持待验证。A02 的模块实验可关联 S02/S03/S04，A03 在 SAR 信号链掌握后进入，A04 可选。已有教学公式不替代实测电路验收。

## 进入仿真的条件

从 `config/local.env` 读取 `ADC_PROJECTS_ROOT`、`ADC_LEARNING_ROOT`。服务器旧学习环境已提供独立 `cds.lib` 和 bridge 配置，先核对目标 PID、cwd、port、库映射与 PDK；不要给当前 GPDK045 课程会话直接混入这些工程。源库留原处，运行前创建可恢复的学习副本，并绑定副本 master。

先前记录指出：8 位系统 TB 的 config 指向 `SAR_ADC/calibre`，保存 ADE state 却指向 schematic；原模型路径带作者机器绝对路径。独立学习库映射选择 SMIC v1.11_4，Pipe_SAR 使用 tsmcN65。这些是已有环境记录，当前模型解析和网表兼容性仍需新检查。前仿先明确绑定 schematic，后仿单独校核 calibre view 和模型。

每个 TB 使用 [模块记录模板](../../notes/circuit-lab-template.md)。完整 OA/PDK/PSF 留服务器，Git 仅保存课文、脚本与证据摘要。先预测，再按新网表和波形检验；仿真器结束、指标有效、设计满足要求分别记录。

下一项具体操作：先完成 A01 的电荷与控制极性判断；第一项新仿真优先选择独立 `BOOSTRAP_test` 工作副本，核对模型和源时钟后短时 transient，观察采样建立与保持。不直接运行长 FFT 或沿用作者 ENOB。
