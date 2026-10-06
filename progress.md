# 续学入口

## 当前：SAR ADC 完整开发设计教程（2026-10-05）

- 用户问题：一般开发是否按 MATLAB/Python→Verilog-A→电路替换推进，要求完整教程。
- 交付：[16 课完整课文](courses/06-sar-development/README.md)、[Python 模型](scripts/sar_design_model.py)、[记录模板](notes/sar-development-template.md)、[本轮记录](notes/2026-10-05-sar-development.md)。主线为单核差分 SAR，Pipelined-SAR 扩展；MATLAB/Python 通常二选一，系统预算与模块 PDK 可行性并行迭代。
- 新证据：[离线计算](notes/evidence/2026-10-05-sar-design-model/summary.json) 与两张图，10 bit/20 MS/s/2 V 的教学预算与五组受控非理想模型；语法、黄金量化/静态指标、错误输入和防覆盖检查完成。**本轮无新增 EDA 仿真、OA 修改、版图或芯片测量。**
- 状态：课文编写完成，学员学习/预测验收与实际工艺设计仍进行中。没有因课文齐全而改动原工程的通过状态；原 SAR/PLL/AFE/精密 ADC 续学点保留。
- 下一项具体操作：先验收 03 的“为什么 CDAC 不能只按 kT/C 选”这一问题，用 23 fF/侧噪声下限与暂设 10.24 pF/侧阵列解释匹配、建立与参考约束；随后将实际 8 位工程的 Cu/源阻抗/采样窗/位窗填进预算，核对保存值与新测量来源，再接 A05 的实际 compare 适配。当前预测待学员回答，不记录已掌握。

## 行为系统建模与实际电路替换分支（2026-10-04）

- 最新课：[A05 建模与替换路线](courses/05-adc-projects/lessons/A05-model-to-circuit.md)，源码/运行：[模型入口](models/adc_behavioral/README.md)，记录：[本轮实验](notes/2026-10-04-adc-modeling.md)。
- 本轮新运行：8 位模块化 Verilog-A 的五样本输出码/八次判决检查、比较器故意慢导致 overrun、残差模型 gain/1% gain error/限幅，共四个 Spectre transient，0 errors/0 warnings；PSF 输出 bus 独立核对通过。是无 PDK 教学结果，不是原 DUT 晶体管性能。
- 真实接口：通过 adc_project_course 实时读取 11 个 schematic，source hash 前后相同。D_adjust2 含 c1 锁存、两段加法链和条件支路；位权/真值/对齐继续核对，不把 6+8−2 当验证。
- 待执行：新的 OA model/symbol/adapter、真实 compare 混合系统、完整 12 位行为流水线和数字等价审计、FFT/noise/PVT。其他课程状态保留。
- 下一项具体操作：先验收 B0 的八次 sample/compare/done/reset/EOC 时间线，接学员 gain-error 预测；然后按实际 compare 定义 reset/极性/VCM/负载适配，核对 SMIC 模型/CDF 后准备 B1 独立副本。12 位后续从实际 D_adjust2 的 SW2-1/adder 真值和 sample_id 开始。

最新精密 ADC 任务：[ADS8681 / ADS1248 的 12 课与 37 张原图](courses/05-adc-projects/precision/README.md) 已准备，没有新仿真；下面的 AFE/SAR/PLL 续学点保留。

## ADS8681 / ADS1248 精密 ADC 逆向分支

- 课程：[12 课](courses/05-adc-projects/precision/README.md)，原图：[37 张关键 schematic](courses/05-adc-projects/precision/schematics.md)，方法：[无 TB 实验路线](courses/05-adc-projects/precision/no-testbench.md)，记录：[本轮检查](notes/2026-10-04-precision-adc.md)。
- 状态：课文与图像准备完成；两套顶层和选定关键连接已只读核对，学员预测/理解与所有本项目仿真待验证。source hash 前后相同，37 张下载图 hash 已核对。
- 已确认结构：ADS8681 PGA→两侧 SWITCH_CAP_2→COMP_BLOCK，另有两个 SAR 子块；BOOTSTRAP 的 CLK→Z 接比较器内部，不能直接称为 VIN 采样开关。ADS1248 INPUT_MUX→双 AMP PGA→SC→AMP_8/9/9S1→COMP 的三对输入；SWITCH_CAP_X4 四份在信号端并联，enable 不同。
- 模型边界：仅在这两个工程目录未找到模型候选文件与 ADE/config view；DEV spectre 等接口 view 不证明 model card 可用。CDF/termOrder/参数密度/控制协议与实际环路阶数、数字滤波仍待确认。
- 当前课：[R04 升压驱动与比较器](courses/05-adc-projects/precision/ads8681/R04-bootstrap-comparator.md)。下一项具体操作：接学员对 CLK→Z 功能的预测，用 C356、P9005/P9006 与 N9054 的端点核对预充/抬升；先只验收结构，再审计模型和父级负载建立独立短 transient。ADS1248 随后从 D02 一侧反馈与 D03 一次电荷转移开始。
- 路径来自 config/local.env 的 ADC_PROJECTS_ROOT / COURSE_REMOTE_ROOT；独立 profile precision_adc_course，不混用 adc_course、afe_course 或 adc_project_course。证据与运行身份见本轮记录。未提交或 push。

## 其他分支的近期任务

- 最后更新：2026-10-04；本轮实际会话和新运行：2026-10-04
- 最新任务：扩展 AFE 完整信号链结构课程；新增六篇结构课、七张原图，实时只读补齐 FILTER→VOL_GEN_1→AMP_BLOCK→ADC 与 DAC_1 返回路径，无 AFE 新仿真；ADC/SAR/PLL 进度保留。

## adc_projects 新实战分支

- 课程：[四工程 ADC 实战](courses/05-adc-projects/README.md)；记录：[接管与建课](notes/2026-10-04-adc-projects.md)，证据：[项目与哈希](notes/evidence/2026-10-04-adc-projects.json)。
- 状态：进行中；已建立课程与 [14 张实际电路图](courses/05-adc-projects/schematics.md)，本轮 live 读取 14 个 cell，源 hash 前后相同；无新网表或仿真，学员学习待验证。接管时仅有旧导出的状态由本项新证据补充，不回写历史。
- 当前课：[A02a BOOSTRAP 具体结构](courses/05-adc-projects/lessons/A02a-bootstrap-structure.md)，记录：[原图与结构检查](notes/2026-10-04-adc-schematics.md)，证据：[live 连接/原图/hash](notes/evidence/2026-10-04-adc-schematics.json)。profile=adc_project_course，独立桌面会话与 ADC/AFE 分别核对。
- 下一项具体操作：先接学员对 track 阶段 Vgs 的预测，沿 NM11→PM5→PM6 的 net52/net57/net56 检验；只验收储能与 gate 抬升的结构解释。随后在 BOOSTRAP_test 独立副本核对模型、clock 脉宽和 2 pF 负载，短 transient 验证两相波形。路径来自 config/local.env 的 ADC_PROJECTS_ROOT / ADC_LEARNING_ROOT。
- 本分支保留以下 AFE、既有 SAR 与基础 PLL 的学习状态；现有 S04 正负交替最终输出实验仍待执行。

## AFE4404 新学习分支

- 当前课：[A01a TIA 输入、偏置与差分电流](courses/04-afe4404/lessons/A01a-tia-transistor-structure.md)
- 当前状态：进行中；课程与原图准备完成，助教完成静态连接检查；学员预测/理解与后续实验待验证。
- 课程：[AFE 九篇主课与六篇结构课](courses/04-afe4404/README.md)；最新入口：[完整信号链结构路线](courses/04-afe4404/signal-chain-guide.md)、[21 张原图](courses/04-afe4404/schematics.md)，记录：[完整链路建课](notes/2026-10-04-afe4404-signal-chain.md)。
- 工程事实：INP/INM 经输入 MOS 接 AMP_6；RC_CELL_2 内 RES_ADJ_3 与 CAP_SWITCH_5 并联返回输入，DAC_2 接输入，SWITCHED_RC_FILTER 接输出。TX 路径为 AMP_5 + SWITCH_BLOCK；DRIVER_1/2 为 I/O 驱动。输入开关的导通条件和晶体管工作点待查。
- 后续接口：FILTER 输出经 S_TRIGATE、VOL_GEN_1 接 AMP_BLOCK，再接 ADC_1；ADC 输出总线还接 DAC_1，返回 AMP_BLOCK.VI2，并接 COUNT_4B_1/MX21_15BX4。完整转换机制、相位和最终接口格式未证明。
- 证据：[来源身份](notes/evidence/2026-10-04-afe4404-discovery.json)、[原图清单与 hash](notes/evidence/2026-10-04-afe4404-schematics.json)、[实际连接及输入尺寸](notes/evidence/2026-10-04-afe4404-connectivity.json)；资料：[AFE 地图](docs/afe4404-map.md)。13 个完整 schematic 与 1 个局部图已导出，来源 hash 前后相同。
- 最新证据：[16 个 live schematic 与七张新增图](notes/evidence/2026-10-04-afe4404-signal-chain.json)。保存值包含输入供给/输出控制、net119 共模感知和差分存储电容；来源 hash 前后相同。P15751_G 驱动在已读邻接中未定位，不能自行补 bias。
- 待验证：CDF/netlisting/model section、完整 ADC 架构、独立 TB 与性能。实时 TOP/SUB/DEV/PDK readPath 已核对；五库未发现 maestro/config/adexl/veriloga view，配套 PDK 未找到 .scs/.lib/.sp，不能据此断言其他位置没有配置或模型。
- 下一项具体操作：接学员对输入驱动 NMOS 作用的预测，在 A01a 固定共模、写明 net73 与工作区假设，推导 P15738/P15737 电流方向；查 P15751_G 驱动和 NMOS 两端电压条件，只验收这一项结构判断。模型就绪后再建独立工作点/微扰实验。
- 路径来自 config/local.env 的 AFE4404_ROOT / AFE4404_WORKSPACE / AFE4404_PDK_ROOT。独立 bridge profile 为 afe_course，目标身份已核对；不能沿用 adc_course。

## SAR ADC 保留续学点

- 当前单元：01 Cadence verification / SAR ADC
- 当前课：[S04 动态比较器](courses/00-circuit-foundations/lessons/S04-comparator.md)
- 当前小任务：[reset/evaluate 与保持输出](courses/00-circuit-foundations/lessons/S04a-reset-evaluate-evidence.md)，四个固定小差分的 nominal 检查已新运行
- 当前状态：进行中；助教完成动态核 nominal reset/判决/方向检查，学员理解、统计与系统实验待验证
- 本课记录：[2026-10-04 比较器实验](notes/2026-10-04-comparator-delay.md)
- 本次证据：[测量 JSON](notes/evidence/2026-10-04-comparator-delay.json)、[新波形图](notes/evidence/2026-10-04-comparator-delay.png)
- 最新补课：[关键 TB 的作用与结果分析](courses/00-circuit-foundations/lessons/00-testbench-results-guide.md)，[补课记录](notes/2026-10-04-testbench-guide.md)；保存配置/只读结构核对，本项无新仿真，学习状态仍待反馈
- 课程准备：新增电路主线 9 课，SAR ADC 关键模块与基础整数 N PLL 优先；原验证 10 课作配套，见 [完整目录](COURSE.md)
- 2026-10-03 静态补查：[ADC/PLL 课程入口与资料身份](notes/evidence/2026-10-03-course-entries.json)，没有新 EDA 运行
- 上述入口检查之后已完成 [比较器新运行](notes/2026-10-03-comparator-nominal.md)，本轮 [模块与运行证据](notes/evidence/2026-10-03-circuit-modules.json)

## 已知工程事实（2026-10-01 会话证据）

- Windows 可通过 `ssh IC_Server` 免交互访问服务器；用户通过远程桌面查看 GUI。
- 教材为服务器 `/home/userone/AAAIC/tutorials/cadence_verification`。两份原包哈希一致，实际在 `originals/`；本次更正索引路径。ADC 包名与 README 版本差异仍保留。
- 工具为 Virtuoso `IC25.1-64b.38`、Spectre `25.1.0.054`。ADC/PLL 启动路径检查通过，新启动的 ADC 会话可只读读取 schematic。
- `maestro.sdb`、`active.state` 与原包不同，active test 变量一致；顶层 `sch.oa` 等抽查文件与原包一致，不能扩大为整个工作副本一致。
- 实际 DUT 为 `I0 → saradcII/10bit_adc_core_w_split_dac_ld1_msb`；控制链到 `I0/I56/I22 → saradc/controller_baseline/veriloga` 的源码已追踪，实际仿真绑定待新网表。
- 源码支持 `SC` 上升沿触发持续转换；稳态为两个采样区间、十个比较区间，结果锁存与下一轮采样起点重叠。这是静态推导，没有实测时序。
- 2026-10-01 通过 Windows SSH 使用服务器 bridge `168943c`、显式 profile `adc_course`；目标用户、主机、工作区和通道已核对。Windows bridge `a04d335` 的旧客户端直连未验证。2026-10-03 旧 ADC 会话已退出，已新启独立 ADC 会话并重新核对 bridge 与工作区。
- 启动前已备份 OA 与工作区入口。顶层和控制逻辑已只读打开；未保存设计、打开 Maestro、生成新网表或启动新仿真。

## SAR ADC 下一项具体操作

先用 TB 导读明确“比较器动态核判决时间”和“最终输出更新时间”的观察路径与差别；随后按下述正负交替输入实验补齐最终输出证据。CDAC 与自举 TB 的用途及基础 PLL 模块/环路实验已补全课文，尚未执行。

先接学员对本轮新波形的解释，验收动态核复位和外层 SR latch 保持的区别。下一实验在独立副本使用正负交替小差分，让新旧结果不同，测最终输出更新；reset 缩短与 memory effect 另立实验，保持共模和负载。系统 sample/DR 时序实验仍未执行，留作 S05/原第 02 课，随后返回 S02 的 CDAC 电荷与位权学习。

2026-10-04 实测摘要：tt、27°C、VDD=1.2 V、VCM=0.6 V、fclk=1.2 GHz，无新增负载/随机噪声；动态核从内部 clock 0.6 V 到原始差分 1.08 V 的延迟，±1 mV 约 190 ps、±100 µV 约 198 ps，四条件方向正确。内部 evaluate 约 446 ps，原始 reset 差分最大约 0.14 µV。未验收带 CDAC 负载的系统预算。

连接复现方法及 profile 注意事项见 [bridge](docs/bridge.md)。路径来自忽略的 `config/local.env`；服务器配置和启动脚本部署在 `COURSE_REMOTE_ROOT`，完整课程仓库目前在 Windows。

## 阻塞与待确认

- ADC schematic、offset nominal 与本轮四个固定小差分 transient 已完成。此前采样判断采用助教假设，本轮比较器预测仍待学员回答，不能记录为已理解或已学完。
- 比较器新网表与 tt 模型可运行，Spectre 0 errors；两次同一 CMI-2426 warning 的精度影响未评估。该成功不能外推全部 TB、ADC 系统或 PLL/AMS。
- 当前 core 的 analog_mux_8 读取未见 vin↔cap 采样实例，新系统网表审计待做。实际自举 cell 未接在已读采样路径，多处采样/clamp 是行为开关。
- PLL 实际模块层级、整数 N 可配置性、旧 AMS 工具兼容性均待验证。自举独立 TB 待建立。
- CIW 有 `dpt` 环境目录缺失 warning；本次读取成功，后续功能影响未判定。
- 当前 bridge 的 `windows` CLI 存在 profile 传递问题，已用 `list-windows` 和显式 Python profile 绕开；未改 bridge 源码。
- ADE Explorer 连续运行会复用/覆盖 ExplorerRun.0。四点已分别即时归档 netlist/PSF/导出，唯一身份用输入条件、point archive 与 hash；不能在循环末按同一 history 名重复读四点。
- 副本 sdb 变量曾被旧 active test state 覆盖，首轮已停止，随后显式 maeSetVar/save，并逐网表核对短时参数。源文件前后 hash 未变，停止/被覆盖的尝试未计入测量数据集。

## 每次会话结束时更新

2026-10-03 完成电路主线与首个比较器 nominal 工具链。2026-10-04 新建 `saradc/course_cmp_delay_20261004` 副本，完成四个固定小差分的 nominal reset/evaluate 检查，新增 S04 实验续篇、测量/绘图脚本与小型波形证据。原源文件 hash 校验未变；完整数据留服务器，其他实验未完成。

2026-10-04 随后定位服务器 AFE4404 反向工程，新增九课课文、资料地图和记录模板；再建立独立 afe_course 会话，只读核对接收/TX 路径与输入尺寸，导出 14 张原图及结构摘要。模型、工作点和 AFE 仿真尚未验证，学员学习待反馈。原 SAR 比较器学习与下一步保留。

把当前状态改为“进行中 / blocked / 已完成”之一，写明最后完成的具体步骤、证据路径、未解问题和下一项动作。课程文件准备、助教检查、学员学习完成与仿真通过分别记录。
