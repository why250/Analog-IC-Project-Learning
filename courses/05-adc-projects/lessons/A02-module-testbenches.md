# A02：沿实际采样链读关键 TB 和结果

实际结构入口：[原生电路图目录](../schematics.md)，以及 [BOOSTRAP 逐器件读图](A02a-bootstrap-structure.md)。2026-10-04 后续已在独立会话实时只读核对并导出这些关键图；本课所列实验尚未执行。

本课把 [A01](A01-async-sar-architecture.md) 的静态模型变成可以运行的实验。以下连接来自已有只读 bridge 导出；各项新仿真仍待执行。所有实验先在独立副本解决 PDK/view/激励配置，再一次只改变一个因素。通用测量方法见 [关键 TB 导读](../../00-circuit-foundations/lessons/00-testbench-results-guide.md)。

## 1. BOOSTRAP_test：采样精度与自举机制

库 `8_bit_sar_adc`，cell 名确实拼作 `BOOSTRAP`。`BOOSTRAP_test/schematic` 中 I4/I5 分别采样 VIP/VIN，输出 SH_P/SH_N；两侧各接一个 2 pF 理想电容。源电源为 1.8 V；输入正弦为 Vcm±vrange，时钟周期为 1/f，边沿参数为 tr，保存器件属性未显式给脉宽。需从新网表确认实际 duty 和采样有效极性。

这是一个有实际负载的双路采样 TB。A01 推导 core 每侧 CDAC 名义总电容约 1.9845 pF，与这里 2 pF 接近；但 CDAC 是浮置、受 reference 切换及比较器耦合的网络，固定接地电容不能替代全部系统环境。

预测问题：在固定 2 pF 和 clock 下，把输入推向摆幅端点，held error 的变化主要来自建立还是关断？先画 BOOSTRAP 中每只 MOS 的 reset/track/hold 导通关系，从实际 gate/source/drain/bulk 找出采样管和浮置电容。不要由“自举”二字假定各端 Vgs 恒定。

第一实验用 DC 输入替代 sine，在同一共模下选中间及两端的电平，短 transient 保存 clock、输入、输出、浮置电容两端、采样管端间电压。区分三个测量：

| 量 | 测量定义 | 如何判断 |
| --- | --- | --- |
| acquisition error | 关断前指定时刻 Vout−Vin | 扩大 track 窗若明显改善，建立是主因之一 |
| pedestal | 关断后稳定值减关断前值 | 保持相同时钟/输入，观察关断电荷耦合 |
| droop | 保持阶段 Vout 随时间变化 | 与泄漏、Cload 和保持时长关联 |

第二实验才用 sine：每个 aperture 后在保持窗口取一个样本，与 Vin(t_aperture) 比较，检查差分误差、共模跳变和输入相关误差。延长采样窗、增加负载与改变输入源阻抗分别作对照。既改善 Ron 又增大 clock driver 负担的修改，需要同时复查建立和端间电压。

输出一张分相图、一张 input/held/error 波形和一张 worst-case Vgs/Vgd/Vgb/Vds 表；额定限值依据实际 PDK。零误差的理想电压源或行为开关不能证明该晶体管模块通过。

## 2. compare 系列：先解决激励与极性，再读 delay/offset/noise

已有 `compare_test`、`compare_os`、`compare_input_noise`，它们均实例化 `8_bit_sar_adc/compare`。这个 comparator 与 GPDK045 教材的 `saradcII/comparator` 是不同电路。

`compare_test:I7` 的 DACP 接 VIN、DACN 接 VIP，OUTP/OUTN 又交叉接到顶层输出；两侧负载为 CL。不能仅凭顶层 OUTP 的名字判断输入正差分的方向。先分别固定小正/负差分，从 DUT 内部到顶层输出建立极性表。

先前导出还显示 VIN 对地有 V7（VCM）和 V9（905 mV）两个理想 DC 源，VIP 对地有 V8（900 mV），同时 V11 在 VIP/VIN 间施加 PWL。该连接可能形成重复约束或不一致的理想源回路；这是静态发现，尚未通过新网表确认。学习副本中应采用唯一明确的共模+差分激励，不凭原设置直接跑性能。

预测问题：输入幅度缩小十倍，evaluate 到决定有效的时间如何改变？保持共模、clock slew、load 和 reset 相位，定义 t0 的 clock 门限，定义有正确符号且保持到接收时刻的输出门限。原始节点与最终输出同时保存；对有输出保持的实现，用正负交替输入测完整更新时间。未决和超时单独计数。

| TB | 原激励特征 | 本课程的结果分析 |
| --- | --- | --- |
| `compare_test` | CL 负载，clock delay 3.5 ns、10 ps 边沿，差分 PWL | 校正激励后测方向、delay、小输入和负载敏感性 |
| `compare_os` | 一端 900 mV，另一端 890→910 mV ramp，CL 负载 | 阈值受 ramp slope/clock/reset 影响；反向扫描和缩步作对照，MC 另立实验 |
| `compare_input_noise` | 一端 900m+Vos，另一端 900m，CL 负载 | 名称不证明噪声启用；逐次判决概率的中心与宽度分别对应有效偏移与随机噪声 |

对噪声，先新网表确认源启用，noise-off/on 对照；每次有效相位采一个决定，统计概率和未决。Gaussian 拟合需要条件适合，并报告样本相关性。对 kickback，理想源可能钳住输入，只表现为注入电流；增加代表性 CDAC/源阻抗后同时看电压扰动。原作者关于比较器 offset 不影响精度或消除 kickback 的概括，必须按实际条件和实验重新判断。

## 3. CDAC/reference：用控制电平分开位权与动态建立

core 的 I34/I35 是 DAC_SW，两侧 P/N 接法互换；电容直接放在 `SAR_ADC` 中，七组受控权重 64…1 与一个固定单位电容。已有 `cap_mc/adexl` 入口只证明文件存在，不能当作已运行的失配结果。

预测问题：64Cu 互补切换是否同时改变顶板共模？理想同值两侧从中间参考切向相反 rails，差分变化约 0.9 V，而共模变化为零；详细电荷推导见 A01。独立模块 TB 需从副本提取同样的 capacitor/switch 网络，给确定的 P/N 序列与 sample 控制，保持两个顶板正确初态。

保存底板控制和电压、SH-P/SH-N、reference 源电流。先看最终差分步幅，再看指定比较时刻的 settling error；改变比较时刻能区分静态权重偏差和动态建立。改变 reference 阻抗后，若误差随大权重切换增强，检查参考电荷需求与恢复时间。理想共模恒定只能作为对照；失配/寄生/非同时切换会使顶板共模变化，进一步改变比较器工作点。

这个工程 VREF 接 VDD、VREF1 单独给中间电平，reference 与供电耦合需要保留。系统 DNL/INL 要依据 ADC 的 transition levels；模块 DAC 电平 DNL/INL 只能定位其中一类原因。

## 4. EN_LOOP/SAR_LOGIC：异步意味着事件约束

保存连接为 `compare → OUTP/OUTN → EN_LOOP/SAR_LOGIC`，再由 VALID、LATCH、CMP_OK 控制判决、更新与终止。A01 的逻辑化简是稳态推导，门延迟和毛刺必须看新 transient。异步环路没有理由让所有位的周期完全相同。

预测问题：某一位小残差使比较器变慢，会仅拉长这一位，还是使后续控制出错？在短 DC 输入运行中逐次标注 sample 结束、每次 evaluate、VALID、位推进、CDAC 切换、CMP_OK、最终 DFF 更新。观察相同采样内有几次有效决定，并校对下一次采样是否清除/重新开始。

正常终止要求最后一位完成后停止转换，最终码对应这一输入样本；有比较活动但没有新有效码，不算转换成功。若 VALID 在 reset 过渡中产生多次事件，应检查逻辑门限/毛刺；若下一次 evaluate 时残差仍变化，应检查 DAC settling 与握手的相对时序。不能机械把所有过程延迟相加，也不能因存在握手就假定模拟建立得到保证。

## 5. 8bit_SAR_ADC_test：输出测量与系统验收

DUT 是 IADC_0→SAR_ADC。I41/I42 的理想 DAC 是测量路径；DOUT<0> 接 vd7，DOUT<7> 接 vd0。整数码为 `Σ 2^(7−j) bit(DOUT<j>)`，先在真实有效更新后取稳定值，校对输入样本与输出延迟。

第一基线只使用避开 code boundary 的 DC 输入，测几个周期。随后用低频 sine、有效码 FFT；保存配置中 fin=3f/1024、f=40 MHz，对应约 117.1875 kHz。1024 个有效样本需 25.6 µs，再加启动舍弃与正确对齐。理想 DAC 的 100 ps transition 不应混入采样码的指标。

| 现象 | 先检查什么 | 受控诊断 |
| --- | --- | --- |
| 码方向/幅度不对 | 极性、位序、参考范围、采集相位 | DC 点与逐位 decode |
| 大进位附近局部错码 | 权重与该位 settling | 单 bit 和延后比较对照 |
| 高输入频率退化 | acquisition、时钟 jitter、输入相关 Ron | 相同幅度下扫频；模块 TB 复查 |
| 随机错误/超时 | 过驱动、noise、reset、握手 | 固定残差重复决定，分开噪声与失配 |

验收报告应同时给出一次转换事件图、可信有效码和指标定义。作者前/后仿 ENOB 7.837/7.377 留作复现目标，当前未运行。下一阶段见 [Pipelined-SAR](A03-pipelined-sar.md)。
