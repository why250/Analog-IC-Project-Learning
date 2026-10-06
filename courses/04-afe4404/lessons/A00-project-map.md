# A00：从顶层连接确认光电接收链

状态：助教已完成 2026-10-04 实际接收输入与反馈的只读追踪，见 [原图与连接表](../schematics.md)。学员预测与理解待验收，没有 AFE 新仿真。初始来源与边界见 [工程地图](../../../docs/afe4404-map.md)。

## 问题与预测

本次只回答：INP/INM 进入哪个实际放大模块，反馈元件在哪里？

打开工程之前，先记录预测：输入电流进入什么节点，反馈电阻跨哪些节点，LED 驱动端与接收输入应如何区别？不要从 AMP_1 或 DAC_1 的名字直接作结论。预测应画出“输入电流 → 放大器 → 滤波/保持”的最小链，并给出一个可能推翻预测的连接证据。

## 阅读方法

数据手册的公开链路为 photodiode → 差分 TIA → 四相 switched RC filter → buffer → ADC；LED driver 与 timing engine 决定照明和采样。反向工程需要用实际端口和器件补上这一功能图。公开资料只能说明产品功能，不能替代 OA 的 master 绑定和 net 连接。

`TOP_HIER` 用来逐层追踪；`TOP_FLAT` 可在确定少量关键节点后作交叉检查。它们存在不证明完全等价，先比较端口与关键支路。技术库 `gf018hv_green` 有 OA 数据也不证明 netlisting CDF 或工艺模型齐全。

## 只读实验

1. 在服务器 source 本机配置，进入 `AFE4404_WORKSPACE`。按现场环境启动或选择独立 AFE Virtuoso；不要在已有 ADC 会话重新定义 AFE 库。
2. 用 bridge 时先按 [连接约定](../../../docs/bridge.md) 阅读工具本机文档，核对 user/host/workdir、CIW 与目标 cellview。2026-10-04 已建立独立 afe_course profile；续学仍须核对实时身份，不能沿用 adc_course 作为 AFE 身份。
3. 以 read 模式打开 `HIX_1907151TOP/TOP_HIER/schematic`。记录顶层实际端口；若名字与数据手册不同，先追 PAD_IO/ESD 与输入方向再作映射。
4. 从两个接收输入各追一条 net，记录实例名、master library/cell/view、terminal 和下一层 net。找到第一放大器及反馈路径，停在这一项问题上。
5. 核对反馈元件另一端、输入共模控制和输出下一站。将实际 master 对照候选 AMP/RES_ADJ/CAP_SWITCH，不能按图形邻近推断连接。

本课不保存来源设计、不迁移 ADE、不生成新网表或仿真。GUI 截图作为辅助，结构化 terminal/net 记录作为主要连接证据；读不到的 master 标为阻塞，不自行用“类似器件”替代。

## 证据与验收

交付一张最多十行的表：上层实例路径、master、输入 terminal/net、输出 terminal/net、反馈 terminal/net、证据来源。再用自己的话说明这条路径为什么具有跨阻反馈，而不是电压放大或 LED 电流驱动。

验收需要至少一条从顶层输入到放大模块的真实连接链、一个反馈闭环和明确的待查项。目录列表只证明文件存在，未达到本课验收。记录用 [模板](../../../notes/afe4404-lab-template.md)。

下一项具体操作：接学员对实际反馈类型的预测/解释，按 [已读连接](../schematics.md) 验收 A00，再进入 [A01 TIA](A01-tia.md) 的输入对与偏置路径；助教读取完成不等于学员已学完。
