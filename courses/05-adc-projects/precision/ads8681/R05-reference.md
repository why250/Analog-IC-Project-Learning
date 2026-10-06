# R05：参考不是一个理想直流源

问题：为什么 REFCAP、REFIO、REFGND 与 AGND 分开出现？先预测：reference 负载只会产生 gain error，还是会形成与码型相关的动态误差？打开 [BANDGAP、AMP_3 原图](../schematics.md#ads8681)。

TOP 的 MI310/BANDGAP 输出 NIBO/PIBO/PIBO1/PIBO2，分别接 `N1169_D`、`P1153_D`、`P1079_S`、`P1151_S`。MI349/PGA 的 NIB/PIB 接其中两条；MI352/AMP_3 的 NIB 接 `P1079_S`，同时接 REFCAP/REFIO。因此不能把 BANDGAP 的某一输出名直接认作最终 reference voltage。逐层追它的电流与参考生成用途。

BANDGAP 中有三只 VNPN、14 个 RES、一只 RNPOLY 及 MOS/逻辑；双极器件和电阻支持查 PTAT/CTAT 的路线，但面积比、电流比、启动和 trim 含义尚待端点推导。AMP_3 有 157 个实例，包含复杂支路，先找反馈取样与输出级，再谈 buffer 稳定性。

研究方法：先不带采样负载查 startup 与工作点，确认 enable 极性、零电流解和输出工作区；随后加入代表性 reference 电流脉冲。TB 保留原反馈、REFGND 回路及外接去耦假设，注明外部电容与 ESR 的来源。理想 `ΔV≈Q/Cdec` 只描述短时电荷抽取，恢复和振铃还由输出阻抗及闭环决定。

结果分析：负载脉冲面积决定需补偿的电荷，重复频率可能使平均值和恢复基线改变。若 droop 随码型不同，可能成为失真；统一参考比例误差主要影响 gain。通过改变脉冲面积、周期和去耦，区分瞬态电荷、平均负载与环路恢复。不要把单次 droop 峰值直接换算成整 ADC ENOB。

噪声与漂移：ADC 输入参考误差需要 reference→采样节点传递、带宽及采样折叠；BJT/MOS noise 参数缺失时不做可信定量报告。温度扫参只有在真实模型和电阻 tempco 有效时才有意义。

验收：一条 BANDGAP 输出到 PGA/AMP_3 的真实路径，一份保留 REFIO/REFCAP/REFGND 的 TB 边界和 droop/恢复指标定义。接 [R06](R06-experiments.md)。
