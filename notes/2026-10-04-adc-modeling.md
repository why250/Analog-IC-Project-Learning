# 2026-10-04：Verilog-A 系统基线与逐模块替换路线

用户询问 8 位异步 SAR 与 12 位 Pipelined-SAR 是否适合先 Verilog-A 建模、再逐模块替换真实电路，允许使用 virtuoso-bridge-lite。本轮先读入口/进度/当前课/笔记与工作树，应用 analog-circuit-research 与既有 Virtuoso bridge 工作流，检查接口并交付 [A05 建模与替换课](../courses/05-adc-projects/lessons/A05-model-to-circuit.md)、[模型/复现入口](../models/adc_behavioral/README.md) 和新行为仿真证据。

## 原工程接口检查

服务器 bridge .venv，profile=adc_project_course、port=65385、PID=188233、cwd=ADC_LEARNING_ROOT、IC25.1-64b cpgbld31。实时读取 11 个 cell，源 sch.oa hash 前后相同，之后再次通过 /proc 启动参数/工作区核对进程。未修改 OA，未操作其他 ADC/AFE/precision 会话。

[接口证据](evidence/2026-10-04-adc-model-interfaces.json) 含 pin/实例端子、相对 source 路径/hash 与会话身份。8 位 SAR_LOGIC 有 P/N<1:8>，DAC_SW 用 P/N<2:8>；compare 与 EN_LOOP 独立。12 位 Pi-SAR_amp 是带 sources 的 TB，第一/第二段 SAR 有实际残差与参考端口。D_adjust2 实际含 c1 锁存一级码的六只 DFF、两段 adder/carry 与受 D2<5>/D2<7> 控制的支路，不能直接替换为随意位移相加。

已有 8bit_ideal_DAC 与 Pipe_SAR 的 DAC_VA/DAC_7bit_0.4ref/DAC_VA12 源码用于输出观察，不是整系统行为模型；部分公式为双极性加权。这些原文件没有修改。

## 新模型和实验

[async_sar8.va](../models/adc_behavioral/async_sar8.va) 含 sample-hold、七组理想 CDAC 位权、延迟比较器、done detector 与八次判决 controller。全部端口为 electrical，先用 Spectre，不依赖 AMS。phase/prefix 与原 P/N 不是同一接口；bits[7] 为 MSB，原 DOUT<0> 为 MSB，适配待建立。

[residue_amp.va](../models/adc_behavioral/residue_amp.va) 含 gain=8 教学假设、gain error、Rout/Cload 和差分限幅。没有 SC 分相、gain-boost poles、CMFB、slew 或器件 noise。未建立完整 12 位流水线；没有晶体管混合系统、PDK 或原 ADE 新运行。

新 Spectre 25.1.0.054 由 SSH CLI 运行，源码/脚本部署在 COURSE_REMOTE_ROOT/2026-10-04-adc-modeling/source，结果在同目录 run01。bridge 用于真实接口读取；未建立新的 veriloga OA view、symbol 或 Maestro。机器路径由 config/local.env 关联。完整 PSF/日志留服务器，摘要记录模型与 netlist hash。

| 新运行 | 结果与条件 | 验收范围 |
| --- | --- | --- |
| sar_nominal | 周期 25 ns，tdec=300 ps；vid=+0.3/−0.3/+1.1/−1.1/+0.3 V，码 149/106/206/49/149 | 每样本八次决策，共 40 次，无 overrun；输出 bus 独立解码通过 |
| sar_timeout | 只把 tdec 改为 3 ns；约 30.015/80.015 ns 检测 overrun | 验收越期被检测；后续采样改写 held input，完成码无效 |
| residue_nominal | G=8，Rout=1 kΩ，Cload=1 pF，diff limit=0.8 V；10/50/150 mV 输入 | 9 ns 观察窗，约 0.08/0.399975/0.799976 V；50 μV 输出误差内通过 |
| residue_gain_error | gain error=1%，其余同前 | 约 0.0808/0.403975/0.799977 V；小信号比例与限幅通过 |

四次 transient 均 0 errors、0 warnings，见 [运行摘要](evidence/2026-10-04-adc-behavioral-baseline.json)。原 -W 调用未捕获 stdout，版本用 PSF header 的 25.1.0.054 核对，不把空字段当版本。

另读真实 PSF ASCII：每次在 EOC 0.9 V 上升沿后 100 ps 解码 bus，对照独立 floor 公式；核对八个 evaluate 边沿、无 overrun。sample 下降沿到 EOC 约 7.080 ns，仅为固定教学参数结果。见 [波形测量/hash](evidence/2026-10-04-adc-behavioral-waveforms.json)、[小型 CSV](evidence/2026-10-04-adc-behavioral-trace.csv)、[图](evidence/2026-10-04-adc-behavioral-trace.png)。

## 推荐替换和限制

8 位先功能/握手基线→真实 compare→EN_LOOP/逻辑逐块→电荷域 CDAC 与兼容采样开关→bootstrap/source impedance→reference/系统指标。研究 kickback 时提前恢复电荷域负载；真实 sampled node 上不能挂理想 held-voltage 源再声称验证 charge injection。

12 位先 residual/range/编码与 sample_id→真实或等价 D_adjust2→逐段 SAR→amp_gainboost→完整混合系统。G、参考跨度与数字权重必须闭合；gain=8 和“6+8−2”不构成实际十二位精度证明。RTL/AMS 为后续可选轨道。

## 预测与下一项

已询问 1% 级间 gain error 的重构误差跟原输入还是一级残差走，答案待反馈。下一项只验收 B0 的 sample→compare→done→reset→下一 bit→EOC 时间线；随后核对真实 compare 的 reset/极性/共模/负载、SMIC 模型与 adapter，准备 B1 学习副本。Pipelined-SAR 完整 P0/P1 和其他 SAR/AFE/PLL 验收点保留。

## 验证状态

三个 Python 脚本编译通过，运行/PSF 分析/绘图正常路径已执行，图已目视检查。错误路径确认拒绝非单调 PSF、缺失 Spectre 与覆盖已有运行目录。10 个 Markdown 的 187 个链接、四次运行的模型 hash 和 11 项原 source hash 检查通过，git diff --check 通过。未提交/push。
