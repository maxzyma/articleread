# 功能概览

探索 Claude 的高级功能和能力。

## 核心功能

这些功能增强了 Claude 在各种格式和用例中处理、分析和生成内容的基本能力。

| 功能 | 描述 | 可用性 |
|------|------|--------|
| **1M token 上下文窗口** | 允许处理更大的文档、维护更长的对话和使用更大型代码库的扩展上下文窗口 | Claude API (Beta)<br>Amazon Bedrock (Beta)<br>Google Cloud's Vertex AI (Beta)<br>Microsoft Foundry (Beta) |
| **Agent Skills** | 使用 Skills 扩展 Claude 的功能。使用预构建的 Skills (PowerPoint、Excel、Word、PDF) 或使用指令和脚本创建自定义 Skills。Skills 使用渐进式披露来高效管理上下文 | Claude API (Beta)<br>Microsoft Foundry (Beta) |
| **批处理** | 异步处理大量请求以节省成本。每批发送大量查询。批处理 API 调用成本比标准 API 调用低 50% | Claude API<br>Amazon Bedrock<br>Google Cloud's Vertex AI |
| **Citations** | 将 Claude 的响应建立在源文档之上。使用 Citations，Claude 可以提供它用来生成响应的确切句子和段落的详细引用，从而产生更可验证、更可信的输出 | Claude API<br>Amazon Bedrock<br>Google Cloud's Vertex AI<br>Microsoft Foundry |
| **上下文编辑** | 使用可配置策略自动管理对话上下文。支持在接近 token 限制时清除工具结果，以及在扩展思考对话中管理思考块 | Claude API (Beta)<br>Amazon Bedrock (Beta)<br>Google Cloud's Vertex AI (Beta)<br>Microsoft Foundry (Beta) |
| **Effort** | 使用 effort 参数控制 Claude 在响应时使用的 token 数量，在响应彻底性和 token 效率之间进行权衡 | Claude API (Beta)<br>Amazon Bedrock (Beta)<br>Google Cloud's Vertex AI (Beta)<br>Microsoft Foundry (Beta) |
| **扩展思考** | 针对复杂任务的增强推理能力，在提供最终答案之前提供对 Claude 逐步思考过程的透明度 | Claude API<br>Amazon Bedrock<br>Google Cloud's Vertex AI<br>Microsoft Foundry |
| **Files API** | 上传和管理文件以与 Claude 一起使用，而无需在每个请求时重新上传内容。支持 PDF、图像和文本文件 | Claude API (Beta)<br>Microsoft Foundry (Beta) |
| **PDF 支持** | 处理和分析 PDF 文档中的文本和视觉内容 | Claude API<br>Amazon Bedrock<br>Google Cloud's Vertex AI<br>Microsoft Foundry |
| **提示缓存 (5分钟)** | 为 Claude 提供更多背景知识和示例输出，以降低成本和延迟 | Claude API<br>Amazon Bedrock<br>Google Cloud's Vertex AI<br>Microsoft Foundry |
| **提示缓存 (1小时)** | 扩展的 1 小时缓存持续时间，用于访问不频繁但重要的上下文，补充标准的 5 分钟缓存 | Claude API<br>Microsoft Foundry |
| **搜索结果** | 通过提供具有适当源归属的搜索结果，为 RAG 应用程序启用自然引用。为自定义知识库和工具实现 Web 搜索质量的引用 | Claude API<br>Amazon Bedrock<br>Google Cloud's Vertex AI<br>Microsoft Foundry |
| **结构化输出** | 通过两种方法保证模式一致性：用于结构化数据响应的 JSON 输出，以及用于验证工具输入的严格工具使用。在 Sonnet 4.5、Opus 4.1、Opus 4.5 和 Haiku 4.5 上可用 | Claude API (Beta)<br>Microsoft Foundry (Beta) |
| **Token 计数** | Token 计数使您能够在向 Claude 发送消息之前确定消息中的 token 数量，帮助您就提示和使用做出明智的决定 | Claude API<br>Amazon Bedrock<br>Google Cloud's Vertex AI<br>Microsoft Foundry |
| **工具使用** | 启用 Claude 与外部工具和 API 交互，以执行更广泛的任务 | Claude API<br>Amazon Bedrock<br>Google Cloud's Vertex AI<br>Microsoft Foundry |

## 工具

这些功能使 Claude 能够通过各种工具接口与外部系统交互、执行代码和执行自动化任务。

| 功能 | 描述 | 可用性 |
|------|------|--------|
| **Bash** | 执行 bash 命令和脚本以与系统 shell 交互并执行命令行操作 | Claude API<br>Amazon Bedrock<br>Google Cloud's Vertex AI<br>Microsoft Foundry |
| **代码执行** | 在沙盒环境中运行 Python 代码以进行高级数据分析 | Claude API (Beta)<br>Microsoft Foundry (Beta) |
| **程序化工具调用** | 启用 Claude 从代码执行容器中以编程方式调用您的工具，从而减少多工具工作流的延迟和 token 消耗 | Claude API (Beta)<br>Microsoft Foundry (Beta) |
| **Computer use** | 通过截取屏幕截图并发出鼠标和键盘命令来控制计算机界面 | Claude API (Beta)<br>Amazon Bedrock (Beta)<br>Google Cloud's Vertex AI (Beta)<br>Microsoft Foundry (Beta) |
| **细粒度工具流式传输** | 在不缓冲/JSON 验证的情况下流式传输工具使用参数，从而减少接收大参数的延迟 | Claude API<br>Amazon Bedrock<br>Google Cloud's Vertex AI<br>Microsoft Foundry |
| **MCP 连接器** | 直接从 Messages API 连接到远程 MCP 服务器，无需单独的 MCP 客户端 | Claude API (Beta)<br>Microsoft Foundry (Beta) |
| **Memory** | 启用 Claude 跨对话存储和检索信息。随时间构建知识库、维护项目上下文并从过去的交互中学习 | Claude API (Beta)<br>Amazon Bedrock (Beta)<br>Google Cloud's Vertex AI (Beta)<br>Microsoft Foundry (Beta) |
| **文本编辑器** | 使用内置的文本编辑器界面创建和编辑文本文件，以执行文件操作任务 | Claude API<br>Amazon Bedrock<br>Google Cloud's Vertex AI<br>Microsoft Foundry |
| **工具搜索** | 通过使用基于正则表达式的搜索动态发现和按需加载工具，扩展到数千个工具，从而优化上下文使用并提高工具选择准确性 | Claude API (Beta)<br>Amazon Bedrock (Beta)<br>Google Cloud's Vertex AI<br>Microsoft Foundry (Beta) |
| **Web fetch** | 从指定的网页和 PDF 文档中检索完整内容以进行深入分析 | Claude API (Beta)<br>Microsoft Foundry (Beta) |
| **Web search** | 使用来自整个 Web 的当前、真实世界的数据增强 Claude 的全面知识 | Claude API<br>Google Cloud's Vertex AI<br>Microsoft Foundry |
