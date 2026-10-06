# R01：从真实网名读 ADS8681 信号链

问题：TOP_HIER 内为何有 `SAR_ADC` 与 `SAR_ADC_1`，还能看到五路 COMP 输出？先预测：它们是并行测同一输入，还是观测了不同的模拟节点？本课只验收“连接在哪里”，具体分辨率分配与时序不由名称猜测。

入口 `HIX_2012210_TOP/TOP_HIER/schematic`，本轮读取 63 个实例；[顶层原图](../schematics.md#ads8681)。逆向顶层有大量内部 X… 端口，不能把它当作封装 pin map。

| 真实路径 | 端子/网名 | 当前证据 |
| --- | --- | --- |
| MI349/PGA | AIN_P、AIN_GND→VOM=`R2086_PLUS`，VOP=`R7526_PLUS` | 外部输入到前端输出已核对 |
| MI381/SWITCH_CAP_2 | VI=`R2086_PLUS`→VO=`C19_MINUS`，VO5=`C638_PLUS` | 一路前端进入 SC 网络 |
| MI385/SWITCH_CAP_2S1 | VI=`R7526_PLUS`→VO=`C7752_MINUS`，VO5=`C8001_PLUS` | 另一差分侧进入相应网络 |
| MI440/COMP_BLOCK | VM=`C19_MINUS`，VP=`C7752_MINUS`；VI1=`C8001_PLUS`，VI2=`C638_PLUS` | 主输入与额外输入分开，不等同单一 comparator |
| MI427/SAR_ADC_1 | VI1/VI2=`R2086_PLUS`/`R7526_PLUS`，另接两侧 VO1…VO4 | 与前端及中间节点同时相连 |
| MI428/SAR_ADC | VI1/VI2=`C638_PLUS`/`C8001_PLUS` | 与 COMP_BLOCK 的一对额外输入共网，顺序不同 |

MI427、MI428 可见输出均为 `Q<5:0>`，这只是这两个子块的接口，不能写成“两颗六位 ADC 相加得到十六位”。COMP_BLOCK 内有 AMP_STAGE1/2/3、五个 COMP_2 变体、bias 和 control，输出包含 Q/QN 及 QS/QNS。需要继续追数字合成、决策时刻和冗余才能判断位数分配。

工程研读实验：用上表在原图标出两条差分路径，再找反向边，例如 MI406/TRIGATE_1 从前端输出返回 PGA 的 VI1/VI2。记录开关控制，不把有边就解释成持续导通反馈。用 OA 端子表核对线交叉与同网标签，图片上看不到的连接不能补画。

证据分析：连接说明有哪些模块互相加载，不说明哪个模块在哪个转换阶段有效。设计判断是先分前端、SC、前置放大、判决与数字校正，再恢复状态机。若无法确定某个控制端状态，就把它列入接口缺口。

验收：提交上述六行的自己的带网名框图，指出至少一条尚未闭合的时序边。下一课 [R02](R02-frontend.md) 只追 AMP_1 到一侧 AMP_2。本课没有仿真。
