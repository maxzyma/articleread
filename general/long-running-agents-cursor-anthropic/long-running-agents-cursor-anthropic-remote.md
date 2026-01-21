# 怎么做 Long-running Agents，Cursor、Anthropic 给了两种截然不同的思路

> 来源：Founder Park（极客公园），2026年1月20日
> 原文链接：https://mp.weixin.qq.com/s/TdrESuxl-SWxfIUg9EMLZg

## 核心观点

**Cursor 和 Anthropic 在实现「Long-running Agents」上采用了两种不同的思路：Cursor 通过多 Agent 并行协作扩展规模；Anthropic 则聚焦于单个 Agent 跨上下文窗口的记忆连续性。**

![Agent 并行协作演示](https://cdn.jsdelivr.net/gh/maxzyma/articleread/general/long-running-agents-cursor-anthropic/images/img-0.gif)

---

## 背景

今天的 Agent（智能体）在一个独立的、短时间任务上的表现已经很不错了。下一步，是怎么让 Agent 能够更长时间地运行，执行更复杂的任务。

业界一直在探索不同的方向：
- 更强大的模型？
- 更长的上下文能力？
- 更复杂的 Multi-Agent（多智能体）架构？

最近 Cursor 和 Anthropic 分享了他们在「Long-running Agents」上的工程实践，有意思的是：**思路不一样，解决方案也不同**。

- **Cursor**：专注通过大规模并行地运行多个 Agent 来执行复杂的、长时任务
- **Claude Code**：侧重解决单个 Agent 在跨越多个工作周期时的「记忆连续性」问题

---

## 01 Cursor：多 Agent 并行协作，引入角色分工

Cursor 的思路是，通过大规模并行地运行多个 Agent 来执行复杂的、长时任务。

Cursor 认为，目前单个 Agent 在处理目标明确、范围有限的「单点任务」时，已经表现得相当出色了。但是针对复杂「项目」时（比如从零开始搭一个全新的软件），能力存在上限。

下一步的方向是像组建人类团队一样，投入成百上千个 Agent 并行工作。但这里的难题是：如何有效地协调这些 Agent，写下超过一百万行代码，处理数以万亿计的 Token（Token）。

### Stripe CEO 对这项研究的评价

![Stripe CEO 对这项研究的评价](https://cdn.jsdelivr.net/gh/maxzyma/articleread/general/long-running-agents-cursor-anthropic/images/img-2.jpg)

### 1.1 在失败中学习：协调机制的两次迭代

Cursor 研究员最初的直觉是，大型项目的开发路径充满了不确定性，在项目启动之初，很难清晰地划分工作。因此，决定从「动态协调」入手：让每个 Agent 根据其他同伴的实时动态，来决定自己下一步该做什么。

#### 第一次尝试：引入锁定机制，扁平化协作

Cursor 构建了一个完全扁平化的系统，在这个系统里，所有 Agent 地位平等，通过访问一个共享文件来进行自我协调。

**流程如下：**
1. 一个 Agent 首先读取这个共享文件，查看其他同伴正在进行的任务
2. 然后，它从任务列表中认领一个尚未被执行的任务
3. 为了防止其他 Agent 同时认领同一个任务，引入了锁定机制，给任务设置一个 lock
4. 完成任务后，它会更新共享文件中的状态，并释放这个 lock

**但这个方案尝试失败了。**

首先，有的 Agent 在执行任务时会锁定过长时间，甚至在任务完成后忘记释放锁，导致其他 Agent 只能排队等待。20 个 Agent 同时工作时，有效吞吐量会骤降到只相当于两三个 Agent 的水平，大量时间被浪费在排队等待上。

其次，这个系统非常脆弱，任何一个环节出错都可能导致连锁反应。比如，一个持有锁的 Agent 可能会因为某些原因意外崩溃，那这个锁就可能永远无法被释放，对应的任务也就被永久阻塞。

此外，还存在 Agent 重复申请自己已持有的锁，甚至在未获得锁的情况下强行更新协调文件，导致整个协作系统陷入瘫痪。

#### 第二次尝试：引入「乐观并发控制」

意识到到锁定机制的局限之后，Cursor 尝试用「乐观并发控制（Optimistic Concurrency Control）」机制来替代原方案。

**简单来说，其逻辑是：**
- Agent 可以随时自由地读取共享文件的状态，不需要等待
- 当一个 Agent 完成任务并准备写入更新时，系统会检查自它上次读取以来，状态文件是否被其他 Agent 修改过
- 如果状态未变，写入成功。如果状态已被修改，本次写入失败，Agent 需要重新读取最新状态，并重新执行任务

这个方案比「锁定机制」更简洁、也更稳健，但暴露了一个更深层次的问题。

**群体性的「畏惧风险」**。在一个没有任何层级、所有个体都平等的结构中，Agent 们表现出了一种强烈的「风险规避」倾向。会主动避开复杂的、具有挑战性的核心任务，倾向于执行细小、安全的代码修改。没有任何一个 Agent 愿意承担起攻克核心难题或负责端到端功能实现的重任。这导致项目在很长一段时间里「原地打转」，毫无进展。

### 1.2「规划者」与「工作者」：引入角色分工

从前两次的失败中汲取教训后，Cursor 决定彻底摒弃扁平化的结构，创建一个职责分明的流水线式协作体系，其中包含三个核心角色：

**规划者（Planner）**
- 定位：类似团队中的架构师或技术负责人
- 核心职责：不是写代码，是持续地探索和分析整个代码库，理解项目需求
- 特殊能力：可以为特定的代码模块派生出「子规划者」，让规划过程本身也能实现并行化

**工作者（Worker）**
- 定位：团队中的主力工程师，纯粹的执行者
- 核心职责：从任务池中领取一个任务，然后心无旁骛地完成它
- 协作方式：不需要与其他「工作者」进行任何形式的沟通或协调，也完全不必关心项目全局。它们只是专注于执行分配给自己的任务，直到完成，然后提交代码

**裁判（Judge）**
- 定位：类似项目经理或质量保证工程师
- 核心职责：在每一个工作周期结束时（比如每隔几小时或完成一定数量的任务后），会有一个 Judge Agent 来评估当前进展，并决定是否继续开始下一轮迭代

这套体系解决了绝大部分的协调难题，能够将项目规模扩展到前所未有的程度，同时避免了任何单个 Agent 因为过度专注于局部陷入到「隧道视野（Tunnel Vision）」中。

### 1.3 实验：数周的持续运行

为了检验这个系统的有效性，Cursor 设定了几个很有挑战性的任务。

**从零构建网页浏览器**
- Agent 团队持续运行了将近一周的时间
- 在 1,000 个独立文件中，编写了超过 100 万行代码
- 成功跑出了一个基础的浏览器
- 尽管代码库规模惊人，新加入的 Agent 依然能够快速理解上下文并做出有意义的贡献
- 数百个「工作者（Agent）」能同时向同一个代码分支提交代码，且冲突率极低

> 📹 **演示视频**：Agent 团队从零构建网页浏览器（8秒）
>
> 虽然看起来像是一张简单的截图，但从零开始构建浏览器极其困难。

![视频封面：从零构建网页浏览器](https://cdn.jsdelivr.net/gh/maxzyma/articleread/general/long-running-agents-cursor-anthropic/images/video-poster.jpg)

**大型代码库原地迁移**
- 另一项实验是在 Cursor 自己的代码库中
- 将一个大型项目的前端框架从 Solid 原地迁移到 React
- 这个任务耗时三周多，产生了 **+266,000 行新增** 和 **-193,000 行删除**
- 虽然这些代码仍然需要人类进行最终的细致审查，但它已经成功通过了「持续集成（CI）」系统和初步的自动化检查

![从 Solid 迁移到 React 的代码合并请求](https://cdn.jsdelivr.net/gh/maxzyma/articleread/general/long-running-agents-cursor-anthropic/images/img-1.jpg)

**产品性能与功能优化**
- 还有一个实验是改进 Cursor 即将发布的一款新产品
- 让一个长期运行的 Agent 负责优化视频渲染模块
- 用 Rust 语言重写了该模块，将渲染速度提升了 **25 倍**
- 同时，还增加了平滑的缩放和平移功能，能够跟随光标，并带有自然的弹簧过渡和运动模糊效果
- 这部分完全由 AI 生成的代码已经被直接合并到主干，很快就会在生产环境中上线

### 1.4 经验与教训

最后，Cursor 研究员进行了经验总结：

**对于超长期任务，模型选择至关重要**
- GPT-5.2 模型在长时间自主工作中表现更佳：它们能更好地遵循指令、保持专注、避免偏离，并且能精确、完整地实现功能
- 相比之下，Opus 4.5 模型倾向于提早结束任务，在方便的时候选择「走捷径」，并迅速交还控制权
- 不同模型擅长扮演不同角色。例如，GPT-5.2 是比 GPT-5.1-Codex 更优秀的「规划者」，虽然 GPT-5.1-Codex 是专门为编码优化的模型
- 现在不再使用通用模型，而是为每个角色选择最适合的模型

**我们的许多改进，来自「做减法」而不是「做加法」**
- 最初设立了一个「集成者」角色，负责质量控制和解决代码冲突
- 结果发现它制造的瓶颈比解决的问题还多
- 事实上，「工作者」Agent 其实已经具备了自行处理冲突的能力

**最好的系统，往往比你想象的更简单**
- 起初试图模仿分布式计算和组织设计中的复杂系统
- 但后来发现，并不是所有的理论都适用于 Agent

**恰到好处的结构，是关键所在**
- 结构太松散，Agent 之间会互相冲突、重复劳动、偏离目标
- 如果结构太严密，系统又会变得脆弱不堪

**系统的绝大部分行为最终都归结于我们如何编写 prompt（提示词）**
- 如何让 Agent 高效协调、避免异常行为，并在长时间内保持专注
- 这些都是需要通过大量的实验来优化的
- 协作框架和模型本身虽然重要，但 prompt 才是重中之重

此外，Cursor 研究员也坦言：多 Agent 协调依然是一个难题，仍然需要进一步探索。目前的系统虽然可行，但远没有达到最优状态。比如：
- 「规划者」应该在任务完成后被自动唤醒，以规划下一步工作
- Agent 偶尔会出现运行时间过长的问题
- 我们仍需通过定期重启来对抗系统性的目标偏离和「隧道视野」

![Cursor CEO Michael Truell 的回应](https://cdn.jsdelivr.net/gh/maxzyma/articleread/general/long-running-agents-cursor-anthropic/images/img-3.jpg)

---

## 02 Claude Code：解决单个 Agent 跨上下文窗口的记忆问题

相比 Cursor，Anthropic 实现「Long Time Run」的思路更轻松一些，核心是：**解决单个 Agent 在跨越多个工作周期时的「记忆连续性」问题。**

想象一下，一个软件团队在做一个大项目，但有一个奇怪的规定：每个工程师只能工作几十分钟，最多几小时，干完就要换一个新的工程师。所以让这个团队完成简单项目任务还行，复杂一点需要长时间运行的项目，比如你让它克隆一个 claude.ai，它就做不到。

这其实就是 Coding Agent 的现状：没有记忆，上下文窗口长度有限。所以要它执行长时间任务，它还做不好。

所以，Anthropic 把重点放在了：如何让 Agent 在跨越多个上下文窗口时依然能持续推进任务。

### 2.1 Agent 在长任务中遇到的主要问题是什么

主要有三种：

**1. 一口气干太多**
比如让 Agent 克隆一个 claude.ai 这样的网站，它会试图一次性搞定整个应用。结果上下文还没用完，功能写了一半，代码乱成一锅粥。下一个会话进来，面对半成品只能干瞪眼，花很多时间猜测前面到底做了什么。

**2. 过早宣布胜利**
项目做了一部分，后来的 Agent 看看环境，觉得好像差不多了，就直接收工。功能缺一大堆也不管。

**3. 测试敷衍**
Agent 改完代码，跑几个单元测试或者 curl 一下接口就觉得万事大吉，根本没有像真实用户那样端到端地走一遍流程。

这三种失败模式的共同点是：Agent 不知道全局目标，也不知道该在哪里停下来、该留下什么给下一位。

### 2.2 参考人类团队的分工协作机制，设计双 Agent 方案

针对这种情况，Anthropic 的解决思路是：**通过引入一个类似人类团队的分工协作机制，将复杂任务拆解成小的可跟踪验证的任务，清晰的交接机制，并且严格验证任务结果。**

研究人员将问题拆成两部分：

**第一步**，需要在初始环境中搭建好提示词要求的全部功能基础，让 Agent 能按步骤、按功能推进。

**第二步**，每次会话中的 Agent 必须每次推进一小步，同时将环境保持在「干净状态」。即能随时安全合并到主分支：没有明显 bug、代码整洁、有清晰文档，开发者随时可以继续加新功能。

按照这种思路，Anthropic 给 Claude Agent SDK 设计了一个双 Agent 方案：

**初始化 Agent（Initializer Agent）**
- 第一次会话用一个专门提示词
- 让模型设置初始环境：生成 init.sh 脚本、claude-progress.txt 工作日志文件，以及一个初始 Git 提交

**编码 Agent（Coding Agent）**
- 在后续会话中接手工作
- 每次只推进一小步，并为下一轮工作留下清晰信息

#### 初始化 Agent

只在项目启动时出场一次，任务是搭好项目运行环境。初始化 Agent 要搭建好所有未来编码会话需要的环境上下文，包括：
- 功能清单（Feature List）
- 渐进式推进（Incremental Progress）
- 测试（Testing）

为避免 Agent 一次性写完整个应用或过早宣布项目完成，研究人员让初始化 Agent 将用户的初始提示，扩展成一个完整的功能需求文件。

例如，在 claude.ai 克隆示例中，它写出了超过 200 个功能，如「用户可以打开新对话、输入消息、按下 Enter，并看到 AI 回复」。

这些功能一开始都标记为「failing」，让后续 Agent 清楚还有哪些功能没完成。

```json
{
  "category": "functional",
  "description": "New chat button creates a fresh conversation",
  "steps": [
    "Navigate to main interface",
    "Click the 'New Chat' button",
    "Verify a new conversation is created",
    "Check that chat area shows welcome state",
    "Verify conversation appears in sidebar"
  ],
  "passes": false
}
```

研究人员要求编码 Agent 只能修改 passes 字段的状态，并明确强调：「不允许删除或修改测试，否则可能导致功能缺失或出现 bug。」

而且，这里有个细节：这个清单不是用 Markdown 来写的，是一个 JSON 数组。因为 Anthropic 在实验后发现，相比 Markdown，模型在处理 JSON 时更不容易随意篡改或覆盖文件。

#### 编码 Agent

在初始化项目后，后续就是编码 Agent 来干活。核心行为准则只有两条：**一次只做一个功能，做完要留下干净的环境。**

编码 Agent 的行为模式被严格地设定为「渐进式推进」，并且遵循一套严谨的工作流程：

**理解现状**：在每个会话开始时，它首先会去阅读 claude-progress.txt 日志文件和 git log 提交历史，来快速了解项目的当前状态。

**单一任务**：从一个明确的功能清单中，选择一个优先级最高的、尚未完成的任务来执行。被严格禁止同时处理多个任务。

**专注实现**：在明确了单一目标后，全力投入到该功能的编码、调试和测试中。

**留下痕迹**：在完成功能开发后，必须将所做的代码修改，连同一条描述清晰的提交信息（commit message），提交到 Git 仓库。同时，还需要在 claude-progress.txt 文件中追加一段新的工作摘要。

这个设计的巧妙之处在于，它把「记忆」外化成了文件和 Git 历史。每一轮的 Agent 不需要依赖上下文窗口里的碎片信息，而是模仿靠谱的人类工程师每天上班会做的事。先同步进度，确认环境正常，再动手干活。

#### 测试环节的改进

研究员发现，Claude 经常在没有充分测试的情况下，就把功能标记为「完成」。它会跑单元测试，甚至用 curl 命令测一下接口，但是发现不了端到端流程里的问题。

问题是很多 bug 只有用户真正操作页面时才会暴露。

**解决方案是，给 Agent 配一个浏览器自动化工具，比如 Puppeteer MCP，并且明确要求它像一个真实用户一样去操作和验证。**

Agent 像真人一样打开浏览器、点按钮、填表单、看页面渲染结果。

这个方法大幅提升了功能验证的准确率。很多只看代码发现不了的 Bug，Agent 自己能定位并修复。

当然也有盲区，比如浏览器原生的 alert 弹窗，Puppeteer 捕捉不到，依赖弹窗的功能容易出 bug。

### 2.3 Agent「开工」的标准流程

所有准备就绪后，每个编码 Agent「上班」第一件事，就是按流程熟悉环境：

1. 运行 pwd 命令，查看当前工作目录：确认当前在哪
2. 阅读 Git 日志和进度文件：快速了解近期完成的工作
3. 阅读功能清单文件：找到优先级最高的未完成任务
4. 运行 init.sh 脚本：启动开发服务器，跑一遍基础测试，确保开工前一切正常

这种方法为 Claude 的每个会话节省了一些 Token，因为它不需要再费力思考如何测试代码。

在这样的设定下，一个典型的会话开始是这样的：

```
[Assistant] I'll start by getting my bearings and understanding the current state of the project.

[Tool Use] <bash - pwd>

[Tool Use] <read - claude-progress.txt>

[Tool Use] <read - feature_list.json>

[Assistant] Let me check the git log to see recent work.

[Tool Use] <bash - git log --oneline -20>

[Assistant] Now let me check if there's an init.sh script to restart the servers.

<Starts the development server>

[Assistant] Excellent! Now let me navigate to the application and verify that some fundamental features are still working.

<Tests basic functionality>

[Assistant] Based on my verification testing, I can see that the fundamental functionality is working well. The core chat features, theme switching, conversation loading, and error handling are all functioning correctly. Now let me review the tests.json file more comprehensively to understand what needs to be implemented next.

<Starts work on a new feature>
```

此外，研究员还总结了，长时间运行的 AI Agent 中四种常见的失败模式和解决方案，包括：过度承诺、过早退出、测试不足和状态不一致等问题。

### 2.4 开放性问题

同样，在最后，Anthropic 也留了一些开放性问题，待进一步探索。

**一个全能 Agent 还是一个专家团队？**
未来是不是需要一个专门的测试 Agent、一个质检 Agent、一个代码清理 Agent，组成一个多 Agent（multi-agent）架构？

**能否跨界？**
这套方法为 Web 开发优化过，未来需要推广到其他领域，比如科学研究、金融建模等等。

---

## 对比总结

| 维度 | Cursor | Anthropic (Claude Code) |
|------|--------|------------------------|
| **核心思路** | 多 Agent 并行协作 | 单 Agent 跨会话记忆连续性 |
| **协调机制** | 规划者-工作者-裁判角色分工 | 初始化 Agent + 编码 Agent 双层结构 |
| **记忆方式** | 通过共享状态文件协调 | 通过 Git 历史 + 进度文件外化记忆 |
| **适用场景** | 超大规模项目（百万行代码） | 复杂功能的渐进式开发 |
| **关键挑战** | Agent 间的协调与冲突 | 跨上下文窗口的状态传递 |

---

## 技术启示

对于正在构建 Agent 系统的开发者：

1. **结构比数量更重要**：无论是 Cursor 的角色分工还是 Anthropic 的渐进式推进，精心设计的协作结构远比简单堆叠 Agent 数量有效

2. **外化记忆**：将 Agent 的记忆外化为文件、Git 历史、进度追踪等持久化存储，是实现 Long-running Agents 的关键

3. **渐进式推进**：让 Agent 每次只完成一个小任务，并留下干净的状态，比试图一次性完成大任务更可靠

4. **严格的测试验证**：像真实用户一样端到端地测试功能，而不仅仅是运行单元测试或 API 调用

5. **Prompt 是关键**：系统的绝大部分行为最终都归结于如何编写 prompt，这比框架和模型选择更重要

---

## 参考资料

- Cursor: [Scaling long-running autonomous coding](https://cursor.com/blog/scaling-long-running-autonomous-coding)
- Anthropic: [Effective harnesses for long-running agents](https://docs.anthropic.com/en/docs/build-with-claude/claude-for-developers)
- 本文编译自 Founder Park 对上述两篇博客文章的整理

---

*翻译整理自 Founder Park 原文，保留了原作者的核心观点和技术细节。*
