# 2026-10-04：ADC 关键电路的实际结构与原图

用户要求学习具体电路结构并查看电路图。本轮完成 14 个真实 schematic 的实时只读读取和原生 PNG 导出，新增 [原图入口](../courses/05-adc-projects/schematics.md) 与 [BOOSTRAP 逐器件读图](../courses/05-adc-projects/lessons/A02a-bootstrap-structure.md)。没有新网表或仿真，学员理解待反馈。

## 问题与预测

已询问自举 track 阶段希望近似恒定的是 Vgs、gate 对地电压还是输出输入之差。截至本记录没有学员独立答案。图片交付与只读检查继续进行，没有将助教解释记作学员已掌握。

## 会话身份与只读边界

先读仓库入口/进度/当前课/笔记并检查工作树，再读本机与服务器 bridge AGENTS、Virtuoso skill、API 源码及 IC251 hiExportImage/hiResizeWindow 文档。API 使用服务器版本 168943c；geOpen 明确 r 模式，schematic.read 只读，图像导出用 hiExportImage 的 entireDesign、biColor、隐藏 grid/axes。没有保存原理图、打开 ADE 或改变任何设计连接。

旧 ADC learning 的 65342 无活动 listener，未将旧记录当作当前会话。新建 profile adc_project_course，port=65385，PID=188233，cwd=ADC_LEARNING_ROOT，DISPLAY=:1，版本 IC25.1-64b cpgbld31。实时核对 8_bit_sar_adc、Pipe_SAR、smic18mmrf v1.11_4 和 tsmcN65 的 readPath。env/log/startup/完整 JSON 留 COURSE_REMOTE_ROOT/2026-10-04-adc-schematics。

首次直接调用 64bit executable 因共享库路径失败，在任何设计读取前结束；改用 tools/dfII/bin/virtuoso 包装启动器后成功。导出脚本的初始字符串语法错误在执行前修正，编译检查后导出成功。PID 以服务器 /proc 与独立日志启动参数确认，未以不可用的 getpid 调用作身份依据。-nocdsinit 用于隔离已有启动配置，不证明 PDK callbacks 或仿真初始化齐全。已有 adc_course、afe_course 和其他用户工作会话保留。

## 新结构证据

- BOOSTRAP 共 14 个 MOS：NM11 的 D/S/G/B=VOUT/VIN/net52/VSS，是主采样管；PM6 的 G=net57、D/S/B=net56，是 MOS 电容接法，保存 m=20。没有独立 MIM 电容实例。预充电、track 与隔离支路由真实端子连接推导，节点电压仍待新波形。
- compare 共 26 个 MOS：NM15/NM16 输入对、NM17 时钟尾管、PM6/PM7 输入节点预充电、上侧 P/N 再生、三级 buffer。其输出结构不同于 GPDK045 comparator 的外层 SR latch；不能跨工程套用保持行为。
- SAR_ADC 中两只 BOOSTRAP、两组 DAC_SW、compare、SAR_LOGIC、EN_LOOP、8 个 DFF 与直接电容阵列均实时核对。SAR_LOGIC 实际含 8 个 SAR_LOGIC_UNIT；7 是受控电容权重组数，不是逻辑单元数。
- Pipe_SAR 的 Pi-SAR_amp、amp_gainboost、ampGA、ampGB、comparator4in2 已实时读取；仅结构与保存参数，未验收残差增益或稳定性。

## 交付与验证

[图像/连接清单](evidence/2026-10-04-adc-schematics.json) 记录 14 个 source/image 的 SHA-256、source 相对路径、尺寸、实例端子与保存参数。PNG 在 notes/evidence/adc-projects/schematics；全部源 sch.oa 导出前后哈希相同，下载的 14 张图片哈希均与清单一致。已目视检查 BOOSTRAP、compare、SAR_ADC、amp_gainboost 的可读性；部分标签重叠为原图属性，不改图修饰连接。11 个相关 Markdown 的链接检查通过，git diff --check 通过。完整未过滤 CDF 参数/位置 JSON 和日志留服务器。

下一项只验收 NM11 gate 怎样经 PM5 与 PM6 形成自举驱动；随后以独立 BOOSTRAP_test 副本检验 net52/net57/net56 与 Vgs 两相波形。原 S04、基础 PLL 与 AFE 分支的下一项保留。
