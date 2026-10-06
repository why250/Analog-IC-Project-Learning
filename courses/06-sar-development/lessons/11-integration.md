# 11：逐块替换与系统闭合

问题：理想 SAR 给出正确数字码，换入真实 comparator 后仍给出同一码，能证明比较器已满足系统需求吗？先预测：若输入由零输出阻抗电压源驱动，kickback 会呈现为输入电压还是源电流？

## 先闭合合同，再替换模块

替换的前提是端口、极性、供电域、共模、时序、负载与数据有效协议一致。Python 是算法黄金模型；Verilog-A 提供模拟时间与电气接口；RTL/门级或真实 SAR_LOGIC 管理数字状态。实际电路没有义务满足教学模型的任意固定延迟，模型应使用电路提取出的范围和失败行为。

推荐建立独立顶层与固定 stimulus：先理想采样、理想 CDAC、行为 comparator、行为控制；随后逐个替换，保留上一配置以便同条件比较。第一项可以选已有独立 TB 的模块，不强制从采样开关开始。每个配置交付新增网表、实际 master/view 清单、输入/clock/reference 条件和逐样本 trace，不能只看 config 界面的文字。

| 替换对象 | 首先恢复的物理条件 | 主要比较量 |
| --- | --- | --- |
| comparator | CDAC 等效电容/阻抗、reset/evaluate、输出负载 | 极性、过驱动、decision latency、kickback、memory |
| CDAC 与开关 | 真实 top/bottom plate、reference source impedance | 实际位权、DAC 建立、共模、reference 电荷 |
| 采样/自举 | VIN source impedance、真实采样电容、时钟斜率 | aperture、held error、pedestal、失真与器件应力 |
| 控制 | 可用的输出电平/边沿、延迟与 dead time | 每位握手、超时、采样覆盖、valid/码锁存 |
| reference/bias | 启动、去耦与回流、实际 load waveform | droop、恢复、供电耦合、功耗与工作点 |

## 理想模型怎样隐藏错误

若 VA 通过 `V(node)<+held_value` 直接钳住共享 top plate，真实比较器注入的电荷可能被理想源吸收。波形很干净只说明边界被钳住。应在电荷域恢复采样电容、开关和有限阻抗，让 ΔQ 在实际 C 上产生 ΔV；保留诊断电流，区分参考或输入驱动提供的电荷。残差模型用理想输出源也会掩盖下一级 CDAC 的动态负载，需要恢复输出阻抗和带宽。

教学 VA 的比较量、MSB 与实际 OA 端口可能不同。`8_bit_sar_adc/SAR_ADC` 的 `DOUT<0>` 是已读控制连接对应的 MSB，而教学 `bits[7]` 为 MSB；需显式位序 adapter。实际 P/N<1:8> 控制与 P/N<2:8> 开关组存在首位差异，不能把行为 DAC 的八个独立电压权重直接接成八组真实开关。端口细节见 [A05 实际替换路线](../../05-adc-projects/lessons/A05-model-to-circuit.md) 和 [接口证据](../../../notes/evidence/2026-10-04-adc-model-interfaces.json)。

## 最小系统实验

先运行中间码、major carry 两侧、接近量程端点与正负交替输入，每个输入保留足够 acquisition 时间；初期不用长 FFT。逐 bit 保存 residual、DAC 共模、compare clock/outputs、done/reset 和 code_prefix。用 sample_id 将采样输入、输出码和 EOC 对齐，明确启动样本与超时样本。

对照必须使用相同 stimulus/seed、clock、reference、source/load 和温度，输出有效时刻可以按各配置实际 latency 对齐。真实模块允许出现已预算的 offset 或 latency；判据应比较模块差异能否解释系统误差，而非要求带非理想的电路逐码等同理想结果。

若码突然反向，先查 polarity/bit order；若只在边沿错，查可用决定阈值与 race；若交替输入比 DC 差，查 reset、sample memory 与 source recovery；若 major carry 附近失败，查位权、reference 电荷和 DAC 建立。更改一个可控条件后用残差和时序归因，禁止仅靠增大采样周期宣称已找到瓶颈。

验收：一张实际 view 绑定表、一个 sample 的逐位对照、一个失败机制的受控反证，以及恢复副本。真实混合系统尚未新运行；已有教学 VA 成功不代替这一步。接 [12 验证](12-verification.md)。
