# 12：静态、动态、PVT 与统计验证

问题：nominal 相干正弦的 ENOB 达标，可以宣布 SAR 设计完成吗？先预测：少量 missing code 能否在一个输入频率的 FFT 中可靠暴露？验收必须同时覆盖转换协议、静态线性、动态性能及使用条件。

## 先证明数据有效

统一数据链：input sample → sample_id → valid/EOC → decoded integer → metric。bit order、输出阈值、码格式、pipeline latency、overrun/reset 都先验证。启动区间按稳定条件排除，不能为了改善 FFT 随意删除样本。若产品要求连续转换，超时/丢样属于失败，应同时报告计数；不允许删去坏码后只算剩余码的 ENOB。

## Transition 与 code density

设第 k 个 code transition 为 T[k]，拟合 LSB 为 q。对内码，`DNL[k]=(T[k+1]−T[k])/q−1`；transition INL 是相对所选理想直线的偏差除以 q。先注明 endpoint 或 best-fit、offset/gain 是否移除、端点码处理。两种拟合能给不同 INL，不能混作同一规格。

无噪声模型可二分查 transition；真实电路有噪声时同一电压不一定给固定码。此时重复转换得到 crossing probability，并定义阈值或采用 code-density 方法。慢 ramp 的 code density 只有在输入密度/斜率已校准、有效码取样均匀时才可用均值计数归一化；正弦输入需按正弦概率密度计算期望计数，不能把均匀密度公式照搬。有限计数中“零次命中”也可能只是采样不足，应给置信范围。

静态 TB 覆盖 full range、major carry、共模、输入源阻抗与必要的转换速率。带足够 acquisition 的慢 ramp 可以查权重/失调，产品速率再查动态建立；两者的差异比一个 INL 最大值更能定位机制。对任一 missing code 记录相邻 transition、bit residual、当时 reference 和 comparator 决策。

## FFT 的口径

相干采样取 `fin=k·fs/M`，k 与 M 互质并低于 Nyquist；本教程用 M=2048、k=901，fin≈8.7988 MHz。矩形窗仅用于相干稳定记录。非相干实验应选合适窗口、积分主瓣并正确处理 coherent gain、等效噪声带宽与谐波泄漏。

将输出转换为输入单位后，去 DC。单边功率谱除 DC/Nyquist 外需双倍功率。定义 signal bins、harmonic orders 及其折叠位置，再算：

- SNR：基波功率除以指定带宽内噪声功率，排除声明的谐波。
- SNDR：基波功率除以噪声与失真总功率；谐波留在分母。
- THD：选定谐波总功率与基波之比，注明阶数和 dBc。
- ENOB：常用 `(SNDR−1.76)/6.02` 对应近满幅正弦口径。若归一到 full-scale，注明幅度修正；不同幅度不得直接比较。

本 Python 示例只移除 2–5 次谐波计算 SNR，SNDR 包含所有非 DC/基波的剩余功率；ENOB 未做幅度修正。扫低频和近 Nyquist、不同振幅/共模/source impedance，才能区分静态失配、输入带宽、jitter 与建立问题。对正弦输入，`SNR_jitter≈−20log10(2πfin·σt)`，高频更敏感；50 ps、8.7988 MHz 约对应 51.2 dB 的纯 jitter 上限，而不代表参考/量化噪声消失。

## PVT、mismatch 与噪声各自回答什么

PVT 查全局工艺、电源与温度下的工作点/速度/端间应力；mismatch 查同一全局条件下器件局部差异；transient noise 查时间随机噪声。corner 通过不能替代统计良率，单个 mismatch seed 不能当良率。电容匹配、比较器 offset 和其他误差可能相关，只有确认独立时才用 RSS。

先用模块实验定位敏感条件，再以架构模型扩大样本数，最后在关键晶体管/PEX 条件检查。每批保存模型版本、seed、实际分布与失败定义，包括超时/启动/不收敛。0/n 失败也不是失败率为零：独立同分布的二项假设下，0 失败的单侧 95% 上界为 `1−0.05^(1/n)`，大 n 时约 3/n。未覆盖的工艺/系统性误差仍在模型之外。

## 设计回归合同

| 类别 | 典型门槛 | 必需证据 |
| --- | --- | --- |
| 转换正确性 | 位数、valid、无覆盖/丢样 | 短 trace、事件计数、sample_id |
| 静态 | 定义后的 DNL/INL、offset/gain | transitions 或校准 histogram |
| 动态 | 指定 fs/fin/幅度/负载下 SNDR | 原始有效码、FFT 设置与谱 |
| 功耗/可靠性 | 指定模式功耗、器件端间限制 | 电流积分、峰值端间电压 |
| 鲁棒性 | 覆盖的 PVT/统计目标 | 条件/seed/失败表及置信范围 |

阈值从 01–03 的规格和预算来，不从一次跑出的值倒推。验收：一份 static/dynamic/协议的同配置结果，解释最差条件与置信边界。所有实际系统前仿仍待执行。接 [13 版图](13-layout.md)。
