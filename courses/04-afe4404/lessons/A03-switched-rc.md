# A03：四相 switched RC 的建立、保持与交接

状态：课文已准备；已只读确认 MI311/SWITCHED_RC_FILTER 接 AMP_6 输出，原图及内部实例统计见 [实际电路图](../schematics.md)。实际 phase net、电容值、buffer 负载和动态建立待查。注意 SWITCH_BLOCK 在顶层接 TX1–TX3，应归 TX 路径，不能仅因名字将它纳入接收分相滤波。

## 问题与预测

先按 [A03a 存储与后级结构](A03a-filter-buffer-structure.md) 定位差分电容、交接开关、VOL_GEN_1 和 AMP_BLOCK；不能省略后级接口而直接用理想 ADC 负载解释全部残差。

相邻两个相位一个大信号、一个接近零，后一个读值为什么仍可能偏离零？先区分 TIA 未建立、采样电容残留、共享 buffer 电容记忆与开关 charge injection，选一个主导假设。

## 电荷与时间

TI 第 14 页 Figure 23 展示四路滤波器分相采样，并在各 conversion phase 接入共享 buffer/ADC。图是单端等效，产品接收链为全差分。采样与转换是不同事件，不应把 sampling switch 关断时刻等同 ADC 完成时刻。

采样期间，一阶等效电容向当前目标靠近，残差约为 `(Vold−Vtarget)exp(-Ts/ReqCs)`；Req 包含滤波电阻、导通开关与驱动源阻抗。实际多极点或 slew 限制时，这只是诊断近似。

保持期间漏电导致 `ΔV≈IleakThold/Cs`。交接到共享节点时，若初始缓冲电容 Cbuf 的电压是 Vbuf，理想瞬时电荷分享为：

```text
Vshare = (Cs·Vs + Cbuf·Vbuf)/(Cs+Cbuf)
```

随后 buffer 和剩余连接可能继续建立，不能把瞬时 Vshare 当最终误差。复位共享节点可能减少前相记忆，但也会改变电荷分享的初值。需要确认 ADCRST 实际复位了哪里。

更大的 Cs 降低理想 kT/C 量级与部分馈通电压，也加重驱动/建立负担。差分连接不自动消除不匹配造成的 pedestal、控制偏斜和共模到差模转换。

## 最小实验

先读实际采样开关、保持电容、conversion switch、buffer input 与 reset 路径，写出各控制相位导通表。实验副本用受控两电平源模拟已建立的 TIA 输出，保留真实开关和负载，主动隔离 TIA 本身的建立。

只改变前一相位幅度，后一相位目标、Ts、Thold、reset、clock、供电与负载固定。保存采样电容、共享节点、buffer 输出和控制边沿。测三个时刻：采样结束前、保持结束前、ADC 使用该值前。

另一轮才能改变 Ts 或 reset duration。若多个因素一起改动，即使残差下降也无法归因。没有模型时可用理想开关先算 charge sharing，真实 leak/charge injection 仍未验证。

## 证据与判断

交付前一相幅度与后一相残差的关系，加上实际相位身份。误差口径为“指定读取时刻减独立长窗参考值”，并注明启动周期舍弃规则。

若误差随前相幅度变化，应进一步定位在哪个节点第一次出现；不能直接称 ADC crosstalk。若单路采样就错，先修建立或 pedestal；若交接后才错，再检查共享节点和 reset。

验收只选择建立、hold droop 或交接记忆中的一项。下一课 [A04](A04-adc.md) 在输入可信后审计 ADC 架构与码值。
