# ADC Verilog-A 教学模型与运行入口

本目录是“先行为系统、再逐模块换电路”的起点。它有独立模块和新 Spectre 基线，**尚未接入原始 OA DUT，不是原工程已跑通的混合系统**。配套 [建模与替换课](../../courses/05-adc-projects/lessons/A05-model-to-circuit.md)。

| 源码模块 | 边界/状态 | 当前精度 |
| --- | --- | --- |
| `learn_sh` | sample 下降沿捕获 VIP/VIN，有限输出 R | 理想捕获，无输入电流/电荷回踢，无真实 acquisition |
| `learn_cdac8` | 差分残差、7 组 ±位权更新、Rout/Cload | 理想 reference 和比例；不是电荷守恒的完整双 CDAC |
| `learn_compare` | evaluate 时采样极性，固定延迟，reset 输出 0/0 | 可扫 vos/tdec；无再生状态、noise 或 kickback |
| `learn_done` | 从 one-hot 输出生成 done | 事件检测/传播延迟；不是 EN_LOOP 门级等价实现 |
| `learn_ctrl8` | 八次判决、下一次由 done reset 触发、最终 bits/EOC | electrical-port 状态机；检测 sample 到来时仍 busy |
| `learn_residue_amp` | 差分增益、比例误差、有限 R/C、输出限幅 | 不含 gain boosting 的 poles、CMFB、slew、SC 分相 |

`async_sar8.va` 的内部 `prefix[7:0]` 是已判决前缀，`phase` 是调试用的已判决数（电压数值 0…8）；不是原 schematic 的 P/N 控制向量。`bits[7]` 是 MSB；原 8 位 DUT 的 `DOUT<0>` 才是 MSB，接入时明确反序。CDAC 第一判决阈值 0，之后七次阈值更新；第八位不再切电容。

差分输入范围为 `[-1.8,+1.8)` V，VCM=0.9 V，理想 unsigned code 定义为 `floor((vid+1.8)/3.6*256)`，两端截为 0…255。这是依据本项目理想差分电荷范围构建的教学定义，原逻辑输出极性和转换协议仍需混合系统验证。输入恰好在码边界时有确定的 ≥ 判决，初期测试避开码边界。

## 已执行的基线

2026-10-04 新运行四个 Spectre transient，均 0 errors、0 warnings：

- 五样本差分 `+0.3,−0.3,+1.1,−1.1,+0.3 V`；码 `149,106,206,49,149`，每样本八次 evaluate，共 40 次；输出 bus 波形独立解码与理想 floor 对照通过。
- 外部周期 25 ns，sample 下降沿到 EOC 0.9 V 上升沿约 7.080 ns。这个时间来自固定参数的教学模型，不是原比较器或 ADC 的性能。
- tdec 从 300 ps 故意改到 3 ns，产生两个 overrun；sample 会更新 held input，原转换因而可能被新输入污染。该运行只验收 overrun 被检测，所有越界转换结果无效；EOC 只是算法结束，不覆盖输入数据有效性。
- 残差模型 gain=8、Rout=1 kΩ、Cload=1 pF，测试 10/50/150 mV 差分输入、1% gain error 和 0.8 V 差分限幅。9 ns 观察点在 50 μV 输出误差阈值内通过；这个窗口/阈值是教学检查条件。

[运行摘要](../../notes/evidence/2026-10-04-adc-behavioral-baseline.json)、[独立波形检查](../../notes/evidence/2026-10-04-adc-behavioral-waveforms.json)、[新波形图](../../notes/evidence/2026-10-04-adc-behavioral-trace.png)。未运行整套 12 位行为流水线，未执行晶体管替换、noise、FFT 或 PVT。

## 在服务器复现

将这两个 .va 和 scripts 以仓库相对结构放入自己的学习工作区；原工程不改。从 config/local.env 读取 COURSE_REMOTE_ROOT，Spectre 在运行环境的 PATH。使用显式且不存在的输出目录：

```bash
python3 scripts/run_adc_behavioral.py --output "$COURSE_REMOTE_ROOT/your_new_run"
python3 scripts/analyze_adc_behavioral.py "$COURSE_REMOTE_ROOT/your_new_run"
```

运行脚本拒绝覆盖旧目录，保留 input.scs、模型副本/hash、日志与 PSF。错误时查看保留的日志，不能用以前成功的 summary 冒充本轮成功。分析脚本仅支持本 TB 输出的 scalar PSF ASCII，不能替代通用波形工具。

原图读取通过服务器 virtuoso-bridge-lite 的 adc_project_course 完成；本次仿真由 SSH 调用 Spectre CLI，未建立 Maestro 或新的 veriloga OA view。下一阶段在独立 learning library 中导入源码、生成 symbol 并做原模块接口适配，再由 bridge 核对 config binding、运行 ADE 并导出波形。
