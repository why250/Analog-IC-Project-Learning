# 续学入口

- 最后更新：2026-09-30
- 当前单元：01 Cadence verification / SAR ADC
- 当前课：[01 接管 SAR ADC 工程](courses/01-cadence-verification/lessons/01-project-map.md)
- 当前状态：课程开头已建立；学员实操未开始
- 本课记录：[notes/01-project-map.md](notes/01-project-map.md)

## 已知事实

- 原工程包含 SAR ADC 和 Fractional-N PLL，两套教材独立。
- 已静态检查 ADC 第一课入口和 Maestro 保存设置，详见课文与资料索引。
- ADC 包目录与 README 版本标识不一致，已记录。
- 建课时两个原包的 SHA-256 核验通过；ADC/PLL 本机启动路径检查通过。当前机器的 `config/local.env` 已配置，不进入 Git。
- 尚未验证当前 Virtuoso/ADE 兼容性、bridge 连接或新仿真结果。

## 下一项具体操作

当前机器可直接执行 `bash scripts/launch.sh adc`；另一台 EDA 主机先配置 `config/local.env` 并执行 `bash scripts/launch.sh adc --check`。阅读第一课第 1 节并写下预测，然后打开 `saradc/10Bit_ADC_TB_new/schematic`，确认 DUT 实例的真实 master，把第一条层级记录写入笔记。

## 阻塞与待确认

- 尚未开展实操，目前没有已确认的实操阻塞。
- 学员后续关注方向（ADC 性能、模块设计、验证自动化等）可随第一课反馈调整。

## 每次会话结束时更新

把当前状态改为“进行中 / blocked / 已完成”之一，写明最后完成的具体步骤、证据路径、未解问题和下一项动作。完成课程文件编写与完成学习实验分别记录。
