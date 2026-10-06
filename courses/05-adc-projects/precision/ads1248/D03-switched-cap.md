# D03：四份 SWITCH_CAP 与一次电荷转移

问题：`SWITCH_CAP_X4` 的 X4 是四级积分器吗？先预测串联、并联或按 enable 选择。[SWITCH_CAP_X4 与 SWITCH_CAP 原图](../schematics.md#ads1248) 配合端子表检验。

MI96…MI99 的四只 SWITCH_CAP 的 VI1…VI5、VO1/2、SW1…SW6、GS 均接同名网。它们在这一级的信号端口并联；ENP 分别为 ENP1、ENP1、ENP2 和内部 pullup 输出。不能把 X4 画成四级级联，也不能说运行时一定四份同时生效。

顶层 VI1/2 接 AMP_6X2 输出 `C604_MINUS`/`C606_MINUS`，VI3/4 接 PGA 输出 `N657_G`/`N3876_G`，VI5=`C569_PLUS`；VO1/2 接 AMP_8 的 VP/VM。SWITCH_CAP_1 与它共享 VO1/2，另接 reference、AMP_6S1_X2 的输出。分离子模块时必须考虑同一接收节点上的另一组贡献。

单份 SWITCH_CAP 有两侧对称 POLYCAP 与传输门。例 C3921 的 PLUS=`C3921_PLUS`、MINUS=`C3917_MINUS`，C3969 的 PLUS=`C3969_PLUS`、MINUS=`C3965_MINUS`，两只保存 c=778.4p、m=2；还有 139p/140p/24p 组。字段比例是查找线索，绝对密度及 m 意义待审计。

## 先做端点表，再写公式

1. 对一个 capacitor group，沿 transmission gate 的 A/Z 找每相端点连到哪个 VI 或 VO。
2. 从实际门级实现确认 SW 的导通极性；不能把 SW 与 SWN 同时置高当作一个抽象理想相。
3. 列 φa、dead time、φb、reset 时每个端点状态，标浮置节点与初始电荷。
4. 对每个浮置节点写 `ΣCi(Vnode−Vi)=Q`，再加入接收端反馈 C；差分两侧分别推导。

在明确的理想 sampled-charge 情况下，`Δvod=s·(Cs/Cf)·Δvid`；s 取决于端点翻转与反馈极性。本项目是否满足该简化式由上面的表证明，不能倒过来从公式补连线。多组电容和并联 block 有效时对 charge 求和，避免把单份系数乘四后忽略 enable。

最小实验先用理想开关证明一次 transfer 的符号与比例：各控制、输入/reference、接收虚地/有限阻抗和初态明确。再加入有限相长/Ron、寄生 C 和开关注入；一次只改变一项，比较 end-of-phase error。最终恢复真实单元时保留相邻并联路径或明确将其关闭的证据。

结果分析：长相位改善的误差是建立候选；长相位仍有误差查比例/寄生/漏电；切相瞬时跳变与采样结束误差分开记录。noise 与 injection 不因波形都呈小跳变就同类。

验收：证明四份在本层信号端并联，一只电容的两相端点表，以及一式有符号的电荷更新。接 [D04](D04-modulator.md)。
