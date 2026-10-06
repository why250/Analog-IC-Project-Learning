# 04：Python/MATLAB 的作用与模型分层

问题：算法模型需要多复杂，才能帮助电路设计？先预测：只写 floor(vin/LSB) 是否能研究 CDAC 失配、某位未建立和比较器 offset？黄金码适合当 reference，不能代替带实际 trial 的搜索模型。

## 三层离线模型

第一层定义采样值、编码、饱和和黄金输出。第二层逐位更新实际 DAC 权重，保存 trial/decision/code，加入固定 offset/权重和每次 decision noise。第三层引入建立状态、采样时刻/jitter、时序 deadline 和校准/冗余。精度提高的依据是要回答的问题，而非代码长度。

带实际 weights 的 unipolar trial 电压为 Σwi·bi；每步试置下一 bit，比较 u 与 trial+Vos+noise，再保留/清除。binary 理想 wi=VFS/2^(i+1)，所有 bits 加一个 dummy unit 才构成完整 2^N 电容分母。若用 actual C 推 weights，分母和 parasitic 也要变化；只往 nominal bit weights 加噪声会漏 normalization。

[sar_design_model.py](../../../scripts/sar_design_model.py) 已实现这些基本环节。失配例子假设单位电容误差独立，group relative sigma≈σunit/√nunits，再除总实际 C；没有 gradient/correlation。σunit=1%、seed=42 的一次 realization 只能说明这份模型的一个样本，不能叫 yield。

## 静态与频谱计算

脚本用逐位 ADC 的 code≥k 条件二分查 transition，按第一/最后 transition endpoint 拟合 LSB；排除外侧饱和 bins。DNL=bin width/LSBfit−1；INL=(Tk−Tideal,k)/LSBfit。缺码候选是宽度在搜索精度内为零，必须注明有限数值分辨率。noise 打开时不要用确定性二分当 transition measurement，改用重复判决概率/码密度。

动态输入采用 M=2048、k=901，fin=k·fs/M≈8.799 MHz，k 与 M 互质、rectangular coherent window。先每样本得到 code，再转换 code-center 电压、减均值、做 rFFT；单边 power 中正频率乘 2，DC/Nyquist 不乘 2。SNDR 分母含除 DC/fundamental 外全部 bins；示例 SNR 另去 2…5 次 folded harmonics，须把阶数记入报告。

输入峰值为满量程峰值的 0.98，未作 fullscale amplitude 修正；直接 ENOB=(SNDR−1.76)/6.02 是该振幅条件下值，不能悄悄归一化。idle tone、非相干信号和旁瓣掩膜是另一个测量问题，不用这个单 bin 算法处理所有数据。

## 一次受控实验

```bash
python scripts/sar_design_model.py --output your_new_directory --seed 42
```

固定输入/seed，依次看 ideal、1% unit mismatch、采样/比较器噪声、50 ps jitter、DAC τ=1 ns。每组只增加指定机制；噪声组含采样 0.6 mV 与逐判决比较噪声 0.4 mV，不能直接将其噪声谱等同一个线性 white source。有限 DAC 状态以 exponential 向 trial 靠近，不是完整电荷域模型。

新计算中 ideal SNDR≈61.89 dB，50 ps jitter≈50.84 dB，τ=1 ns 的 DAC≈33.56 dB。这些是教学算法模型趋势；后者提示 2.2 ns bit window 与 τ 不相容，不证明真实 ADC 有相同失真。摘要见 [新离线结果](../../../notes/evidence/2026-10-05-sar-design-model/summary.json)。

验收：手算 u=1.26 V 的搜索并与 floor 码 645 对照，解释一个异常是位权、噪声还是建立；再在 MATLAB 或 Python 中改变单一参数。不必重复写两种语言。接 [05](05-veriloga-rtl.md)。
