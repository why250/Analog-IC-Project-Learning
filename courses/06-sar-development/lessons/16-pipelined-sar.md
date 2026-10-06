# 16：扩展到 Pipelined-SAR

问题：6 bit 第一级加 8 bit 第二级、有名义增益 8，是否天然得到 12 bit？先预测：总分辨率由“位数相加减冗余”决定，还是由真实 stage range、residue gain 与 digital code map 共同决定？

## 残差模型先定义物理单位

以相同输入参考坐标表示原输入 x、第一级重构值 xq1、残差 r1，放大器实际增益 G、误差 eamp 和第二级量化结果 yq2：

```text
r1 = x − xq1
y  = G·r1 + eamp
xhat = xq1 + yq2/G0
```

G0 是数字重构采用的名义增益。符号、共模、参考域和 stage code offset 必须按实际电路定义；上式不是任何工程都可直接使用的 bus 公式。输入等效误差约含 `(G/G0−1)·r1 + eamp/G0 + eq2/G0`；固定增益误差随 residue 呈现锯齿状结构，不能总当白噪声 RSS。

第二级差分跨度 FS2、位数 B2 对应输入步长 `FS2/(2^B2·G0)`。若输入总跨度 FS1，以此步长覆盖的等效 levels 为 `FS1·2^B2·G0/FS2`，但只有第一/二级 range overlap、数字重构、边界与误差都满足时，这个步长才成为可用精度。FS1=FS2 时，B2=8/G0=8 的步长只对应 11 bit；实际工程可能有不同 range/encoding，需证据核对，不能由名字推断。

## Range、冗余与残差放大器预算

对每个 coarse code 写出实际 DAC 重构值、允许 residue、放大器线性范围和 stage2 输入窗口。范围应容纳第一级 comparator offset、CDAC mismatch、reference droop、dynamic settling 与共模变化。冗余指 coarse 边界附近存在可校正的重叠窗口，依赖实际 decision thresholds 与数字合成；不是一个任意的 bit-count 减数。

放大器预算包括 DC gain、非线性、noise、输出共模、slew、闭环建立与第二级采样电荷。负载应包含 stage2 CDAC 和开关事件。gain boosting 改善输出阻抗/低频增益，同时新增 pole/局部 loop；需要分别审查辅助环路、主环路和 CMFB，再做大/小残差动态实验，不能只看 open-loop gain 变大。

先长窗提取静态增益/非线性，再短窗看 slew 与残差余差；扫正负 residue、共模、stage2 负载和 previous sample。reset/hold 的记忆与级间 feedthrough 同样进入预算。amp 的最终误差经 G0 归一输入端，但超出 stage2 range 后是不可恢复的 clipping。

## 数字合成与样本对齐

第一级码、第二级码和 valid 带同一 sample_id；两级可处理不同样本，不按波形同一横坐标直接相加。黄金模型应定义 stage codes → corrected output 的真值、signed/offset representation、carry、boundary/saturation 和 latency。先以穷举/边界向量验证数字逻辑，再用 residue 波形验证模拟值和编码的对应。

本仓库实际入口 `Pipe_SAR/Pi-SAR_amp` 是含源的 TB，仅有顶层 OUTA 引脚；已读 I0=`DYSAR6b_200M`、I3=`amp_gainboost`、I11=`PiSAR_2st_8bit`、I14=`D_adjust2`。`D_adjust2` 有 c1 锁存、两段 carry/adder 与 D2<5>/D2<7> 条件支路；不能替换为未经验证的 `(coarse<<6)+fine`。名义 G=8 尚未由真实放大器新运行验证。见 [实际 A03](../../05-adc-projects/lessons/A03-pipelined-sar.md) 和 [原图](../../05-adc-projects/schematics.md)。

## 行为系统到真实电路

先建立两级算法与数字黄金映射，行为系统显式保留 sampling/residue transfer/stage2 quantization 的相位、有限阻抗、sample_id 和超时。独立 residue TB 只回答放大器模型的增益/限幅/建立，不等价于完整 pipeline。然后替换实际 stage1 CDAC、residue amp、stage2 和数字合成，每一步看范围、重构残差、边界误差和有效码。

已有 2026-10-04 的 residue VA 实验使用 G=8、Rout=1 kΩ、Cload=1 pF 与限幅/增益误差，属于无 PDK 教学结果；完整 12 位行为流水线及原电路替换尚未运行。贯穿教程的 Python 脚本是单核 SAR，未实现完整 pipeline。后续扩展模型应先完成真实 D_adjust2 的编码与对齐审计，不能借用单核模型宣称流水线已闭合。

验收：实际 FS1/FS2/G0 和粗码阈值表、residue/range 覆盖、正确数字映射及一个 sample 的跨级 trace，然后才测完整系统 INL/SNDR/PVT。到此完整开发流程课文已齐全，实验与学习状态按 [续学入口](../../../progress.md) 单独推进。
