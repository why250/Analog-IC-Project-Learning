# 本机环境与跨电脑同步

## 本机首次配置

在 EDA 主机的仓库根目录执行：

```bash
cp config/local.env.example config/local.env
# 编辑 config/local.env，指定本机资料目录和 IC 安装目录
bash scripts/launch.sh adc --check
bash scripts/launch.sh adc
```

如果已有 `config/local.env`，直接编辑，不要再次复制覆盖。脚本进入原工程的 `WORK/saradc`，设置该工程需要的 `PROJECT` 等变量。PLL 对应 `bash scripts/launch.sh pll --check` 和 `bash scripts/launch.sh pll`。

`--check` 仅验证工作目录、`cds.lib` 和 Virtuoso 可执行文件；不代表库解析、许可证、Spectre、模型或 ADE 配置已可用。许可证和仿真器 PATH 沿用本机正常 EDA 环境。脚本不执行原包的 `project.cshrc`，其中保留了原作者的软件和服务器路径。

启动后优先浏览和记录。保存 ADE 会话或修改电路前，在本机备份相关工作库，或使用 Virtuoso 的复制功能建立实验副本，并检查复制后的层级引用。记录相对于原工程的每项设置变更；原包归档用于回溯。

## 在另一台电脑继续

首次获取课程：

```bash
git clone https://github.com/why250/Analog-IC-Project-Learning.git
cd Analog-IC-Project-Learning
```

每次学习前，先检查本地修改，再同步：

```bash
git status
git pull --ff-only
```

若有未提交修改，先完成或妥善保存；若分支已分叉，检查双方变更后合并，不要用强推处理笔记冲突。

然后阅读 `progress.md` 和当前笔记。运行实验前配置本机 `config/local.env`：

- **本机装有 EDA**：准备相同原包，按 [资料索引](sources.md) 核验 SHA-256，并记录本机工具版本。
- **通过另一台 EDA 服务器运行**：资料与启动脚本在 EDA 主机侧配置，工作电脑使用 [bridge](bridge.md) 连接。Git 不会复制正在运行的 Virtuoso 会话。
- **暂时没有 EDA**：可以读课文、整理笔记、提出预测；把实验步骤保留为待验证。

原始资料和本地修改后的 OA 数据库不随课程 Git 仓库迁移。换 EDA 主机时还需通过自己的资料存储或服务器准备它们。自编脚本、小型配置变更说明和结果摘要随 Git 同步，保证能重建实验；课程不假定“相同原包”就意味着“相同工作副本”。

## 每次结束

1. 在 `notes/` 写下本次观察、实验条件、证据位置和疑问。大波形保留在 EDA 主机，笔记给出主机别名、路径和运行 ID；关键结论附小型表格或图。
2. 更新 `progress.md`：当前步骤、已确认事实、阻塞点、下一项具体操作。
3. 审阅并提交本次文件。例如只更新了第一课笔记和进度时：

   ```bash
   git diff
   git add notes/01-project-map.md progress.md
   git diff --cached
   git commit -m "notes: record lesson 01 observations"
   git push
   ```

在另一台电脑开始前，确保上一台已 push。两台电脑同时编辑时，建议分别追加带日期的记录，减少覆盖。
