# A02：输入 offset cancellation 与数字 ambient subtraction

状态：课文已准备；已只读确认 TOP_HIER 的 MI495/DAC_2 输出接 AMP_6 两输入，内部 15 个 DAC_CELL_2，见 [实际原图与连接](../schematics.md)。DAC 电流极性、码步、控制映射与仿真未验证，其余 DAC 必须按实际连接分配。

## 问题与预测

逐器件入口为 [A02a 电流 DAC 结构](A02a-current-dac-structure.md)，先区分 DAC_2 输入取消与 DAC_1 转换返回的位置，再做本课的 DC/headroom 判断。

如果 TIA 在 LED-on 相位已经饱和，之后从 ADC 结果减去 ambient code 能否恢复 PPG AC？先画出相减发生的位置，预测输入 offset DAC 的极性、所需电流以及相位切换后最容易出错的时间区间。

## 机制

数字相减处理两个已经量化的数据。上游若仍在线性区、各相位增益一致且时间关系合理，它可以抑制共同背景；如果 TIA 已经削顶，丢失的信息不能通过相减重建。

输入 offset cancellation 在 TIA 放大之前改变净电流。用带符号电流记账：

```text
Ieff = Iambient + ILED_DC + iPPG + Ioffset
Vdiff ≈ s · 2Rf · Ieff
```

s 为实际端口决定的正负号。TI 第 17–18 页说明每个相位可设置独立取消电流与极性；LED-on 要兼顾 ambient 与 LED 引起的 DC，ambient 相位主要处理背景。相位切换不仅改变一个 DC 值，还可能把 DAC glitch、镜像恢复及控制馈通带到 TIA。

码步过大时，剩余 DC 的保守量级与半个有效电流码步有关；实际还需考虑 DAC 非线性、温漂、噪声和范围。提高取消电流不会保证改善噪声：DAC 自身电流噪声也通过 TIA 放大。码越大越好不是合理规则。

不要把 LED 的 6-bit 电流控制当成输入 offset DAC 的位数。本轮没有审阅寄存器 3Ah 的详细字段，也没有读取 DAC 晶体管与译码，码宽须另行确认。

## 最小实验

先从顶层连接区分 TIA 输入 DAC 与 TX 路径 DAC，再建立独立 TB。第一项只测输入 DAC：固定共模和电源，扫少量相邻合法码，用支路电流确认极性、单调性与 ΔI；不能仅测 TIA 输出猜测 DAC 电流。

随后另立实验，把已验证 DAC 接入 TIA，在固定 Rf/Cf 下比较 cancellation off/on。photodiode 输入包含相同 DC 加相同小 AC，保持 Ts 和负载。初次只比较稳态 headroom 与 AC 小信号幅度，不同时扫描供电和 bias。

需要分析相位切换时，保留 DAC 实际控制边沿、输入净电流与 TIA 差分。定义进入允许误差带并保持至采样末端的时刻；把静态取消不足与切换后建立不足分开归因。

## 证据与判断

至少保存实际码、电流方向、净电流、TIA 共模/差分、是否饱和。用 off/on 结果回答：同一 AC 是否恢复线性放大？剩余 DC、glitch 或噪声是否抵消收益？

验收不要求结果必然改善；若 DAC 极性相反或使环路过载，保留失败点并解释。没有真实模型时，用理想电流源只验证 headroom 机制，不能称 DAC 验证通过。下一课 [A03](A03-switched-rc.md) 检查这些相位信号如何被滤波与保持。
