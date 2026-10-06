# 2026-10-03：电路主线与比较器 nominal 新运行

状态：助教完成实际电路读取与一次新 transient；学员理解与后续模块验收待验证。

## 问题与预测

用户明确希望学习 SAR ADC 关键电路和基础 PLL，并询问能否通过 virtuoso-bridge-lite 运行实际 TB。此前课文偏重 verification，本轮补齐 [电路主线九课](../courses/00-circuit-foundations/README.md)，保留既有十课作配套实验。

已向学员提出预测问题：输入差分减小时，再生判决时间与误判概率怎样变化？截至本记录未收到独立预测，本次运行仅用于建立实际 TB 的 nominal 工具链；不记为学员已掌握再生或噪声机制。助教采用假设：小差分会延长理想再生时间，实际误判与 noise/offset/时间窗口相关；本次 ramp 不是对此假设的完整实验。

## 恢复与会话身份

- Windows 经 `ssh IC_Server` 使用服务器 bridge commit `168943ca917e592c492a0db1b70aca0544f311c0`，显式 profile `adc_course`、端口 65379。
- 旧 ADC 会话已退出，status 的持久 banner 不能当作实时连通证据。本次在远程桌面 `:1` 新启动独立 ADC Virtuoso，核对 CIW 与工作目录后 bootstrap；其他工程会话未作为课程目标。
- Virtuoso `IC25.1-64b.38`，Spectre `25.1.0.054`。当前 ADC 的工作目录为包内 `WORK/saradc`。
- 运行副本为 `saradc/course_cmp_offset_20261003/maestro`，从 `saradc/comparator_offset_TB_new/maestro` 复制设置，移除旧 history 条目，并调整副本的保存路径。TB 绑定仍为原 `saradc/comparator_offset_TB_new/schematic`。
- 原 schematic 未改；原 maestro 的 `maestro.sdb`、`active.state`、`master.tag`、`data.dm` 前后 SHA-256 均相同。完整 PSF、网表和导出片段留服务器。
- 服务器记录目录为 `COURSE_REMOTE_ROOT/2026-10-03-circuits`，路径映射来自本机 config。副本设置保存后再 run，运行 history 明确绑定，没有采用教材历史波形。

## 本次新运行及证据

| 项目 | 保存/运行条件或实际结果 |
| --- | --- |
| ADE / test | `saradc/course_cmp_offset_20261003/maestro` / `saradc:comparator_offset_TB_new:1` |
| 新 history | `ExplorerRun.0`（在新副本中第一次生成，名称可与原包旧历史相同，须结合路径） |
| 仿真模式 | Single Run, Sweeps and Corners；nominal，一点，非 Monte Carlo |
| 分析 / 模型 | tran；gpdk045 `tt`；27°C；VDD=1.2 V |
| 输入 / clock | 差分 ramp ±20 mV，resolution=100 µV；fclk=1 MHz |
| stop | 新网表表达式对应 800.1 µs |
| 新网表 hash | `dad7535315471abf5be362f36eee6c51d446d4f51e67f517cb1a1e8dc0a239e6` |
| Spectre 完成 | 0 errors，2 warnings，8 notices；elapsed 约 25.4 s |
| warnings | 同一 `CMI-2426` 报告两次：I0.I0.I10.NM3 的 Pdiblc2 为负；模型适用性影响尚未定量评估 |
| ADE 完成日志 | 1 point completed；Number of simulation errors: 0 |
| `Offsetf` / `Offsetr` | 保存表达式测得 −50 µV / +50 µV |
| `Offset` | 保存表达式测得约 6.418×10⁻¹⁷ V；两方向求平均，不代表这种精度 |

实际新网表包含 `saradcII/latchonly_updated/schematic` 的 11 个 MOS，offset ramp 使用行为源。导出 198–202 µs 的输入 ramp 和 `outb−out` 片段，分别为 `ExplorerRun.0-ramp.txt`、`ExplorerRun.0-decision.txt`，显式绑定该 history。

Bridge `read_results` 的 scalar 输出可读，waveform 类型输出的 value 留空，不能当作缺失波形；PSF 实际有 transient 数据，片段导出成功。其 `overall_yield` 原始字符串含 `ErrorPoints 1`，与本次 ADE 日志 0 simulation errors 不一致，接口口径未审计，不据此声称整项统计验证通过；原始返回 JSON 保留服务器。

小型 Git 证据：[模块与新运行 JSON](evidence/2026-10-03-circuit-modules.json)。模块实际连接见 [电路地图](../docs/circuit-map.md)。

## 设计判断与边界

1. SSH→bridge→实际 ADE→新网表→Spectre→新结果读取链路已跑通一次比较器 nominal transient。不同 TB 和 AMS 分析仍需独立验证。
2. ±50 µV 两个翻转点与 100 µV ramp 网格相近；上升/下降方向和保存 cross 表达式须结合 clock 采样解释。不能把平均接近零写成真实失调为零、无迟滞或高精度测量。
3. 此次 fclk=1 MHz，不支持 core 在约 1.2 GHz 比较时钟下满足判决时间的结论。未运行 mismatch Monte Carlo、transient noise 或 kickback 实验。
4. 自举 cell 为独立晶体管实现，当前 ADC 采样路径多处经行为开关；CDAC 位权、自举性能、ADC 系统和 PLL 均未新仿真。

## 下一项具体操作

从 [S04 比较器](../courses/00-circuit-foundations/lessons/S04-comparator.md) 的 reset/evaluate 开始。先接学员预测，在独立模块副本将输入改为固定正/负小差分，并统一共模、负载和 clock；测内部再生与最终输出延迟，按新网表选节点。先只验收一组 nominal 小差分判决，不同时做 Monte Carlo。随后回到 S01/S02 的电荷与位权学习。
