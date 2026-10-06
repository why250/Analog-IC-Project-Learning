# A05a：TX 环路、供电与信号链的配套电路

本课问题：产生光信号的 TX 如何被控制，偏置、参考、供电和数字边沿怎样进入接收链？已确认 TX 端口路径，未测 LED 电流、光学响应、PSRR 或启动。

原图：[AMP_5](../../../notes/evidence/afe4404/AMP_5.png)、[SWITCH_BLOCK](../../../notes/evidence/afe4404/SWITCH_BLOCK.png)、[LDO_1](../../../notes/evidence/afe4404/LDO_1.png)。这些配套结构贯穿接收课，分别在 A05/A06/A07 做详细实验。

## TX 的实际闭环入口

顶层 MI152/AMP_5.VP=PAD1、VM=net770、VO=net830、VS=TX_SUP。MI341/SWITCH_BLOCK.VI=net830、VO=net770，并直接连接 TX1/TX2/TX3。因此 AMP_5 的输出驱动开关模块，开关模块另一个端口返回 AMP_5 输入；实际反馈方向与电流感知位置需要继续逐支路证明。

SWITCH_BLOCK 内有 64 个 SWITCH_CELL_1，S0–S3 各有六个控制位，另有 CTRL_1/CTRL_2。这支持研究重复输出单元、幅度选择与相位选择，不能据此把 64 个实例全当有效电流源，或直接指定某一组就是某 LED 的 6-bit 电流寄存器。

此前按名字列出的 DRIVER_1/2 实际用于 ADC_RDY/PAD7/CLK 的 I/O。TX 学习从上述真实端口链开始；名字、重复数量和公开规格都不能替代电流路径证据。

## 从电流路径建立设计判断

先对一个合法控制态追踪 TX pin→选择 MOS→控制/感知节点→供电回路，并列出每个串联器件需要的压降。在偏置正常且器件工作区合适时，反馈可降低电流对 LED 端电压的敏感性；compliance 用尽后，放大器输出或串联器件饱和，电流不再由码值单独决定。

脉冲电荷为 `QLED=∫ILED(t)dt`。对短脉冲，rise/fall、过冲与建立占比可能很大，稳态平台电流相同也不保证电荷相同。光电输入还取决于 LED 光效率、光路与 photodiode 响应，不能把 QLED 与 ADC 码之间当作没有条件的线性常数。

预测应先选择一个因素：LED 端电压改变、脉宽缩短或 code 改变。实验保持其他条件固定，在 [A05](A05-led-driver.md) 测对应的平台电流、compliance 或积分电荷，不同时扫描全部因素。

## 供电域与偏置不是旁注

已读顶层 AMP_6/DAC_2/FILTER/AMP_BLOCK 的 VS 接 X13454_VS；VOL_GEN_1 另有 VS1=RX_SUP；ADC_1 的 VS 接 X13488_VS；TX 使用 TX_SUP。这些实际 net 名不直接提供电压值，也不能证明两域的 regulator 来源和时序。

对每一域记录源头、enable、负载、decoupling、bulk 连接和跨域接口。在 LDO_1 图中辨认 pass device、误差控制、反馈节点和 startup/关断路径，需要由 terminal/net 和 bias 条件确认；本轮没有逐器件完成 LDO 功能证明，也没有负载相位裕度。

AMP_6.NIB 在顶层接 P14100_D，参考端 P14069_D 同时出现在 TIA、VOL_GEN_1、AMP_BLOCK 与 ADC 相关接口。一个共享参考噪声可能在不同相位相关，不能将各级参考贡献都当独立噪声作均方相加。进一步的来源追踪和注入实验按 [A06](A06-bias-reference-ldo.md) 完成。

Bias current 改变 gm、ro、slew、noise 与恢复，增大电流也可能移动共模或影响镜像 headroom。只观察带宽增加不足以验收设计改动。修改前同时记录工作点与供电电流，后续至少检查对接口与共模的影响。

## 数字控制怎样进入模拟误差

本轮读到 CTRL_3 的 Z1/Z1N 接滤波器后的 MI312/MI313 输出选择控制，输入均衡 N20855 由 X21158_ZN 控制。TIA 输入 MOS 的 gate 来自 X21176_ZN，与 BUF_BLOCK.Z7N 连接。控制信号来源明确后，还需核对有效电平、使能状态、非重叠和配置生效边界。

开关控制的 charge injection、供电回流、共用参考和跨域电平切换都可能把 TX/数字边沿带到接收路径。第一轮归因固定 analog input，仅改变一个 control event 的位置，观察误差首次出现的节点；不能看到 ADC 码异常就直接称为 ADC 噪声。

## 串回完整课程

结构验收需给出一个 TX 控制态的电流路径，以及接收模块的 supply/bias/reference 接口表。A06 验证偏置与供电条件，A07 将采样、交接、转换、DAC 更新和 ADC_RDY 串成事件表，A08 才评价系统性能。

在 [A08](A08-noise-design-review.md) 中分别汇总输入电流噪声、输入电压噪声、Rf 热噪声、offset DAC、采样与参考贡献；噪声需通过各自传递函数折算，跨相相关性另计。系统设计判断必须同时满足摆幅、建立、转换时间、噪声和功耗，不能以最终数据字长代替这些预算。
