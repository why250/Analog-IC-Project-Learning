# 02：架构与逐位转换机制

问题：SAR 的 N 位输出是否意味着 N 次完全相同的电容切换？先预测：Vcm-based switching 的首次符号判决，是否一定先切最大电容？用一次真实电荷过程检验，不从 generic 框图推断。

## 从逐位搜索到真实电荷

理想 unipolar 输入 u∈[0,VFS)，LSB=VFS/2^N，黄金量化 code=floor(u/LSB)，超出范围饱和。逐位从 MSB 开始试置 1，对 trial DAC 电压比较，保留/清零，直到 LSB。只有阈值、编码和 floor 定义一致，算法才与黄金码对应。

差分 centered 输入 x∈[−VFS/2,+VFS/2)，可先作 u=x+VFS/2 的数值变换。但实际电容网络的共模和初态不会因此消失。Vcm switching 常先对 sampled x 做符号判决，再以互补底板动作修正残差；可能有 N 次比较、N−1 组控制。已有 8 位项目就是八次判决与七组受控电容，见 [真实电荷推导](../../05-adc-projects/lessons/A01-async-sar-architecture.md)。

## 架构选择需要的证据

| 选择 | 获益候选 | 必须检查的代价 |
| --- | --- | --- |
| binary CDAC | 电荷关系直观、权重与数字映射简单 | Ctotal/面积、MSB matching、输入/reference 电流 |
| split/bridge | 减少大阵列和输入负载 | bridge 比、MSB/LSB 子阵列寄生、非整数有效位权 |
| segmented/冗余 | 特定切换/匹配/时序容错 | 编码和冗余范围、校准复杂度、额外比较/电容 |
| 同步 | 固定 bit window、时序验证直观 | 按慢判决预留，内部 clock 速度/功耗 |
| 异步 | 完成事件推进、可省不必要等待 | done/reset/死区、尾部迟决、外部 deadline |
| Pipelined-SAR | 分摊转换工作，允许重叠吞吐 | 残差放大、级间范围、数字样本对齐 |

不是所有高速设计都需要异步，不是所有高分辨率都需要 split 或校准。先拿两个候选结构写电容/时序/面积数量级，再做 PDK 可行性检查；若 Ron、unit C 或比较器延迟不合理，就回退架构。

## 架构实验

在 Python 中运行同一量化定义的两个搜索策略，固定三组输入：零附近、MSB 转换附近、满量程附近。记录每次 trial、decision、残差、共模的定义与最终 code。再给一个试验位权偏移，预测哪个码段出错；标准阈值算法的结果不等于原始差分 CDAC 已验证。

画 sampling→hold→compare→DAC update→下一 bit→latch 的状态图，标 reference、输入、共模与每个浮置节点。没有状态初值的“理想 SAR”可能给正确最终码但解释不了真实电荷和 reset。

验收：两种候选架构的资源比较、一条逐位轨迹与一个明确的负载/时序风险。接 [03 预算](03-budget.md)。
