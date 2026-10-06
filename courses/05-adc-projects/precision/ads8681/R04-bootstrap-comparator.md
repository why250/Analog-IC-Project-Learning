# R04：BOOTSTRAP 升压驱动与比较器锁存

问题：这里的 BOOTSTRAP 是否就是模拟输入采样开关？先预测：只带 CLK、Z 和电源的模块，能否直接完成 VIN→VOUT 采样？[BOOTSTRAP 原图](../../../../notes/evidence/precision-adc/schematics/HIX_2012210_SUB__BOOTSTRAP.png) 是本课第一张图。

`HIX_2012210_SUB/BOOTSTRAP` 只有 CLK、Z、AVDD、AGND，无 VIN。已读取的父级：COMP_2/MI198 将 CLK 接 CLK、Z 接 `C8856_MINUS`；COMP_2S1/MI197 将 CLK 接 `X4134_Z`、Z 接 `C940_MINUS`。连接支持它是比较器内的时钟升压/驱动候选，不能当作前端信号采样管。

## 逐器件看两相

| 元件 | 实时端点 | 作用推导 |
| --- | --- | --- |
| C356 | PLUS=`C356_PLUS`，MINUS=`C356_MINUS` | 浮置储能电容 |
| P9053/N9054 | AVDD/AGND 到 C356_PLUS，G 分别为 NAND 输出/CLK 反相 | 一端由预充低电位转向供电 |
| P9006 | D=AVDD，S/B=C356_MINUS，G=Z | 给浮置一端预充/隔离的自控支路 |
| P9005 | D=Z，S/B=C356_MINUS，G=P9005_G，保存 m=4 | 储能节点到输出的连接 |
| P9007/N9008 | P9005_G 到 AVDD/Z；G=CLK/延迟后的 CLK | 切换 P9005 gate 的参考点 |
| N9009/N9010 | Z→N9009_S→AGND | 输出放电；串联控制避免与升压持续短接 |
| C357 | Z 对 AGND | 显式输出电容，另有父级负载 |

稳态 CLK 低时，反相链与 NAND 对 C356_PLUS 的控制支持拉低；P9007 支路将 P9005 gate 拉到供电，Z 放电。CLK 高时 C356_PLUS 上升，若另一端已存储电荷、隔离有效，会抬升 C356_MINUS，并通过 P9005 驱动 Z。理想“接近两倍供电”只是无损无负载上限思路，实际高度由充电、器件阈值/导通、寄生和负载决定。边沿延迟与非重叠尚未新测。

另一个 `BOOTSTRAP_1` 在 AMP_STAGE1/MI199 内，Z=`P9161_D`、VO=`C189_MINUS`。它有不同 body 接法和 VO/CLKON 接口，不能沿用上表；详见 [图集](../schematics.md#ads8681)。

## 比较与保持分开学习

COMP_BLOCK 中 AMP_STAGE1/2/3 驱动不同 COMP_2 变体。COMP_2S2 实際有四只 LATCH：MI171→Q、MI181→QN、MI172→QS、MI182→QNS，锁存时钟不同。输入经 C8815/C8816 耦合，另有 dummy C。Q 不改变可能是判决不足，也可能是观察到另一锁存相或旧值。

最小实验先是结构分相表。模型恢复后：独立升压 TB 看 CLK、C356 两端、P9005_G、Z 和逐管 Vgs/Vgd/Vds；负载扫参检验幅度/保持时间。比較 TB 固定 VCM，使用正负交替差分，同时保存原始判决节点与 Q/QS；测控制边沿到有效输出的延迟，明确阈值和窗口。

验收：解释为何这里的 BOOTSTRAP 不能直接称 VIN 采样开关，并以端点给出预充与抬升路径。所有电压幅度、器件工作区与延迟待仿真； `_H` 名称不证明耐压。接 [R05](R05-reference.md)。
