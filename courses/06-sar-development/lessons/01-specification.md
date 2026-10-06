# 01：先写规格与测量合同

问题：用户说“10 bit、20 MS/s”，是否足以开始选 CDAC？先预测：同样位数和采样率，低频传感器与接近 Nyquist 输入是否需要相同的采样/时钟设计？答案从输入带宽、源阻抗、噪声和测量条件开始。

## 规格必须能转成实验

| 规格组 | 必须明确 | 后续设计约束 |
| --- | --- | --- |
| 输入 | 差分/单端、跨度、共模、允许过载、最大 fin、源阻抗与驱动方式 | switch headroom、采样时间、输入带宽、kickback |
| 输出 | nominal bits、码格式、极性、满量程/饱和、latency/valid | SAR 搜索、数字接口与解码 |
| 精度 | SNDR/SNR/THD、DNL/INL、offset/gain、码噪声，各自测试条件 | noise、matching、建立、reference 与校准 |
| 时序 | fs、采样窗、启动/reset、外部 clock 范围/jitter、数据有效 | 同步/异步控制与每位 budget |
| 环境 | PDK、VDD/reference 范围、温度、源/负载、PVT/统计口径 | 器件/模型选择与可靠性 |
| 资源 | power/area、参考是否片上、输入 driver 是否计入、测试接口 | 架构和实现边界 |

“N bit”是编码分辨率；ENOB 来自测量条件下的 SNDR，不是 nominal bits。“高精度”还可能要求低漂移、无 missing code 或高 DC linearity，这些不是同一个指标。给 SNR 目标必须注明输入振幅/频率和分析带宽，给 DNL/INL 必须注明 endpoint/best-fit 与饱和 bins 的处理。

## 教学需求例子

本教程暂设 N=10、fs=20 MS/s、差分跨度 VFS=2 V、300 K、目标 ENOB≥9；满量程差分正弦峰值 1 V。电路可行性假设 VDD=1.2 V、VCM=0.6 V，则差分两端满量程各为 0.1…1.1 V，是否能被选定 switch/comparator 处理要在 PDK 中验证。2 mW 仅为资源示例，未设计或测得。

先给 DNL/INL 一个讨论用目标，例如内区 |DNL|≤0.5 LSB、|INL|≤0.5 LSB；这不自动由 ENOB≥9 推出，也不是已有项目需求。FS、时钟、温度与 power scope 变化时重新审计 budget，不能只改一个仿真变量然后沿用原验收条件。

## 最小实验与判断

暂不跑 Spectre：把 spec 表填完整，将一项模糊要求改成实验。例如“20 MS/s 正确输出”改为“每 50 ns 捕获一个输入样本，指定 latency 后输出对应 sample_id 的有效码；过期转换不能冒充新码”。把“ENOB≥9”改成振幅、频率、样本长度、窗、码采样相位明确的 SNDR 测试。

实际工程练习分别读 `8_bit_sar_adc/8bit_SAR_ADC_test` 和 `SAR_ADC`：source/TB/DUT 边界不同，作者报告、保存状态和新测量要分开。入口见 [A01](../../05-adc-projects/lessons/A01-async-sar-architecture.md)。

验收：一页 spec、一个数据有效时序图、一个未确定的需求。下一课 [02](02-architecture.md) 把它转成架构，不直接从位数指定器件大小。
