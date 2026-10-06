# R02：PGA 的反馈、缓冲与旁路

问题：PGA 是一个简单的可变增益运放吗？先预测：图中两只 AMP_2 是构成差分输入对，还是分别驱动两个输出？打开 [PGA 与 AMP 原图](../schematics.md#ads8681)。

`HIX_2012210_SUB/PGA` 中实际有一只 AMP_1、两只 AMP_2、四只 TRIGATE、BIAS_7 和 CTRL_8。MI331/AMP_1 接 AIN_P/AIN_GND、REFCAP/REFGND，其 VOM/VOP 分别为 `R1551_MINUS`/`R1550_MINUS`。MI350/AMP_2 的 VP=`R1551_MINUS`、VO=VOM；MI348/AMP_2 的 VP=`R1550_MINUS`、VO=VOP。因此两只 AMP_2 分别接两侧，不可把整个 PGA 抽成一只理想差分放大器后忽略内部负载。

MI274、MI272 的 TRIGATE 将 AMP_1 输出接 VI1/VI2；MI269、MI270 则将 VOM/VOP 接 VI1/VI2。两组 OE/OEN 分别来自 `X636_ZN/X632_ZN` 与 `X5011_ZN/X630_ZN`。这说明存在可选择路径；是否为旁路、反馈或某阶段校准，需要读 CTRL_8 真值和上层 MI406/TRIGATE_1，不仅凭符号判断。

进入 AMP_1：MI323/AMP 的 VI1=`P1364_G`、VI2=`P1380_G`，VOM=`R1264_PLUS`、VOP=`R1214_MINUS`；ADJ_RC_1 的 PLUS/MINUS=`P1364_G`/`R1264_PLUS`，形成一条可追的输入到输出支路。还有 ADJ_RES、reference 切换和输出电容。先分清用于比例设定、频率补偿、负载和参考注入的支路，再推 gain。

实验分两步。结构阶段沿 AIN_P 到 AMP 内输入 MOS，再沿一个输出返回输入，写每个开关的条件。模型恢复后保留 PGA 的两侧、BIAS_7 和代表性 SC 负载，做小差分 DC sweep：`VINP=VCM+vid/2`、`VINM=VCM-vid/2`；在确认的每种 gain 状态拟合 `vod=G·vid+b`。前端外部输入不一定直接使用上述内部差分激励，TB 要注明激励所在边界。

结果分析：中央线性段 slope 是增益，intercept/G 是相应边界的输入参考 offset；输出限幅不纳入拟合。改变 VCM 或源阻抗后再看变化，不能把输入范围限制解释成增益错误。长窗正常、短窗异常时，查看 AMP_2 输出与 SC 加载节点的建立，而非只看静态 transfer。

验收：一条真实反馈链、两组 TRIGATE 状态表及线性段拟合方案。当前控制极性、增益码映射和工作点待验证，不报告 PGA 增益实测值。接 [R03](R03-capacitors.md)。
