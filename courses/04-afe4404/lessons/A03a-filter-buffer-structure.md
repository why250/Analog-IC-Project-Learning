# A03a：差分存储、交接开关与 ADC 前模拟接口

本课问题：TIA 输出采样后，电荷保存在什么节点，经过哪些接口电路才到 ADC？原图：[SWITCHED_RC_FILTER](../../../notes/evidence/afe4404/SWITCHED_RC_FILTER.png)、[VOL_GEN_1](../../../notes/evidence/afe4404/VOL_GEN_1.png)、[AMP_BLOCK](../../../notes/evidence/afe4404/AMP_BLOCK.png)。控制相位和动态性能尚未验证。

## 预测：保持值与 ADC 输入为什么可能不同

先预测两个变化：前一相位幅度增大、ADC 前端负载增大。在 TIA 输出相同且采样时间不变时，哪些节点会首先出现不同？将采样本身的残差、交接瞬间 charge sharing 与后级建立分开。

## 实际差分存储节点

新读取的四只 mim_1p0fF 存储实例跨两个信号节点，而不是都接地：

| 实例 | TOP | BOT | 保存的 c / m |
| --- | --- | --- | --- |
| C18695 | net52 | net44 | 4.21707483 pF / 6 |
| C18694 | net54 | net46 | 同上 |
| C18693 | net56 | net48 | 同上 |
| C18692 | net58 | net50 | 同上 |

c 与 m 是保存字段，未核对 netlisting/CDF 前不将 4.217 pF 或其六倍作为仿真总电容。两端都是信号节点意味着电容直接存储差分电荷；每端的对地寄生、开关寄生和 bulk 仍影响共模，不能用差分电容一项描述全部状态。

VOUT1 的四路选择开关 MI290–MI293 接 net52/net58/net54/net56；VOUT2 的 MI294–MI297 接 net44/net50/net46/net48。同一对存储节点的输出选择使用同组 OE/OEN，例如 net52/net44 对用 X21138_ZN/X21273_ZN。控制属于内部 nets，尚未将它们命名为 LED1/LED2/ambient 的具体相位。

开关的 A/Z 端名是子 cell 端口，模拟导通后通常要按两端电压求双向电流；不能从 A→Z 的图形箭头推导单向电荷传输。下一步需同时核对输入侧电阻/采样开关与输出选择，写出每只电容的 sample、hold、transfer 状态。

## 顶层接口已经接完整

```text
FILTER.VOUT1=net829 → MI312.A/Z → net721 → MI199/VOL_GEN_1.VI1
FILTER.VOUT2=net761 → MI313.A/Z → net720 → MI188/VOL_GEN_1.VI1
MI199.VO=net822 → AMP_BLOCK.VI1_1
MI188.VO=net765 → AMP_BLOCK.VI1_2
AMP_BLOCK.VO1_1/VO1_2=net820/net821 → ADC_1.VI1_1/VI1_2
```

N20855 的 D/S 跨 net720/net721，G=X21158_ZN。因此交接节点之间还存在受控通路；何时均衡或复位需要 gate 相位证明，不能直接称它为 ADCRST 开关。MI312/MI313 的 OE/OEN 来自 CTRL_3 的 Z1N/Z1 连接，但有效电平需下降到开关单元确认。

## VOL_GEN_1 的电压反馈证据

两只 VOL_GEN_1 共用 VI2=P14069_D，VS=X13454_VS、VS1=RX_SUP，各有 NIB 与 enable。在内部，P25107.G=VI1、P15100.G=VO、S 均为 P15098_S。这组共源 PMOS 将外部输入和自身输出同时送入内部支路，支持局部电压反馈的结构判断。

VO 还有 N16359.D 与 P14966.D 两条上下供电支路，gate 分别为 net76/net77；C18765/C18764 连接 VO 与 net93/net94。由此可学习输入比较、输出驱动及内部动态耦合；不能尚未核对负反馈方向就宣称它是理想 unity buffer，也不能保证增益正好为 1。

VI2 影响多只 NMOS gate，供电又有 VS/VS1 两域。共模参考、headroom、enable 初始化与动态驱动都可能影响传输。做接口实验时不能只保留一个“理想 buffer”而丢失这些条件，再将结果当真实电路性能。

## AMP_BLOCK 是多条路径汇合的模块

AMP_BLOCK 内包括 MI315/AMP_3、MI3/MI5 两个 AMP_2、MI83/AMP_1，以及 CAP_SWITCH_1、CAP_SWITCH_1S1、CAP_SWITCH_3、RC_SWITCH、RC_CELL_1。其 VI1、VI2、VI3 三组差分入口分别由不同顶层模块驱动。

MI83/AMP_1 的 VOP/VOM 直接接 VO1_1/VO1_2，VP/VM 接 VI2_2/VI2_1；MI87/MI86 的 RC_CELL_1 从输出返回 VI2_1/VI2_2。VI2 同时接 DAC_1 输出，所以这层不能只看 VI1 而忽略数字返回电流。

两个 AMP_2 的输入输出经电阻、电容选择和其他开关与 AMP_3/AMP_1 网络相连。AMP_3 有 VOP1/VOM1 与 VOP2/VOM2 两组输出，后一组接 AMP_BLOCK.VO2。端口数量与图上有几个放大器不能直接证明积分器阶数；需要确定每个相位哪些电容闭合、哪些电阻有效、哪些状态跨周期保存。

原图：[AMP_1](../../../notes/evidence/afe4404/AMP_1.png)、[AMP_2](../../../notes/evidence/afe4404/AMP_2.png)、[AMP_3](../../../notes/evidence/afe4404/AMP_3.png)。逐个下降时先将 bias/enable 与信号端分组，再追电荷状态；从一个固定相位求等效电路，比一次给整个模块贴架构标签更容易验证。

## 电荷和建立的推导条件

差分电容可写 `q=C(VTOP−VBOT)`。它与外界断开时，理想差分电荷保持；实际 leak 与两端寄生使电压继续变化。交接时若两个存储单元和寄生连接成新网络，应对每个浮置节点列电荷守恒，同时加入参考或低阻驱动的边界条件。

简单的 `Vshare=(CsVs+CbufVbuf)/(Cs+Cbuf)` 只适用于相同参考端、同一瞬间近似无源的单端网络。这里跨信号节点的电容不能未经变换直接套入该式。交接之后 VOL_GEN_1 和 AMP_BLOCK 还可能继续驱动和建立，瞬间阶跃不等于最终测量误差。

## 最小实验与验收

当前验收选择一对存储电容，标出两个采样入口、两端保持节点、输出选择、N20855 和 ADC 前节点。相位未知处明确空缺。模型就绪后固定当前相位输入，只改变前一相位幅度，逐节点定位第一处残差；负载变化留下一轮。

进入 [A03](A03-switched-rc.md) 分别测建立、droop 或记忆。ADC 之前的接口可信后，再进入 [A04a](A04a-adc-feedback-readout.md) 研究判决与返回路径。
