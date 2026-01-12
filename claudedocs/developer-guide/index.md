# Claude Developer Guide 索引

> 本文档提炼 Claude 官方 Developer Guide 的核心要点，作为快速查阅索引。
> 官方文档：https://platform.claude.com/docs

## 目录结构

```
Developer Guide/
├── 入门指南 (First steps)
├── 使用 Claude 构建 (Build with Claude)
│   ├── 功能概览
│   ├── 核心概念
│   └── Capabilities (功能特性)
├── Tools & Agent Skills (工具和代理技能)
│   ├── Tool Use (工具使用)
│   ├── Agent Skills (代理技能)
│   └── Agent SDK (代理开发包)
└── 其他资源
```

---

## 一、入门指南 (First steps)

### 核心 URL
- **Intro to Claude**: https://platform.claude.com/docs/en/intro
- **Quickstart**: https://platform.claude.com/docs/en/get-started

### 关键要点
1. **Claude 模型选择**
   - Claude Sonnet 4.5：平衡性能和成本（推荐）
   - Claude Opus 4.5：最强推理能力
   - Claude Haiku 4.5：最快速度、最低成本

2. **API 密钥获取**
   - 访问 Claude Console: https://console.anthropic.com
   - 创建 API 密钥用于应用集成

---

## 二、使用 Claude 构建 (Build with Claude)

### 2.1 功能概览
**URL**: https://platform.claude.com/docs/en/build-with-claude/overview

**核心功能**：
- Messages API：与 Claude 对话的主要接口
- 流式响应：实时获取生成内容
- 批处理：异步处理多个请求
- 多模态支持：文本、图像、PDF

### 2.2 核心概念

#### Working with Messages (使用消息 API)
**URL**: https://platform.claude.com/docs/en/build-with-claude/working-with-messages

**要点**：
- 使用 Messages API 发送对话
- 支持多轮对话上下文
- 可配置系统提示词
- 支持流式和非流式响应

#### Context Windows (上下文窗口)
**URL**: https://platform.claude.com/docs/en/build-with-claude/context-windows

**要点**：
- 不同模型有不同上下文窗口大小
- Claude 4.5: 200K tokens
- 超出上下文窗口需要使用提示缓存或上下文编辑

### 2.3 Capabilities (功能特性)

#### 提示缓存 (Prompt Caching)
**URL**: https://platform.claude.com/docs/en/build-with-claude/prompt-caching

**关键功能**：
- 缓存系统提示和重复内容
- 减少 API 调用成本
- 提高响应速度
- 适用场景：长对话、重复上下文

#### 上下文编辑 (Context Editing)
**URL**: https://platform.claude.com/docs/en/build-with-claude/context-editing

**关键功能**：
- 自动清理旧的工具结果
- 减少上下文窗口占用
- 保持重要信息
- 适用场景：长对话、复杂工作流

#### 扩展思考 (Extended Thinking)
**URL**: https://platform.claude.com/docs/en/build-with-claude/extended-thinking

**关键功能**：
- 让 Claude 在回复前进行深入思考
- 提高复杂问题的解决质量
- 增加推理透明度
- 适用场景：复杂推理、问题解决

#### Effort (努力程度)
**URL**: https://platform.claude.com/docs/en/build-with-claude/effort

**关键功能**：
- 控制 Claude 的响应详细程度
- 选项：low, medium, high
- 影响 token 使用和响应质量

#### 流式传输 (Streaming)
**URL**: https://platform.claude.com/docs/en/build-with-claude/streaming

**关键功能**：
- 实时接收生成内容
- 提升用户体验
- 支持 Server-Sent Events (SSE)

#### 批处理 (Batch Processing)
**URL**: https://platform.claude.com/docs/en/build-with-claude/batch-processing

**关键功能**：
- 异步处理多个请求
- 降低成本（50% 折扣）
- 适用场景：大批量处理

#### Citations (引用)
**URL**: https://platform.claude.com/docs/en/build-with-claude/citations

**关键功能**：
- Claude 自动引用信息来源
- 支持 Web Search、Web Fetch
- 增强回答可信度

#### 多语言支持 (Multilingual Support)
**URL**: https://platform.claude.com/docs/en/build-with-claude/multilingual-support

**支持语言**：
- 多种自然语言
- 代码理解和生成
- 跨语言能力

#### Token 计数 (Token Counting)
**URL**: https://platform.claude.com/docs/en/build-with-claude/token-counting

**要点**：
- 了解输入/输出 token 使用
- 优化成本
- API 响应中包含 token 计数

#### Embeddings (嵌入)
**URL**: https://platform.claude.com/docs/en/build-with-claude/embeddings

**关键功能**：
- 将文本转换为向量
- 语义搜索
- 相似度计算

#### Vision (视觉)
**URL**: https://platform.claude.com/docs/en/build-with-claude/vision

**关键功能**：
- 理解图像内容
- 多图像输入
- 视觉问答

#### PDF 支持 (PDF Support)
**URL**: https://platform.claude.com/docs/en/build-with-claude/pdf-support

**关键功能**：
- 处理 PDF 文档
- 提取文本和表格
- 表单填写
- 文档合并

#### Files API (文件 API)
**URL**: https://platform.claude.com/docs/en/build-with-claude/files

**关键功能**：
- 上传/下载文件
- 文件持久化
- 与工具配合使用

#### Structured Outputs (结构化输出)
**URL**: https://platform.claude.com/docs/en/build-with-claude/structured-outputs

**关键功能**：
- 强制输出 JSON 格式
- 定义输出模式
- 确保数据一致性

---

## 三、Tools & Agent Skills

### 3.1 Tool Use (工具使用)

#### Overview (概览)
**URL**: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview

**核心概念**：
- Client Tools：客户端工具（Bash、Code Execution、Text Editor）
- Server Tools：服务器端工具（Web Search、Web Fetch）
- MCP (Model Context Protocol)：集成外部工具

#### 工具列表

1. **Bash Tool** - 执行 shell 命令
2. **Code Execution Tool** - 代码执行（沙盒环境）
3. **Text Editor Tool** - 文本编辑（查看、创建、编辑文件）
4. **Web Fetch Tool** - 获取网页内容
5. **Web Search Tool** - 网络搜索
6. **Memory Tool** - 跨会话记忆存储
7. **Tool Search Tool** - 动态工具发现
8. **Programmatic Tool Calling** - 程序化工具调用
9. **Computer Use Tool** - 桌面自动化（Beta）
10. **Fine-grained Tool Streaming** - 细粒度工具流式传输

### 3.2 Agent Skills (代理技能)

**URL**: https://platform.claude.com/docs/en/agents-and-tools/agent-skills

**核心概念**：
- 模块化能力扩展
- 文件系统存储
- 渐进式披露（Progressive Disclosure）
- 三个加载级别：
  1. 元数据（始终加载）
  2. 指令（触发时加载）
  3. 资源和代码（按需加载）

**预构建 Skills**：
- PowerPoint (pptx)
- Excel (xlsx)
- Word (docx)
- PDF (pdf)

**自定义 Skills**：
- 创建领域特定能力
- 打包组织知识
- 跨 Claude 产品使用

### 3.3 Agent SDK (代理开发包)

**URL**: https://platform.claude.com/docs/en/agent-sdk

**核心功能**：
- 构建自主 AI 代理
- 内置工具（Read、Write、Edit、Bash、Glob、Grep）
- Python 和 TypeScript 支持
- 与 Claude Code 相同的代理循环

**关键特性**：
- 自动工具执行
- 权限管理
- Hooks（工具调用前后执行自定义代码）
- Sessions（多轮对话）
- MCP 集成

---

## 四、Prompt Engineering (提示工程)

### URL
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview

### 核心技巧

1. **Clear and Direct** - 清晰直接
2. **Multishot Prompting** - 多示例提示
3. **Chain of Thought** - 思维链
4. **XML Tags** - XML 标签组织
5. **System Prompts** - 系统提示词
6. **Prefill Response** - 预填充响应
7. **Chain Prompts** - 链式提示
8. **Long Context Tips** - 长上下文技巧
9. **Extended Thinking Tips** - 扩展思考技巧

---

## 五、Test & Evaluate (测试与评估)

### URL
https://platform.claude.com/docs/en/test-and-evaluate

### 核心内容

1. **Define Success** - 定义成功标准
2. **Develop Test Cases** - 开发测试用例
3. **Evaluation Tool** - 评估工具
4. **Reduce Latency** - 降低延迟
5. **Strengthen Guardrails** - 加强防护
   - 减少幻觉
   - 提高一致性
   - 缓解越狱
   - 处理流式拒绝
   - 减少提示泄露
   - 保持角色一致性

---

## 六、Administration & Monitoring (管理与监控)

### URL
https://platform.claude.com/docs/en/build-with-claude/administration-api

### 核心 API

1. **Administration API** - 管理 API
2. **Workspaces** - 工作空间管理
3. **Usage and Cost API** - 使用和成本 API
4. **Claude Code Analytics API** - 分析 API

---

## 七、第三方平台集成

### 平台列表

1. **Amazon Bedrock**
   - AWS 托管服务
   - URL: https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock

2. **Google Vertex AI**
   - Google Cloud 托管
   - URL: https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai

3. **Microsoft Foundry**
   - Azure 托管
   - URL: https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry

---

## 八、MCP (Model Context Protocol)

### URL
https://modelcontextprotocol.io/

### 核心 MCP 工具

1. **MCP Connector** - MCP 连接器
2. **Remote MCP Servers** - 远程 MCP 服务器

### 用途
- 连接外部数据源
- 扩展 Claude 能力
- 标准化工具接口

---

## 快速参考

### 常用端点
- **Messages API**: `https://api.anthropic.com/v1/messages`
- **Stream Messages**: 使用 Server-Sent Events

### 必需标头
```
x-api-key: $ANTHROPIC_API_KEY
anthropic-version: 2023-06-01
content-type: application/json
```

### 模型版本
- `claude-sonnet-4-5-20250929` - Claude Sonnet 4.5（推荐）
- `claude-opus-4-5-20251101` - Claude Opus 4.5（最强）
- `claude-haiku-4-5-20251001` - Claude Haiku 4.5（最快）

### Beta 功能标头
- 提示缓存: `anthropic-beta: prompt-caching-2024-07-31`
- 上下文编辑: `anthropic-beta: context-management-2025-06-27`
- Skills: `anthropic-beta: skills-2025-10-02`
- 代码执行: `anthropic-beta: code-execution-2025-08-25`
- Web Fetch: `anthropic-beta: web-fetch-2025-09-10`

---

## 相关资源

### 官方资源
- **Claude Console**: https://console.anthropic.com
- **API Reference**: https://platform.claude.com/docs/en/api/overview
- **Release Notes**: https://platform.claude.com/docs/en/release-notes/overview
- **MCP 官网**: https://modelcontextprotocol.io/

### 社区与支持
- **GitHub**: https://github.com/anthropics
- **Discord**: https://www.anthropic.com/discord
- **Support**: https://support.claude.com/
- **Status**: https://status.anthropic.com/

---

## 文档更新记录

- **2025-01-12**: 创建索引文档，提炼 Developer Guide 核心要点
- 基于 Claude 官方文档 v2025.01

---

> **注意**: 本文档为开发者指南的索引和要点提炼，完整内容请访问 Claude 官方文档。
