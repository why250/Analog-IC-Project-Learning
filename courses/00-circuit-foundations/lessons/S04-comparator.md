# S04：动态比较器如何复位、放大和再生？

问题：相同输入差分下，为什么输出已经翻转仍不能证明比较器满足 SAR 每位判决时间？先预测：输入差分减小时，再生时间与误判概率怎样变化？

## 当前比较器的真实层级

core 的 `I55 → saradcII/comparator` 包含 `I0 → saradcII/latch_buffer`、`I1 → saradc/srlatch_nand` 和 `I11 → saradc/clockdriver`。`latch_buffer:I0 → saradcII/latchonly_updated` 是晶体管动态再生核，外有 clockdriver 缓冲。

锁存核中 `NM4` 是 gate 接 `clk`、源接 `vssa!` 的尾管；`NM2/NM3` 是输入差分对，源共接 `net041`，gate 接 `Din+/Din−`。`PM4/PM5` 预充电内部 `net049/net043`，`PM0/PM3` 预充电 `sb/rb`，gate 都接 `clk`。`NM0/NM1` 与 `PM1/PM2` 构成交叉耦合再生支路。

因此逻辑低相位对应尾管关断和预充电，逻辑高相位进入 evaluate；实际相位还受前级 clockdriver 极性影响。结构属于单尾动态再生比较器，适合用 StrongARM 类机理分析；具体支路连接、输出 polarity 和缓冲阶段仍按本图核对，不依据名称认定标准拓扑。

## 三个过程要分开测

Reset 要把内部和输出节点恢复到已知初态。复位不足产生 memory effect，表现为前一次判决影响下一次。Evaluate 初段由输入差分电流拉开内部电压，再进入交叉耦合正反馈。近似再生关系为 `Δv(t)=Δv0 exp(t/τreg)`，`τreg≈Ceff/gm,reg`；到输出阈值的时间近似 `τreg ln(Vtarget/|Δv0|)`，总延迟还包括前放大、clock path 和输出缓冲。

输入差分越小，理想确定性判决时间越长；真实噪声和 offset 决定初始差分，可能改变方向。没有达到输出阈值的样本应记录为未决，不能从统计分母删掉。SAR 需要的是在有效窗口内给出正确且稳定的决定。

本工程在 comparator 到 latch_buffer 的 `Din+/-` 有交换，外层 SR latch 又重新映射 `out/outb`。必须做小正差分/小负差分对照，从最终 `outp` 回到控制器追踪符号；仅看锁存核的 sb/rb 会遗漏反相。

## Offset、噪声与 kickback

系统性 offset、mismatch offset 和随机噪声分别来自不同实验。nominal 扫输入得到的阈值不是 Monte Carlo 分布；无 transient noise 的多次相同运行不能测随机误判概率。噪声实验扫差分电压并重复判决，拟合 `P(1)` 转移曲线；若采用高斯模型，曲线中心与宽度分别估计 offset 与输入等效噪声，但应报告模型假设和未决比例。

Kickback 是内部快速跳变经寄生耦合输入。理想电压源把端电压强行固定，可能只能看到注入电流；以有限源阻抗或 CDAC 等效负载测输入扰动，才接近系统条件。减小输入对尺寸可能减小耦合，但会损害初段增益、噪声与 mismatch，要用同条件对照。

## TB 对应与最小实验

`saradc/comparator_offset_TB_new` 的 DUT 是 `saradc/comparator`；`saradc/comparator_noise_TB_new` 的 DUT 是 `saradcII/comparator`。本轮只读比较发现两者外层连接相同，都指向相同 latch_buffer；仍需新网表确认最终 view、尺寸与模型。offset TB 保存 tt transient/ramp；noise TB 保存 PSS/PNoise，不能因为名字带 noise 就当成多次随机判决实验。

先运行 offset TB 的独立 ADE 副本，证明网表、模型和 transient 工具链可用。然后在模块实验副本中用固定差分输入，扫 ±1 LSB、±0.25 LSB 与接近零的小输入，保持相同共模、clock 和负载；保存内部两节点、sb/rb 和最终输出。记录 evaluate 边沿到正确输出门限的时间，以及下一次复位前是否反转。

随后缩短 reset 时长，以交替大正/大负输入检查记忆效应。噪声/Monte Carlo 最后各自独立运行。验收：给出 reset/evaluate 导通图、polarity 对照、判决时间曲线和适用输入范围；新运行的具体结果写实验记录，课文中的公式不算验证通过。

下一课：[SAR 时序与预算](S05-sar-timing-budget.md)。

实际实验续篇：[reset/evaluate 与保持输出的新波形](S04a-reset-evaluate-evidence.md)。2026-10-04 已完成四个固定小差分条件的 nominal 动态核检查；不是 S04 整课、统计噪声或系统判决预算验收。

配套实验读图：[关键 TB 的作用与结果分析](00-testbench-results-guide.md)。区分保存配置、待执行实验与已新运行的结果。
