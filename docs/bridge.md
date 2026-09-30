# 用 virtuoso-bridge-lite 辅助学习

Bridge 用来让 LLM 获取实际工程证据、读取会话状态，并在后续实验中辅助操作 Virtuoso。第一课可以完全通过 GUI 完成；不依赖 bridge 已连通。

本页依据 [资料索引](sources.md) 中记录的本地版本。工具本身的安装与连接方法以所用 checkout 的 `AGENTS.md` 和 `README.md` 为准。当前机器源码在 `/home/userone/virtuoso-bridge-lite`，其他机器在 `config/local.env` 中记录各自位置。

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
