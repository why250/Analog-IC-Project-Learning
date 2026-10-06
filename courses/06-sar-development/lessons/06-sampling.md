# 06：采样开关、自举与输入驱动设计

问题：自举把 Vgs 保持近似恒定后，是否采样线性就保证了？先预测体效应、源阻抗、馈通和 hold 初态哪项还会影响结果。配合 [实际 BOOSTRAP 原图](../../05-adc-projects/schematics.md) 与 [逐器件分析](../../05-adc-projects/lessons/A02a-bootstrap-structure.md)。

## 从工作过程到器件约束

预充阶段给 bootstrap C 充电、reset sampled node，track 时将储能浮置并随 VIN 抬升 gate，hold 时隔离输入并恢复 gate。先列每相各 MOS 的 G/S/D/B 和浮置节点；再检查 gate source reference 随哪个信号变化。VIN 极限、启动和死区常比稳态更容易暴露问题。

MOS triode 的粗略 Ron≈1/[μCox(W/L)(Vgs−Vth)]，用于初步趋势而非最终尺寸。自举改善 Vgs 随输入的变化，Vth 仍可能因 body effect 变化，Ron 也受温度、低 overdrive、非对称端子和寄生影响。W 增大有助降低 Ron，同时增加 gate/overlap、bootstrap 负载、clock driver 功耗和注入，需整体迭代。

从 [03](03-budget.md) 的 acquisition error 给 Rtotal·C 的界限，减去 source/route resistance 再得到 switch 候选 Ron。bootstrap C 由预充能力、驱动总电容、允许 gate droop 与泄漏决定；按电荷分享估算 ΔV≈ΔQ/Cboot，最终以真实两相和输出负载验证，不能直接固定“Cboot=Csample 的某倍”。

端间应力检查 Vgs/Vgd/Vgb/Vds/Vdb 等与 PDK 可靠性限制，特别是浮井、startup 和跨供电节点。gate 对地超过 VDD 本身不是端间应力证明； `_H` 命名也不是耐压验收。

## 实际设计迭代的操作顺序

先从 PDK 的允许器件/电压域选择 main switch 与预充路径；把 source resistance 从约 117 Ω 总预算扣除，若 source 已超过总预算，应改 driver、C 或 acquisition，不能靠加宽 MOS 补救。随后在输入范围与共模网格上提取候选开关的 Ron/建立，以最差点筛 W/L。增加 W 后重新计 gate/overlap 与 clock load，而不是固定第一次的 bootstrap 负载。

若仅用“已充至 VDD 的 Cboot 与初始未充电 Cload 电荷共享”作起步近似，得到保持电压 VDD·Cboot/(Cboot+Cload)，相对 droop≤ε 需 Cboot≥(1/ε−1)Cload。例：ε=10% 对应至少 9Cload；这是特定初态的电荷共享估算，不是通用尺寸比例。真实电路的 gate 随 VIN 移动、寄生另一端也移动，且有预充/驱动电阻和泄漏，必须回到分相电荷方程与 transient。

最后依次 sweep Cboot、预充开关、gate driver/dead time 与 main W；目标同时满足 held error、预充完成、功耗和端间限制。把可行范围交给 03 的系统 budget，而不是给出脱离 PDK 的一组 final W/L。

## 采样精度与 jitter

held error 定义为 aperture 的理想输入值减实际稳定 held 值，分 acquisition 残余、pedestal、signal-dependent injection、leakage 与噪声。clock feedthrough 即使是固定 pedestal 也可能与输入/前态相关，不能全部用一个 constant offset 校掉。

小独立时钟误差 Δt 使 e≈(dx/dt)Δt。对正弦，误差 RMS≈A·2πfin·σt/√2，故 jitter-limited SNR≈−20log10(2πfinσt)。用 fin 而不是 fs 代入，且该近似不包含 deterministic jitter/clock coupling。接近 Nyquist 的输入对 clock/buffer/开关非线性更敏感。

## 独立 TB 与结果分析

保留真实 source impedance/driver、两侧 sampling/CDAC 负载、非重叠 clock 和 VCM，观察 bootstrap 电容两端、main switch gate、held node 和 supply/reference current。先 DC/大阶跃短 transient 检查范围和建立，再 sweep acquisition、VIN、VCM、负载与前一输入。取相末 held error，不以输入和输出“波形看起来重合”验收。

长窗仍有输入相关误差查 injection/body/拓扑；延长 track 显著改善查建立；hold 时间变化后漂移查漏电/负载；正负/不同前态不对称查 memory/reset。最后做离散有效样本的 sine，而非连续 ideal DAC 波形 FFT。

验收：分相导通表、Ron/boot C 初步约束、一个端间电压最坏场景、held error 随 track time 曲线。没有选 PDK 就不填写 final W/L 或 reliability passed。接 [07](07-cdac.md)。
