# 09：SAR 控制、异步握手与数据有效

问题：输出 code 已更新，是否一定对应当前输入？先预测“done 为高”和“八次转换均合法”是否等价。本仓库行为 slow-case 已说明 overrun 后 EOC 可能仍出现而码失效，见 [A05](../../05-adc-projects/lessons/A05-model-to-circuit.md)。

## 同步与异步的合同

同步控制规定固定 bit clock、reset/evaluate/DAC 更新边沿和余量。异步控制规定 evaluate→判决→valid detection→锁存/更新→reset→再 arm→下一 bit，并包含 non-overlap 与终止。reset 去除 valid 的时刻也是协议的一部分，VALID/CMP_OK/LATCH 名称不能自动认作相同事件。

每位时间预算从事件图求关键路径；重叠过程不是简单相加，串行保守总和也不能证明门级路径闭合。DAC 电荷建立、clock buffer 和判决输出 loading 都可能改变 next-trigger。特别检查 LSB、近边界迟决、外部新采样与内部仍 busy 的交互。

本教程 50 ns 周期中的 4 ns 余量是示例数字；后续用真实 worst condition、时钟分布和可接受 error rate 更新。若一转换超过可用窗，定义丢弃/错误标记/停采策略，不能把上一 code 当本次新结果。初期教学模型保持 external acquisition 刺激并拉 overrun，用于展示污染；真实产品协议需明确处理。

## RTL/门级验证

为每个样本标 sample_id，跟踪 N 次 decision、最多允许的 DAC updates、结果锁存和 valid latency。DOUT 位序、unsigned/offset binary/two's complement、output inversion 与 signed arithmetic 分开。已有 8 位 DOUT<0> 为 MSB，不按 bus 数字大小猜权重。

RTL assertions/scoreboard 可验收无非法状态、decision count、valid 不提前、旧结果不误标。门级或 electrical system 再检查实际 voltage thresholds、延迟、glitch 与 reset；逻辑正确不能替代 analog settling。异步 CDC/输入边沿附近还需用实现流程检查 metastability risk 与 synchronizer/handshake 边界。

## 最小实验

固定三值交替输入，在每次 valid 采样 bus；用 comparator done 延迟和 DAC settling 延迟分别做扰动。再注入一次 missing done、一位极性反转、旧 bit/多一 pulse，确认 checker 会失败。第一轮几周期足以验证协议，不先跑长 sine。

看波形时将 sample aperture、内部 compare 完成、算法结束、最终码稳定四种时刻标出。输出稳定并不保证关联的 held sample 未被新 acquisition 覆盖，算法 EOC 也不等于外部接口有效。

验收：状态/事件图、sample_id 对齐表、一个受控失败与输出无效处理。接 [10](10-reference.md)。
