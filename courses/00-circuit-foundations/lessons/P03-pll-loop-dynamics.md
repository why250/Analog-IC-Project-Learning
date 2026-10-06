# P03：带宽、阻尼和锁定时间怎样从电路参数推导？

问题：增大 CP 电流是否只会提高带宽？先预测：固定 R/C/N/Kvco，Icp 加倍后自然频率与阻尼分别怎样变？

## 先统一单位

用相位单位 rad：`Kpd=Icp/(2π)`，单位 A/rad；若测量 `Kvco` 为 Hz/V，则 `Kv=2π Kvco`，单位 rad/s/V。VCO 的相位响应是 `Kv/s`，feedback divider 相位增益为 `1/N`。

开环 `L(s)=Kpd Z(s) Kv/(N s)`。对最简 `Z(s)=(1+sRC)/(sC)`：

```text
L(s) = Kpd Kv (1+sRC) / (N C s²)
ωn² = Kpd Kv/(N C)
2ζωn = Kpd Kv R/N
ζ = (R/2) sqrt(Kpd Kv C/N)
```

这是理想连续时间二阶近锁模型。固定 R/C 时 Icp 加倍，ωn 和 ζ 都增加 √2。闭环带宽、ωn 与开环交越频率相关但不同，不能混用。增加并联 C2 后是更高阶模型，零点和高频极点影响相位裕量，二阶结果只能作起始估计。

Type-II 环路包含 filter 积分与 VCO 相位积分，在理想线性条件下消除恒定频率偏差对应的稳态相位误差；真实 CP leakage/dead zone 等可产生非零工作点相位差。Type 与 order 是不同分类。

## 从电路测量到模型

用模块 TB 在选定锁点取得 Icp、Kvco、filter R/C 和 divider N，建立参数表并检查单位。画开环幅相和闭环响应，分别标自然频率估计、交越频率、相位裕量及 peaking。连续模型用于解释小扰动，不能替代大偏差捕获阶段。

若 loop bandwidth 接近 fref、divider/driver 延迟显著或 CP 更新为明显脉冲，应考虑采样与延迟模型。单凭 Bode 图漂亮不能证明电路捕获无 cycle slip，也不能保证 Vctrl 不进入饱和。

## 最小实验

第一项在已经锁定的整数 N 环路施加小参考相位阶跃，记录相位误差和 Vctrl，比较模型的 overshoot 与恢复时间；同时检查刺激足够小，输出没有整周期跳跃。

第二项单独改变 Icp 或 R，预测并实测响应变化；第三项才测试远离锁点的初态与重调谐。保持相同 lock 判据：频率误差阈值、相位误差阈值、持续保持时间及目标输出端。不把短时穿越容限写成锁定。

验收：一张单位可审计的参数表、预测与实测小扰动响应、差异归因，以及明确的线性模型适用边界。启动细节与旧 AMS config 兼容性接 [启动与锁定实验](../../02-pll-verification/lessons/08-startup-lock.md)。下一课：[基础噪声与杂散](P04-pll-noise.md)。

配套实验读图：[关键 TB 的作用与结果分析](00-testbench-results-guide.md)。区分保存配置、待执行实验与已新运行的结果。
