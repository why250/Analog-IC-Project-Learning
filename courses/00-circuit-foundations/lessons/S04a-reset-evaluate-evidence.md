# S04 实验续篇：动态核复位，为什么最终输出没有复位？

本次只验收一个问题：固定小差分输入下，实际动态核是否正确复位、在 evaluate 窗口内完成正确方向的再生？新 transient 已运行；学员理解仍待反馈。主课见 [S04](S04-comparator.md)，条件与运行身份见 [实验记录](../../../notes/2026-10-04-comparator-delay.md)。

## 先预测，再看证据

已提出预测：相同共模和时钟，输入差分从 ±1 mV 减小到 ±0.1 mV，判决时间怎样变化？截至记录尚未收到独立预测。助教采用“更慢、方向保持”的待检验假设；以下是实验结果，不代表学员已独立得出结论。

## 用实际晶体管解释 reset/evaluate

实验 DUT 是 `saradcII/comparator`，层级为 `I9/I0 → latch_buffer`、`I9/I0/I0 → latchonly_updated`。核心的 `NM4` 是时钟尾管，`NM2/NM3` 是输入对。`PM4/PM5` 分别预充电 `net049/net043`，`PM0/PM3` 分别预充电 `sb/rb`。交叉耦合的 NMOS/PMOS 支路决定再生。

| 动态核时钟 | 器件动作 | 节点后果 |
| --- | --- | --- |
| 低，相位尾端 | NM4 关；四只时钟控制 PMOS 开 | x=`net049`、y=`net043`、sb、rb 被预充电，原始差分归近零 |
| 上升并进入高相位 | PMOS 预充电逐步关断，NM4 导通 | 输入对拉开内部差分，随后交叉耦合支路放大差分 |
| 高相位后段 | 再生进入大信号 | sb/rb 一高一低，后级 buffer 与 SR latch 保持决定 |

这个表是相位端点的机制说明。MOS 导通是连续过程，时钟缓慢跨越期间存在过渡；不能把 0.6 V 测量门限当作所有 MOS 同时切换的物理瞬间。

本实现把 comparator 的 Din+/Din− 在 latch_buffer 入口交换。正外部差分对应内部 Din− 更高：其支路较快放电，经再生得到 sb>rb。外层 NAND SR latch 的映射最终使 `out>outb`。负差分的方向相反。本次正负四个条件都与这条连接推导一致。

## 新波形与测量口径

![比较器内部时钟、节点、原始判决和保持输出](../../../notes/evidence/2026-10-04-comparator-delay.png)

条件：tt，27°C，VDD=1.2 V，输入共模=0.6 V，外部 clock=1.2 GHz，源边沿=10 ps，tran stop=10 ns，maxstep=2 ps，无随机噪声，无新增输出负载。保留原 `comparator_noise_TB_new` 的理想 balun/DC 输入连接及比较器内部 buffer/SR latch。

图以稳态某次 **动态核 clock 跨过 0.6 V** 为 t=0。上图显示 x/y 的预充电与放电；中图显示 sb−rb 的复位和再生；下图显示最终 out−outb 保持前一次结果。图是小型重采样片段；测量用原始 adaptive-step 波形和线性 crossing 插值。

延迟定义为内部 clock 上升过 0.6 V，到带预期符号的 sb−rb 达到 1.08 V（0.9VDD），并保持到 evaluate 窗口结束。先舍弃三次启动 evaluate，再测五次连续 evaluate。

| 外部差分 | 动态核判决时间，约 | evaluate 尾端最终 out−outb |
| --- | --- | --- |
| +1 mV | 190 ps | +1.2 V |
| −1 mV | 190 ps | −1.2 V |
| +0.1 mV | 198 ps | +1.2 V |
| −0.1 mV | 198 ps | −1.2 V |

内部 clock 的实际 0.6 V 高相位约 446 ps；顶层 clock 到内部测量边沿约 63 ps。原始节点在 evaluate 前回到近零差分，本组最大 reset 差分小于 0.2 µV；这是对称 nominal 固定输入条件下的结果，不代表 mismatch 或交替输入下没有 memory effect。

## 如何形成设计判断

输入缩小十倍，测得延迟增加约 8.5 ps，方向不变；没有增加十倍。简化模型 `t≈tinitial+τreg ln(Vtarget/|Δv0|)` 提示输入与延迟之间不是线性比例，但本次只测两个幅度，不能据此拟合或确认 τreg。总测量还包含输入放电和大信号输出建立。

最终 SR latch 在 reset 相位继续保留此前输出，因此固定正输入的连续周期中 out 一直为高。只从最终输出找 crossing，会漏掉再生完成事件或得到零延迟。要测外层 buffer/SR latch 的完整更新延迟，需要输入交替、让新旧决定不同，并同时保存原始节点。

本轮四个条件通过约定的 nominal 检查：reset 差分归近零、原始决定在本地 evaluate 窗口达到门限并保持、最终符号正确。约 2 ps 的最大步长、moderate 精度与线性插值意味着细小小数位不是测量精度声明。没有运行随机噪声、失配、有限源阻抗、实际 CDAC 负载或系统控制采集窗口，所以不能宣称 SAR ADC 的高速判决预算已闭合。

下一项具体操作：在同一实验系列中改用正负交替小差分，测最终决定从旧值更新的时间，并缩短 reset 检查 memory effect；先只选择其中一个可验收问题。随后回到 [S02 CDAC](S02-cdac.md) 的电荷与位权学习。
