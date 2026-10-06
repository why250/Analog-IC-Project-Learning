# 2026-10-04：固定小差分的 reset/evaluate 与判决时间

状态：助教完成新 nominal 模块实验；学员预测与理解待反馈，S04 整课未完成。

## 问题—预测

用户要求继续，按照续学入口推进 S04。已询问输入差分从 ±1 mV 减小到 ±0.1 mV 时的判决时间变化。尚未收到独立预测；助教工作假设为更慢、输出方向不变。没有把“好的，请继续”记作电路预测或掌握。

## 电路与运行身份

- 已读 README、progress、当前 S04 和前次笔记，再检查工作树。已有未提交课文保持，未提交/push。
- 经 Windows SSH 使用服务器 bridge commit `168943ca917e592c492a0db1b70aca0544f311c0`，profile `adc_course`、65379。实时 status 确认 host/user/ADC `WORK/saradc`；沿用独立课程 Virtuoso。
- 当前工具实时身份为 Virtuoso IC25.1-64b、Spectre 25.1.0。使用本机文档核对复制、保存、变量设置及停止接口。
- 复制 `saradc/comparator_noise_TB_new/schematic`，经 `dbCopyCellView` 创建 `saradc/course_cmp_delay_20261004/schematic`。DUT 为 `I9 → saradcII/comparator`。未改源 TB 或比较器器件尺寸。
- 从 offset TB 的 tt transient 设置建立独立 maestro，重绑新 TB，移除旧输出表达式，设置 maxstep=2 ps。具体配置以本轮新网表为准。
- 修改前将 source TB、比较器、锁存核 OA 和源 maestro 设置备份到服务器 `pre-experiment-sources.tar.gz`；前后 hash 校验均相同。恢复工作是保留源文件并使用副本，不在原设计中回滚试验性修改。
- 服务器完整记录目录：`COURSE_REMOTE_ROOT/2026-10-04-comparator-delay`。路径来自 config/local.env。

## 实验条件与验收规则

新 transient 四个独立输入：+1 mV、−1 mV、+100 µV、−100 µV。实际输入用理想 balun，测得共模 0.6 V；VDD=1.2 V、tt、27°C；clock=1.2 GHz、源 rise/fall=10 ps；stop=10 ns、maxstep=2 ps、moderate、无 transient noise。没有新增输出负载，保留内部 buffer 与 SR latch。

本次只验收动态核 reset/evaluate：

1. 内部时钟 `/I9/I0/net11` 上升过 0.6 V 定义 evaluate 起点，同节点下降过 0.6 V 定义本地窗口终点。
2. `/I9/I0/sb − /I9/I0/rb` 按连接预期符号达到 1.08 V，并保持到窗口末端；未决或方向错误仍记失败，不能删除。
3. 最终 `/net8 − /net011` 在 evaluate 尾端与预期符号一致且幅度至少 1.08 V。
4. 先舍弃三次 evaluate，测后续五次；上升前 20 ps 的原始差分要求小于 1 mV。

外部正差分预期原始 sb>rb、最终 out>outb；该方向来自实际输入交换、再生支路和 NAND latch 接法，随后用正负实测对照。

## 结果—证据

| 输入差分 | 原始判决延迟，约 | 最终方向 | 约定检查 |
| --- | --- | --- | --- |
| +1 mV | 190 ps | out 高 | 通过 |
| −1 mV | 190 ps | outb 高 | 通过 |
| +100 µV | 198 ps | out 高 | 通过 |
| −100 µV | 198 ps | outb 高 | 通过 |

内部 evaluate 宽度约 446 ps，外部 clock 到动态核测量边沿约 63 ps；reset 差分最大约 0.14 µV。reset 采样时 sb/rb 约 1.205 V，存在轻微时钟过渡扰动；没有进行应力/可靠性验收。

四个保留运行各为 Spectre 0 errors、2 warnings、7 notices；同一 CMI-2426 报告两次，涉及 I9.I0.I10.NM3 的负 Pdiblc2，未改模型，精度影响未定量评估。

证据：[测量与 hash JSON](evidence/2026-10-04-comparator-delay.json)、[单周期小型 CSV](evidence/2026-10-04-comparator-cycle.csv)、[波形图](evidence/2026-10-04-comparator-delay.png)。JSON 保留每点实际新网表 hash、原始导出 hash、五次完整测量、源文件 hash 和校验结果；全文网表/PSF 留服务器。

### 运行过程中的配置修正

- 第一次准备的副本只修改了 maestro.sdb 变量，活跃 test state 仍带旧 fclk/TSTOP。实际新网表暴露 fclk=1 MHz、TSTOP 为旧 ramp 表达式；运行超时后显式停止。该尝试没有计作通过。
- 随后通过 `maeSetVar` 显式设置 test 的 VDD/fclk/TSTOP/vin，save 后 run，核对每个新网表确实为 fclk=1.2G、TSTOP=10n。
- ADE Explorer 对后续多次运行仍返回并覆盖 `ExplorerRun.0`。首次循环未逐点留 PSF，结果不作为测量数据集；重新执行四点，每次结束后、下一点运行前将完整 netlist/PSF 及导出归档到 `point_1m`、`point_neg_1m`、`point_100u`、`point_neg_100u`。
- 因此 history 名不能唯一标识这些点。唯一身份为新 TB、输入条件、point archive、网表与波形 hash。四点测量均来自各自归档，不是运行末尾同一 history 的重复读取。

## 设计判断与限制

输入减小十倍后，测得原始判决延迟增加约 8.5 ps，方向保持。两幅度不足以建立完整 delay-vs-input 曲线，也不能拟合稳定的 τreg。五次相同输入无随机噪声的重复周期不是五次统计试验。

固定输入下 SR latch 持有上一轮决定，最终 out/outb 不必每周期重新翻转；本轮测的是动态核重新建立决定，未测每次最终码改变的完整 clock-to-output 延迟。图和机制解释已补入 [S04 实验续篇](../courses/00-circuit-foundations/lessons/S04a-reset-evaluate-evidence.md)。

没有实测噪声、失配、有限输入 Rs 或 CDAC kickback；未加入系统真实负载、控制器采集与各位残差，所以仍不能验收 100 MS/s SAR 的系统时序。插值结果的小数位不意味着亚皮秒精度。

## 脚本检查与复现

新增 [测量脚本](../scripts/measure_comparator_delay.py)，在服务器 bridge venv 运行；新 [绘图脚本](../scripts/plot_comparator_delay.py) 用 matplotlib。两脚本语法、实际数据正常路径和缺输入错误路径已检查；原始数据检查与 EDA 成功分别记录。

在服务器 source 本机配置后，使用服务器 venv 对记录目录运行测量脚本；它从 points.json 定位每点 archive，并从源导出计算 crossing。绘图命令：

```text
python scripts/plot_comparator_delay.py notes/evidence/2026-10-04-comparator-delay.json notes/evidence/2026-10-04-comparator-cycle.csv notes/evidence/2026-10-04-comparator-delay.png
```

绘图环境需 matplotlib，本机安装在忽略的 `artifacts/local/plot-env`，未修改系统 Python。波形图只使用约一个 evaluate 周期的小片段。

## 下一项具体操作

接学员对本轮图的解释，先验收“动态核复位与 SR latch 保持”的区别。下一实验用正负交替差分，使每次新旧结果不同，保存同一组节点，测实际输出更新时刻。再另立 reset 缩短实验检验记忆效应；不在同一轮同时改变 clock、共模和负载。
