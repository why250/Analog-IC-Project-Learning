# Analog IC Project Learning

面向熟练模拟 IC 工程师的 Virtuoso 实际工程研修课。以现有工程为教材，沿着 **设计意图 → 电路与模型 → testbench → 仿真证据 → 误差归因 → 设计判断** 学习。

第一站是 `cadence_verification` 中的 SAR ADC，随后扩展到 Fractional-N PLL。默认已掌握模拟电路、ADC/PLL 基础和 Virtuoso 常规操作；每课围绕一个工程问题，完成一份可以在另一台电脑上继续的实验记录。

## 从这里开始

1. 阅读 [课程路线](COURSE.md)，了解每个阶段的工程产出。
2. 按 [环境与同步](docs/environment.md) 配置本机路径。
3. 开始 [第 01 课：接管 SAR ADC 工程，建立验证地图](courses/01-cadence-verification/lessons/01-project-map.md)，约 60–90 分钟。
4. 在 [第一课记录](notes/01-project-map.md) 填写观察，在 [续学入口](progress.md) 留下下一步。

当前只展开第一课；其余课程保留路线，依据实际实验逐课构建。**课程已建立，学习和仿真尚未完成。**

## 仓库内容

| 入口 | 用途 |
| --- | --- |
| [COURSE.md](COURSE.md) | 课程目标、顺序和验收产出 |
| [courses/](courses/01-cadence-verification/lessons/01-project-map.md) | 课文、操作任务和复盘问题 |
| [notes/](notes/01-project-map.md) | 学习记录、证据索引和未解决问题 |
| [progress.md](progress.md) | 跨电脑、跨会话续学的单一入口 |
| [docs/sources.md](docs/sources.md) | 原始工程定位、版本差异和校验值 |
| [docs/bridge.md](docs/bridge.md) | 使用 virtuoso-bridge-lite 辅助学习 |
| [AGENTS.md](AGENTS.md) | 后续 LLM 继续授课和维护课程的约定 |

GitHub 同步课文、笔记、小型结果摘要和自编脚本。Cadence 原始资料、PDK、OA 库和完整仿真结果保留在各自 EDA 环境；用资料校验值、相对路径和实验记录关联。换电脑后可以接着读课和写笔记，实际运行仿真还需要本地或远程 EDA 环境。

给下一次对话的起手提示：

> 请阅读 AGENTS.md、progress.md 和当前课的笔记，按熟练模拟 IC 工程师的水平继续授课。先让我对当前工程问题作出判断，再通过工程证据检验。每次只推进一个可验收的小任务，结束时更新续学入口。
