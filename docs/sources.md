# 教材与证据索引

本文路径均相对 `CADENCE_VERIFICATION_ROOT`；本次建课时该目录为 `/home/userone/AAAIC/tutorials/cadence_verification`。检查日期：2026-09-30。

## 原包身份

| 包 | 归档文件 | SHA-256 |
| --- | --- | --- |
| ADC | `archives/adc_verification_v5.0_001.tar.gz` | `d2d30077c9d2243b86b2addc207ae8089468a2f7707d0812eab516d6bd2b2095` |
| PLL | `archives/pll_verification_ws_v1.0_001.tar.gz` | `278739de1cdf9263ee7b3714cd5ce03b93a818155a3be3c65a27f80a895cb016` |

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

PLL 当前仅定位资料，尚未展开内容审计和仿真复现。

## Bridge

本次参考本机 `virtuoso-bridge-lite` 的 `README.md`、`AGENTS.md`，本地 Git HEAD 为 `93be53e`；remote 指向 `https://github.com/Arcadia-1/virtuoso-bridge-lite.git`。课程中的命令据本地文档编写，尚未通过它连接本课会话。新机器应记录自己所用版本并核对命令帮助。

课程只保存原创导学与必要配置摘要，完整原始工程和厂商文档由本机资料目录提供。
