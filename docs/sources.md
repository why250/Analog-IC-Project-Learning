# 教材与证据索引

Cadence verification 的 ADC/PLL 路径相对 `CADENCE_VERIFICATION_ROOT`；本次建课时该目录为 `/home/userone/AAAIC/tutorials/cadence_verification`。初始检查日期：2026-09-30。AFE 资料单独使用 `AFE4404_ROOT`；新增 ADC 实战资料使用 `ADC_PROJECTS_ROOT`，机器路径由 config/local.env 提供。

## adc_projects（2026-10-04 新增课程）

四个项目共 14 个库，原包在各项目 originals/，资料在 docs/，OA 在 libraries/。以下原包 SHA-256 于本轮重新计算，与 ADC_PROJECTS_ROOT/SHA256SUMS 相应项一致；这不能代表模型或仿真通过。

| 原包相对路径 | SHA-256 |
| --- | --- |
| `async_sar_8bit_40MSps/originals/8位40M异步SAR_ADC(3).zip` | `62ecdcb32d1c069682160ff1179c6598facbb141dd31866f2dcdcc06f789916f` |
| `pipelined_sar_12bit_100MSps/originals/Pipe_SAR.tar.gz` | `0675ceaa4f97bf44599a4c65ac8ab92e47a72a3afbc900660e60c09530090d0e` |
| `ads8681_reverse_engineering/originals/ads8681.tar.gz` | `e7feec63758ee9448ed7ef2988c347cd23e195b3c5b32d344eaec915cc68438c` |
| `ads1248_reverse_engineering/originals/ads1248.zip` | `fdd0d4819e7e7476de68bc9c449e66d7d193772a3b69ab47509d25352a5d578e` |

ADC_LEARNING_ROOT 中已有 2026-09-29 路线、首课及只读 bridge 导出。本轮复核 14 个关键导出，并检查对应当前 OA 哈希与原清单一致；导出没有被当作本轮 live 读取。完整 JSON/器件参数留服务器，小型身份/连接摘要见 [项目证据](../notes/evidence/2026-10-04-adc-projects.json)。首课整合入本仓库并记录来源哈希。

课程见 [真实 ADC 项目路线](../courses/05-adc-projects/README.md)。四工程未新网表或仿真，SMIC/TSMC PDK 与旧 state 绑定待检查，作者 ENOB 不作为本机验证结果。

## AFE4404（2026-10-04 新定位）

服务器原包为 `AFE4404_ROOT/originals/afe4404.7z`，SHA-256 为 `e21f8ec458ab36723817ce742423bcf755628b68be3da3165d69d2c5e88d42b2`；TI 数据手册 `docs/afe4404.pdf` 的 SHA-256 为 `6704bbac93ec071ab807387bcc8f3cfc389d6efab8ff42774f0a8d34faaab8e4`。本轮重新计算原包与 PDF hash，当前 SUB/TOP schematic hash 也已归档；未做原包与工作库逐文件比较。

五个 HIX_1907151* 库、TOP_HIER/TOP_FLAT、独立工作区与 gf018hv_green OA 工艺库已定位。详细来源、数据手册审阅范围、候选模块及未验证项见 [AFE 工程地图](afe4404-map.md) 和 [检查 JSON](../notes/evidence/2026-10-04-afe4404-discovery.json)。课程见 [AFE4404](../courses/04-afe4404/README.md)，尚无 AFE 新网表或仿真。

## 原包身份

| 包 | 归档文件 | SHA-256 |
| --- | --- | --- |
| ADC | `originals/adc_verification_v5.0_001.tar.gz` | `d2d30077c9d2243b86b2addc207ae8089468a2f7707d0812eab516d6bd2b2095` |
| PLL | `originals/pll_verification_ws_v1.0_001.tar.gz` | `278739de1cdf9263ee7b3714cd5ce03b93a818155a3be3c65a27f80a895cb016` |

2026-10-01 经 `ssh IC_Server` 重新计算两份归档的 SHA-256，均一致。此前索引写为 `archives/`；本次服务器实际目录为 `originals/`。小型证据见 [环境检查摘要](../notes/evidence/2026-10-01-environment.json)。

校验值来自本地 `SHA256SUMS`，建课时另行核对原包。若另一台主机保留了同一目录布局和校验清单，可运行：

```bash
source config/local.env
(cd "$CADENCE_VERIFICATION_ROOT" && sha256sum -c SHA256SUMS)
```

归档校验只识别原包，不能证明解包后工程没有改动。后续实验还需记录工作副本变更。

## ADC 阅读路径

以下均位于 `adc_verification_v5.0_001/`：

| 资料 | 本课程用途 |
| --- | --- |
| `README.txt` | 顶层 testbench、使用方式、原测试工具版本 |
| `WORK/saradc/cds.lib`、`common.lib` | 追踪设计库、PDK 和工具库的解析 |
| `DESIGNS/GPDK045/SARADC/cds.lib` | 设计库定义与工艺库引用 |
| `DESIGNS/GPDK045/SARADC/oa/saradc/10Bit_ADC_TB_new/maestro/maestro.sdb` | 第一课变量及表达式的静态来源 |
| 同一 `maestro/` 下的 `active.state` | 分析设置、模型文件及视图列表的静态来源 |
| `WORK/saradc/SARADC_ENOB_calculation.xlsx` | 后续动态指标审计的候选资料，尚未审计 |

版本差异：归档/目录名为 `v5.0_001`，内附 README 标记 `v3.0-001`。README 记录测试环境 IC6.1.8-64b.83 / Spectre 18.1.0.235.isr3；不能据此假定任意新版本均兼容。

已在文件系统核实 `saradc/10Bit_ADC_TB_new` 的 `schematic`、`maestro`，以及 `10Bit_ADC_Run_Plan/maestro`。工程中带有历史 result/state 文件；课程建立时未执行新的 Virtuoso 仿真。

## PLL 阅读路径

以下均位于 `pll_verification_ws_v1.0_001/`：

- `README.txt`：Fractional-N PLL 工程说明；原测试版本 IC6.1.6 / Incisiv 13.2 / MMSIM 13.1。
- `DESIGNS/GPDK045/FRACNPLL/docs/Specification/Cadence_Zambezi_Synthesizer_Macro_Spec_Ver_1.0.pdf`。
- `DESIGNS/GPDK045/FRACNPLL/docs/Simulation_Description/Zambezi_SimulationTestbenches_2008-01-31.doc`。
- 同一目录的 `Zambezi_Top-Level_SimPlan_2008-01-30.xls`。
- 电路入口 `zambezi45/pll/schematic`，testbench 入口 `zambezi45_sim/pll_sim/schematic`。

PLL 文档已定位，规格数值与表格内容尚未审计，仿真未复现。2026-10-03 另核实 `pll_sim` 的 `config_function`、`config_plllock_TR`、`config_powerup1`、`config_function_post_layout`，以及对应 `ams_*` 保存 view；这些是旧工程入口，不等于当前 Maestro 状态或 AMS 已兼容。

## Bridge（2026-09-30 建课参考）

本次参考本机 `virtuoso-bridge-lite` 的 `README.md`、`AGENTS.md`，本地 Git HEAD 为 `93be53e`；remote 指向 `https://github.com/Arcadia-1/virtuoso-bridge-lite.git`。课程中的命令据本地文档编写，尚未通过它连接本课会话。新机器应记录自己所用版本并核对命令帮助。

课程只保存原创导学与必要配置摘要，完整原始工程和厂商文档由本机资料目录提供。

## 2026-10-01 服务器接管证据

- EDA 主机别名 `IC_Server`；实际 hostname 为 `xunipc`。工具报告 Virtuoso `IC25.1-64b.38`、Spectre `25.1.0.054`。
- 当前顶层 `schematic/sch.oa`、工作区 `cds.lib`、`common.lib`、`.cdsinit` 与 ADC 归档逐字节相同；只核对了这些文件，未证明整个工作副本未改动。
- 当前 `maestro.sdb`、`active.state` 与归档不同，摘要记录双方 SHA-256。active test 变量与归档一致；`active.state` 的 `projectDir` 已映射到 `userone` 的服务器目录，并存在字段和序列化格式差异。不能将全部差异解释成仅路径修改，也不能据此认定有新仿真通过。
- 已通过新启动的 Virtuoso 会话读取 `I0` 的 master：`saradcII/10bit_adc_core_w_split_dac_ld1_msb`。其可用视图为 `symbol`、`schematic`；仿真绑定仍待新网表确认。
- 当前 `gpdk045` 的会话 `readPath` 落在 `TECH/GPDK045/gpdk045_v_4_0/gpdk045`，与 `gpdk045 -> gpdk045_v_4_0` 符号链接一致；`analogLib` 的工具路径解析到 `tools.lnx86`。
- 实际运行的服务器 bridge checkout 为 `/home/userone/AAAIC/virtuoso-bridge-lite`，HEAD `168943ca917e592c492a0db1b70aca0544f311c0`；Windows checkout HEAD `a04d33552d06ccb95078c895cdfe826a72cc1c12`。本轮使用服务器虚拟环境，通过 Windows SSH 调用；具体连接说明见 [bridge](bridge.md)。

## 2026-10-03 完整课文的来源范围

通过 SSH 只读核实后续 ADC testbench 的 view，以及 PLL 的配置/状态 view；读取两包 README 核对工程入口和原测试版本。清单与资料文件哈希见 [课程入口证据](../notes/evidence/2026-10-03-course-entries.json)。这次没有连接 OA/ADE、迁移状态、保存设计或运行仿真。

完整课文的理论公式和实验设计是原创研修内容；PLL 的具体 RF/参考频率、锁定与噪声数值要求保留为第 07 课的资料审计任务，不从未读的规格中编造数值。课程记录模板保持未执行。
