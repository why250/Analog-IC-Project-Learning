# 第 01 课续篇：谁定义真正的采样事件？

**工程问题：** 顶层 `SC` 的保存周期是 `1 s`，为什么这个 test 仍保存了 `fsample=100M`？本次只追踪采样控制入口，暂不评估 ENOB。

这是 [第一课](01-project-map.md) 的一个小任务。服务器已接管，助教完成静态逻辑追踪，新网表和波形检验待完成；记录写入 [第一课笔记](../../../notes/01-project-map.md)。

## 1. 问题与工作假设

本轮先询问 `SC` 是启动/使能还是逐次采样时钟。用户选择按助教建议推进，因此采用工作假设：**`SC` 触发启动，内部控制逻辑产生真正的采样与有效码事件。**这不是学员独立预测。

下次跑波形前请先预测：稳定转换后，`sample` 的高电平会持续几个内部时钟周期？`DR` 拉高是否与新一轮采样开始重叠？

## 2. 实际层级与控制链

来源：2026-10-01 新启动的 Virtuoso 会话，经 bridge 只读读取 schematic；[证据摘要](../../../notes/evidence/2026-10-01-environment.json) 保留关键实例、连接、保存参数和源码哈希。

| 位置 | 保存参数或实际连接 |
| --- | --- |
| 顶层 `I0` | `saradcII/10bit_adc_core_w_split_dac_ld1_msb`，可用 `symbol`、`schematic` |
| 顶层 `V1` | `analogLib/vpulse`：`PLUS=SC`，`per=1`、`td=10n`、`pw=900.0m` |
| 顶层 `V2` | `analogLib/vpulse`：`PLUS=CLK`，`per=1/fclk` |
| DUT `I0/I56` | `saradc/10Bit_ADC_logic`，顶层 `SC/CLK` 进入这里 |
| 控制 `I0/I56/I22` | `saradc/controller_baseline`：`go=SC`、`clk=clk_dly`、`valid=DR`、`sample=sample2` |
| 控制 `I0/I56/I33 → I36` | 两个 `saradc/inv` 将 `clk` 经 `clk!` 传到 `clk_dly` |
| 控制 `I0/I56/I38` | `saradc/or2`：`sample=OR(DR,sample2)` |
| 控制 `I0/I56/I49 → I47` | `saradc/inv` 与 `saradc/and2`：`sample_clkb=AND(clk!,NOT(sample))`，忽略传播延迟的逻辑关系 |
| 比较器 `I0/I55` | `saradcII/comparator`：`clk=sample_clkb`、输入 `sump/sumn`、`outb=outp`；`outp` 回到控制器 `comp_out` |

`V1` 保存表达式按时间单位解释为周期 1 s、延迟 10 ns、脉宽 0.9 s，最终仍需核对新网表。不能把这个长脉冲直接当成 100 MHz 的采样时钟。

## 3. 从行为控制器解释 12 个周期

源文件位于 ADC 包相对路径 `DESIGNS/GPDK045/SARADC/oa/saradc/controller_baseline/veriloga/veriloga.va`，本次校验与原包一致。`controller_baseline` 只有 `symbol`、`veriloga`；控制器不是晶体管数字逻辑。当前 switch view list 支持选到它，但**尚未生成新网表确认实际绑定**。

源码第 46 行在 `go` 上升穿越阈值时设置 `convert=1`，没有对应的 `go` 下降沿清零。第 48 行在 `clk` 上升穿越阈值时推进状态机。因此，源码支持“上升沿启动后持续转换”的判断，比“高电平实时使能”更准确。

下表按稳定循环解释，忽略门延迟与 `transition()` 延迟。状态名取实际代码中的整数；不能把参数名 `sWait/sSample/sConv/sDone` 当成真实状态划分。

| 时钟边沿处理前的 state | 执行动作 | 到下一边沿的区间 |
| --- | --- | --- |
| `12` | 判最后一位、锁存 result；`data_ready=1`、`sampledata=1`、state 回到 `1` | 第一段采样，同时 `DR` 为高 |
| `1` | state 进入 `2`，`data_ready=0`，保持 `sampledata=1` | 第二段采样 |
| `2` | `sampledata=0`，置第一试探位 `test_0=1`，state 进入 `3` | 开始首位比较 |
| `3…11` | 依次采集比较结果、置下一试探位 | 后续逐位比较 |
| 再次 `12` | 采集第十次比较并锁存，重新开始采样 | 下一轮 |

**推导：** 12 个内部周期由 2 个采样区间和 10 个比较区间组成；结果锁存与第一段采样的起始边沿重叠。不是另外分配一个独立输出周期。按保存变量 `fclk=1.2 GHz`，采样高电平约 `1.667 ns`，相邻稳定采样起点约 `10 ns`。这些是代码推导，尚无实测值。

首轮还有 `state=0` 的启动分支，源码没有显式 `initial_step` 初始化流程；启动有效码、稳态开始时刻和模拟延迟不能只凭上述循环确定。

## 4. 最小实验与验收

1. 远程桌面已只读打开顶层和 `saradc/10Bit_ADC_logic/schematic`。先沿上表找到 `I22`、`I38`、`I47`，确认采样控制和比较器时钟的连接。
2. 后续在有恢复副本的 ADE 设置中建立新 nominal 网表，确认控制器及门的实际 view、模型 section、分析与保存信号。记录生成路径和配置身份。
3. 新 transient 保存顶层 `SC`、`CLK`、`data_ready`，以及控制器时钟、内部 `sample`、`sample_clkb`、逐位控制与输出码。信号名以新网表为准；本页 schematic 路径不能直接当作 Spectre 节点名。
4. 验收稳定循环：相邻采样事件约 10 ns，采样高电平覆盖约两个内部周期，每轮十次比较，`DR` 与结果锁存及新采样起点的关系符合源码。测量延迟后再决定 FFT 取码相位和启动舍弃区间。

当前只完成静态链路与代码审计。尚未运行，不能写“100 MS/s 时序通过”。下一项具体操作是准备这一个时序实验，第一课的幅度和动态指标审计随后继续。
