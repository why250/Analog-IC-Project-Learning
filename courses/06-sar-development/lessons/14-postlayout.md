# 14：PEX、后仿与寄生归因

问题：后仿 SNDR 下降 6 dB，是否应该先把 comparator 做快一倍？先预测：把采样窗变长和把每位 DAC 窗变长，这两个实验分别能排查什么？后仿的价值是找出前仿假设在哪里失效。

## 先核对提取身份

记录版图版本/hash、LVS 状态、提取器与 deck、RC corner、coupling 处理、器件模型、view 绑定与 testbench。RC corner 和 transistor corner 分别记录，采用 PDK 指定的有效组合；不能将一个自命名 fastRC 当成器件 fast。源码中的 `calibre` 视图名称只表示入口，实际内容和生成版本必须确认。

前后仿同条件比较，使用同 sample_id、输入/clock/source/reference/load、统计模式及测量脚本。确保外加模型中的 C/R 没有与 PEX 同一元件双计。例如前仿手加 top-plate 负载，提取后它可能已存在；若是外部 board/package capacitance 则仍应保留，并注明边界。

## 寄生如何进入预算

寄生不是统一的“速度下降”。到固定节点的 top-plate C 会改变分压/有效权重；split 中间节点 C 改变 bridge ratio；bottom-plate route R 与 reference output impedance 改变每位建立；clock/input 耦合产生随相位/码型变化的电荷；supply/return R/L 使 comparator 工作点和 decision latency 随数字活动变化。

先对 extracted CDAC 做单 bit/major-carry/共模实验，得到实际权重和 settling，再回填 Python 模型。若只加一个统一 τ 无法复现错误，改为每位/每相参数或使用电荷矩阵；不能通过拟合一个 FFT 值把错误机制隐藏掉。比较器提取实验保留真实输入源阻抗与负载，判断 reset、kickback、memory 是否改变。

## 从短实验到系统后仿

1. 短 DC/交替输入和逐位 trace：确认拓扑、code order、握手及功耗没有突变。
2. 提取模块对照：CDAC 权重/建立、sampling held error、comparator 延迟与 reset、reference droop。
3. 静态敏感点与 acquisition/DAC-window 对照：分离权重误差、采样建立和转换建立。
4. 同一有效码提取方法下的动态谱：观察谐波、spur/noise、输入频率依赖。
5. 覆盖确定的 PVT/RC/失配条件，回归功耗和端间电压；统计资源与模型适用性明确记录。

层次化替换可以将一个 block 的 extracted view 换回 schematic 进行归因，但耦合寄生跨层时须保证分界电容和连接一致；简单删掉 coupling 会改变物理问题。受控删除/缩放仅用于敏感性诊断，最终成绩使用完整批准提取模型。分块改善不能代替整系统的 coupling 检查。

## 结果分析与闭合

静态 INL 改变且低速仍存在，优先查有效位权/bridge/电压系数；低速恢复但高速下降，查 acquisition、reference 与 bit settling；正负交替比恒定输入差，查 held memory/reset；仅高 fin 恶化，查输入带宽/aperture 与时钟；共模或 supply sensitivity 上升，查输入对工作点、回流与耦合。每项都以波形和一项受控条件确认，不靠症状单独定案。

把提取出的 C、R、delay、reference transfer 与误差分布回填 03/04/05，重新评估预算。局部修路由不足时，可以调整 unit C、sampling window、switch sequence、reference 架构或分辨率/速率目标；这是开发迭代的正常路径。后仿没有闭合时不进入“流片就能看到”的验收。

验收：同条件前后仿表、一个主导寄生机制的证据、修订预算及完整后仿回归范围。原 8 位系统与 12 位流水线尚未运行新 PEX；这一章是待执行流程。接 [15 实测](15-silicon.md)。
