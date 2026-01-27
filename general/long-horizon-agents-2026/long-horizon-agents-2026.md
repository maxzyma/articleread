# 红杉对话 LangChain 创始人：2026 年 AI 告别对话框，步入 Long-Horizon Agents 元年

> 来源：微信公众号 海外独角兽，2026-01-27
> 原文链接：https://mp.weixin.qq.com/s/KX-k9r5FOwz2Yu6NQOSD3g

Sequoia Capital 在 **2026: This is AGI** 这篇文章中断言 **AGI 就是把事情搞定（Figure things out）的能力**。

如果说过去的 AI 是 Talkers 的时代，那么 2026 年则是 **Doers 的元年**。转变的核心载体正是 **Long Horizon Agents（长程智能体）**。这类 Agent 不再满足于对上下文的即时回复，而是具备了**自主规划、长时间运行以及目标导向**的专家级特征。

作为 **LangChain 的创始人**，Harrison Chase 一直处于这场变革的最前沿。

---

## 核心观点提炼

- **Long Horizon Agents 价值**在于为复杂任务提供高质量初稿
- **Agent 的突破**需要围绕模型构建的、有主见的（Opinionated）软件外壳（Harness）
- **文件系统权限**将成为所有 Agent 的标配
- **通用 Agent 可能就是一个 Coding Agent**
- **Traces 成为新的 "Source of Truth"**
- **经过长时间磨合、内化了特定任务模式与背景记忆的 Agent**，将形成极高的 moat
- **理想的 Agent 交互**是异步管理和同步协作的统一

---

## 01. Long-Horizon Agents 的爆发

### Harrison Chase：

我同意它们终于开始真正 work 了。让 LLM 在一个循环中运行并自主决策，这一直是 Agent 的核心理念。AutoGPT 就是这样，它之所以能激发人们的想象力，是因为 LLM 在循环中能自主决定下一步做什么。

问题在于，当时的模型不够好，周围的 Scaffolding 和 Harness 也不够好。

**现在模型变强了，我们在过去几年也学到了什么是好的 Harness，所以它们开始真正起作用了。**

我们最先在 **Coding 领域**看到这一点，这也是最快起飞的地方，并正在向其他领域扩散。

虽然你仍需给 Agent 下达指令、提供合适的工具，但它能运行的时间越来越长。所以 **Long Horizon 这个说法非常贴切**。

### 杀手级应用

需长时间运行，产出某项任务初稿的场景，就是 Long Horizon Agents 的杀手级应用。

**Coding 是个典型**。你通常提交一个 PR（Pull Request），而不是直接推送到生产环境。

**AI SREs 也是同理**，通常是把结果提交给人审查。

**生成报告也是**，没人会直接发给所有粉丝，总得自己先看一遍、改一改。

我们在金融领域已经看到了很多这类应用。当一线 AI 搞不定要转人工时，系统不会直接把烂摊子丢给人，而是有一个在后台运行的 **Long Horizon Agent 生成一份前因后果的总结报告**，再移交给人工。

---

## 02. 从通用框架到 Harness 架构

### Framework vs Harness

早期我们就是这样定义 LangChain 的，它本质上是 Agent Framework。但进入 Deep Agents 时代后，我更愿意称之为 **Agent Harness**。

- **模型**：显然就是 LLMs，输入 Token，输出 Token
- **Framework**：围绕模型建立的抽象层，让切换模型、添加工具、Vector Store 和 Memory 变得容易。它是 Unopinionated（无预设）的，价值在于抽象
- **Harness**：更像是开箱即用的。谈到 Deep Agents 时，Harness 默认内置了 Planning tool，它非常 Opinionated（强预设），认为这就是做事的正确方式

### 关键能力

我们需要做压缩。Long Horizon Agent 运行时间很长，虽然 Context Window 变大了，但终究有限。到某个时间点，必须对 Context 进行压缩。

我们提供给 Agent 的另一套关键能力是**文件系统交互**，无论是直接读写还是通过 Bash 脚本。

### Why Now - 共同进化

很难单纯归功于 Harness 或模型，因为现在的模型本身也是在大量此类数据（代码、CLI）上训练出来的。

**这是一种共同进化**。若回到两年前，我不认为我们能预知基于文件系统的 Harness 会是终极方案，因为那时的模型还没针对这些场景充分训练。

所以这是多因素叠加：
- 模型确实变强了，特别是 Reasoning Models 功不可没
- 因为我们搞清楚了围绕压缩、Planning 及文件系统工具的一系列 Primitives（原语）

是这两者的结合带来了突破。

---

## 03. Coding Agent 是通用 AI 的终局形态吗

### 核心理念

我也想知道。但我确信，**"让 LLM 在循环中运行并自我编排的算法，让它自己决定把什么拉入 Context"**这一极简且通用的 Agent 核心理念，终于实现了。

未来的手工 Scaffolds 会越来越少。目前像压缩这类操作还很依赖 Harness 作者的手动设计。Anthropic 正尝试让模型自主决定何时压缩。

另一个重点是 **Memory**。在长时程任务中，Memory 其实就是长周期的 Context Engineering。核心算法很简单：**Run LLM in a loop**。

接下来的竞争点在于围绕它的 Context Engineering 技巧。

### 通用 Agent = Coding Agent？

我现在最大的疑问是，目前成功的 Harness 大多针对 Coding。即使是非编程任务，你也可以辩称"写代码"本身就是极好的通用手段。

**Harrison Chase：**

这是个大问题。我深信，**构建 Long Horizon Agent 必须给它文件系统权限**。

文件系统在 Context 管理上太有用了。比如压缩时，把原始消息存进文件，只留摘要在 Context 里，模型需要时再去查阅；或者返回巨大的 Tool Call 结果时，不要全塞给模型。把它存进文件系统，让它自己去查。

**所有 Agent 是否最终都是 Coding Agent 也是我们目前思考的最多的问题之一。**

---

## 04. 构建 Long Horizon Agent vs 构建软件

### 本质区别

构建软件时，逻辑全写在代码里，可见可控。

构建 Agent 时，逻辑不全在代码里，很大一部分来自模型。这意味着**你不能只看代码就推断 Agent 在特定场景下的行为，必须实际运行**。

这就是最大区别。我们引入了非确定性黑盒系统，且它置于代码之外。

### Source of Truth 的变化

软件的 Source of Truth（单一事实来源）是代码。

**Agent 的 Source of Truth 是代码 + Tracing。**

这意味着 Trace 成了你思考 Testing 的地方。你更需要 Online Testing，因为行为只有在遇到真实世界输入时才会涌现。

### Tracing 成为团队协作的支点

出问题时，大家不是说"去 GitHub 看代码"，而是说"看看 Trace"。

开源社区也是，用户反馈 Deep Agents 跑偏，我们会要 **LangSmith Trace 而非代码**。

### 更 Iterative

还有一点，构建 Agent 更加 Iterative。软件是你设定好目标再迭代，发布前行为已知。Agent 在发布前行为未知。为了让它达标、通过概念上的 Unit Test，你需要更多迭代。

**这也是为何 Memory 重要。Memory 是从交互中学习。**

---

## 05. 从人类判断到 LLM-as-a-Judge

### Eval 的本质

构建软件和 Agent 的另一个本质区别在于 Eval。传统软件依赖程序化断言，但 Agent 做的是人做的事，评判需引入 **Human Judgment**。

如何把人类判断带入 Traces？

#### 1. 直接引入人

- Data Labeling 公司
- LangSmith 中的 Annotation Queues
- 人直接去标注 Traces，给出自然语言反馈

#### 2. LLM-as-a-Judge

建立人类判断的 Proxies。关键在于确保它与人类判断对齐。

**大多数人在 Evals 中用它来给 Trace 打分**。

但另一个被忽视的领域是，在 **Coding Agents 本身就能看到这一点**。Coding Agent 工作过程遇到 Error，随即纠正这个 Error。这实际是在评判自己之前的工作。

我们在 **Memory** 中也看到了，Memory 很大一部分就是反思 Trace 然后更新东西。

所以，无论是对自己的还是之前的会话，LLM 有充分的能力反思 Trace。本质上，**它们是同一回事**。

### Recursive Self-improvement

其实这听起来像是真正的 **Recursive Self-improvement**。

最理想的状态是 Agent 产出初稿，如修改了 Prompt，然后人类进行审核，确保它不跑偏。

我们推出了 **LangSmith Agent Builder**。其有个很酷的功能是 Memory。当你与 Agent 交互时，如果说"你应该做 Y 而不是 X"，它会修改它自己的 Instructions。

我们正计划增加每晚运行、查看当天 Trace 并更新自身状态的功能，即 **Sleep time compute**。

---

## 06. 未来的交互与生产形态

### Memory 是真正的 Moat

我非常看好 Memory。让 Agent 自我改进很酷，但并非全场景适用。

但在 Agent Builder 里，你构建的是特定工作流。比如我的 Email Agent，之前积累了很多 Memory。后来我想迁移进 Agent Builder，结果丢了旧 Memory。新 Agent 体验远不如旧的。

**这就是为何我认为 Memory 是真正的 Moat。**

### Sync vs Async 模式

我认为需要 **Sync mode（同步模式）** 和 **Async mode（异步模式）** 的结合。

Long Horizon Agent 运行时间长，默认应该是 Async 的。像 Linear、Jira 和 Kanban 看板这类工具，甚至包括 Email，对于构思如何管理这些 Agent 很有参考价值。

但对于大多数 Agent 来说，在某个节点，你一定会想切换到同步沟通模式。

### Hybrid Mode

**未来的交互形态就是 Hybrid Mode**：你异步管理一堆后台运行的 Agent，但在关键时刻，你进入 Sync Mode 与它 Chat，同时你们都在盯着同一个 State 看。

### File System Pilled

关于文件系统，我是坚定的 **"File System Pilled"**。我认为某种形式上，**所有 Agent 都应该能访问文件系统**。

- 关于文件系统：所有 Agent 都应该能访问
- 关于 Coding：我大概 90% 确信这是标配
- 关于 Browser Use：目前的模型还不够好

**所以，Code Sandboxes 绝对是未来的核心组件。**

---

## Pure Async 在目前是跑不通的

一年前，我们发布了 Agent Inbox 第一版，当时的主打概念是 Ambient Agents。Agents 在后台运行，偶尔 Ping 你一下。

最初的版本没有 Sync Mode，它 Ping 你，你回一句，然后只能干等它下次 Ping 你。这种体验非常破碎。

后来我们做了一个巨大的转向。用户点开 Inbox 时，会直接进入 Chat 界面。

**我的判断是：Pure Async（纯异步）在目前是跑不通的。**

除非模型进化到完全不需要 Human-in-the-loop 纠错的程度。否则我们注定要在 Async 和 Sync 之间来回切换。

---

## 总结

红杉这篇访谈揭示了 2026 年 AI 发展的核心趋势：从对话框式的 Talkers 到长程自主执行的 Doers。

Long Horizon Agents 的爆发不是偶然，而是模型能力、Harness 架构和 Context Engineering 共同进化的必然结果。

关键洞察：
1. 文件系统权限是标配
2. Traces 取代代码成为 Source of Truth
3. Memory 形成真正的 Moat
4. Coding Agent 可能是通用 Agent 的终局形态
5. 异步管理 + 同步协作的 Hybrid Mode

2026 年，AI 告别对话框，步入 Long-Horizon Agents 元年。
