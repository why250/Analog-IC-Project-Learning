# 第 01 课实验记录

状态：进行中。2026-10-01 助教已完成服务器环境检查和部分只读工程观察；学员掌握情况和仿真仍待验证。以下初始表格保留待填写项，本次实证见下方日期记录，不计作学员已完成本课。

## 会话信息

- 日期 / EDA 主机别名：待填写
- 资料包校验与工作副本变更：待填写
- Virtuoso / Spectre 实际版本：待填写
- Bridge 版本与目标 profile（若使用）：待填写
- 本次目标：建立 `saradc/10Bit_ADC_TB_new` 验证地图

## 预测

1. 采样周期与转换周期：待填写
2. 近 Nyquist 测试的覆盖与遗漏：待填写
3. 行为模型影响哪些结论：待填写

## 工程地图

| 模块 / 实例路径 | Library / Cell | 当前视图及确认方式 | 功能与模型边界 | 证据 |
| --- | --- | --- | --- | --- |
| DUT | 待确认 | 待确认 | 待确认 | 待填写 |
| 采样 / CDAC | 待确认 | 待确认 | 待确认 | 待填写 |
| 比较器 / 控制 | 待确认 | 待确认 | 待确认 | 待填写 |
| 输出观测 | 待确认 | 待确认 | 待确认 | 待填写 |

## 条件与测量审计

| 检查项 | 当前会话观察 | 来源 / 推导 | 待验证问题 |
| --- | --- | --- | --- |
| fsample / fclk / fin | 待填写 | 待填写 | 待填写 |
| 输入幅度 / 共模 / 编码 | 待填写 | 待填写 | 待填写 |
| tran / strobe / 输出更新相位 | 待填写 | 待填写 | 待填写 |
| 模型文件 / section / 统计开关 | 待填写 | 待填写 | 待填写 |
| 指标表达式 / 取样窗口 / FFT 点数 | 待填写 | 待填写 | 待填写 |
| f_fftbin 是否被引用及其用途 | 待填写 | 待填写 | 待填写 |
| 旧路径与本机映射 | 待填写 | 待填写 | 待填写 |

## 下一课最小实验

- 假设：待填写
- test / 条件 / 参数：待填写
- 需要保存的信号（实际层级名）：待填写
- 通过判据与失败时优先排查项：待填写
- 本地证据路径 / 运行 ID：尚未运行

## 结论与后续

- 已确认事实：待填写
- 推断及其依据：待填写
- 未解决问题 / 阻塞：待填写
- 下一项具体动作：待填写

以后在下方按日期追加会话记录，保留预测与修正过程。

## 2026-10-01：换电脑后的服务器接管与采样控制追踪

**本次目标：** 检查 Windows → `IC_Server` 环境，找到真实 DUT，完成采样控制入口的静态追踪。

### 用户提供的信息与预测状态

- 用户确认教材为 `/home/userone/AAAIC/tutorials/cadence_verification`，先学习 SAR ADC verification；通过远程桌面查看服务器 GUI。
- 用户提供本机 bridge checkout：`D:/Users/Administrator/Documents/GitHub/virtuoso-bridge-lite`。
- 关于额外两个转换周期的最初回复给出了教材路径，不能记为电路预测。
- 用户随后要求按助教建议推进；采用助教工作假设“SC 触发启动，内部 sample 定义采样事件”。学员未独立预测，不记录为已理解。

### 环境与证据

- Windows 课程工作树起初干净；新增忽略的 `config/local.env`，保存服务器路径和 Windows bridge 路径。
- SSH 免交互连通，服务器 hostname `xunipc`。Virtuoso `IC25.1-64b.38`、Spectre `25.1.0.054`。
- 两份原包 SHA-256 一致，实际归档在 `originals/`。顶层 `sch.oa` 等抽查文件与归档一致，Maestro 保存状态不同；active test 变量相同。未完整比对全部工作副本。
- 在服务器部署现有 `launch.sh` 和本机配置；Bash 语法、ADC/PLL `--check` 正常路径、无效 target 拒绝符合预期。没有修改脚本；检查不属于仿真验证。
- 启动前备份 OA 和三个工作区入口文件，位于 `/home/userone/.local/state/analog-ic-project-learning/2026-10-01-environment/pre-session-oa.tar.gz`；SHA-256 `3c774a1112b9dab99765ac817977ccd2c9ad9dcbd3315dd159cd6629b9d8aef0`，范围不含历史波形。
- 桌面 `:1` 经访问检查成功。新启动 Virtuoso PID `3566`，workdir 为 ADC `WORK/saradc`；PID、窗口 ID、桌面授权均只表示本次会话。
- 实际用服务器 bridge HEAD `168943c`、profile `adc_course`，daemon 端口 `65379`；经 Windows SSH 调用服务器 `.venv`。`status` 核对主机、用户、工作区，通道计算 `1+2` 返回 `3`。
- Windows bridge HEAD `a04d335`，既有 `.env` 指向 `IC_Server`；只读核对，没有覆盖配置。与服务器认证协议不同，未验证 Windows 旧客户端直连。
- 小型 Git 证据：[环境与控制链摘要 JSON](evidence/2026-10-01-environment.json)。服务器同目录保存 `top-schematic.json`、`top-schematic-unfiltered.json`、`dut-schematic.json`、`logic-schematic.json`、查询脚本和启动日志；完整工程数据不进入 Git。

### 已确认的静态控制链

`saradc/10Bit_ADC_TB_new:I0 → saradcII/10bit_adc_core_w_split_dac_ld1_msb:I56 → saradc/10Bit_ADC_logic:I22 → saradc/controller_baseline/veriloga`。

这里最后的 `veriloga` 是已存在的模型源码，实际仿真绑定待新网表。DUT 本身可用 `symbol`、`schematic`；控制器可用 `symbol`、`veriloga`。

- `SC` 接到控制器 `go`；源码第 46 行仅在上升穿越阈值时设置 `convert=1`，未见下降沿清零。因此源码支持启动触发，而非逐次采样时钟或实时电平使能。
- `CLK` 经 `I33/I36` 到 `clk_dly`；控制器 `valid` 输出 `DR`、`sample` 输出 `sample2`。`I38` 产生外部 `sample=OR(DR,sample2)`；`I49/I47` 组合 `clk!` 和 `NOT(sample)` 产生 `sample_clkb`。门传播延迟未测量。
- 比较器 `I0/I55` 的时钟是 `sample_clkb`，输入 `sump/sumn`，`outb=outp` 返回控制器。比较器内部实现未审计。
- 控制器源码 SHA-256 `fd5fa51e5ef26187f89163f42a1693bd6914cd2ba71150e180522f07c34b941c`，与原包一致。

### 推导与边界

按稳定循环、忽略延迟：state `12` 采最后一位并锁存结果，同时开始第一段采样；state `1` 清 `DR` 并继续第二段采样；state `2` 结束采样、置首试探位；state `3…12` 完成十次决策。共 12 个内部周期；额外两个是两段采样区间，锁存与第一段开始重叠。由保存的 `fclk=1.2 GHz` 推导采样高电平约 1.667 ns，重复周期 10 ns。**不是实测时序。**

顶层 `SC` 源保存 `per=1`、`td=10n`、`pw=900.0m`；源表达式和控制器初始化、延迟、首次有效码都需新网表与 transient 核对。顶层与控制逻辑 schematic 已以只读 `r` 模式打开。本轮未保存设计、打开 Maestro、生成网表或启动新仿真，已有历史结果未计作本轮实验。

### 下一项具体操作

按 [采样入口续篇](../courses/01-cadence-verification/lessons/01a-sampling-entry.md) 准备一个 nominal 时序实验：先预测 `sample` 高电平宽度与 `DR` 相位，再核对新网表的模型绑定和节点名，观察十次比较及两段采样。第一课整体仍进行中。

待验证：ADE/模型/许可证、新网表绑定、启动稳态与有效码相位，以及 CIW 的 `dpt` 目录 warning 对后续功能的影响。当前无已确认的 schematic 读取阻塞。

## 2026-10-03：电路学习目标澄清与模块新实验

用户明确希望学习 SAR ADC 的自举开关、比较器、CDAC 和基础 PLL。已增加 [电路主线](../courses/00-circuit-foundations/README.md)，verification 作配套实验，Fractional-N 留后续扩展。本轮独立 ADC 会话已重建，实际模块和模型边界见 [电路地图](../docs/circuit-map.md)。

通过 bridge 新运行了比较器 nominal transient，具体条件和限制见 [运行记录](2026-10-03-comparator-nominal.md)。这一运行没有验收系统采样时序或 ADC 指标；此前未运行的系统条目仍保持待验证。下一项操作转到 S04 的固定小差分判决时间，以实际 reset/evaluate 电路展开授课。

## 2026-10-03：完整课程准备

用户要求生成完整课程，已补齐 SAR ADC 02–06、PLL 07–09 和设计变更 10，建立各课记录表、[完整目录](../COURSE.md) 和 [统一实验规范](../docs/experiment-protocol.md)。新增课文是研修内容与待验证实验方案，不计作学员完成。

本次仅经 SSH 查后续 testbench/config/AMS view 的文件存在性，并读取 README；小型证据见 [入口清单](evidence/2026-10-03-course-entries.json)。没有读取新波形、打开或保存 EDA 会话，也没有运行新仿真。PLL 规格数值尚未审计。

下一项具体操作仍为第 02 课的新 nominal 时序基线：先预测 sample/DR 相位，再建立恢复副本与新网表，验证控制模型绑定和连续转换。第一课整体继续保持进行中。
