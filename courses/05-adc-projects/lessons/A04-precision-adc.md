# A04：从商业 ADC 逆向库学习真实模块

2026-10-04 已补成 [ADS8681 / ADS1248 两套完整课文，共 12 课](../precision/README.md)，配套 [37 张实际关键电路图与连接入口](../precision/schematics.md) 和 [没有 TB 时的实验方法](../precision/no-testbench.md)。以下保留总导读；最新结构事实与实验边界以这些课文及本轮证据为准。

问题：一套逆向 OA 库能支持哪些电路判断？预测：仅有顶层连线与器件几何，能否得出商业器件的 noise、INL 或 ENOB？本课用 ADS8681 与 ADS1248 两套库研究结构与选定子模块，不将可见库当成已验证的完整芯片。

## 两个不同的学习目标

| 工程 | 文件系统确认的入口 | 课程重点 |
| --- | --- | --- |
| ADS8681 | `HIX_2012210_TOP/TOP_HIER/schematic`，下级库 `HIX_2012210_SUB` | SAR 信号链、模拟前端/PGA、reference、采样、比较器与控制 |
| ADS1248 | `HIX_2012180TOP/TOP_HIER/schematic`，下级库 `HIX_2012180SUB` | ΔΣ/PGA、低频精度、SC 电路、reference、bias 和时钟 |

每套还有 DEV/INT/LIB/SHT 库，共六个。本轮已经实时读取两套 TOP_HIER 和选定关键模块，原生导出 37 张 schematic，并追踪 BOOTSTRAP 在比较器内的父级实例；没有穷尽所有层级。功能、极性与阶段仍须由连接、控制和新波形检验，不能只看 BOOTSTRAP/COMP/AMP/BIAS 名称。

ADS8681 的官方系列定位是 16 位 SAR，ADS1248 是 24 位 ΔΣ。额定位数与 ENOB 不等同；服务器已有 PDF 和先前学习记录，下一步按实际型号的数据手册核对接口、输入/reference range、模式、数据率及规格条件，再与逆向可见部分对照。

## 先画一条模拟路径

从 TOP_HIER 的一个输入端开始，沿层级记录“外部端口→保护/选择→模拟前端→采样或积分节点→量化器→可见数字输出”。另外标 reference、bias、clock 及电源域。每条边注明真实网名、实例和 master；无法追踪的块明确留下缺口，不由商业芯片名称补画。

| 要查的机制 | 读图与推导 | 最小子模块实验 |
| --- | --- | --- |
| SAR 采样/reference | 开关状态、电容权重、参考驱动和负载 | 给定输入与控制，测建立、reference 扰动和 bit 步幅 |
| 精密 PGA | 输入共模、反馈网络、开关位置和 gain setting | 合适模型下扫增益/共模，分 offset、settling 与 noise |
| ΔΣ 积分/量化 | 各相电荷转移、积分状态、反馈 DAC | 短序列检查电荷/状态更新，再看过载与恢复 |
| reference/bias | 启动、镜像、补偿和负载分配 | 输出负载阶跃、启动与工作点；噪声需有有效模型 |
| clock/control | 两相先后、reset、数据有效和数字边界 | transient 逐事件验证；不靠信号名推有效极性 |

对 ΔΣ，采样域的 state update 和实际环路阶数/反馈路径先明确，再建立线性化模型；量化误差也只有在适用假设下才能视作不相关白噪声。若数字 decimation filter 缺失，bitstream 分析必须注明带宽与外部滤波定义，不能报告成完整 ADC 输出性能。

## 缺少模型时如何分析结果

DEV 库可能提供器件 symbol 或仿真接口 view，这不证明已有匹配的 model card。先查实例对应的 model name、include/section、器件端口与电源域。没有原模型时，可以用明确标注的近似模型研究极性、分相和归一化趋势；器件阈值、噪声、失配、工艺寄生和可靠性结论不能随之移植。

建立子模块 TB 时保留该模块的 reference、bias、clock 和代表性负载；删去周边后若失去工作点或反馈，模块 TB 可能不再代表真实运行。先做 DC/短 transient 验证，再量性能，最后回接一级上层验证耦合。

对于精密指标，码密度/transition-level 线性、输入参考噪声、offset/gain 随温度漂移、reference noise 与 PSRR 需要分别定义条件。看到架构能解释潜在误差来源，必须经过受控实验才能判断主导项。

验收是可追溯的一条信号链、一份模型可用性清单和一个可解释的子模块实验。ADS8681 优先作为 SAR 进阶，ADS1248 在 SAR 和基础 PLL 主线之后选修。当前所有仿真结果待验证。
