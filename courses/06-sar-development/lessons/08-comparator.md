# 08：比较器从系统预算到动态电路

问题：nominal 1 mV 差分判决够快，是否就能用于所有 SAR bits？先预测共模、前态、noise/offset 与负载变化会怎样改变迟决概率。实际图/实验分别见 [异步 compare](../../05-adc-projects/schematics.md) 与 [GPDK 实验](../../../notes/2026-10-04-comparator-delay.md)，它们是不同电路/模型。

## 机理与初步尺寸方向

输入 stage 将差分电压变成初始差分电流/电荷；再生阶段正反馈放大差分。局部线性近似 Δv(t)=Δv0·exp(t/τreg)，τreg≈Cnode/gm,regen,net，达到阈值的时间约 t0+τreg ln(Vdecision/|Δv0|)。输入 gm、预放大增益、reset 和负载决定 Δv0/Cnode，这不是全波形精确延迟公式。

输入对增大可提高 gm/降低某些 mismatch，代价是 CDAC 负载、kickback、power/reset capacitance。再生管增大改变 gm 与 C，不保证 τ 单调下降。单/双尾、preamp 等结构需要按 VCM、headroom、noise、reset 和 supply budget 选择，不仅按速度排名。

过驱动趋近零时，简单式延迟发散；实际由 noise/offset/初态决定，SAR 的码边界无法避免极小差分。应定义允许不确定转换区间、判决窗和系统 error probability，不能在模型中随意钳一个最小 overdrive 后宣称不会迟决。

## 把时间目标转成设计方向

局部模型给出 `gm,net ≥ Cnode·ln(Vdecision/|Δv0|)/(tdecision−t0)`。若暂设 Cnode=10 fF、Δv0=1 mV、Vdecision=0.6 V、总窗 300 ps、输入建立/启动 t0=100 ps，得到 gm,net≈320 μS。数值只是单极点再生例子；Δv0 是进入再生的内部差分，不一定等于外部 1 mV。

在 PDK 中先找 VCM/headroom 下输入对的 gm、current 和 mismatch，再检查其给再生节点建立的初态。依次调整 input pair、tail、regen pair 和输出 buffer，并测实际 Cnode、reset 与负载；不能从 320 μS 直接查一只 MOS 的 gm 就确定整个比较器尺寸。增大 input pair 后，应同步更新 CDAC load 和 kickback；增大 regen/buffer 后，应更新 reset 和供电脉冲预算。最终用延迟分布和系统有效决定条件替代这个数量级式。

## offset、noise、memory 与 kickback

offset 是判决概率曲线的中心偏移；decision noise 是固定差分下重复试验的随机分布；PVT 系统偏移、失配与 transient noise 分开。单次固定输入判对不等于 offset/noise 验收。动态比较器不能未经条件证明用静态 AC noise 代替相末输入参考噪声。

reset 不充分或外层 latch 保持会使前一状态影响结果，交替正负差分比重复同号更易发现。kickback 应以实际 CDAC/source impedance 测采样节点扰动及判决影响，强理想电压源会将它压住。输入 VCM 随 CDAC 相位移动，须按真实 trajectory 检查。

## TB 递进

1. 新网表/model section，固定 VDD/VCM，reset/evaluate 短 transient，明确原始动态节点与最终 latch。
2. 正负交替输入、overdrive/VCM/负载、reset 时间 sweep；量从哪条 clock 阈值到哪条输出阈值的 delay。
3. 固定差分做重复 noise trials，固定工作条件做 mismatch trials，分别拟合概率曲线与统计 offset。
4. 带真实 CDAC 回到 SAR 闭环，查看迟决、dead time 与下一 bit residual，不只沿用独立 TB 的 delay。

已有 GPDK 190/198 ps 局部结果不能移植到 SMIC 的 compare 或本教程 0.3 ns budget。delay/offset/noise 参数需要实际提取后回填 VA，distribution 的尾部和失败也保留。

验收：极性/reset、delay 测量定义、一个 memory/kickback 反证实验与 noise/offset 分离计划。接 [09](09-control.md)。
