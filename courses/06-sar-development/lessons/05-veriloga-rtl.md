# 05：从离散算法到 Verilog-A/RTL 的接口和时序

问题：为什么 Python 正确而 Virtuoso 系统仍可能错？先预测：样本对齐、reset、阈值、负载和求解器哪个会被 floor 模型遗漏？Verilog-A 的价值是明确电气边界和模拟时间，不是只把公式搬到 analog block。

## 先定 module contract

每块写端口/方向/参考地、范围/VCM、VDD/阈值、输出 R/C/负载、reset 状态、clock edge、delay、valid 协议和 source impedance。控制块记录 bit order、sample_id、busy、终止/超时与 latency。补一个错误注入测试，例如一周期旧码、错误输出极性、未 reset 或迟决。

模拟相关部分用 VA；SAR controller/编码/寄存器适合 RTL。pure electrical VA + MOS 可以由 Spectre 模拟，RTL event domain 混合要审计 AMS/Xcelium/license、connect rules、timescale/logic supply。初期可以用 electrical VA 状态机验证协议，之后再换 RTL，不能认为这样已覆盖门级噪声/供电。

## 建模容易隐藏的物理机制

- 时钟事件用 cross 给出过阈值的具体时刻；reset/initial_step 不可省。
- transition 适合分段常量状态的有限边沿，不应拿来把持续变化的输入当平滑滤波器；连续动态用电流/电容或适当传递函数。
- 零输出阻抗源会钳住 kickback、reference droop 与 stored charge；用于功能测试时可以，替换物理节点时必须撤除/改成相容的网络。
- `$strobe` 是内部事件记录，最终 bus、valid 和输入波形仍应独立解码；算法结束并不保证没有 overrun。
- 独立随机采样噪声、固定芯片失配、colored noise 与逐判决噪声分开，seed/相关性/带宽不可混用。

本仓库已有 [async_sar8.va 与残差模型](../../../models/adc_behavioral/README.md)：8 位教学模型五个样本的新 Spectre bus 解码通过，slow comparator 有 overrun。它是功能/接口起点，不是 PDK 精度模型。内部 phase/prefix 是调试端口，原 SAR 的 P/N 要经 adapter；bits[7] 与原 DOUT<0> 的 MSB 映射需明确。

## 与 Virtuoso bridge 结合

先读本机 bridge AGENTS/文档，核对 profile/PID/cwd/port/library readPath；在独立学习库建立 model/symbol/config，原库只读保留。每次 netlist 后确认目标实例实际绑定到哪个 master/view/source，include 的 model section 和 pin/termOrder 是否正确。config 的意图不是最终网表证据。

已有 2026-10-04 行为仿真由 SSH Spectre CLI 运行，bridge 用于实际接口读取；未建立新 OA model views。后续用 bridge 跑 ADE 需按本机版本的 GUI/session 流程，不能编造 SKILL API。操作原则见 [bridge 文档](../../../docs/bridge.md)。

验收实验：同输入在 Python 与 VA 取有效输出码，约定误差/latency，故意超时证明检测；确认与 VDD/VCM/负载的合同。接 [06 采样设计](06-sampling.md)。
