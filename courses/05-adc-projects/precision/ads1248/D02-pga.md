# D02：双 AMP 与电阻梯中的 PGA

问题：PGA 的差分增益由哪个反馈比例决定，CLK 参与什么机制？先预测：仅改变内部 ADJ 端是否就等于改产品 gain register？打开 [PGA 与 AMP 原图](../schematics.md#ads1248)。

`HIX_2012180SUB/PGA` 实際含 25 个 RES、两只 AMP、十二只 VH_TRIGATE、两只 S_MX21 和逻辑。X4588/AMP 的 VP=`P1929_D`、VM=`R3200_PLUS`、VO=`P1930_S`；X4589/AMP 对应另一侧 VP=`P1933_D`、VM=`R3201_PLUS`、VO=`P1934_S`。两侧 AMP 的 PLUS/MINUS 还交叉接 VOP/VOM，不能当作无作用的电源/普通单端运放端口。

电阻梯有 320m、640m、1.28、2.56、5.12 等保存 r，显示比例线索。它们是逆向库保存字段，不是已验证欧姆值；与 w/l、实际电阻类型和单位比较后才用于定量 TB。有 R3158 两端均为 VOM、R3157 两端均为 VOP 的实例，不能计入有效反馈电阻。

AMP 中还包含 CLK、MUX22、BIAS_4/5、AMP_1/3 与 ADJ_RC。这些结构提示时变校准/切换的可能，但 chopper、auto-zero 或其他方式必须用 switch 端点和相位检验；有 CLK 不构成功能证明。

研读实验：选择一侧，沿输出通过 S_MX21、R3159 与电阻梯返回 AMP 的输入，写所有有效状态下的闭环支路；再做另一侧，检查对称与跨侧连接。保留 cross-coupling 与 bias，不把一个 AMP 单独拆出来之后套仪表放大器公式。

模型可用后最小 PGA TB：确认两侧的完整 enable/CLK、ADJ vector、VCM 和负载，先短 transient 检查周期稳态，再扫小差分。在中央线性段拟合 slope/intercept；比较不同 control state 的 ratio。另扫 VCM 与输入源阻抗，用输出 headroom、输入电流和恢复时间解释非线性。

低频分析：offset 与 noise 分开；周期切换的 ripple 和 alias 需注明采样相位。输入参考白噪声密度不能直接换成低频 RMS，需定义积分带宽、1/f 与数字滤波。若无模型，使用无量纲电阻比证明静态反馈，不能报告 μV offset 或 nV/√Hz。

验收：一侧真实闭环、各开关状态对应的电阻比、对 CLK 功能的一项可检验预测。下一项 [D03](D03-switched-cap.md)。
