# 13：版图与实现约束

问题：CDAC unit capacitor 大小相同、按 common-centroid 放置，就一定保住前仿线性吗？先预测：如果 MSB top-plate 路由比 LSB 多一段寄生，增加 unit 面积能否自动消除这项系统误差？

## 版图前需要什么合同

前仿应交付 unit/array 选择、实际 switch map、每相电压/电流、reference pulse、comparator 输入/输出负载、clock dead time 和 error budget。版图与 schematic 并行评审，避免把 reference return、shield 和开关布置留到阵列摆完才考虑。

电容模型应明确 top/bottom plate、电容密度、边缘项、寄生到 substrate/邻线、匹配统计及电压系数。common-centroid 可减弱特定低阶空间梯度，不能修复随机失配、电压系数、不同走线/邻接环境或所有高阶梯度。unit shape/orientation、dummy、邻接、电介质环境与连接方式须一致；实际工艺规则和 model 优先于通用摆法。

## CDAC 与关键节点

对各 bit group 保持单元统计与对称环境，并管理组间/两侧路由。底板连接开关与 reference 的 R/C 影响 settling 和 code-dependent droop；顶板是采样/比较器共享高阻节点，寄生既改变有效位权，也接收 clock/数字/供电耦合。split array 的 bridge 和中间节点寄生特别敏感，电容比与布线要在电荷矩阵中一起评审。

guard/shield 的选择需计入新增电容：静态 shield 可减耦合但增加负载；错误的动态 shield 可能注入电荷。差分对称不保证误差取消，因为两侧的转换历史、源阻抗与相位可能不同。按实际电荷路径检查，不以“图形对称”替代提取分析。

## 比较器、采样与控制

比较器输入对/再生对的局部匹配、负载与 clock arrival 应共同处理；输入走线靠近复位/大摆幅节点会增加 kickback。bias/reference/地回路与 digital return 分析实际阻抗，井/衬底隔离依照 PDK 和敏感节点安排。匹配器件的 dummy、方向、应力环境、接触和源漏连接应遵从工艺建议，不能只要求 W/L 一致。

自举浮置节点、预充电电容和驱动串接决定实际端间电压；路由寄生可改变 bootstrap ratio 和恢复时间。保证输入线和两侧开关环境，同时检查最大电压、ESD/IO 条件、clock slew。时钟树的实际斜率/偏斜会同时改变 acquisition、reset、DAC dead time 和 jitter 敏感度。

数字控制靠近 DAC switch 有助速度，但大扇出/回流会污染模拟节点。先标出高阻节点、脉冲电流路径、禁止并行走线区域和 reference decap 位置，再比较速度/耦合/面积代价。所有 EM/IR 条件使用瞬态峰值与 duty，不只平均功耗。

## 版图评审与实验

评审分三件事：DRC 是几何规则；LVS 是提取后的拓扑/参数等价；性能依赖 PEX 与运行条件。LVS 通过不能说明 reference settling 或电容 matching 达标。层次化 review 保存 array map、关键路径、shield/return 和版图版本。

可先对一个 unit、一组 MSB、bridge 或 comparator 做小块提取，比较新增 C/R 的来源，再决定整阵列路由。对于线性敏感节点，画“设计电容—提取有效电容—相位位权”对应表，而不只报告寄生总量。系统大图完成后统一核对 LVS/PEX 的 master 与前仿绑定。

验收：一份阵列单元/环境图、关键节点与电流回路标注、局部提取预算，说明哪些误差 common-centroid 可减、哪些必须靠路由/模型解决。尚未提供新的版图或 PEX 性能结果。接 [14 后仿](14-postlayout.md)。
