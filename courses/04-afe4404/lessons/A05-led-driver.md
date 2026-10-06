# A05：LED 电流控制、compliance 与脉冲电荷

状态：已只读确认 TX 路径为顶层 `MI152 → HIX_1907151SUB/AMP_5` 与 `MI341 → SWITCH_BLOCK`，后者直接连接 TX1–TX3。原图见 [图册入口](../schematics.md)。此前 DRIVER_1/2 候选经连接更正，它们实际在 ADC_RDY/PAD7/CLK 的 I/O 路径；LED 控制码、工作点与器件模型未验证。

## 问题与预测

先读 [A05a TX 与配套结构](A05a-tx-support-structure.md)，明确 AMP_5/SWITCH_BLOCK 的端口环路、供电与接收耦合，再测码步和 compliance。

固定一个 LED 电流码，逐渐降低 driver 支路可用电压，电流在哪个范围开始下降？先从器件堆叠预测 compliance 约束，并预测大电流短脉冲比小电流长脉冲更容易受哪项限制。

## 驱动机制

TI 第 1、16 页说明 common-anode LED 配置与 6-bit programmable current，默认 0–50 mA，63 个间隔；一个理想步长约为 50/63 mA，而不是 50/64。加倍模式约 100 mA，高电流端可能因饱和而精度变差。这些是资料规格，不能直接写成 HIX 支路的当前电流。

实际镜像或受控电流 sink 需要足够端电压维持工作区。可用电压约等于 LED 供电减 LED forward voltage、连接压降和开关压降；器件堆叠、反馈放大器输出范围与 bias 决定额外余量。先读 actual TX polarity，再确定扫哪个节点以及安全电压范围。

光信号对电流、LED 光效、光路和 photodiode responsivity 均敏感。用于起步的固定 CTR 只是系统行为假设，不能代替组织/光路模型。电学实验优先测 `Qpulse=∫ILED dt`，同峰值下脉冲建立与关断尾巴会改变实际电荷和平均功耗。

高电流脉冲也扰动 TX_SUP、地回路及邻近接收链。供电网络理想化时无法评估这些耦合；即使 LED 电流本身平坦，也不能证明 TIA 不受影响。

## 最小实验

从 TX1–TX3 追到真实 driver 与控制 DAC，区分三 LED 相位与同一支路内的码位。建立独立电流驱动 TB，先选一个支路，一个中等合法码，一套固定 bias。

第一轮用受控端电压扫 compliance，记录平台电流、相对误差、关键器件工作区与电源电流。允许电流误差先按实验目标规定，不能事后把拐点附近的误差当合格阈值。

第二轮固定端电压后才测 pulse：保存码、enable、ILED、TX 电压与供电电流，测实际积分区间、峰值、达到允许误差带的时间及关断尾电荷。理想电压钳位会省略真实 LED I–V，报告时注明。

## 证据与判断

验收一个问题：固定码的有效 compliance 范围，或固定脉宽的电荷误差。把静态 DAC 非线性、输出阻抗与脉冲建立分开。

若加大 driver 尺寸改善 compliance，却增加门控充放电、glitch 和功耗，后续变更应保留这些约束。不要以电流越大推断 PPG SNR 必然越高。下一课 [A06](A06-bias-reference-ldo.md) 确认供电和参考条件。
