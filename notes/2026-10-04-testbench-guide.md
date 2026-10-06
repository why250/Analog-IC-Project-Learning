# 2026-10-04：关键 TB 的作用与结果分析

用户要求课程明确关键 testbench 的作用和结果分析。本轮补齐 [导读课文](../courses/00-circuit-foundations/lessons/00-testbench-results-guide.md)，链接到课程目录与相关模块课，并扩展 [模块记录模板](circuit-lab-template.md)。

## 本轮证据与状态

- 对七个 SAR 源 TB 的 schematic 作只读读取，分析和表达式来自保存 ADE XML；没有审计当前 Maestro 的生效配置，没有修改源 OA，没有新网表或仿真。
- 小型证据：[2026-10-04-testbench-guide.json](evidence/2026-10-04-testbench-guide.json)。记录源配置相对路径和 SHA-256；完整只读 schematic JSON 保留服务器 `COURSE_REMOTE_ROOT/2026-10-04-testbench-guide`。
- 已读 DUT、stimulus 和 saved outputs 分别标注；保存的 `mc` section、`noiseruns`、`noisefmax` 不作为 Monte Carlo/随机噪声启用证据。
- 课文的实测比较器数字仅来自此前 [offset 新运行](2026-10-03-comparator-nominal.md) 和 [延迟新运行](2026-10-04-comparator-delay.md)，没有使用源工程历史结果。
- 学员预测与设计判断：尚未验收。本轮新增教材，不能据此将模块或系统实验改为已完成。

## 得到的具体判断

`10Bit_capdac_TB_new` 由理想/行为 `saradc/adc_10bit` 驱动 `saradcII/10BIT_CAPDAC_ld1`，适合学习 DAC 重构、有效位权和建立；静态位权/DNL/INL 需独立可控激励，不能称已测完整 ADC 线性。

`comparator_tran_noise_TB` 的 `/out` 是额外的 0/1 observer：DUT net8/net011 经 E0 VCVS，送入 I9 `ahdlLib/comparator`。原 `average(clip(...))` 是时间平均，需校对窗口/观察器才能解释为决定概率；建议每次有效 evaluate 后定相位计数，并单列未完成决定。此发现避免把 `/out` 错认为 DUT 引脚或失效表达式。

`comparator_noise_TB_new` 的 InputReferredNoise 使用保存变量 gain=100；采样时刻与局部实际增益尚未验证。`clockPhaseGenerator_TB_new` 的 jitter 名称标 ps，表达式请求 Second，需核对显示/数据单位。顶层 ADC bus 顺序和 FFT 频率界限也需新网表/有效码审计。

比较器四点的 190/198 ps 是内部 clock→原始差分门限延迟。约 248 ps 是当前定义下的本地 evaluate 剩余时间；外层 SR latch 持有旧决定，系统采集与 CDAC settling 未覆盖。offset 双向 ±50 µV 与 100 µV ramp 网格相符，不能由平均近零推出零失调。

PLL 实际模块 master 尚未读取；新增 PFD/CP/filter/VCO/divider、startup/lock、小扰动动态、noise/spur 的实验用途和读图方法，均标为待执行。

## 下一项操作

沿现有独立比较器副本使用正负交替小差分，让最终输出更新，测 clock 到可采集输出的延迟。先验收这一项；reset/memory、CDAC、采样自举和 PLL 各另立实验。
