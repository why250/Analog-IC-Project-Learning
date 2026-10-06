# D01：ADS1248 的实际可见模拟链

问题：三个 AMP 和 COMP 三对输入，是否足以证明三阶 ΔΣ？先预测：放大器数量和状态积分器数量是否必然相等？本课只验收可见连接。[TOP_HIER 原图](../schematics.md#ads1248) 来自 `HIX_2012180TOP`，共 74 个实例。

| 真实路径 | 关键端点/网名 |
| --- | --- |
| MI151/PAD_IO_8B→MI84/INPUT_MUX | AIN0…AIN7 经 pad 子块，到 MUX 的对应 AIN；含数字 I/O 功能，不能全简化成纯电阻 |
| MI84→MI74/PGA | VOP=`P2909_D`，VOM=`N2902_D`→PGA 的 VP/VM |
| MI74→MI78/AMP_6X2 与 MI100/SWITCH_CAP_X4 | VOP=`N657_G`，VOM=`N3876_G`；AMP_6X2 输出为 `C604_MINUS`/`C606_MINUS`，接 MI100 的 VI1/2 |
| MI100、MI106/SWITCH_CAP_1→MI85/AMP_8 | 共同 VO1/VO2=`X1190_A`/`X1192_A`→AMP_8 的 VP/VM |
| AMP_8→MI64/AMP_9 | VOP2/VOM2=`P1105_S`/`P4200_S`→AMP_9 VP/VM |
| AMP_9→MI86/AMP_9S1 | VOP/VOM=`C1181_MINUS`/`C1231_MINUS`→下一块 VP/VM |
| 三组状态→MI87/COMP | VP1/VM1=`C1055_MINUS`/`C4090_MINUS`；VP2/VM2=`C1181_MINUS`/`C1231_MINUS`；VP3/VM3=`C1238_MINUS`/`C1271_MINUS` |
| COMP→MI105/CLK_CTRL | Q=`X0250_A`→同名控制输入；反馈可能还经其他逻辑，需追状态 |

这组连接支持“多组模拟输出经电容网络进入量化器，并影响控制”，不能单凭 AMP_8/9/9S1 三个名称下结论为某个标准三阶拓扑。每个状态是否积分、是否 reset、反馈从哪相注入，需要 D03/D04 的电荷方程。

结构实验：从 AIN0 只追一条被选中的路径，列出 MUX select、PGA 增益选择和 SC 相位；从 Q 反向追到一次 reference 注入。未确定状态的支路用虚线并注明，不填推测的数字 decimation 方框。

验收：带网名的一条输入链、一条候选反馈链和三个未闭合接口。当前完整数字滤波/24 bit 码输出协议未核对，额定位数不等于实测有效精度。接 [D02](D02-pga.md)。
