# S05：模块设计怎样闭合到 100 MS/s SAR？

问题：100 MS/s 与 1.2 GHz 时钟为每个模块留下多少时间和噪声余量？先预测：比较器提速一倍一定能让采样率提升一倍吗？用实际每位关键路径解释。

## 实际控制器与时序边界

`I56/I22 → saradc/controller_baseline/veriloga` 是行为控制器；数字门和比较器时钟另有电路路径。保存变量为 `fsample=100M`、`fclk=(10+2)fsample`。源码静态推导稳态为两个采样区间、十个比较区间，结果锁存和下一轮采样起点重叠；[采样入口续篇](../../01-cadence-verification/lessons/01a-sampling-entry.md) 有逐状态证据。

推导 `Tclk≈833 ps`，采样窗约 `1.667 ns`。实际采样边沿、内部比较器 evaluate 宽度、driver 延迟和首次有效码必须以新 transient 测量，不能把完整 Tclk 都分配给比较器。

每位的因果链是 bit 更新→reference mux/driver 动作→CDAC 残差建立→比较器 evaluate→buffer 输出→控制器采集。其预算形式是 `Tbit ≥ Tlogic + TDAC + Tcmp + Tcapture_margin`，但若部分过程重叠，须画出实际窗口，不能简单求和重复计时。MSB 与 LSB 的阶跃、负载和比较器残差不同，逐位记录比统一最坏值更有解释力。

## 噪声与线性预算

理想量化 RMS 为 `LSB/√12`，若有噪声预算目标，可按采样热噪声、比较器输入等效噪声、reference 噪声与其他来源分配。只有近似独立、换算到同一输入端和带宽后，才可用方差相加。Offset 与确定性谐波不能塞进随机 RMS 预算。

CDAC 大电容降低采样噪声并可能改善匹配，但增大输入与参考负载；比较器更大输入对改善噪声/mismatch，却增加 kickback 与 CDAC 负载；自举开关更强 driver 提高建立，同时可能增加时钟馈通。课程结论应回答哪种代价在当前预算中可接受。

## 最小系统实验

先完成一组 nominal 稳态时序：逐位测 CDAC 从跳变到残差进入误差带的时间、比较器输出稳定时刻、控制器采样时刻。误差带按输入等效量与该位预算定义，不能任意使用“看起来平了”。此步骤先接原 TB，不替换模块。

选一个瓶颈，在恢复副本中仅改变相关因素。例如先延长时钟周期检验动态建立，再改 mux driver 或比较器尺寸；若只延长时钟后误码消失，仍需通过残差/输出时刻定位责任模块。与原 nominal 保持输入序列、模型、初态和码采样口径相同。

最后才进入 [nominal 基线](../../01-cadence-verification/lessons/02-nominal-baseline.md)、[动态指标](../../01-cadence-verification/lessons/03-dynamic-metrics.md) 与后续统计验证。验收是一个模块参数改变如何影响时序、噪声或线性的完整链，并报告行为采样开关、行为控制器尚未覆盖的结论。

ADC 阶段的作品：实际模块地图、split 位权推导、开关分相图、比较器判决曲线、每位预算和一次受控变更。基础 PLL 从 [P01](P01-pll-architecture.md) 开始。

配套实验读图：[关键 TB 的作用与结果分析](00-testbench-results-guide.md)。区分保存配置、待执行实验与已新运行的结果。
