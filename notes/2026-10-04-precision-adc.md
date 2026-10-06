# 2026-10-04：ADS8681 / ADS1248 关键结构、课程与无 TB 路线

用户要求学习两套逆向项目的具体电路、查看关键 schematic、生成课程，并询问没有 TB 时如何学习。交付 [12 课完整课文](../courses/05-adc-projects/precision/README.md)、[37 张原图索引](../courses/05-adc-projects/precision/schematics.md)、[无 TB 方法](../courses/05-adc-projects/precision/no-testbench.md) 与 [记录模板](precision-adc-lab-template.md)。课程准备完成；学员学习和所有本项目新仿真待验证。

## 会话与来源

按仓库约定先读入口、进度、当前课与笔记并检查工作树，保留已有 ADC/AFE 改动。读本机/server bridge AGENTS、Virtuoso skill 与 API/导图文档；用 SSH IC_Server 在服务器 bridge .venv 执行。没有使用其他任务会话。

独立 profile=precision_adc_course、port=65387、PID=195992、IC25.1-64b cpgbld31。工作区在 COURSE_REMOTE_ROOT/2026-10-04-precision-adc/workspace；cds.lib 合并两个既有 workspace 的标准库与十二个 HIX 库映射，没有改原 workspace。启动器用 CDSHOME/tools/dfII/bin/virtuoso，DISPLAY/XAUTHORITY 来自 config/local.env，-nocdsinit 隔离旧启动。实时核对 TOP/SUB/DEV readPath，身份保存在 [清单](evidence/2026-10-04-precision-adc-schematics.json)。此启动不证明模型或 CDF 初始化可用于仿真。

原包身份沿用 [四项目来源证据](evidence/2026-10-04-adc-projects.json)，本轮 37 个 schematic 单独记录原始相对路径和 source/image SHA-256；源 sch.oa 导出前后哈希相同。geOpen 明确 r 模式，schematic.read 不过滤参数，hiExportImage entireDesign 黑白导出，不保存设计、不生成网表、不打开 ADE、不运行 Spectre。完整原始读取 JSON、脚本和日志留服务器同一 state 目录。

## 实际结构事实

- ADS8681 TOP_HIER 63 个实例，PGA 输出 R2086_PLUS/R7526_PLUS 分别入 SWITCH_CAP_2/2S1，再接 COMP_BLOCK；两个 SAR 子块接不同节点，Q 接口均可见 Q<5:0>，不能据此推完整位数合成。
- PGA 是 AMP_1、两只 AMP_2、四只 TRIGATE 和 bias/control。COMP_BLOCK 有 AMP_STAGE1/2/3 和五个比较子块。COMP_2S2 有四只 LATCH，Q/QN 与 QS/QNS 分别锁存，不能沿用其他 comparator 的时序。
- BOOTSTRAP 无模拟 VIN，仅 CLK、Z 与供电；C356 浮置储能、P9005/P9006 自控连接与预充支路。父级 COMP_2/MI198、COMP_2S1/MI197 的 Z 接内部电容网，见 [父级端子证据](evidence/2026-10-04-precision-adc-bootstrap-parents.json)。BOOTSTRAP_1 在 AMP_STAGE1/MI199 中，接口与 body 接法不同。
- ADS1248 TOP_HIER 74 个实例，INPUT_MUX→PGA→AMP_6X2/SC→AMP_8→AMP_9→AMP_9S1；COMP 接三组差分输入，Q=X0250_A 进入 CLK_CTRL。未证明实际环路阶数或完整数字滤波。
- SWITCH_CAP_X4 中四份 SWITCH_CAP 的 VI/VO/SW 同网，信号端并联，ENP 不同。PGA 有两只 AMP、开关电阻梯，部分同端点电阻；AMP_9 有从 N1336/N1337 gate 网到 VOM/VOP 的反馈电容候选路径。不寻常 D/S/body 接法须与模型端口核对。

## 模型与实验边界

[目录审计](evidence/2026-10-04-precision-adc-model-audit.json) 仅覆盖两个 reverse project 目录：未找到 .scs/.sp/.spi/.cir/.va/.vams/.mdl/.lib 候选；view 目录未见 maestro/config/adexl/veriloga。DEV spectre 等接口 view 的 master.tag 指 symbol.oa，尚未核对 CDF simInfo/model name/termOrder，也不排除外部模型。原图说明几何由照片测得；c/r 与 m/面积需要审计，不能当真实校准参数。

没有 TB 的路线：先真实连接/分相与反馈方程，再理想/归一化实验，最后在匹配模型可用时建学习副本的器件模块 TB。首批建议升压、SC 一步、比较判决/锁存、PGA feedback 与 reference 负载；不直接整芯片 FFT。未建立新的 OA TB，未运行晶体管或行为实验。

## 学员预测与下一项

已询问 ADS8681 的 CLK→Z BOOTSTRAP 是升压驱动还是直接模拟采样，答案待反馈。下一项只验收 C356 的预充与抬升路径；随后审计父级负载/控制和器件模型，准备一个短 transient。ADS1248 之后从 D02 一侧反馈和 D03 一次电荷转移进入。既有 GPDK SAR 正负交替最终输出、异步 SAR 自举、基础 PLL 和 AFE 分支的验收点保留。

## 交付检查

37 张下载 PNG 全部 SHA-256 与清单一致，总计约 14.08 MB；已目视检查 BOOTSTRAP、AMP_1、ADS1248 PGA 和 AMP_9，原图的留白和标签显示限制在图集说明，不重画连接。24 个相关 Markdown 的 274 个本地链接检查通过，三个证据 JSON 可解析，37 项 source/image 与会话身份检查通过，git diff --check 通过。为补齐父级来源证据，额外只读核对 COMP_2/COMP_2S1 的 source hash 前后相同，随后在该独立会话打开 BOOTSTRAP 供远程桌面查看。没有提交/push。
