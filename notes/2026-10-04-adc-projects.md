# 2026-10-04：adc_projects 接管与新课程

用户提出服务器 adc project 下还有 ADC 工程，可建立学习课程。本轮定位真实目录、复核先前课程和静态导出，新增 [四工程课程](../courses/05-adc-projects/README.md)。工作状态为进行中；课程准备完成，新工程实验与学员学习均待验证。

## 本轮完成的事实

- `ADC_PROJECTS_ROOT` 对应服务器 adc_projects，四个项目共 14 个库。路径写入忽略的 config/local.env，模板新增配置键。
- 四个原包及 docs 文件重新计算 SHA-256，与原 SHA256SUMS 相应项比对；14 个所选 schematic 的当前 OA 哈希与清单一致。校验范围未扩大为全目录。
- `ADC_LEARNING_ROOT` 已有 2026-09-29 路线、首课、schematic 导出及资料文本。复核其中 14 个关键 cell 的已有导出，本轮没有 live bridge/OA 读取；不能称新验证全部连接。导出和来源文件哈希已记录。
- 新增 A01 异步 SAR、电荷与位序；A02 采样/比较器/CDAC/握手/系统 TB 和分析；A03 Pipelined-SAR 残差、放大器与数字对齐；A04 精密 SAR/ΔΣ 逆向研读。首课由服务器已有课文整合。
- 本轮没有新网表、仿真、设计修改或改变现有 Virtuoso 会话。原工程、PDK 与既有学习目录保持原状；服务器仅在课程 state 目录写入此次摘要。

证据：[2026-10-04-adc-projects.json](evidence/2026-10-04-adc-projects.json)。记录原包/文档/选定 OA/已有导出相对路径与 hash、master 和刺激连接。完整数据留服务器。

## 与当前课程的对应

异步 SAR core I32/I33→BOOSTRAP，I34/I35→DAC_SW，I36→compare，I37→SAR_LOGIC，I38→EN_LOOP。BOOSTRAP_test 中两侧各 2 pF，提供 S03 的实际自举实验入口；对比 core 每侧名义 CDAC 约 1.9845 pF 时仍需注明系统耦合不同。

compare_test 已有导出存在同一 VIN 上两个 DC 源，VIP/VIN 又有固定源和 PWL 的候选约束冲突；输入/输出还交叉连接。运行前逐新网表核对，学习副本采用明确共模与差分，源工程保持不改。噪声 TB 名称不证明随机噪声启动。

Pipe_SAR/Pi-SAR_amp 有六位第一级、八位第二级、amp_gainboost、D_adjust2 和十二位 DAC observer。需分别验收残差传递、gain/settling 和 code alignment。报告 ENOB 11.6 与 SNR 61.2 dB 的同口径一致性待复查，未当作性能已达成。

ADS8681/ADS1248 顶层文件存在；当前未读取其 OA 层级。官方架构用于选学习主题，逆向模块功能不由名字推定；缺原模型时只作注明条件的拓扑/行为研究。

## 尚未验证与下一步

先前笔记记录 SMIC v1.11_4 与 tsmcN65 独立库映射，原 state 的作者路径、8 位 config 的 calibre 绑定和实际 clock 脉宽需运行前审计。未执行新模型解析、许可证 checkout、Spectre 或后仿。现有 GPDK045 比较器数据属于另一个工程。

下一项：先验收 A01 电荷与位序；随后建立 BOOSTRAP_test 的恢复/工作副本，核对模型及源参数，短 transient 测建立与保持误差。独立目标会话先核对 PID/cwd/port。现有 S04 交替输入实验保持待执行，基础 PLL 与另一个 AFE 分支的记录保留。
