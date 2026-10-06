# S03：采样开关为什么要自举，实际实现怎样分相？

问题：让 gate 随输入运动是否足以保证 10 bit 线性？先预测：增大 bootstrap capacitor 能改善什么，又会给 clock driver、输入端和建立时间带来什么代价？

## 普通开关的误差来源

普通 NMOS 的 gate 由固定电源驱动。输入上升时 `VGS−VTH` 变小，`Ron` 变化；body effect 使阈值也随输入变化。近似 `Ron≈1/[μCox(W/L)(VGS−VTH)]` 只在合适工作区定性有效，不能跨整个输入范围替代模型。

Transmission gate 用 NMOS/PMOS 的互补导通能力改善输入范围，但两支路总导纳仍非恒定。工程的 `saradcII/mos_switch` 是实际 NMOS/PMOS transmission gate，`CLK/CLKB` 分别控制两类器件，可作对照。

采样误差至少区分 acquisition、关断瞬间 feedthrough/charge injection、保持漏电、采样热噪声和时钟抖动。对正弦输入，抖动近似限制 `SNRj=−20 log10(2π fin σt)`；改善 Ron 不会消除这个限制。简单 `kT/C` 估计须说明所用等效采样电容、差分相关性及带宽。

## 自举原理与本工程的区别

常见 NMOS bootstrap 先给浮置电容充电，采样时把其参考端接到输入，让 gate 约为 `Vin+Vboot`，使 VGS 更恒定。有限电容、寄生分压、泄漏、充电不足和输入相关的 body effect 仍造成误差。gate 对地超过 VDD 不直接等于某个端间电压越限；必须看实际器件的 Vgs/Vgd/Vgb/Vds。

本工程确有 `saradcII/boosted_SH_switch/schematic`，但它的主信号管是 **`M4 → gpdk045/pmos2v`**，`S=Vin`、`D=Vout`、`G=net013`、`B=net015`。这不是可以直接套 NMOS `Vin+VDD` 波形的实现。另有 `M5 → pmos2v`、1 V 辅助器件和三只 MIM 电容 `C0/C1/C2`。`C1` 跨 `net010/net013`，`M2` 跨 `net015/Vin`，各支路参与 gate/body 的充电和跟随。主 PMOS 希望采样时获得稳定的 VSG；哪个节点向上或向下自举应由分相连接和波形确定。

第一项电路练习是按 `phi1/phi2` 的合法状态逐管写导通表，画出电容预充电回路、采样时的浮置回路和关断恢复回路。不能单凭 cell 名推断其时钟极性，也不能把 `pmos2v` 名称当作辅助 `nmos1v/pmos1v` 的允许应力。

**与当前 ADC 的关系：** 已读的实际 core 及其 mux/clamp 路径没有实例化这个 bootstrap cell，多处经 `bmslib/sw_no` 采样。核心中的 `clockPhaseGenerator` 虽存在，若输出落在 noConn 上，就不能证明 bootstrap 在工作。系统 ENOB 不足以验证此自举电路的线性与应力。

## 独立 TB 的搭建与测量

自举独立 TB 尚未确认，需在实验 library 中建立：输入源串有限 Rs、实际 gate driver/两相时钟、DUT、可配置负载电容、明确 body/电源连接。先与普通开关在相同 Rs/Cload/采样窗下比较，记录所有差异，禁止在原 core 中直接替换后声称收益来自唯一因素。

第一项只跑三种 DC 输入的预充电与采样过程，保存 Vin/Vout、`net013/net015/net010`、电容两端及关键器件端间电压，验收导通表与实际轨迹一致。随后扫输入共模与采样时间，测保持前残差；再测关断后的 pedestal，最后才用正弦样本计算谐波。

若使用理想阶跃 Rs=0 的输入，可遮蔽 kickback 与源建立；若直接对连续 Vout 做 FFT，可把保持阶梯的频谱误当采样失真。按实际采样事件提取保持值，并统一舍弃启动区间。

尺寸实验每次只改一个因素：主开关 W、Cboot 或 dead time。验收要同时报告建立、pedestal、输入电流扰动、谐波与端间应力；允许限值来自具体 PDK 文档，本轮未审计限值。

下一课：[动态比较器](S04-comparator.md)。

配套实验读图：[关键 TB 的作用与结果分析](00-testbench-results-guide.md)。区分保存配置、待执行实验与已新运行的结果。
