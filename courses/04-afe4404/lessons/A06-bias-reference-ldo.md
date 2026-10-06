# A06：偏置、参考与 LDO 的实际用途

状态：课文已准备；已读 LDO_1 原图与部分实际 bias/reference/supply 连接，见 [TX 与配套结构](A05a-tx-support-structure.md)。VOL_GEN_1 的实际接收接口位置已确认，见 [A03a](A03a-filter-buffer-structure.md)，不能只因名称将它当独立参考源。BIAS/VREF/LDO 的完整用途、启动和仿真仍待查。

## 问题与预测

RX_SUP 上同一个小扰动，是通过 LDO output、bias current 还是 reference 最容易影响接收码？先根据真实供电连接提出一条耦合路径，预测它改变的是增益、offset、共模还是时间常数。

## 电路阅读

数据手册第 16–17 页给出独立 TX、RX 与 IO 电源域及内部 1.8 V LDO。这是公开产品架构，不能把未知 HIX 节点都接到 1.8 V。顶层 pad、LDO input/output 与各模块 supply 要逐条追踪。

对 bias cell，找 master reference current、镜像比例、启动支路与 enable；对 VREF，查输出供给了 ADC、DAC、common-mode 还是 LDO error amp。一个名为 VOL_GEN 的 cell 也可能承担局部电压产生，不能凭名字认定 bandgap。

偏置电流改变 gm、slew 与噪声，参考扰动可能改变满量程或 DAC 电流，LDO 扰动会经过模块 PSRR 和共模到差模转换。对全差分链路，差模误差依然可能由两路不匹配和时序不对称生成。

startup 必须排除零电流平衡点，并满足后续采样前的恢复时间。若依靠显式 initial condition 才工作，要记录这一条件，不能称自主启动通过。LDO 的稳定性又依赖输出负载、补偿、电容与 ESR，理想外接电容可能掩盖真实问题。

## 最小实验

先只读形成“供电/参考节点 → 被供给模块”的表。选一个最容易隔离且模型完整的模块，不一次运行全部 bias/LDO。

首次只验收 startup 或 DC regulation：记录真实 supply ramp、enable、load、output/branch currents 与允许稳定区间。独立副本中改变一个初态或一个负载，其他条件固定。

需要 PSRR 时另立小信号实验：明确测量输出是 LDO rail、TIA differential 还是 ADC code，固定负载和工作点。电压到电压的常用抑制度可写为 `20log10(|δVsupply/δVout|)`；若输出是电流，先定义归一化口径和单位，不能直接照用该公式。

检查 reference 和 bias 实际噪声路径后才做噪声仿真。一个低频扰动点不能代表全频 PSRR，也不能代表 LED pulse 的地弹响应。

## 验收与设计判断

交付一个有供电路径依据的因果判断：哪个节点首先改变，接收输出为何受影响。启动或稳定失败点保留条件，不用延长仿真时间隐藏恢复过慢。

后续改补偿或 bias 时必须重新看负载范围、功耗与模块建立；本轮不对 PVT 作无证据外推。下一课 [A07](A07-timing-control.md) 把供电、采样与转换事件对应起来。
