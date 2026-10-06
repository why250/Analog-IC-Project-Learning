# D04：多级状态与电容量化求和

问题：怎么从真实 SC 结构建立 ΔΣ 状态模型？先预测：COMP 三对输入是在时间上依次判决，还是经电容求和后一次判决？用 [AMP_8、AMP_9/9S1、COMP 原图](../schematics.md#ads1248) 查证，不凭标准框图回答。

顶层 AMP_8 的 VOP1/VOM1 直接进 COMP 第一对，VOP2/VOM2 进 AMP_9；后两组也进入 COMP。AMP_8 内有 59 个 MOS、POLYCAP 和切换支路，AMP_9/9S1 有多组 POLYCAP 与传输门、三组 CLK/CLKN 和 reference 接口。必须逐相追闭环，确定哪些电容保存状态、哪些负责 offset 消除或 reference 注入。

AMP_9 的具体研读起点：N1336 的 G=`C1231_PLUS`，N1337 的 G=`C1181_PLUS`；C1231 从前者 gate 网接 VOM，C1181 从后者 gate 网接 VOP，另有并行 C1233/C1183。两只 MOS 在 OA 中 D 同接 `N1336_D`，S 分别接内部两侧网；N1465 与隔离井 MOS 再接 bias/输出。这是可核对的电容反馈/输入候选路径。逆向 D/S 和 body 标注存在不寻常接法，不能未经模型/端子检查就重命名为标准 common-source 输入对。

COMP 中有 14 个 POLYCAP、少量 MOS、传输门、VH_LAN 锁存与 buffer。C1133/C1139 的保存 m=7，C1144/C1160 为 11，C1162/C1178 为 5；它们接不同内部端点，不能直接宣布调制器系数就是 7/11/5。还有两端同接 AVSS_1 的 dummy。先追三对 VP/VM 经 switches 到 summing node，核对 m、相位与有效电容。

实验方法：对每一阶段用零输入、一小段正差分、再回零的序列，检查状态是否保持、按周期累加或复位。如果保留原 feedback network 的输出仍持续累加，支持积分机制；只有普通 step settling 不能区分全部 SC 状态。若拆掉反馈造成开环漂移，这不是积分器证据。

理论模型在结构闭合后写 `x[n+1]=A x[n]+B u[n]+E y[n]`、`v[n]=C x[n]+D u[n]`、`y[n]=Q(v[n])`，同时注明相位采样定义。状态数由独立储能/更新方程决定，阶数不由 AMP 个数决定。反馈极性用一小步 y 改变后的状态方向验证。

线性化量化噪声模型可用于求 STF/NTF，但过载、idle tone、小 DC 下相关量化误差不能当不相关白噪声处理。将行为模型的状态幅度和稳定范围与实际 headroom 分开，防止行为仿真稳定却器件饱和。

验收：一条量化求和路径、一条 Q→control→reference 的真实反馈边与至少一个阶段的更新方程。当前反馈时序、实际系数与阶数均待进一步核对；本次没有 bitstream 或 NTF 测量。接 [D05](D05-reference.md)。
