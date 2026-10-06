# P02：PFD、CP、filter、VCO 和 divider 分别怎样设计？

问题：PLL 里哪个模块的局部误差会变成稳态相位差，哪个模块会变成周期性调制？先预测：UP/DN 电流失配能否在平均锁定状态下消失？

以下是基础拓扑和实验方法，**不是已确认的 zambezi45 模块实现**。读取实际层级后逐项对照，保留不同之处。

## PFD 与 reset 路径

经典 PFD 用两只 DFF，D 置高，reference 与反馈分别触发 Q=UP/DN；两 Q 同高后组合门异步 reset。reference 先到产生 UP 脉冲，反馈先到产生 DN。Reset 延迟决定最小共同脉冲和 dead zone：过短可能被 CP driver 吞掉，过长增加同时导通、开关注入与 reference 周期扰动。异步 reset 释放的 recovery/removal 和同步边沿附近的数字时序也需检查。

模块 TB 固定两频率相同，扫正负相位差，测 UP/DN 宽度、重叠、极小相位附近的连续性；再加入小频率差，确认持续校正方向。只输出理想脉宽的行为 PFD 不足以判断晶体管 driver 的死区。

## Charge pump

基础 CP 包含受 UP 控制的源电流支路、受 DN 控制的 sink 支路及偏置/镜像。输出随 Vctrl 变化时，两支路有限 ro、compliance 与开关位置造成电流不等；current steering、regulated cascode 和保持内部节点等结构可改善动态误差，但增加电压余量、功耗与局部稳定性问题。

一次周期的净电荷是 `Qnet=∫ICP(t)dt`。锁定时为补偿 leakage、电流失配或注入，可能需要非零平均相位差；瞬时周期电流依然造成 Vctrl ripple 和 spur。测量重点是电荷面积，不能只比较脉冲平台电流。

CP TB 扫输出电压，分别测 IUP/IDN 与有效范围；再加规定脉宽，测单支路电荷和 UP/DN 重叠净电荷。报告 driver 上下沿、控制逻辑电压与输出负载，理想开关可能屏蔽动态失配。

## Passive loop filter

最简结构是 CP 输出经串联 R、C 到地，阻抗 `Z=R+1/(sC)`，提供积分和零点。实际常在 CP 节点并一个小电容 C2，使 CP 电流尖峰不直接形成大电压跳变，也增加高频极点。

以串联支路电容为 C1、并联为 C2：`Z(s)=(1+sRC1)/[s(C1+C2)+s²RC1C2]`。器件寄生、漏电、filter 输出接哪个节点都需从实际图确认。TB 可用 AC 电流源测阻抗，再用单电荷脉冲测电压跳变、恢复和长期漂移。

## VCO

Ring VCO 通过延迟级调频，频率随供电、偏置和负载敏感；LC VCO 用谐振腔、负阻与可变电容调频，关注起振、振幅限制、Q、调谐非线性与离散电容 bank。先读取工程才能判断使用哪类结构。

模块 TB 扫 Vctrl/调谐码，测频率与局部 `Kvco=df/dV`，而不是用全范围线性拟合替代某个锁点。随后核对启动时间、振幅和负载，再按振荡器适用方法做 PSS/PNoise。行为 VCO 可以检验环路动态，但不能给出实际 startup margin 或晶体管 phase noise。

## Divider

固定整数链常由高速 prescaler 与低速计数构成；多模链还需保证 modulus 控制在允许边沿更新。关注最大输入频率、输入 swing、占空比、输出边沿 jitter、reset 确定性和额外周期延迟。

Divider TB 用已知频率扫幅度与占空比，逐周期核对计数和输出间隔；不能只对长窗口频率取平均，因为偶发漏计可能被稀释。基础阶段先固定 N。

验收：每个模块都有结构图、一个可验收的局部测量和它进入系统的参数，例如 PFD 最小脉宽、CP 净电荷/有效范围、filter 阻抗、VCO 局部 Kvco、divider 边沿延迟。所有实际 cell 名称与数值在执行时补入 [模块记录](../../../notes/circuit-lab-template.md)。下一课：[环路动态](P03-pll-loop-dynamics.md)。

配套实验读图：[关键 TB 的作用与结果分析](00-testbench-results-guide.md)。区分保存配置、待执行实验与已新运行的结果。
