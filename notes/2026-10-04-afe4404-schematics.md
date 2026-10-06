# 2026-10-04：AFE 关键电路原图与实际连接

状态：助教完成独立会话只读结构核对与 14 张图像导出；学员预测/理解待反馈，无 AFE 新网表或仿真。

## 问题与预测

用户要求学习关键电路的具体结构并查看电路图。已读 README/progress/A00/当前笔记，再检查工作树；新增的 ADC 项目课及 TB 导读等其他改动保留，未提交/push。

先提出 TIA 反馈是连续时间 R∥C、SC 还是组合的预测问题。截至本记录尚未收到学员预测。读取和图片交付继续进行，但没有将其写成学员已掌握。

## 会话与操作

服务器 bridge 版本 `168943ca917e592c492a0db1b70aca0544f311c0`。先读其 AGENTS、Virtuoso skill 和相关 Python 源码；IC251 本机文档核对 geOpen、hiExportImage、hiResizeWindow、hiZoomIn、hiWindowSaveImage、ddGetObj 等。实际只用 geOpen 的 r 模式与只读 schematic.read，以及原生 CAD 导出和缩放。

在 AFE4404_WORKSPACE 新启动课程会话。第一次启动受用户默认 .cdsinit 影响，自动加载旧协议 bridge 65377；bootstrap 不会替换已运行 daemon，鉴权也未通过，因此未通过它读取任何设计。核对 PID/cwd/专属日志后仅终止本次新启动的 AFE 进程，再以 -nocdsinit 重启。现有 ADC 和其他工程会话保留。

当前成功身份：profile=afe_course，port=65383，user=userone，host=xunipc，workdir=AFE4404_WORKSPACE，Virtuoso IC25.1-64b，PID=183741，目标 CIW=0x3800010，桌面=:1。本机 env 在 COURSE_REMOTE_ROOT/2026-10-04-afe-schematics/bridge.env；不含 Git 同步凭据。实时 readPath 核对 TOP/SUB/DEV 与 gf018hv_green。

原始 schematic 未保存修改，未打开 ADE、生成新网表或运行仿真。-nocdsinit 是此只读会话的启动条件，不能据此认定 PDK callbacks 与仿真初始化齐全。

## 发现与更正

- 实际接收链：INP → N15955.D/S → net707 → MI499/AMP_6.VP；INM → N15954.D/S → net708 → AMP_6.VM。NMOS 导通状态仍待 gate 条件。
- 输出 VOP/VOM=net713/net714。MI336/MI337 的 RC_CELL_2 形成返回对侧输入的反馈；其内部 RES_ADJ_3 与 CAP_SWITCH_5 并联。
- MI495/DAC_2 的 VO1/VO2 与上述 TIA 输入同节点；15 个 DAC_CELL_2，实际极性与码步未测。
- MI311/SWITCHED_RC_FILTER 的 VIN1/VIN2 接 TIA 输出，静态接收路径已经确认。
- AMP_6 中 P15737/P15738 为一组共源 PMOS 输入对，另有较小 PMOS 输入对及输入驱动 NMOS。尺寸只代表保存值，工作点与噪声贡献未测。
- TOP_HIER 有 226 个实例和 363 个端口，许多是内部节点暴露，不能当成封装 pin 列表或完整产品仿真接口。
- 之前按名字列 DRIVER_1/2 为 LED 候选需要更正：实际顶层这些 cell 接 ADC_RDY/PAD7/CLK 的 I/O。TX1–TX3 接 MI341/SWITCH_BLOCK，与 MI152/AMP_5 经 net770/net830 相连。
- ADC_1 含 17 个 ADC_CELL_1 和 15 个 output buffer，Z<14:0>；完整架构、最终码格式与产品 22/24-bit 表示的对应仍未证明。

## 交付与验证

[原图与读图说明](../courses/04-afe4404/schematics.md)、[本地图册](../courses/04-afe4404/schematic-gallery.html)。13 张完整原图加 AMP_6 输入局部图，使用 hiExportImage，白底黑线、隐藏 grid/axes；完整图保留全部来源实例，包括 UNUSED。原生局部导出不是补画或改变连接。

[图像清单](evidence/2026-10-04-afe4404-schematics.json) 保存 export window、source path/hash、image hash、尺寸字节数和 cell 统计；[连接摘要](evidence/2026-10-04-afe4404-connectivity.json) 保存关键 terminal/net、输入器件尺寸和实时库路径。完整 OA 查询 JSON、CIW 日志和 env 留服务器 COURSE_REMOTE_ROOT/2026-10-04-afe-schematics。

导出前后 source hash 相同，且这些文件与本轮此前 discovery 的 hash 相同；下载 PNG hash 与服务器 manifest 一致。部分原图标签重叠是来源图属性，解释以结构化读取为准。

沙箱内 scp 无法读取 SSH 配置，经自动审批允许后仅下载本次图片/摘要，没有改连接配置。图册内置浏览器检查被 file 协议安全限制拒绝，未改协议或用其他浏览器绕过；改用原图文件查看。HTML 资源存在性、脚本语法作本地检查，浏览器交互未验证。

## 下一项具体操作

先接学员对反馈类型的预测及解释，随后只分析 AMP_6 的 P15737/P15738 与相连 NMOS：由连接与 bias 追踪差分电流如何到输出。不要同时展开整颗 ADC 或所有噪声实验。模型、工作点和新仿真均待后续独立副本。
