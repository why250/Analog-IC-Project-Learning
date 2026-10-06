# R03：从电容端点得到 CDAC 与采样机制

问题：看到几十只 METALCAP_M2 是否就能读出 ADC 位权？先预测：接电源去耦、接同一网的 dummy 与真正切换电容，在分析中是否都应进入分母 Ctotal？打开 [SWITCH_CAP_2、SWITCH_15B、SAR_ADC 原图](../schematics.md#ads8681)。

SWITCH_CAP_2 有 21 个 METALCAP_M2，另含电阻、六种 SWITCH_15B 子块、MUX2_1/2 和 SWITCH_CAP_1。SWITCH_15B 的 VI 与十五个 VO 支路经 D_TRIGATE 变体连接；控制为 OE/OEN，GS/VS 为内部轨。先追 switch 的 A/Z、供电/井轨，再沿电容到比较输入；不能由“15B”认定完整十五位 CDAC。

SAR_ADC 可见 84 个 METALCAP_M2、MUX2_4/5/6、COMP_1、SAR_REG 与控制；SAR_ADC_1 则是 74 个 METALCAP_M2、更多 MUX、COMP_1S1、SAR_REG_1 和直接 MOS。电容数量不等于位数，有分组、dummy、桥接及去耦可能。两者接口的 `Q<5:0>` 仅说明可见输出宽度。

结构实验：建立 `实例→PLUS/MINUS→控制相→角色` 表。从一个比较输入节点找所有 incident C，分固定端、切换端、桥接端和无效同网端。未确认 CDF 时，保存 c、w/l、m 分列；不要重复乘 m。原图有照片测得的尺寸，绝对 c 和工艺寄生尚未校准。

对一个浮置节点，理想电荷守恒写成 `Σ Ci(Vx−Vi)=Q0`；切换时若参与集合不变，`ΔVx=Σ CiΔVi/Σ Ci`。若存在桥接电容或多个浮置节点，建立联立电容矩阵，不能套单节点分母。差分两侧分别写方程，最后取差与共模，符号由端点决定。

最小 TB：先用理想开关与归一化电容，固定输入和其他 controls，只切一个确认支路，测比较输入 long-window 步幅；再加有限 reference 源阻抗和接收负载。实器件 TB 在模型与状态闭合后运行。测 `Qref=∫iref dt`、峰值 droop、比较时刻的残余误差。

结果分析：长等待仍偏差通常指向比例/桥接/寄生或状态错误；增加等待可改善的项更可能是建立；不对称两侧同时看共模，不把共模位移直接记成码误差。一次切换正确不代表整码线性，之后才做 bit sweep 和转移点。

验收：一个真实节点的完整电容端点表、一组状态前后的方程与 reference 动态实验定义。没有运行，不填 INL/DNL。接 [R04](R04-bootstrap-comparator.md)。
