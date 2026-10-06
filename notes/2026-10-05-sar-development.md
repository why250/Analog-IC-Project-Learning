# 2026-10-05：SAR ADC 完整开发设计教程与离线模型

## 问题、预测与范围

用户希望理解一般开发流程，问是否应先 MATLAB/Python、再 Verilog-A、再逐块替换实际电路，并要求完整教程。已建立 [16 课完整开发教材](../courses/06-sar-development/README.md)，主线为单核差分 SAR，扩展 Pipelined-SAR。MATLAB/Python 通常是替代工具；电气接口/时序用 VA/RTL 建模，模块可行性、误差预算和架构并行迭代，电路/PEX/实测参数回填模型。

授课首个待验收问题：CDAC 是否只需要满足 kT/C？已发出可选预测问题，尚未获得回答。课文完成不等于学员学完；本次不扩展成 PDK 尺寸设计或新 EDA 实验。

## 交付

- 01–05：规格/测试合同、架构、电荷与时间/噪声预算、Python/MATLAB、VA/RTL。
- 06–10：采样/自举、CDAC/开关、比较器、控制与数据有效、reference/bias/供电；含 sizing 方向、模块 TB、失败归因。
- 11–15：物理端口/负载恢复与逐块替换、静态/动态/PVT/统计、版图、PEX 与实测。
- 16：residue gain/range/冗余、gain boosting/CMFB、数字样本对齐；实际 D_adjust2 映射仍待审计。
- [Python 源码](../scripts/sar_design_model.py)、[开发设计记录模板](sar-development-template.md)，已接入主目录、课程/笔记索引与 progress。

## 例子与来源边界

本次数值例子：10 bit、20 MS/s、差分跨度 2 V、300 K、ENOB 目标≥9，VDD=1.2 V/VCM=0.6 V 与功耗 2 mW 是未选工艺的教学假设。单位电容暂设 10 fF，没有 PDK density/mismatch 证明。实际 OA 名称/端口来自既有 [2026-10-04 接口读取](evidence/2026-10-04-adc-model-interfaces.json)，本轮没有重新读取服务器。

已有真实 8 位图、GPDK 比较器和 VA 运行分别引用原记录。2026-10-04 的 8 位 VA 四次 transient 是无 PDK 行为实验；GPDK 的 190/198 ps 是另一电路/负载条件；完整 12 位 pipeline 尚未运行。它们都不构成本教程示例工艺可行性的证据。

## 新离线计算

运行入口 `scripts/sar_design_model.py --output artifacts/local/sar-design-20261005-final --seed 42`，使用既有本地 Python 环境 `artifacts/local/plot-env/Scripts/python.exe`，NumPy 2.5.3、Matplotlib 3.11.2。小型结果复制到 [证据目录](evidence/2026-10-05-sar-design-model/summary.json)，大型/临时输出留忽略的 artifacts/local。

源码 SHA-256：`00d8a3eed3a5a5342dd1f3a216aea42754d4b9f4577c613ba11f91f296538a1a`；summary 中 hash 已与最终源码核对。种子 42；失配假设 unit errors 独立、无 gradient/相关寄生；FFT M=2048、k=901、fin≈8.798828 MHz、差分正弦峰值 0.98 V，相干矩形窗。transition 按第一/最后 transition endpoint 拟合，外侧饱和 bins 排除。

| 预算量 | 新计算 | 假设/解释 |
| --- | --- | --- |
| LSB | 1.953125 mV | 差分跨度 2 V / 1024 |
| quantization RMS | 0.56382 mV | 均匀量化近似 |
| 非量化 RMS 余量 | 0.97751 mV | 满幅正弦、ENOB=9、功率扣除 |
| 采样 C 噪声下限 | 23.01 fF/侧 | 两侧独立 2kT/C，采样分配 0.6 mV |
| 暂设阵列 C | 10.24 pF/侧 | 1024×10 fF，非最终选择 |
| 该 C 采样噪声 | 28.44 μV | 同上理想热噪声假设 |
| acquisition τ 上限 | 1.20225 ns | 10 ns、2 V 阶跃、0.25 LSB |
| Rtotal 上限 | 117.407 Ω | 单极点、10.24 pF |
| DAC τ 上限 | 0.28854 ns | 2.2 ns、1 V 阶跃、同 allowance |
| 保守时间余量 | 4 ns | 50−10−10×3−6 ns，非电路闭合 |

图：[噪声与电容](evidence/2026-10-05-sar-design-model/noise-capacitance.png)、[采样建立](evidence/2026-10-05-sar-design-model/acquisition-settling.png)。这些解析图不包含实际 slew、多个极点、注入/回踢或 reference feedback。

| 受控模型 | SNDR (dB) | 解释范围 |
| --- | --- | --- |
| ideal | 61.8877 | 10 位搜索 + 量化，非满幅修正 |
| 1% unit mismatch、一个 seed | 61.2317 | 固定实际位权，不代表良率 |
| 采样 0.6 mV + 每判决 comparator 0.4 mV | 57.5850 | 指定随机机制，非 PDK noise |
| jitter 50 ps | 50.8379 | 随机 aperture 扰动 |
| DAC τ=1 ns | 33.5616 | trial 的一阶状态建立，无完整电荷拓扑 |

同一 mismatch realization 的 max|INL|=0.31272 LSB，DNL −0.15253…+0.24930 LSB，搜索容差内零宽内码数为 0；这不是 MC yield 或真实无 missing code 证明。u=1.26 V 的逐位 code=645 与独立 floor 对照一致。脚本尚未实现动态 deadline 或完整流水线；time margin 为分析预算，slow DAC 是建立模型。

## 验证

源码 py_compile 通过；6/8/10 位分别用 259/1027/4099 个包含阈值、相邻浮点数、码中心和饱和点的输入与独立 floor 量化对照一致；理想 endpoint INL/DNL 近零（容差 10⁻⁵ LSB）。五种 dynamic cases 正常生成 JSON/PNG。

11 类非法输入被拒绝：负失配、超出教学位数、缺 RNG 的 comparator noise、负 τ、非互质 FFT、奇数 FFT 长度、超过量化下限的精度目标、零 C、负噪声分配、零 settling allowance、非有限预算。重复输出目录被拒绝，运行前后结果 hash 相同。交付核对覆盖 16 课与索引/记录等 25 个 Markdown 文件，262 个本地链接均存在；summary JSON/源码 hash 一致，两张 PNG 目视检查可读，git diff --check 未报告空白错误（现有文件有 LF/CRLF 提示）。这些软件检查不是 EDA 验证。

## 下一步

先只验收 03：解释为什么噪声下限 23 fF 与暂设阵列 10.24 pF 不矛盾，以及增 C 对 Ron/参考/速度的反作用。然后将实际 8 位 SAR 的 Cu/source/clock windows 回填合同，审计 SMIC model/CDF 和 compare adapter，再推进 A05 的真实混合替换。原 SAR 比较器、PLL、AFE 与精密逆向分支均保留；未提交或 push。
