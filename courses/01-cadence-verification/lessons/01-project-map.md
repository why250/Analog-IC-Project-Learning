# 第 01 课：接管 SAR ADC 工程，建立验证地图

**工程问题：** 接手一个带 Maestro 的 ADC 工程后，你需要哪些证据，才能判断它跑出的指标有意义？

本课约 60–90 分钟，完成工程侦察和验证计划。无需先跑完整仿真。输出写入 [本课记录](../../../notes/01-project-map.md)。

2026-10-01 已接管 `IC_Server` 的 ADC 工作区，完成原包校验和部分只读层级检查，尚无新仿真。当前小任务见 [续篇：谁定义真正的采样事件？](01a-sampling-entry.md)，用实际 `I0/I56/I22` 控制链解释 12 个内部周期，并准备波形检验。

## 1. 先提出判断（10 分钟）

先不看后面的推导，写下你的预测：

1. 对一个 10 bit、100 MS/s SAR ADC，转换时钟与采样时钟可能是什么关系？哪些事件消耗额外周期？
2. 接近 Nyquist 的单音测试，可能暴露哪些问题，又可能遗漏哪些问题？
3. 顶层混用晶体管和行为模型时，哪些性能结论需要特别核实模型边界？

目标是形成可检验的判断。后面发现预测有误时保留原判断，并记录改变判断的证据。

## 2. 找到工程入口（15 分钟）

按 [环境说明](../../../docs/environment.md) 检查路径并启动 ADC 工作区。先读原包 `README.txt`，再在 Library Manager 定位：

| 用途 | Library / Cell / View |
| --- | --- |
| 顶层 testbench | `saradc / 10Bit_ADC_TB_new / schematic` |
| 本课 ADE 入口 | `saradc / 10Bit_ADC_TB_new / maestro` |
| 后续回归计划 | `saradc / 10Bit_ADC_Run_Plan / maestro` |

从顶层原理图识别 DUT 实例及其真实 master。不要仅凭库中存在 `10bit_adc_core`、`10bit_adc_core_ideal` 等名称，就认定它们被当前 testbench 使用。

沿一条实际层级追踪输入采样、CDAC、比较器、SAR 控制和输出观测路径。用表格或手绘框图记录：实例路径、功能、master、可用视图、当前绑定视图和边界假设。未能确定实际绑定时先标“待网表确认”。

检查 `WORK/saradc/cds.lib → common.lib → 设计 cds.lib/工具 cds.lib` 的包含关系及后续重定义，确认 `saradc`、`saradcII`、`gpdk045`、`analogLib` 解析到本机存在的目录。工程能在 Library Manager 出现，不等于其模型与仿真设置全部可用。

## 3. 用配置还原测试意图（20 分钟）

下面是建课时从 `10Bit_ADC_TB_new/maestro/maestro.sdb` 的 active test 静态读取的值，来源见 [资料索引](../../../docs/sources.md)。**它们是文件中的保存配置，仍需与当前 ADE 会话及最终网表核对。**

| 变量 | 文件值/表达式 | 需要解释的工程含义 |
| --- | --- | --- |
| `numberofbits` | `10` | 与输出位宽、控制周期是否一致？ |
| `VDD`、`VCM` | `1.2`、`VDD/2` | 供电和输入共模如何进入 DUT？ |
| `fsample` | `100M` | 采样事件实际由哪个信号定义？ |
| `fclk` | `(numberofbits+2)*fsample` | 额外两个周期分别做什么？ |
| `numPoints`、`tone` | `1024`、`503` | 实际 FFT 是否使用同样的长度与输入频点？ |
| `fin` | `(fsample/numPoints)*tone` | 单音与采样序列之间的关系 |
| `percentFullScale` | `840m` | 数值为 0.84；沿表达式和输入源核对其幅度定义 |
| `fullInputScale`、`vin` | `VDD/2`、`percentFullScale*fullInputScale` | 单端/差分、峰值/峰峰值的实际约定 |
| `TSTOP` | `(4+numPoints)*tsample` | 前后额外样本是否足以覆盖启动过程？ |
| `TSTOP_tran` | `TSTOP+40n` | 与真正的截取窗口是否一致？ |

先自己计算，再与以下参考推导比对：

- `tsample = 10 ns`；`fclk = 1.2 GHz`，每个采样周期对应 12 个内部时钟周期。每个周期的用途必须由电路和波形确认。
- `fin = 49.12109375 MHz`；若确实以 100 MS/s 取连续 1024 点，则记录长度为 10.24 µs，FFT 频点间隔为 97.65625 kHz，输入对应第 503 个频点。503 与 1024 互质支持这一相干采样安排；仍需确认启动已结束、输出解码和实际取样时刻正确。
- `TSTOP = 10.28 µs`，`TSTOP_tran = 10.32 µs`。这不能直接证明某个 FFT 表达式拿到了 1024 个有效码。
- 按变量表达式，`vin = 0.504 V`。不要在检查差分源连接之前，将它直接解释为 ADC 差分输入峰值。

另一个值得调查的线索：文件中 `f_fftbin = fnyquist/128`，按当前变量得到 390.625 kHz，与上述 1024 点频点间隔不同。**这不是已确认的错误**：找出它是否被使用、用于哪个表达式、是否对应不同的数据长度或旧配置；查清之前不修改。

## 4. 审查模型和测量边界（20 分钟）

建课时从 `active.state` 读取到：

| 配置 | 保存值 | 本课检查任务 |
| --- | --- | --- |
| simulator / design view | `spectre` / `schematic` | 与当前 test 和实际网表一致吗？ |
| transient stop | `VAR("TSTOP_tran")` | 会话解析出的终止时间是多少？ |
| `strobeperiod` / `errpreset` | `10n` / `moderate` | strobe 相位与有效输出码的关系是什么？ |
| model file / section | `$PROJECT/TECH/GPDK045/gpdk045/models/spectre/gpdk045.scs` / `mc` | 文件存在吗？section 内容是什么？ |
| switch view list | `spectre cmos_sch cmos.sch schematic veriloga` | 关键模块最后会采用哪个实现？ |
| stop view list | `spectre` | 层级在哪里停止展开？ |

`mc` 是保存的模型 section 名；仅凭这个名字不能断言启用了 Monte Carlo 分析。同样，保存了 `strobeperiod` 不能证明 FFT 取到了正确的码更新相位。核对 ADE 的分析、统计设置、输出表达式和实际数据路径。

选取一个动态指标表达式，追踪它的输入信号、数字码到数值的转换、采样相位、截取区间、点数和幅度标定。将读不到的部分写成第二课的验证任务，不填猜测值。

再检查旧机器绝对路径。保存状态中存在原作者的仿真输出目录；记录当前会话是否仍引用它，并规划映射到本机的工作目录。不要直接批量替换 OA 数据库内部内容。

## 5. 本课交付与复盘（10–15 分钟）

完成 [记录表](../../../notes/01-project-map.md)，至少交付：

- 一条从输入到输出的实际层级链及模型边界，含库/cell/view 或 GUI 证据。
- 一份采样/内部时钟/输入频率/仿真长度的计算，并核对 ADE 中当前值。
- 一个测量表达式的审计记录，或明确写出当前无法审计的阻塞原因。
- 第二课的最小实验计划：选哪个 test、哪些条件、看哪些信号、什么现象算通过。

用于讨论的问题：如果指标很漂亮，但比较器采用了无噪声的行为模型，你愿意签字确认哪一条结论？还需要什么实验才能扩大结论范围？

**完成判据：** 能用证据解释该 test 的目的、条件和模型边界，并列出尚未确认之处。如果尚不能打开工程或读取关键配置，记为 blocked/进行中。创建课文或读过本页不算完成实操。

下一课将按这里确定的条件建立 nominal transient 基线，先确认采样与逐次逼近时序，再讨论频域性能。
