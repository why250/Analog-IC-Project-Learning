# A07：PRF 周期中的采样、保持、复位与转换

状态：课文已准备；已只读读取 CTRL_3、COUNT_4B_1，确认滤波后开关的部分控制来源与 ADC 总线的计数/MUX 入口，见 [A04a](A04a-adc-feedback-readout.md)、[A05a](A05a-tx-support-structure.md)。完整 CTRL/clock/config/phase 事件表与新波形仍待验证，不能以静态连接宣称 PRF 时序通过。

## 问题与预测

只有 ADC_RDY 周期正确，能否证明四个结果来自正确光相位？先画一个 PRF 周期，标出 LED enable、TIA gain/offset、sampling switch、conversion switch、ADC reset 与结果锁存；指出最容易错位的交接点。

## 公开时序与实际时序

TI 第 13–15 页说明一 PRF 周期对应四组结果。2-LED 与 3-LED 模式的第二相不同：Ambient2 或 LED3。不能把 register 标签写有 ambient 当成当时物理 LED 一定关闭。

每一相都需要区分“照明稳定”“TIA 建立”“filter 采样”“hold”“共享 buffer 交接”“ADC reset/conversion”“结果更新”。部分动作可以在不同滤波支路间重叠。不要把全部动作想成单一串行四拍，也不要在没有波形时认定任何重叠安全。

最基本的建立约束是从实际输入/配置变化到读取时刻的可用时间。可写为 `Tavailable ≥ Trequired + Tmargin`，但 Trequired 是否等于各阶段延迟之和取决于阶段是否重叠。先建立事件依赖图再做预算。

控制位从配置到模拟开关可能经过 decoder、level shifter、buffer 与 reset。脚本设置值、磁盘保存值、当前会话值和实际 transient gate 波形是不同证据。此前 ADC 课程已出现保存设置被 active state 覆盖，本工程也必须看新网表而不是只看配置文件。

## 最小检查与实验

第一项可以只读：从一个 sampling switch 的 gate 向上追踪到控制源，写出相位身份与必要逻辑条件，不一次审计全部 I²C。

模型和 TB 就绪后，用外部可控 clock 和已知初始化开始一个受控 PRF 实验；内部 OSC 的启动另做。接口行为模型如被采用，要明确它提供哪些寄存器值、忽略哪些协议时延。

给四个输入相位赋不同但安全的电平或电流标签，保存 LED enable、gain/offset select、sample/convert/reset、held voltage、ADC result 与有效事件。不同幅度让相位交换可见；固定相同输入会掩盖错位。

先丢弃明确的启动周期，随后验收一个稳定 PRF 周期。每个结果都要对应先前真实采样窗，不能只按数组 index 标 phase。时序寄存器字段与极性在运行前查本机数据手册详细章节及实际源码，本课不编造地址。

## 证据与判断

交付事件表，包含事件边沿、实际相位、读取节点、允许建立时间、测得残差和 run 身份。一次只判定一个交接点，例如 sample → hold 或 reset → conversion。

若 ADC_RDY 正确但相位标签错位，系统失败点必须保留。验收正确时序后才能做 [A08](A08-noise-design-review.md) 的相位相减和系统误差预算。
