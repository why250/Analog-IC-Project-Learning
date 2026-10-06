# 第 07 课：从 PLL 规格和配置建立验证地图

**工程问题：** 哪个 PLL test 和模型层级能回答功能、锁定与噪声问题？建议两次 60–90 分钟研修。

前置：[ADC 单元的证据方法](../../01-cadence-verification/lessons/06-regression-plan.md)；也可独立开始，但须掌握 [环境说明](../../../docs/environment.md) 和 [实验规范](../../../docs/experiment-protocol.md)。记录：[第 07 课](../../../notes/07-spec-model-map.md)。状态：入口已静态核实，规格内容和 AMS 运行待审计。

## 1. 预测

若 PFD、分频器或 VCO 换成理想行为模型，平均输出频率、锁定时间、reference spur、phase noise 中哪些仍有意义？“反馈分频相位稳定”是否能证明目标 RF 输出频率正确？

先给每个指标所需的模型效应，再从实际配置检查。此教材 README 说明为 GPDK045 的 Fractional-N PLL，原测试工具 IC6.1.6/Incisiv 13.2/MMSIM 13.1；当前 IC/Spectre 新版本存在不代表 AMS 数字内核和历史状态已兼容。

## 2. 精确入口与版本边界

原包为 `pll_verification_ws_v1.0_001`，原包身份见 [资料索引](../../../docs/sources.md)。先通过 `launch.sh pll --check` 检查路径，再在专属 PLL 工作区启动/定位会话，不能用 ADC 库中同名 gpdk045 代替 PLL 环境。

| library / cell | 已静态核实的 view / 用途候选 |
| --- | --- |
| `zambezi45/pll` | `schematic`、`symbol`、`physConfig` |
| `zambezi45_sim/pll_sim` | `schematic`、`readme` |
| 同一 testbench | `config_function` / `ams_function` |
| 同一 testbench | `config_plllock_TR` / `ams_plllock_TR` |
| 同一 testbench | `config_powerup1` / `ams_powerup1` |
| 同一 testbench | `config_function_post_layout` / `ams_function_post_layout` |

2026-10-03 已从文件系统核实这些 view。配置名提示测试用途，实际绑定和分析尚未读取；不能直接认定某个 `ams_*` 在当前 ADE 能打开，或将它当作 Maestro view。先读 `pll_sim/readme` 和配置内容，确定旧状态的受支持打开/迁移方式，迁移在副本完成。

## 3. 把原规格改写为可测量的需求

原始资料位于包相对路径 `DESIGNS/GPDK045/FRACNPLL/docs/`：规格 PDF、Simulation_Description 下的 testbench 说明 DOC 与仿真计划 XLS。先读规格，再逐条核对仿真计划；课程不预填尚未审计的 RF 频率、参考频率、锁定时间或噪声阈值。

| 需求 | 要提取的定义 | 测量节点与条件 |
| --- | --- | --- |
| 频率/通道 | `fref`、整数/分数分频、输出路径、允许误差 | VCO、反馈节点与最终输出分别确认 |
| 启动/重调谐 | 上电、复位、寄存器和校准顺序；计时起点 | 电源、reset、配置写入和输出有效性 |
| 锁定 | 频率/相位误差界、保持时间、失锁行为 | 连续时间或逐参考周期的定义 |
| 噪声/杂散 | offset 范围、积分带宽、dBc/Hz 与 dBc | 指定载频、输出端口、工作模式 |
| 功耗/范围 | 供电域、电流、调谐和校准覆盖 | 模型是否真的有电源电流路径 |

`fVCO=(N+α)·fref` 只对确认的反馈拓扑成立。最终输出若另有分频，需再除以该比例。`N/α` 若来自程序字，检查编码、实际写入、量化步长和运行时取值；不把标签上的通道号当作频率证据。

## 4. 配置与模型地图

沿实际 testbench DUT 记录 PFD、CP、loop filter、VCO、divider、DSM、SPI/register/reset、校准逻辑和 connect module。模块存在与信号名从当前电路取得，不假设完整链路与常规 PLL 完全相同。

对每个 config 记录 cell/instance 绑定、stop/view list、模拟与数字域、接口规则、电压逻辑阈值、供电及 reset 极性；检查外部 Verilog/Verilog-A 文件、timescale、编译库与模型路径。`zambezi45_connectLib` 的实际接口规则可能影响电平与边沿，不能只审模拟模型。

| 模型层级 | 可回答的问题 | 尚需更高模型精度的内容 |
| --- | --- | --- |
| 理想事件/行为模型 | 配置、频率关系、功能状态机 | 实际功耗、器件噪声与非理想边沿 |
| 含参数非理想的行为模型 | 明确建模的延迟、死区、量化与噪声趋势 | 模型参数如何校准、未建模效应 |
| 晶体管/混合绑定 | 对应条件下的电路工作点与动态 | 长时间统计成本、数字/模拟边界遗漏 |
| 提取后配置 | 该提取对象包含的寄生效应 | 实际提取范围、corner、其他仍理想的模块 |

## 5. 最小检查与验收

本课只检查：选 `config_function` 或经原资料解释的入门配置，确认 active design、DUT、关键绑定和分析；列出数字内核/编译/旧状态迁移的阻塞。没有需求和配置地图前，不直接跑长锁定或 pnoise。

交付三张表：需求来源及阈值、配置/模型边界、现有 test 到需求的覆盖。每个数值写文档页/表或当前设置来源；未提供的规格记缺口，课程实验阈值另列。

验收：能选出一个回答 nominal 启动/锁定的配置，说明为何，明确它不支持的产品结论。下一课只以该配置建立短功能/启动试跑再扩大窗口。

下一课：[08 启动与锁定](08-startup-lock.md)。
