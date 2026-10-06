# P04：基础 PLL 的噪声与 reference spur 从哪里来？

问题：为什么提高 loop bandwidth 可以压低某些噪声，却使另一些噪声更容易到输出？先预测：VCO 自身的低 offset 噪声与 reference 高 offset 噪声分别受到什么作用？

## 相位域传递

令 `L=Kpd Z Kv/(N s)`。从 reference 相位到 VCO 输出的闭环传递为 `Href=N L/(1+L)`；VCO 端直接注入的相位噪声传递为 `Hvco=1/(1+L)`。前者近似低通，后者近似高通。Divider 在反馈端加入相位噪声，进入输出前也受环路与 N 放大；必须说明噪声的注入点。

CP 电流噪声到输出相位的传递为 `Hcp=(Z Kv/s)/(1+L)`，不要把电流 PSD 直接与相位 PSD 相加。Filter 电阻噪声、VCO 控制端电压噪声与供电 pushing 各有不同耦合路径。仅对近似不相关的源按 PSD 相加，参考与供电的相关扰动要单独分析。

扩大带宽通常更强地抑制带内 VCO 噪声，同时放行更多 reference/PFD/CP/divider 来源。最优带宽来自各噪声谱、稳定性和调谐需求，不是越大越好。

## Reference spur 的电路链

UP/DN 失配、最小脉宽、charge injection 与 leakage 使每个参考周期有确定性净电荷。Filter 将它变成 Vctrl 周期纹波，Kvco 将其转为频率/相位调制，在载波周围出现 reference 相关边带。即使平均频率准确，这种周期误差仍存在。

做因果对照时单独理想化 CP 电荷失配或 driver 脉冲，保持同一锁点与输出端；观察 ICP 电荷面积、Vctrl 中 fref 分量及输出边带是否同时变化。供电耦合也可产生相同频点边带，不能凭 spur 位置认定来源。

## 测量与分析边界

整数 N 周期稳态的 PSS/PNoise 需确认完整周期、所有数字状态重复和工具支持。若混合信号模型无法进行该分析，可用模块噪声加传递模型，并在 transient 中测确定性调制；不能将方法受限包装成整环 phase-noise 仿真通过。

若单边带 `L(f)` 使用 dBc/Hz，在常用小相位噪声约定下 `Sφ(f)=2·10^(L(f)/10)`，积分指定 offset 区间得到 `σφ²`，`σt=σφ/(2π fout)`。说明单/双边约定、积分端点和目标载波。Discrete spur 的功率不能按噪声密度直接积分；单独报告或采用明确的总 jitter 口径。

## 最小实验与验收

先固定整数 N、选一个稳定锁点，记录 lock 证据并选择足够稳态窗口。第一项测 reference ripple 与边带；第二项才核对噪声预算和模块频谱；第三项改变带宽，比较预测与实测噪声变化。

验收：噪声注入点和传递表、CP→Vctrl→spur 的受控对照，以及积分 jitter 的完整口径。基础阶段完成后再学习 [fractional/DSM、噪声与杂散扩展](../../02-pll-verification/lessons/09-noise-spurs.md)，新增分数序列前应保留整数 N 基线。

配套实验读图：[关键 TB 的作用与结果分析](00-testbench-results-guide.md)。区分保存配置、待执行实验与已新运行的结果。
