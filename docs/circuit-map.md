# 实际电路地图（2026-10-03）

来源：独立 ADC Virtuoso 会话，经服务器 bridge `168943c`、显式 `adc_course` profile 只读 schematic。完整 JSON 留在服务器 `COURSE_REMOTE_ROOT/2026-10-03-circuits`；小型摘要见 [证据 JSON](../notes/evidence/2026-10-03-circuit-modules.json)。这是工作副本保存结构，新仿真只验证了下述比较器 TB 的实际网表。

| 目标 | 已确认的电路 | 当前边界 |
| --- | --- | --- |
| ADC core | `saradcII/10bit_adc_core_w_split_dac_ld1_msb` | 顶层 `I0`；混合晶体管与行为模型 |
| CDAC | 两边 gpdk045 MIM unit arrays、C54/C55 bridge、reference mux | unit 保存 15.2265 fF，bridge 保存 15.724 fF；新系统网表展开待验证 |
| 采样路径 | `analog_mux_*`、`*_ld1`、`backplate_clamp*` | 已读多处 `bmslib/sw_no`；不能用系统结果验收自举非理想 |
| 自举候选 | `saradcII/boosted_SH_switch` | 晶体管/电容实现，主信号管 M4 为 `pmos2v`；独立 TB 尚待建立，未在当前已读 core 路径实例化 |
| 普通开关 | `saradcII/mos_switch` | `nmos1v_lvt/pmos1v_lvt` transmission gate，可作模块对照 |
| 比较器 | `saradcII/comparator → latch_buffer → latchonly_updated` | 11 管动态核、clockdriver、NAND SR latch；新 offset TB 网表已确认该锁存核为 schematic |
| 控制 | `saradc/10Bit_ADC_logic → controller_baseline/veriloga` | 行为状态机 + 门/时钟路径；12 周期关系仍为静态推导 |
| PLL | `zambezi45/pll` 与 `zambezi45_sim/pll_sim` | 入口存在；实际 PFD/CP/filter/VCO/divider master 与仿真绑定待读取 |

## 两个易混淆的模块 TB

- `saradc/10Bit_capdac_TB_new:I6` 是 `saradcII/10BIT_CAPDAC_ld1`，不是 core 内某个 CDAC 子实例。其结构和实际 core 相近，但 core 混用非 ld1/ld1 mux，独立测试结论需匹配后才能外推。
- `saradc/comparator_offset_TB_new:I0` 是 `saradc/comparator`；noise TB 的 `I9` 是 `saradcII/comparator`。本轮读到二者外层连接相同，都引用 `saradcII/latch_buffer`，但 lib 名称仍分别记录。新 offset transient 确认的器件参数仅适用于该运行。

## 待核对的采样支路异常

已读 `saradcII/analog_mux_8` 中没有读到其他 mux 所有的 `vin↔cap` 采样开关实例；当前 core 的 `I16` 引用它。先在实际 schematic 和新 core 网表中确认是否为缺支路、其他实现或读取边界，再决定修复。当前没有改该 cell，也没有宣称 ADC 系统通过。

## 新仿真范围

仅新运行比较器 offset TB 的独立 ADE 副本 `saradc/course_cmp_offset_20261003/maestro`，绑定原 `comparator_offset_TB_new/schematic`，未改原 schematic/maestro。详见 [实验记录](../notes/2026-10-03-comparator-nominal.md)。CDAC、自举和 PLL 仍未新运行。
