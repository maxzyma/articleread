# Claude Developer Guide：核心功能概览

> **核心总结**：本文介绍 Claude 的核心功能，这些功能增强了 Claude 在处理、分析和生成各种格式内容方面的基本能力。主要功能包括：100 万 token（词元）上下文窗口、Agent 技能、批处理、引用、上下文编辑、Effort 参数、扩展思考、文件 API、PDF 支持、提示词缓存、搜索结果、结构化输出、Token 计数，以及 Bash、代码执行、程序化工具调用、计算机控制等工具。这些功能可通过 Claude API、Amazon Bedrock、Google Cloud Vertex AI 和 Microsoft Foundry 等平台使用。

**文档分类**：开发者文档
**主题**：Claude 核心功能
**更新日期**：2025 年 1 月
**原文链接**：https://platform.claude.com/docs/en/build-with-claude/overview

---

## 简介

这些功能增强了 Claude 在处理、分析和生成各种格式和用例的内容方面的基本能力。

---

## 核心能力

| 功能 | 描述 | 可用性 |
|------|------|--------|
| **100 万 token 上下文窗口** | 扩展的上下文窗口，允许您处理更大的文档、维持更长的对话，并使用更广泛的代码库。 | Claude API (Beta)<br>Amazon Bedrock (Beta)<br>Google Cloud Vertex AI (Beta)<br>Microsoft Foundry (Beta) |
| **Agent 技能** | 通过技能（Skills）扩展 Claude 的能力。使用预构建的技能或使用指令和脚本创建自定义技能。技能使用渐进式披露来高效管理上下文。 | Claude API (Beta)<br>Microsoft Foundry (Beta) |
| **批处理** | 异步处理大量请求以节省成本。每批发送大量查询。批处理 API 调用的成本比标准 API 调用低 50%。 | Claude API<br>Amazon Bedrock<br>Google Cloud Vertex AI |
| **引用** | 在源文档中为 Claude 的响应提供依据。使用引用功能，Claude 可以提供其用于生成响应的确切句子和段落的详细引用，从而产生更可验证、更可信的输出。 | Claude API<br>Amazon Bedrock<br>Google Cloud Vertex AI<br>Microsoft Foundry |
| **上下文编辑** | 使用可配置的策略自动管理对话上下文。支持在接近 token 限制时清除工具结果，以及在扩展思考对话中管理思考块。 | Claude API (Beta)<br>Amazon Bedrock (Beta)<br>Google Cloud Vertex AI (Beta)<br>Microsoft Foundry (Beta) |
| **Effort 参数** | 使用 effort 参数控制 Claude 在响应时使用的 token 数量，在响应完整性和 token 效率之间进行权衡。 | Claude API (Beta)<br>Amazon Bedrock (Beta)<br>Google Cloud Vertex AI (Beta)<br>Microsoft Foundry (Beta) |
| **扩展思考** | 针对复杂任务的增强推理能力，在交付最终答案之前提供对 Claude 逐步思考过程的透明度。 | Claude API<br>Amazon Bedrock<br>Google Cloud Vertex AI<br>Microsoft Foundry |
| **文件 API** | 上传和管理文件以与 Claude 一起使用，而无需在每次请求时重新上传内容。支持 PDF、图像和文本文件。 | Claude API (Beta)<br>Microsoft Foundry (Beta) |
| **PDF 支持** | 处理和分析 PDF 文档中的文本和视觉内容。 | Claude API<br>Amazon Bedrock<br>Google Cloud Vertex AI<br>Microsoft Foundry |
| **提示词缓存（5分钟）** | 为 Claude 提供更多背景知识和示例输出，以降低成本和延迟。 | Claude API<br>Amazon Bedrock<br>Google Cloud Vertex AI<br>Microsoft Foundry |
| **提示词缓存（1小时）** | 扩展的 1 小时缓存持续时间，用于访问频率较低但重要的上下文，补充标准的 5 分钟缓存。 | Claude API<br>Microsoft Foundry |
| **搜索结果** | 通过提供具有适当源归属的搜索结果，为 RAG（检索增强生成）应用程序启用自然引用。为自定义知识库和工具实现网络搜索质量的引用。 | Claude API<br>Amazon Bedrock<br>Google Cloud Vertex AI<br>Microsoft Foundry |
| **结构化输出** | 通过两种方法保证模式（schema）一致性：用于结构化数据响应的 JSON 输出，以及用于验证工具输入的严格工具使用。适用于 Sonnet 4.5、Opus 4.1、Opus 4.5 和 Haiku 4.5。 | Claude API (Beta)<br>Microsoft Foundry (Beta) |
| **Token 计数** | Token 计数使您能够在将消息发送给 Claude 之前确定其中的 token 数量，帮助您就提示词（prompt）和用量做出明智的决策。 | Claude API<br>Amazon Bedrock<br>Google Cloud Vertex AI<br>Microsoft Foundry |
| **工具使用** | 使 Claude 能够与外部工具和 API 交互，以执行更多种类的任务。有关支持的工具列表，请参阅工具表。 | Claude API<br>Amazon Bedrock<br>Google Cloud Vertex AI<br>Microsoft Foundry |

---

## 工具

这些功能使 Claude 能够通过各种工具接口与外部系统交互、执行代码并执行自动化任务。

| 功能 | 描述 | 可用性 |
|------|------|--------|
| **Bash** | 执行 bash 命令和脚本以与系统 shell 交互并执行命令行操作。 | Claude API<br>Amazon Bedrock<br>Google Cloud Vertex AI<br>Microsoft Foundry |
| **代码执行** | 在沙盒环境中运行 Python 代码以进行高级数据分析。 | Claude API (Beta)<br>Microsoft Foundry (Beta) |
| **程序化工具调用** | 使 Claude 能够从代码执行容器中以编程方式调用您的工具，从而减少多工具工作流的延迟和 token 消耗。 | Claude API (Beta)<br>Microsoft Foundry (Beta) |
| **计算机控制（Computer Use）** | 通过截屏和发出鼠标及键盘命令来控制计算机界面。 | Claude API (Beta)<br>Amazon Bedrock (Beta)<br>Google Cloud Vertex AI (Beta)<br>Microsoft Foundry (Beta) |
| **细粒度工具流式传输** | 无需缓冲/JSON 验证即可流式传输工具使用参数，降低接收大参数的延迟。 | Claude API<br>Amazon Bedrock<br>Google Cloud Vertex AI<br>Microsoft Foundry |
| **MCP 连接器** | 直接从 Messages API 连接到远程 MCP（Model Context Protocol）服务器，无需单独的 MCP 客户端。 | Claude API (Beta)<br>Microsoft Foundry (Beta) |
| **记忆** | 使 Claude 能够跨对话存储和检索信息。随着时间推移构建知识库，维护项目上下文，并从过去的交互中学习。 | Claude API (Beta)<br>Amazon Bedrock (Beta)<br>Google Cloud Vertex AI (Beta)<br>Microsoft Foundry (Beta) |
| **文本编辑器** | 使用内置的文本编辑器界面创建和编辑文本文件，以进行文件操作任务。 | Claude API<br>Amazon Bedrock<br>Google Cloud Vertex AI<br>Microsoft Foundry |
| **工具搜索** | 通过使用基于正则表达式的搜索动态发现和按需加载工具，扩展到数千个工具，优化上下文使用并提高工具选择准确性。 | Claude API (Beta)<br>Amazon Bedrock (Beta)<br>Google Cloud Vertex AI (Beta)<br>Microsoft Foundry (Beta) |
| **Web 获取** | 从指定的网页和 PDF 文档中检索完整内容以进行深入分析。 | Claude API (Beta)<br>Microsoft Foundry (Beta) |
| **网络搜索** | 使用来自整个网络的当前真实世界数据增强 Claude 的全面知识。 | Claude API<br>Google Cloud Vertex AI<br>Microsoft Foundry |

---

*来源：Claude Developer Guide - "Features overview"
*原文：https://platform.claude.com/docs/en/build-with-claude/overview*
