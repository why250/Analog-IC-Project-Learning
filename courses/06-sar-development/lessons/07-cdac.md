# 07：CDAC、开关与匹配设计

问题：binary array 按 1:2:4 比例画好，位权就正确吗？先预测 top-plate parasitic、bridge 和差分互耦谁会改变实际比较残差。实际结构入口 [S02](../../00-circuit-foundations/lessons/S02-cdac.md) 与 [异步 SAR 图](../../05-adc-projects/schematics.md)。

## 先求电荷，不先猜位权

单浮置节点 Q=ΣCi(Vx−Vi)，切换保持电荷、参与集合不变时 ΔVx=ΣCiΔVi/ΣCi。多个浮置节点用电容矩阵 C·Δv=b；split bridge、差分耦合和接收负载不能压成一个不变的 Ctotal。分别求差分与共模，标 sampling/reset 状态的初始 Q。

设计表列每只/每组 C 的数值、端点、有效相、switch control、dummy/去耦角色。binary dummy 加入分母；两端同网 C 不产生相应位权，但版图下其附近耦合可能仍有影响。Cadence 保存的 c、几何与 m 必须审计，不能重复计 multiplicity 或直接把面积当真实电容密度。

## matching 与容量选择

单位电容由 process density、mismatch、最小尺寸、边缘/底板寄生和 routing 选择。独立随机 unit 求和时 σgroup relative≈σunit/√n，这是解析假设；真实 gradient/相关性/版图边缘不随 unit count 同样衰减。MSB carry 处理想 DAC 增量 wMSB−Σwlower=LSB，比例/寄生偏差可使 transition 异常，需用实际 ADC 搜索测 DNL/INL。

分割阵列减 C 的同时增加 bridge/LSB 子阵列敏感性；segmentation 可改变梯度/切换模式，代价在 decoder/switch/边缘面积。先用实际寄生/失配权重在 Python 找容限，再回推 layout/matching；没有 PDK 匹配常数不能确定最小 Cu。

### 用 major carry 回推单位匹配的数量级

十位 binary 的 MSB 有 512 units，低九位共 511 units。忽略分母的微小变化时，major-carry 电容差理想为 Cu，独立 unit 绝对误差 σCu 对应差值 RMS≈σCu·√1023。除以 nominal LSB 后，carry step 的 RMS 误差约 √1023·σunit，其中 σunit=σCu/Cu。

若只为这个 carry 设 3σ≤0.5 LSB，需 σunit≤0.5/(3√1023)≈0.521%。教学脚本采用 1% unit sigma，约对应此 carry 0.320 LSB 的 RMS；一个 seed 的 INL 达标不能说明设计满足统计要求。这里的 3σ 不是全 ADC 良率：多个 carry、两侧相关性、分母变化、gradient/寄生与测试定义尚未计入。

当 PDK 给出明确的 `σrelative=A_C/√area` 且单位/配对定义一致时，初估 unit area≥(A_C/σrequired)²，再按 density 得 Cu。若 PDK 给的是两只电容差值的 sigma，需要先换成单 unit 误差或直接按其公式使用，避免多算/漏算 √2。此后回到阵列/版图 Monte Carlo，检查面积、驱动与 reference 预算是否仍可行。

## switches 与 reference

不同位负载、步幅和剩余时间不同，不一定所有 switch 同尺寸或 bit time 一样。Ron 影响建立，switch capacitance/injection 改位权和共模；大型 buffer 的供电扰动会通过参考/基底返回比较器。保持 break-before-make，确认有效 OE/OEN，避免短 reference rails。

reference 提供离散电荷脉冲。分别积分每条 rail 的 I(t)，计算 E=∫VI dt 和平均功耗，注明是否允许回馈。ΣCV²fs 是粗估，不替代特定 switching sequence 的 reference 能量，也不含前端/driver 全部功耗。

## 最小 TB

先理想开关验证 charge/bit sign，再换真实 switch，保持输入与其他 controls，单 bit 及 major carry 状态对照。测 long-window 位权、short-window residual、共模和 reference droop，扫 source impedance/去耦。对 split 先局部 C matrix/branch perturbation，再全系统。

若 long window 有固定比例误差，检查 ratio/bridge/parasitic/control；short window 异常而长窗正确，检查 RC/reference 恢复；只在某一差分侧异常，查 mirror layout/共模与注入。对 noise 与静态失配分别建实验。

验收：电容端点/权重矩阵、Cu 选择依据、一组 long/short window 对照和 reference charge。接 [08](08-comparator.md)。
