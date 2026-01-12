# 使用知识图谱（Knowledge Graph）记忆构建 AI 智能体（Agent）：Graphiti 全面指南

> **核心总结**：现代 AI 智能体（Agent）正在超越简单的向量数据库（Vector Database），转向复杂的时间知识图谱（Temporal Knowledge Graph）以实现类似人类的记忆。Graphiti 是一个开源框架，能够从非结构化交互（episodes，情节）中自动提取结构化知识，构建时间知识图谱。本文深入探讨了 Graphiti 的架构、核心组件（情节管理、实体提取与解析、关系建模、时间推理引擎）、安装配置、使用方法以及实际应用场景。

**副标题**：现代 AI 智能体（Agent）如何超越简单的向量数据库（Vector Database），转向复杂的时间知识图谱（Temporal Knowledge Graph）以实现类似人类的记忆

**发布日期：** 未注明
**分类：** AI 架构 / 知识图谱（Knowledge Graph）教程
**作者：** Saeed Hajebi
**来源：** [Medium](https://medium.com/@saeedhajebi/building-ai-agents-with-knowledge-graph-memory-a-comprehensive-guide-to-graphiti-3b77e6084dec)

---

## 1. 引言：AI 智能体（Agent）的记忆危机

想象一下一个 AI 助手，它不仅记得你昨天告诉它什么，还理解这些信息如何与你上个月的目标联系起来，识别你随时间的行为模式，并能够推理对话中不同信息片段之间的关系。这不是科幻小说——这是基于知识图谱（Knowledge Graph）的记忆系统（如 Graphiti）的承诺。

传统 AI 智能体（Agent）遭受着我们可能称为"数字健忘症"的困扰。它们要么在会话之间忘记一切，要么依赖粗糙的向量相似度搜索（Vector Similarity Search），错过了人类知识和体验的丰富、相互联系的本质。虽然检索增强生成（RAG）系统改善了信息检索，但它们仍然将记忆视为孤立的文档，而不是随时间演变的相互关联的体验。

Graphiti 是一个开源框架，为 AI 智能体（Agent）带来了时间知识图谱（Temporal Knowledge Graph），使它们能够构建、维护和推理复杂的记忆网络，镜像人类的实际思考和记忆方式。

在本全面指南中，我们将探讨 Graphiti 如何革命性地改变 AI 智能体（Agent）的记忆，从其理论基础到实际实现、性能考虑和现实世界应用。

---

## 2. 当前记忆解决方案的问题

### 2.1 当前方法的局限性

大多数现代 AI 应用依赖向量数据库（Vector Database）和检索增强生成（RAG）系统进行记忆和上下文检索。虽然这种方法在文档搜索和基本问答方面证明有效，但在构建复杂的 AI 智能体（Agent）时，它暴露了根本局限性，这些智能体（Agent）需要：

- 理解时间关系
- 跟踪实体（Entities）演变
- 推理复杂网络
- 跨会话维持连贯的身份

### 2.2 核心挑战

挑战不仅仅是找到相关信息——而是理解信息如何连接、演变，以及跨时间和上下文的关系。传统方法在以下方面挣扎：

**时间上下文（Temporal Context）**：理解事件何时发生以及事实如何随时间变化

**实体解析（Entity Resolution）**：识别不同提及是否指代同一实体

**关系推理（Relationship Reasoning）**：理解实体（Entities）之间复杂的关系网络

**知识演化（Knowledge Evolution）**：处理新旧信息的冲突和更新

### 2.3 超越向量相似度（Vector Similarity）

向量相似度（Vector Similarity）虽然强大，但仅捕获语义相似度。两段文本可能在语义上相似但在时间上无关，反之亦然。我们需要的是一个不仅能理解语义含义，还能理解时间上下文（Temporal Context）、实体关系（Entity Relationships）和知识演化的系统。

### 2.4 我们真正需要的是什么

人类记忆不仅仅是文档的集合——它是体验、关系和时间理解的丰富、相互关联的网络。我们需要 AI 记忆系统能够：

- **理解时间**：知道事情何时发生以及如何变化
- **解析实体（Entities）**：识别跨不同上下文的同一实体
- **推理关系**：理解实体（Entities）之间的复杂连接
- **演化知识**：随着新信息的出现而更新和理解

---

## 3. 知识图谱（Knowledge Graph）：缺失的一环

### 3.1 什么是知识图谱（Knowledge Graph）？

知识图谱（Knowledge Graph）是现实世界实体（Entities）及其关系的结构化表示。与传统数据库将数据存储在表或文档中不同，知识图谱（Knowledge Graph）将信息建模为相互连接的节点（实体（Entities））和边（关系（Relationships））网络。

知识图谱（Knowledge Graph）的基本构建块是三元组：（主体，谓语，客体）。例如：
- (Alice, WORKS_ON, 认证服务项目)
- (认证服务项目, PART_OF, 移动应用)

### 3.2 为什么知识图谱（Knowledge Graph）对 AI 重要

知识图谱（Knowledge Graph）为 AI 应用提供了几个优势：

**结构化知识**：显式建模实体（Entities）和关系（Relationships）

**推理能力**：能够遍历图以发现复杂的关系

**灵活模式**：轻松适应新的实体（Entities）类型和关系（Relationships）

**上下文丰富**：捕获传统方法错过的丰富关系网络

### 3.3 时间维度（Temporal Dimension）

传统知识图谱（Knowledge Graph）通常是信息的静态快照。然而，现实世界的知识随时间演变：

- 用户偏好改变
- 项目状态更新
- 关系形成和结束

时间知识图谱（Temporal Knowledge Graph）通过建模不仅是什么是真实的，还有它何时是真实的以及它如何随时间变化来解决这个问题。

### 3.4 从情节（Episodes）到知识

Graphiti 创新之处变得清晰的地方。与需要手动知识图谱（Knowledge Graph）构建不同，Graphiti 自动从非结构化交互（情节，episodes）中提取结构化知识。

**情节（Episodes）示例：**
```
"Alice 提到她完成了认证服务。Bob 由于数据库架构冲突被数据库迁移阻塞。团队决定将移动应用发布推迟到二月。"
```

**从每个情节（Episode），Graphiti 提取：**
- **实体（Entities）**：Alice、Bob、认证服务、数据库迁移、移动应用
- **关系（Relationships）**：Alice COMPLETED 认证服务、Bob BLOCKED_ON 数据库迁移
- **时间信息**：事件发生的时间
- **上下文**：情节（Episode）的来源和描述

这种自动提取将 AI 交互的混乱、非结构化世界转化为干净的、可查询的知识图谱（Knowledge Graph）。

---

## 4. Graphiti 架构：AI 的时间知识图谱（Temporal Knowledge Graph）

### 4.1 高级概述

Graphiti 的架构围绕来自情节（Episodic）数据的时间知识图谱（Temporal Knowledge Graph）构建为中心。让我们分解关键组件：

```
情节（Episode）→ [提取] → 图更新 → [检索] → 上下文
```

系统由几个关键层组成：

**情节（Episode）管理层**：接收和处理原始数据

**提取引擎**：使用大语言模型（LLM）提取实体（Entities）和关系（Relationships）

**图存储**：持久化知识图谱（Knowledge Graph）

**检索引擎**：搜索和检索相关上下文

**时间推理**：理解和推理时间信息

### 4.2 核心组件深入分析

#### 4.2.1 情节（Episode）管理

情节（Episode）代表信息或交互的离散单元。Graphiti 处理情节（Episodes）以提取：

- **实体（Entities）**：提到的人、地点、事物
- **关系（Relationships）**：实体（Entities）之间的连接
- **时间信息**：事件何时发生
- **上下文元数据**：来源、描述等

#### 4.2.2 实体（Entity）提取和解析

Graphiti 最复杂的特性之一是实体解析（Entity Resolution）——确定不同提及何时指代同一现实世界实体的能力。

**场景示例：**
- "Alice Smith 说..."
- "Alice 提到..."
- "史密斯女士指出..."

传统系统可能会创建三个独立的实体（Entities）。Graphiti 使用基于大语言模型（LLM）的实体提取和基本名称匹配技术来识别不同提及何时可能指代同一实体，尽管这种解析的复杂性取决于底层大语言模型（LLM）的能力和提及的相似性。

#### 4.2.3 关系（Relationship）建模

Graphiti 中的关系（Relationships）不仅仅是简单的连接——它们是随时间可以演变的丰富时间结构。

**关系（Relationship）结构：**
- **主体**：关系的源实体（Entity）
- **谓语**：关系类型（例如：WORKS_ON、BLOCKED_BY）
- **客体**：目标实体（Entity）
- **时间属性**：created_at、valid_at、invalid_at、expired_at

Graphiti 将关系（Relationships）存储为具有以下关键属性的 EntityEdge 对象：

- **created_at**：Graphiti 学习关系的时间
- **valid_at**：关系变为真实的时间
- **invalid_at**：关系变为不真实的时间
- **expired_at**：Graphiti 学习它不再有效的时间

#### 4.2.4 时间推理引擎

Graphiti 的时间推理能力使其能够理解：

- 事实何时为真
- 事实如何随时间变化
- 事件之间的因果链接
- 时间重叠和序列

**查询示例**："数据库迁移开始时 Alice 在做什么？"

这需要理解：
- 数据库迁移何时开始
- Alice 在那个时候的工作状态
- 时间线上的事件顺序

#### 4.2.5 图存储架构

Graphiti 通过驱动抽象层支持多个图数据库后端：

**数据库特性：**
- **Neo4j**：完全支持，时间属性
- **其他**：通过抽象层支持

**示例 Neo4j 模式：**

```cypher
// 实体（Entities）
CREATE (alice:Person {name: "Alice", entity_type: "person", uuid: "..."})
CREATE (project:Project {name: "认证服务", entity_type: "project"})

// 带时间属性的关系（Relationships）
CREATE (alice)-[:WORKS_ON {start_date: "2024-01-01", status: "active"}]->(project)

// 情节（Episodes）
CREATE (episode:Episode {name: "standup_2024_01_15", valid_at: "2024-01-15T10:00:00Z"})
CREATE (episode)-[:MENTIONS]->(alice)
CREATE (episode)-[:MENTIONS]->(project)
```

---

## 5. 安装和配置

在安装 Graphiti 之前，确保你有：

- Python 3.9 或更高版本
- Neo4j 数据库实例

### 5.1 安装 Graphiti

```bash
# 从 PyPI 安装 Graphiti
pip install graphiti-core

# 安装带可选大语言模型（LLM）提供程序依赖
pip install graphiti-core[anthropic]     # Anthropic Claude 支持
pip install graphiti-core[groq]          # Groq 支持
pip install graphiti-core[google-genai]  # Google Gemini 支持
```

### 5.2 Neo4j 配置

Graphiti 需要 Neo4j 数据库进行图存储。你有几个选项：

```bash
# 启动 Neo4j 容器
docker run \
    --name neo4j \
    -p 7474:7474 -p 7687:7687 \
    -d \
    -e NEO4J_AUTH=neo4j/password \
    neo4j:latest
```

### 5.3 环境配置

创建一个 `.env` 文件，包含你的配置：

```bash
# Neo4j 配置
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# 大语言模型（LLM）配置（选择一个）
OPENAI_API_KEY=your_openai_key_here
# OR
ANTHROPIC_API_KEY=your_anthropic_key_here
```

---

## 6. 使用 Graphiti

### 6.1 情节（Episodes）类型

Graphiti 通过 EpisodeType 枚举支持各种情节（Episode）类型，每种针对不同类型的信息进行优化：

**1. 消息情节（Message Episodes）**
- 聊天消息
- 对话语句
- 用户交互

**2. 文档情节（Document Episodes）**
- 文档
- 文章
- 报告

**3. JSON 数据情节（JSON Data Episodes）**
- 结构化数据
- API 响应
- 数据库记录

**可用的 EpisodeType 值：**
- `text`：通用文本内容
- `message`：聊天/消息数据
- `document`：文档内容
- `json`：JSON 数据

### 6.2 初始化 Graphiti

```python
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from datetime import datetime, timezone

# 初始化 Graphiti 客户端（本地 Neo4j 示例）
client = Graphiti(
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password"
)

# 添加一个情节（Episode）（对话、文档、事件）
episode = await client.add_episode(
    name="weekly_standup_2024_01_15",
    episode_body=(
        "Alice 提到她完成了认证服务。"
        "Bob 由于架构冲突被数据库迁移阻塞。"
        "团队决定将移动应用发布推迟到二月。"
    ),
    source=EpisodeType.text,
    source_description="每周团队站会",
    reference_time=datetime.now(timezone.utc)
)
```

### 6.3 搜索实体（Entities）

```python
# Graphiti 自动处理实体解析
# 使用搜索查找实体及其信息
entity_results = await client.search("Alice Smith 信息", num_results=10)

for result in entity_results:
    print(f"实体事实：{result.fact}")
    if hasattr(result, 'created_at') and result.created_at:
        print(f"首次出现：{result.created_at}")
```

### 6.4 搜索关系（Relationships）

```python
# 使用搜索查询关于连接的事实
relationship_results = await client.search(
    query="Alice 雇佣工作关系",
    num_results=10
)

# 搜索结果包含关系事实
for result in relationship_results:
    print(f"关系事实：{result.fact}")
    if hasattr(result, 'created_at') and result.created_at:
        print(f"创建时间：{result.created_at}")
```

### 6.5 完整示例

```python
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from datetime import datetime, timezone

# 初始化 Graphiti 客户端
client = Graphiti(
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password"
)

# 添加你的第一个情节（Episode）
await client.add_episode(
    name="first_conversation",
    episode_body="你好，我是 Alice，一名从事机器学习项目的软件工程师。",
    source=EpisodeType.text,
    source_description="初始用户介绍",
    reference_time=datetime.now(timezone.utc)
)

# 搜索信息
results = await client.search("Alice 软件工程师", num_results=5)

for result in results:
    print(f"找到：{result.fact}")
```

---

## 7. 大语言模型（LLM）集成

Graphiti 在管道的几个关键点使用大语言模型（Large Language Models, LLMs）：

**实体提取**：从文本中识别实体（Entities）

**关系提取**：识别实体（Entities）之间的关系

**实体解析**：确定提及何时指代同一实体

**摘要生成**：创建情节（Episodes）的摘要

该系统设计为大语言模型（LLM）无关的，支持：

- OpenAI (GPT-4, GPT-3.5)
- Anthropic Claude
- Groq
- Google Gemini
- 其他兼容 OpenAI API 的提供程序

---

## 8. 性能考虑

Graphiti 通过以下方式优化性能：

- **增量更新**：不需要完全重新计算
- **缓存机制**：减少重复的大语言模型（LLM）调用
- **并行处理**：同时处理多个情节（Episodes）
- **高效存储**：优化的图数据库模式

查询性能通常在毫秒范围内，使其适合实时应用。

---

## 9. 现实世界应用

**客户支持**：跟踪客户问题和解决方案随时间的演变

**个人助手**：记住用户偏好和上下文跨会话

**研究工具**：组织和连接研究发现的复杂网络

**项目管理**：跟踪项目状态、依赖关系和团队成员贡献

---

*来源：Medium - Saeed Hajebi*
