# 停止使用检索增强生成（RAG）作为智能体记忆（Agent Memory）

> **核心总结**：基于我在 AI Engineer World's Faire 的演讲，本文阐述了为什么你不应该使用检索增强生成（RAG）作为记忆机制——以及应该使用什么替代方案。检索增强生成（RAG）作为记忆失败的根本原因在于：它无法处理时间序列、因果关系和事实失效。解决方案是基于时间感知的知识图谱（Knowledge Graph）——Graphiti 框架，它采用双时间记忆模型（Bi-Temporal Memory），能够跟踪事实的创建时间、生效时间、失效时间和过期时间。

**发布日期：** 2025 年 6 月 10 日
**分类：** AI 架构 / 智能体记忆（Agent Memory）
**作者：** Daniel Chalef（Zep AI 创始人）
**来源：** [Zep Blog](https://blog.getzep.com/stop-using-rag-for-agent-memory/)

---

## 问题：会遗忘的智能体（Agent）

我是 Daniel，Zep AI 的创始人。我们为 AI 智能体（Agent）构建记忆基础设施，我来告诉你：**你们处理记忆的方式全都错了。**

嗯，也许不是你直接做的——但很可能是你用来构建智能体（Agent）的框架。

## 我的激进观点

让我明确我的立场：

**激进观点 #1：停止使用检索增强生成（RAG）作为记忆**

**激进观点 #2：知识图谱（Knowledge Graph）是智能体记忆（Agent Memory）的未来**

## 为什么记忆很重要

在深入上述观点之前，让我们先明确为什么这很重要：

我们正在构建的智能体（Agent）普遍遭受三个关键问题的困扰：

**上下文丢失（Lost Context）**：智能体（Agent）忘记过去交互中的重要信息

**通用响应（Generic Responses）**：没有适当的记忆，输出变得不个性化和不准确

**信任侵蚀（Eroded Trust）**：当智能体（Agent）无法记住基本偏好时，用户会失去信心

这绝对不是通往通用人工智能（AGI）的道路——或者更实际地说，这不是留住客户的道路。

---

## 检索增强生成（RAG）记忆问题

让我用一个具体例子说明为什么检索增强生成（RAG）作为记忆会失败：

考虑这个电商场景：

- 用户表达了对 Adidas 运动鞋的喜爱
- 他们的鞋子 2 个月后坏了，导致沮丧
- 用户偏好转向 Puma
- 用户问："我应该买什么运动鞋？"

在基于检索增强生成（RAG）的系统中，查询"我应该买什么运动鞋？"与最初的 Adidas 偏好在语义上最相似。向量数据库（Vector Database）返回那个过时的事实，智能体（Agent）错误地推荐 Adidas——完全忽略了偏好的变化。

**核心问题：**

**时间序列（Temporal Sequence）**：哪个事实先发生？

**因果关系（Causal Relationships）**：鞋子坏了 → 失望 → 偏好改变

**事实失效（Fact Invalidation）**："喜爱 Adidas"应该被后续事件覆盖

---

## 向量嵌入（Vector Embeddings）vs 知识图谱（Knowledge Graph）

以下是问题的可视化表示：

在向量空间中，这些事实作为孤立的点存在，没有明确的关系。查询找到最相似的嵌入（Embedding），但完全错过了因果链和时间上下文（Temporal Context）。

然而，知识图谱（Knowledge Graph）可以用时间有效期显式地建模这些关系。注意图表如何显示：

- "喜爱"关系在特定日期被失效
- "坏了"关系创建了因果链接
- Puma 的新"喜欢"关系当前有效

---

## 介绍 Graphiti

💡 Graphiti 是 Zep Cloud 的核心，Zep 的商业记忆服务。[在此注册。](https://app.getzep.com/api/auth/register)

这引出了我们的解决方案：

**Graphiti** 是 Zep 的开源框架，用于构建**实时、动态的知识图谱（Knowledge Graph）**。它专门设计来解决我概述的记忆问题。

**关键特性：**

**时间感知（Temporally-Aware）**：跟踪事件何时发生以及它们何时被学习

**关系性（Relational）**：实体（Entities）+ 关系（Relationships）+ 社区

**实时（Real-time）**：无需昂贵的重新计算即可动态更新

---

## 秘密武器：双时间记忆（Bi-Temporal Memory）

以下是 Graphiti 的时间模型如何工作。每个事实跟踪四个时间戳：

**created_at**：Graphiti 学习事实的时间

**valid_at**：事件实际发生的时间

**invalid_at**：事实变为不真实的时间

**expired_at**：Graphiti 学习它不再有效的时间

这实现了强大的时间推理："用户在 2 月偏好什么？"变得可回答。

---

## 智能冲突解决

当 Graphiti 遇到冲突信息时，它不只是添加另一个嵌入（Embedding）。相反：

**新事实**："Adidas 鞋子坏了，[用户不高兴]"

**检测到冲突**：这使"喜爱 Adidas"关系失效

**时间解决（Temporal Resolution）**：设置 invalid_at 日期并创建因果边

**结果**：每个偏好的明确时间边界

结果图谱保留了历史，同时清楚地表明当前有效性。这是"更接近人类可能处理和回忆随时间变化状态的方式。"

---

## 不要丢弃嵌入（Embeddings）！

Graphiti 不会放弃嵌入（Embeddings）——它使它们更智能。系统使用混合方法：

**语义搜索（Semantic Search）**：通过嵌入（Embeddings）查找相关内容

**关键词搜索**：BM25 全文搜索特定术语

**子图遍历（Sub-Graph Traversal）**：从初始结果导航关系

**结果融合（Result Fusion）**：结合所有方法以获得全面的上下文

**结果：快速、准确、上下文的检索**，以毫秒而非秒为单位运行。

---

## 特定领域记忆

Graphiti 的强大功能之一是领域建模。心理健康应用需要存储与电商智能体（Agent）非常不同类型的记忆。

Graphiti 允许你使用熟悉的工具（如 pydantic）定义自定义实体（Entities）和边（Edges），给你：

**任何数据源**：动态集成对话和业务数据

**相关检索**：仅检索与应用相关的实体（Entities）和事实

**熟悉的工具**：使用 pydantic 定义你的实体（Entities）和边（Edges）本体

---

## 适合任务的工具

我不是主张在任何地方替换检索增强生成（RAG）。每种方法都有其优势：

| 方法 | 用例 | 更新 | 时间处理 | 查询速度 |
|------|------|------|----------|----------|
| 语义检索增强生成（RAG） | 静态文档（Static Documents） | 批量重新计算 | 共存未解决 | 快速（毫秒） |
| Microsoft GraphRAG | 静态语料库摘要 | 批量重新计算 | 受限于大语言模型（LLM）判断 | 慢（秒） |
| Graphiti | 实时、动态数据 | 实时增量 | 带时间跟踪的边失效 | 快速（毫秒） |

大多数智能体（Agent）应用都可以从同时使用检索增强生成（RAG）方法处理静态知识和 Graphiti 处理动态记忆中受益。

---

## 结论

**智能体记忆（Agent Memory）不是关于知识检索。**

---

## 经过验证的结果

证据在于性能。Zep/Graphiti 在旨在复制复杂现实世界企业场景的基准测试中 crush：

**Zep**：71.2% 准确率
**全上下文基线**：60.2% 准确率

我们发布了一篇详细的架构和性能结果的综合论文。你可以在幻灯片中的 [arXiv 链接](https://zep.link/sota-paper)找到它。

---

## 超越简单记忆

Zep 构建在 Graphiti 之上，超越了简单的智能体记忆（Agent Memory），构建统一的客户记录。它创建一个不断演变的用户图谱，集成：

- 聊天对话
- 来自 SaaS 应用程序的业务数据
- 业务线系统（客户关系管理 CRM、计费等）

这使你的智能体（Agent）能够全面、实时地理解每个用户，使他们能够有效地解决复杂问题。

---

## 开始使用

智能体记忆（Agent Memory）的未来已经到来，它是建立在时间感知的知识图谱（Knowledge Graph）之上的。

准备尝试吗？[git.new/graphiti](https://git.new/graphiti)

Graphiti 框架是[开源](https://github.com/getzep/graphiti)的，今天就可以使用。寻找跨平台的 [模型上下文协议（MCP）记忆服务](https://github.com/getzep/graphiti/blob/main/mcp_server/README.md)？试试我们的 [Graphiti MCP](https://github.com/getzep/graphiti/blob/main/mcp_server/README.md)。

这篇博文基于我最近在 [AI Engineer World's Faire](https://www.ai.engineer/) 2025 关于智能体记忆（Agent Memory）和知识图谱（Knowledge Graph）的演讲。你可以在 [YouTube 上观看完整录制的视频](https://youtu.be/ZNqGFsTyhvg)。

---

*来源：Zep Blog - Daniel Chalef*
