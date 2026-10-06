# 2026-10-04：完整 AFE 信号链结构课程

状态：课程扩展与助教静态检查完成；学员预测/理解待反馈，AFE 工作点、网表和新仿真未运行。原 ADC 项目、自举课、SAR/PLL 记录保留，未提交或 push。

## 用户目标与预测

用户要求继续，并希望课程完整了解信号链上的关键电路。已先读 README、progress、A01、首批原图笔记，再检查工作树。通过异步输入提出当前读图预测：P15737/P15738 的漏端相连 NMOS 也由 VP/VM 驱动，它们主要起什么作用，差分变化时各支路电流如何变化？记录时尚未收到回答。

本轮补齐课文并作独立只读检查；没有将助教推导记为学员理解。当前只准备验收 A01a 一个支路问题，其余课文供后续逐次推进。

## 实际检查

读取本机 config/local.env 的 COURSE_REMOTE_ROOT、AFE4404_ROOT、AFE4404_WORKSPACE、VIRTUOSO_BRIDGE_ROOT。SSH 沙箱最初无法使用 IC_Server 别名，经自动审批后连接既有服务器；未修改 SSH 配置或凭据。初次本机解析漏掉 export 前缀，返回空路径的只读 ls/cat 失败，随后修正解析；这些失败不计入工程证据。

复核 bridge AGENTS、schematic API 签名和源码接口；doc_info 确认 IC25.1，安装文档核对 getWorkingDir、geOpen、hiExportImage。显式使用原有 afe_course profile/env，实时 getWorkingDir 返回 AFE4404_WORKSPACE，未切换或重启 ADC/其他会话。

通过 schematic.read 新读取 16 个 schematic：TOP_HIER、AMP_6、SWITCHED_RC_FILTER、VOL_GEN_1、AMP_BLOCK、AMP_1、AMP_2、AMP_3、DAC_1、ADC_1、COUNT_4B_1、CTRL_3、DAC_CELL_2、DAC_CELL_1、ADC_CELL_1、CAP_SWITCH_5。读取前后各来源 sch.oa SHA-256 相同，7 张新增图导出后再次确认对应来源 hash 相同。geOpen 使用 r 模式，未保存设计、打开 ADE、生成网表或运行仿真。

本轮完整读取 JSON 留服务器 COURSE_REMOTE_ROOT/2026-10-04-afe-signal-chain；连接小型摘要为 [signal-chain.json](evidence/2026-10-04-afe4404-signal-chain.json)。该摘要包含各 cell 的来源 hash、实例统计、选定端口连接、输入/偏置/共模邻接、存储电容保存字段及新增图片 hash。

## 关键发现与课程补齐

1. 接收链在 FILTER 后，经 MI312/MI313、MI199/MI188 的 VOL_GEN_1，进入 AMP_BLOCK 的 VI1，再从 VO1 接 ADC_1.VI1。不能省略接口放大和内部电荷路径。
2. ADC_1.Z 与 DAC_1.A 共用 net832<0:14>；DAC_1 的 VO1/VO2 接 AMP_BLOCK.VI2。已确认静态返回链，转换机制、反馈方向与更新算法仍待事件表证明。
3. AMP_BLOCK 内为 AMP_3、两只 AMP_2、AMP_1 和开关 RC/电容网络；MI83/AMP_1 输出直接接 VO1，输入同时接 VI2 返回路径。不能仅把它当作单一 buffer。
4. FILTER 四只存储电容分别跨 net52/net44、net54/net46、net56/net48、net58/net50；c=4.21707483p、m=6 属于保存字段，未核对 CDF/netlist 前不认定总电容。
5. AMP_6.net73 经 P15753/P15751 接供电；net79/net78 进入后续支路，net89/net87 驱动输出下拉。N15838/N15836 两端实际工作区未定，不能只根据输入 gate 猜功能。
6. AMP_6 的输出经两只 R 和两只 C 接 net119，P15669.G 接 net119；共模感知结构已确认，完整环路方向与稳定性未验证。
7. P15751_G 在已读实例邻接中仅找到 P15751 gate，没有明确驱动；需要继续查实际 net/pin/inherited connection 与原图，不能擅自补 bias。
8. 更正首批 schematics.md 中 N15955/N15954 的 master：实际读取为 gf018hv_green/nmos_3p3。原连接摘要本身已记录正确；本轮修正课文表格，不回写旧证据。

新课文：[完整链路路线](../courses/04-afe4404/signal-chain-guide.md)、[A01a 输入结构](../courses/04-afe4404/lessons/A01a-tia-transistor-structure.md)、[A01b 共模与反馈](../courses/04-afe4404/lessons/A01b-feedback-common-mode.md)、[A02a 电流 DAC](../courses/04-afe4404/lessons/A02a-current-dac-structure.md)、[A03a 滤波与后级](../courses/04-afe4404/lessons/A03a-filter-buffer-structure.md)、[A04a ADC 返回与读出](../courses/04-afe4404/lessons/A04a-adc-feedback-readout.md)、[A05a TX/配套](../courses/04-afe4404/lessons/A05a-tx-support-structure.md)。九篇原主课保留作理论与实验配套。

## 原图与验证范围

新增 VOL_GEN_1、AMP_BLOCK、AMP_1、AMP_2、AMP_3、DAC_1、COUNT_4B_1 七张原图，原生 hiExportImage entireDesign、6400 px 宽、黑线白底、隐藏 grid/axes；没有重新绘制或改连接。下载后原图与 [图册](../courses/04-afe4404/schematic-gallery.html) 合计 21 张。AMP_BLOCK 原图已视觉查看，需放大读标签；精确数值使用结构化摘要。

本地检查通过：24 个 Markdown 文件的 277 个相对链接、HTML 脚本语法、21 个图册资源与全部下载图像 SHA-256，16 个 live cell 的 source hash 前后相同；重读来源与首批导出 hash 一致。git diff --check 无空白错误。图册浏览器交互仍未验证，沿用此前 file 协议限制的记录；没有用其他协议或浏览器绕过。所有检查属于资料与结构验证，不是 EDA 仿真通过。

## 下一项具体操作

接学员对输入 NMOS 的预测，先在 A01a 固定共模、假设 net73 小信号稳定，对 P15738/P15737 推导电流方向，再检查相连 NMOS 的电压条件；只验收这一项。继续只读查 P15751_G 的驱动、enable 状态和 NIB 路径。随后才能在可恢复副本审计模型、取工作点并作微扰；完整 ADC/接口时序与系统仿真留后续课，不能因路线课文齐全而认定工程已跑通。
