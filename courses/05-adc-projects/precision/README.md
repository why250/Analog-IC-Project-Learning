# ADS8681 / ADS1248 逆向电路课程

可以学习到实际模块和晶体管连接。这套课程以本次从 Virtuoso 读取的 OA 连接与 **37 张原生原理图** 为教材，分别研究精密 SAR 与 ΔΣ。先读 [电路图与连接索引](schematics.md)，再按下表进入课文。所有晶体管仿真均待执行；课程准备完成不代表学员学完。

读者已熟悉模拟设计，重点是从复杂逆向工程中找反馈、分相、误差路径与模块边界，不重复基础 MOS 教科书。两个项目没有现成 TB；我们先研读结构，再用 [无 TB 实验方法](no-testbench.md) 做归一化实验，最后在模型可用时搭实际模块 TB。

## ADS8681：精密 SAR 前端、参考与模块电路

| 课 | 核心问题 | 可验收产物 |
| --- | --- | --- |
| [R01 实际信号链](ads8681/R01-signal-chain.md) | 两个 SAR 子块与五路比较输出怎样接在前端后面？ | 一条带实例/网名的信号链与未闭合接口 |
| [R02 前端与 PGA](ads8681/R02-frontend.md) | AMP_1、两只 AMP_2 和旁路开关各承担什么？ | 反馈路径、控制状态与输入负载判断 |
| [R03 开关电容与 CDAC](ads8681/R03-capacitors.md) | 有哪些电容真正参与量化？ | 电容端点表、两状态电荷方程、一步 reference 扰动 |
| [R04 升压与比较器](ads8681/R04-bootstrap-comparator.md) | BOOTSTRAP 是给谁驱动，判决与锁存怎样区分？ | 逐器件分相表与观察节点 |
| [R05 参考与偏置](ads8681/R05-reference.md) | BANDGAP、AMP_3 与 REFCAP 如何分工？ | 参考路径、bias 边界与负载实验条件 |
| [R06 最小 TB 与误差归因](ads8681/R06-experiments.md) | 没有整芯片控制时如何获得有用证据？ | 可恢复实验副本、误差曲线与模型声明 |

建议首项只验收 R04 的升压驱动结构，再回 R02/R03。现有 8 位 SAR 与 GPDK045 comparator 可作已知工具链的练习，不能用其模型或延迟代替本项目结果。

## ADS1248：ΔΣ、PGA、SC 与低频精度

| 课 | 核心问题 | 可验收产物 |
| --- | --- | --- |
| [D01 输入到量化器](ads1248/D01-signal-chain.md) | 实際可见的多级信号、reference 和反馈如何连接？ | INPUT_MUX→PGA→SC→AMP→COMP 的带网名地图 |
| [D02 PGA 与低频误差](ads1248/D02-pga.md) | 两只 AMP、开关电阻梯与 CLK 为什么一起出现？ | 反馈支路、增益状态与 offset/noise 分离 |
| [D03 SC 电荷转移](ads1248/D03-switched-cap.md) | SWITCH_CAP_X4 的四份电路是串联还是并联？ | 各相开关表与一次差分电荷转移 |
| [D04 多级放大与量化](ads1248/D04-modulator.md) | COMP 的三对输入怎样形成量化前状态？ | 状态与量化求和地图、反馈方向检验 |
| [D05 reference、bias 与输入激励](ads1248/D05-reference.md) | PGA/SC 和传感器激励怎样共享参考？ | reference/电流源耦合路径与 ratiometric 条件 |
| [D06 低频结果与系统模型](ads1248/D06-low-frequency.md) | 没有数字滤波器时哪些指标仍可研究？ | 明确带宽/滤波/启动条件的教学实验与评审 |

先学 D02 的反馈梯，再学 D03 的一次电荷转移。环路阶数、反馈系数、数字 decimation 实现和商业器件性能没有在本次结构检查中验收。

## 证据与使用边界

2026-10-04 独立 profile `precision_adc_course`，实时核对 TOP/SUB/DEV readPath；只读打开、读取并导图，未保存原设计、未生成新网表、未运行 Spectre。来源、原图 SHA-256 与端子表在 [证据清单](../../../notes/evidence/2026-10-04-precision-adc-schematics.json)，[模型目录检查](../../../notes/evidence/2026-10-04-precision-adc-model-audit.json)，[会话记录](../../../notes/2026-10-04-precision-adc.md)。完整 JSON/日志留服务器，机器路径来自 `config/local.env`。

原图标注器件尺寸由照片测得；保存的 c/r 数值也需要审计。例如部分 c 数值与面积呈固定比例，部分同端点电容和电阻两端接同网。不能直接把这些标注当作已校准模型参数，也不能直接按产品额定位数验收逆向仿真。将 datasheet 规格、保存值、理论推导和新测量分别记录。

每课使用 [实验记录模板](../../../notes/precision-adc-lab-template.md)，按问题—预测—实验—证据—设计判断推进；一次只验收一个机制。课文中的 TB 是明确的实验方案，不是已经建立的 OA TB。
