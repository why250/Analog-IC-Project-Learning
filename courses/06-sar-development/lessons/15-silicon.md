# 15：流片评审、测试可观测性与实测

问题：仿真满足规格，而芯片测得 SNDR 较低，怎样判断是 ADC、信号源、clock、reference 还是数据采集？先预测：换一台低失真信号源得到更好 SNDR，能否直接反推出 ADC 原本的 THD？

## 流片前留出可观测性

评审同时关闭规格、设计、物理实现和测试接口。确认启动、reset/掉电、reference 可用、clock 范围、数据有效、IO 电压域、ESD/可靠性、DRC/LVS/PEX 与 PVT/统计覆盖。offset/gain/calibration 参数与写入/读回方式属于产品功能，不能只保存在仿真脚本。

在面积/功耗允许下保留 test mode：外部参考或 bias 选择、转换/采样速率控制、固定码型/控制序列、独立电源测量、内部状态可观测性。敏感高阻节点不能为了探测直接拉到 pad；buffer、开关和 pad 寄生都可能改变性能。测试模式要在设计阶段规定边界和对正常模式的负载。

数字输出明确 endian/bit order、signed/offset-binary、采样编号、latency 和 valid。bring-up 先检查固定输入与 clock/EOC 协议，然后才采集长码流。扫描、配置、复位和掉电恢复每项都有可重复脚本/操作表。

## 测试板也是信号链的一部分

输入源的谐波/噪声、driver 的输出阻抗/共模、滤波网络和 balun 都会影响量程/建立/线性。reference 的噪声、去耦位置、回流、ESR/ESL 与采样电荷匹配；clock source、分配和接收 buffer 共同决定 aperture jitter。board/package 模型边界与 ADC 仿真边界一致，实测应记录具体接线和 probe loading。

在 ADC 输入端尽可能确认实际幅度与共模，校准量程和频率；有源差分驱动需检查两侧相位/振幅与带宽。电源纹波和数字采集串扰可能通过 reference/ground 进入输入。仪器的标称指标不足以证明 bench floor，在使用带宽/幅度/阻抗下进行参考测量或替代源/clock 交叉检查。

不能把实测 THD 以 dB 相减得到 ADC THD：同频谐波可相干叠加且具有相位。已知独立噪声才可在功率域减去；相干失真需复数幅相或受控对照。去嵌应注明可识别参数、测量不确定度与未建模项，避免得到貌似精确的裸芯片数字。

## Bring-up 与性能实验

| 顺序 | 实验 | 结果解释 |
| --- | --- | --- |
| 1 | 电源限流、启动/复位、reference/bias | 识别短路/启动/配置，固定模式与温度 |
| 2 | 中间/正负/端点 DC、valid/位序 | 识别接线、格式、极性、丢样与饱和 |
| 3 | DC 重复码与慢 ramp/transition | noise、offset/gain、DNL/INL，校准输入源 |
| 4 | 低频相干正弦，幅度 sweep | 静态失配/失真与量程限制 |
| 5 | fin/fs/共模/source/clock sweep | 输入建立、jitter、reference recovery |
| 6 | supply/温度/模式与多 die | 实际使用边界、变异与功耗 |

每批保存原始码、有效码规则、仪器/板卡/芯片身份、源设置和数据分析版本。实测电源功耗注明 ADC core、reference/buffer、clock/IO 是否包含；测量带宽和工作模式相同才可与预算比较。性能分布需多 die/批次，单 die 的温度扫描不代表工艺良率。

## 用实测修订模型

如果 reference 改善后某些码型 distortion 减少，提取码型相关 droop/恢复参数；如果 fin 上升时 SNDR 按 jitter 近似下降，仍需区分 source/clock/输入带宽；若慢速 INL 不变而高速差，应回到 acquisition 与每位建立。用同一误差注入模型同时解释静态/动态/条件依赖，比只拟合一个 ENOB 更可靠。

验收：流片前可观测性/覆盖评审、bring-up 表、校准后的原始数据链和误差归因报告。没有芯片或测试板实测时本章保持计划状态。本教程所有数字例子属于模型计算。接 [16 Pipelined-SAR](16-pipelined-sar.md)。
