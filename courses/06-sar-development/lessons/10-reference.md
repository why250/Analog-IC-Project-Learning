# 10：reference、bias、供电与系统耦合

问题：用 ideal VREF 跑通 SAR 后，最先遗漏的 reference 约束是什么？先预测平均 load 与单个 MSB 电荷脉冲谁更能暴露 driver 问题。两者都要定义，不能只看静态电压。

## 从负载波形设计参考驱动

根据实际 switching sequence 提取 Iref(t) 与 ΔQ。短时间理想去耦近似 droop≈ΔQ/Cdec，之后恢复由输出阻抗/feedback、ESR/ESL、布线与 bias 决定。driver 的 drive current、稳定性和去耦不是独立旋钮；加大 Cdec 可能减峰值、改变 poles/启动和恢复时间。

每位 reference 污染经当时有效电容和输入参考比例传到比较残差。与 code/相位相关的 droop 可产生失真，而静态 reference 比例通常主要表现 gain error；共享 reference 还可能使差分侧相关。先写 transfer/phase，不能将某条 reference 的 RMS 直接 RSS 到输入。

## bias 与 supply

bias current/mirror 的范围、startup、温度和 supply sensitivity 会改变 comparator delay、输入 drive 和 control threshold。先检查 DC/周期工作点，再 noise/PSRR；动态阶段可能切换 bias，不使用一个全周期平均电流说明每相性能。

分 supply domains 与实际 return path、well/substrate、clock/reference/input route。ideal supply/ground 会隐藏数字切换、reference bounce 与 common-mode coupling；逐步引入受控 source impedance/decoupling，再用真实 board/package 模型。不要在缺少阻抗模型时直接把电源 ripple 模拟成未知整芯片误差。

## TB 和测量

参考 TB 保留原 feedback、代表性 pulse load 和去耦/ESR；先 startup/no-load，再 pulse area、repetition、去耦/阻抗 sweep。保存 output/ref-at-CDAC 两个位置，量 droop、比较时刻余差、恢复与 ring。比较不同 pulse area 与间隔，区分电荷抽取、平均输出电流和 loop dynamics。

bias TB 固定输出 compliance，扫负载/电源/温度后回到 comparator operating point。system TB 有限 supply/reference 阻抗时保留电流积分与 sample_id，检验某个码型的异常是否随 reference bandwidth 变化。功耗范围注明包含 buffer、输入 driver、clock 和数字哪些部分。

实测也需关注测试板参考去耦、接地和外部 source；芯片不同模式/负载之间不可只比较 DMM 的均值。

验收：一份 reference pulse/load 合同、droop 到 input error 的 phase 映射、一个启动/振铃反证条件。接 [11 系统整合](11-integration.md)。
