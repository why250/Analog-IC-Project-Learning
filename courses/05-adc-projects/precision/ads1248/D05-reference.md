# D05：内部参考、bias 与传感器激励

问题：内部 VREF 和外部 reference 输入在采样网络中如何相遇？先预测：同一个 reference 同时用于 excitation 和 ADC，能否无条件消掉 reference noise？打开 [BANDGAP、AMP_7、VREF_MUX 原图](../schematics.md#ads1248)。

MI69/BANDGAP 接 VREFCOM、VREFOUT_1，并输出若干 VO；MI95/VOL_GEN 输出 `P929_G`→MI59/AMP_7 的 VP。AMP_7 的 VO=`P870_D`，该网实际接 AMP_8/9/9S1、COMP 和 INPUT_MUX 的 VREF，也进 CHARGEPUMP 的 VI。MI168/VREF_MUX 则输出 REFP_OUT=`N4027_G`、REFN_OUT=`N4157_G`，它们接 SC/reference 路径；两类网不可合并称“同一个理想 VREF”。

BANDGAP 含两只 NPN、25 个 RES、RES_DIV、AMP_2/5 和 BIAS_3/6。先识别 BJT 的端点、电流比与放大器反馈，再研究 PTAT/CTAT 与 trim。多级 reference output/buffer 的功能不由 VO 编号判断。

MI169/ADJ_CURRENTSOURCE 的八路 ISOURCE 接 AIN pad 后的网络，VREF=`P929_G`；MI150/BIAS_9 的 PIBO0…7 直接接 AIN0…7。这些真实连接是研究传感器激励/bias 与输入负载的入口，确切模式和输出电流需追 controls。CHARGEPUMP 的 CLK/VI/VO 是供电/电压生成候选，不能套基础 PLL charge pump 的相位鉴别解释。

最小 TB 在模型有效后分为 reference buffer 负载阶跃与单路 current-source compliance sweep。前者保留反馈/去耦，观察 P870_D 与 REFP/REFN 的扰动及恢复；后者固定确认的 ADJ/enable，扫输出电压，测电流平台及退出区，不用饱和区斜率估算标称电流精度。

Ratiometric 教学推导：理想 code 比例为 `Iexc·Rsensor/Vref`，若 Iexc 与同一 Vref 成比例则静态比例可能抵消。实际两条路径的带宽、延迟、寄生及不同 reference 节点会使动态噪声不完全抵消；用同时保存的 excitation/reference/input 三条波形分析，不凭“共源”就删除误差预算。

验收：把 P929_G、P870_D、REFP/REFN 三类路径分别标清，写一个动态抵消成立所需的条件。所有电流、温漂、noise 和 compliance 数值待仿真。接 [D06](D06-low-frequency.md)。
