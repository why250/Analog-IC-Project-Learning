# 用 virtuoso-bridge-lite 辅助学习

AFE 新入口（2026-10-04）：独立 profile `afe_course`，port `65383`，本机 env 位于 `COURSE_REMOTE_ROOT/2026-10-04-afe-schematics/bridge.env`。实时身份已核对为 xunipc/userone、AFE4404_WORKSPACE，使用 -nocdsinit 新启动只读查看会话，避免用户默认旧 bridge 自动加载。当前只读取/导出原理图，没有 AFE 仿真；不能从此启动条件推断 PDK callbacks 与仿真初始化齐全。详情见 [查看记录](../notes/2026-10-04-afe4404-schematics.md)，adc_course 保留用于原 ADC 会话。

Bridge 用来让 LLM 获取实际工程证据、读取会话状态，并在后续实验中辅助操作 Virtuoso。第一课可以完全通过 GUI 完成；不依赖 bridge 已连通。

本页依据 [资料索引](sources.md) 中记录的版本。工具本身的安装与连接方法以所用 checkout 的 `AGENTS.md` 和 `README.md` 为准。路径以各机 `config/local.env` 为准；2026-10-01 已核对服务器 checkout 为 `/home/userone/AAAIC/virtuoso-bridge-lite`。

## 连接并确认对象

在已安装 bridge 的虚拟环境中，按该项目文档配置本地或远程 profile。本地模式使用 `VB_REMOTE_HOST=localhost`；远程模式配置目标 EDA 主机。连接配置留在本机。

```bash
virtuoso-bridge profile show
virtuoso-bridge start
# 在目标工程的 CIW 中执行 start 实际打印的 load(...) 行
virtuoso-bridge status
virtuoso-bridge windows
virtuoso-bridge snapshot
```

先核对 profile、目标主机和窗口对应的库/cell/view，再读取目标。多会话时不能用“当前焦点应该是它”作为依据。`status` 成功也不证明本课 testbench 能跑通；snapshot 信息不足时继续从 GUI 或经文档验证的读取接口获取证据。

## 第一课给 LLM 的任务

> 请先阅读本课程 AGENTS.md、progress.md 和第一课。核实 bridge 的目标会话是本课 SAR ADC 工作区，读取 `saradc/10Bit_ADC_TB_new` 的层级和 Maestro 配置。列出 DUT、实际选用的模型视图、采样/转换时钟关系、分析和模型 section，并给出证据来源。读不到的项标为待验证。先让我预测，再解释观察；本次只做工程检查，不启动仿真或保存设计。

不要假设 bridge 有某个 Python 方法或 SKILL API。新增自动化前查看当前版本源码、相关 skill 和本机 Cadence 文档；bridge 文档列出的查询入口包括：

```bash
virtuoso-bridge doc-info
virtuoso-bridge skill-find dbOpenCellViewByType
virtuoso-bridge skill-info dbOpenCellViewByType
```

日后生成脚本时注明版本、输入、目标 cellview、输出路径和验证方式。执行结果与自己的推断分开写入笔记，便于下一台机器继续。

## Windows → IC_Server：本次已验证的入口

Windows checkout 已有 `.env`，目标为 `IC_Server`；没有重建或覆盖它。Windows 与服务器 checkout 版本不同，服务器版本增加了认证协议，本次没有用旧客户端连接新 daemon，也没有修改两份源码。当前方式为 **Windows OpenSSH → 服务器 bridge 虚拟环境 → 同机 Virtuoso**。

服务器上单独建立课程 profile `adc_course`，端口 `65379`。配置文件仅在服务器本机：`/home/userone/.local/state/analog-ic-project-learning/2026-10-01-environment/bridge.env`。脚本必须显式选此 env 和 profile；没有给虚拟环境绑定默认 profile。

在服务器 Bash 中先 source 本机 `config/local.env`。本轮部署位置为 `/home/userone/.local/state/analog-ic-project-learning/config/local.env`，然后执行：

```bash
run_root="$COURSE_REMOTE_ROOT/2026-10-01-environment"
cd "$VIRTUOSO_BRIDGE_ROOT"
.venv/bin/virtuoso-bridge status --env "$run_root/bridge.env" -p adc_course
.venv/bin/virtuoso-bridge list-windows --env "$run_root/bridge.env" -p adc_course --top-level --json
```

`status` 已确认 daemon user `userone`、CIW host `xunipc`，workdir 为 ADC 的 `WORK/saradc`，`1+2` 返回 `3`。当前顶层 schematic 已以 `r` 模式打开。没有打开 Maestro、保存设计或生成新网表。

此 checkout 的 `windows -p adc_course` 内部未将 profile 传给 `VirtuosoClient.from_env()`，在只有带后缀配置时失败。本次用 `list-windows` 核对 CIW，Python 查询显式使用 `VirtuosoClient.from_env(profile="adc_course")`。不要把这个 CLI 问题当成服务器连接失败。

后续若采用 Windows 端 Python bridge，应先在独立虚拟环境中对齐客户端和 daemon 的协议版本，再核验主机、用户、工作区和目标窗口。本轮尚未验证 Windows 旧客户端的直连链路。

## 2026-10-03：实际 TB 仿真链路

本轮发现旧 ADC 会话已退出，65379 不响应；status 的持久 banner 不是当前活跃会话。新启动独立 ADC Virtuoso，使用 `list-windows --top-level --json` 的 explicit CIW，再执行 `bootstrap --window WINDOW_ID --env ... -p adc_course`。重新核对实时 workdir、host、user 后读取模块。

已通过服务器版本的 Python API 跑通一个新比较器 nominal transient。操作顺序为：创建独立 ADE 副本→`maestro.open_gui_session`→核对 snapshot→`save_setup`→`run_and_wait`→按返回 history `read_results`→检查新网表与 Spectre/ADE 日志→按同一 history 导出波形。具体 API 以 checkout 源码及 IC251 本机文档为准。

`open_gui_session` 有清理其他 ADE session 的行为，只能在已核对的独立课程 Virtuoso 中使用。`run_and_wait` 的 done 仅表示回调完成，仍要读仿真器错误、输出状态和测量定义。本轮 nominal 日志为 0 simulation errors，但 bridge 的 yield 字符串存在不一致，未以其作统计验收。原 maestro 未保存修改，新副本名为 `saradc/course_cmp_offset_20261003/maestro`。

见 [实验记录](../notes/2026-10-03-comparator-nominal.md)。这个结果证明实际 TB 可通过 SSH/bridge 运行；不证明所有分析或 PLL 的旧 AMS 状态兼容，也不证明自举开关或 ADC 系统性能。

2026-10-04 的 [固定小差分实验](../notes/2026-10-04-comparator-delay.md) 补充两项实际注意事项：副本的 sdb 变量可能被旧 active test state 覆盖，须显式设置并核对新网表；ADE Explorer 可能重复返回并覆盖 `ExplorerRun.0`，须在下一点运行前逐点归档 netlist/PSF 和导出，结合 point archive、条件和 hash 定位。仅有 history 名仍可能不足以区分点。
