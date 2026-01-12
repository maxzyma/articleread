# 文章解析归档项目

## 项目概述

此项目用于从各种来源（小红书、Twitter、博客、官方文档等）提取、整理和归档文章内容。

## 核心规则

### 目录结构

```
articleread/
├── claudecodedocs/              # Claude 相关文档
│   ├── getting-started/         # 入门教程
│   │   ├── claude-code-31-tips.md
│   │   └── claude-code-31-tips.metadata.yaml
│   └── core-features/           # 核心功能
│       ├── build-with-claude-overview.md
│       └── build-with-claude-overview.metadata.yaml
│
├── knowledge&memory/            # 知识与记忆
│   ├── basics/                   # 基础概念
│   │   ├── memory-vs-rag.md
│   │   ├── ai-memory-in-five-scenes.md
│   │   └── *.metadata.yaml
│   ├── solutions/                # 解决方案
│   │   ├── stop-using-rag-for-agent-memory.md
│   │   ├── graphiti-knowledge-graph-memory-guide.md
│   │   └── *.metadata.yaml
│   └── comparison/               # 对比分析
│       ├── rag-vs-memory-for-ai-agents.md
│       └── rag-vs-memory-for-ai-agents.metadata.yaml
│
├── openapidocs/                 # OpenAI 相关文档
│   └── openai-responses-api/
│       ├── openai-responses-api.md
│       └── openai-responses-api.metadata.yaml
│
└── general/                     # 通用主题（未分类）
    └── (预留)
```

### 设计原则

1. **按主题分类**：文章按主题归入不同目录（如 `claudecodedocs`、`knowledge&memory`）
2. **按子主题组织**：每个主题下可根据内容类型划分子主题（如 `basics`、`solutions`、`comparison`）
3. **同级目录平铺**：若无子主题，文章直接放在主题目录下平铺
4. **元数据同级**：文章和元数据放在同一目录，便于管理和引用
5. **相对路径引用**：元数据中的 `content_file` 使用相对路径 `./文章名.md`

### 添加新文章工作流程

当用户要求添加新文章时：

1. **确定主题**：根据文章内容选择合适的主题目录
   - `claudecodedocs` - Claude 相关
   - `knowledge&memory` - 知识图谱、记忆、RAG
   - `openapidocs` - OpenAI 相关
   - `general` - 其他或未分类

2. **确定子主题**（如有）：
   - 若主题有子主题分类，选择合适的子主题目录
   - 若无，直接放在主题目录下

3. **提取内容**：
   - 从网页/图片等来源提取正文内容
   - 整理成干净的 Markdown 文件
   - 去除转发者/中间人的个人评论，保留原作者内容
   - 保留必要的原作者信息和来源说明

4. **语言处理规则**：
   - 文章内容翻译成中文
   - 技术术语格式：中文（英文）
   - 示例：知识工程、神经网络（Neural Network）、Transformer 架构

5. **创建文件**：
   - 正文文件：`主题/子主题/文章名.md`
   - 元数据文件：`主题/子主题/文章名.metadata.yaml`

### 元数据文件模板

```yaml
---
title: "文章标题"
original_title: "原标题（如果不同）"
extraction_date: "YYYY-MM-DD"

source:
  platform: "平台名称（小红书/Twitter/博客等）"
  url: "原始URL"
  forwarder: "转发者（如果有）"
  forwarder_note: "转发者处理说明"

original_author:
  name: "作者姓名"
  title: "作者职位/身份"
  # 其他相关字段

content:
  type: "内容类型（技术教程/观点文章/新闻等）"
  topic: "主题"
  format: "格式（清单/长文/访谈等）"
  # 其他相关字段

extraction_method:
  - "使用的方法（如：Chrome DevTools、图片识别、人工校对）"

verification:
  status: "completed/pending"
  verified_against: "对照来源（原始网页/原始图片等）"
  issues_found_and_fixed:
    - "发现的问题及修复"

content_file: "./文章名.md"

tags:
  - "标签1"
  - "标签2"

notes: |
  其他备注信息
```

### 文件命名规范

- **文章文件**：使用小写字母、数字、连字符，如 `claude-code-31-tips.md`
- **元数据文件**：与文章同名，扩展名为 `.metadata.yaml`
- **主题目录**：使用小写字母、连字符，如 `claudecodedocs`
- **子主题目录**：使用小写字母、连字符，如 `getting-started`

### 示例

**主题目录示例：**
- `claudecodedocs/` - Claude 文档
- `knowledge&memory/` - 知识与记忆
- `openapidocs/` - OpenAI 文档

**子主题目录示例：**
- `knowledge&memory/basics/` - 基础概念
- `knowledge&memory/solutions/` - 解决方案
- `knowledge&memory/comparison/` - 对比分析

**文件示例：**
- 正文：`knowledge&memory/basics/memory-vs-rag.md`
- 元数据：`knowledge&memory/basics/memory-vs-rag.metadata.yaml`

## 提取计划管理

### 嵌套结构设计

项目采用嵌套的 extraction-plan 结构，便于模块化管理各主题的提取任务：

```
articleread/
├── extraction-plan.yaml              # 主计划文件
│   ├── summary                       # 全局统计
│   ├── general                       # General 主题详细计划
│   ├── subplans                      # 其他主题引用
│   └── global_failed                 # 全局失败记录
│
├── claudecodedocs/
│   └── extraction-plan.yaml          # Claude Code 子计划
│
├── claudedocs/
│   └── extraction-plan.yaml          # Claude 文档子计划
│
├── knowledge&memory/
│   └── extraction-plan.yaml          # 知识与记忆子计划
│
└── openapidocs/
    └── extraction-plan.yaml          # OpenAI 文档子计划
```

### 主计划文件（extraction-plan.yaml）

主计划文件包含：
- **summary**: 全局统计信息（需要定期手动更新）
- **general**: General 主题的详细计划（直接管理，不创建子文件）
- **subplans**: 其他主题的引用和摘要
- **global_failed**: 需要特殊处理的跨主题失败任务
- **工作流程说明**: 详细的使用指南

### 子计划文件（主题目录/extraction-plan.yaml）

每个主题目录（general 除外）都有自己的 extraction-plan.yaml 文件：
- **claudecodedocs/extraction-plan.yaml**: Claude Code 相关文档
- **claudedocs/extraction-plan.yaml**: Claude 官方文档
- **knowledge&memory/extraction-plan.yaml**: 知识图谱、记忆与 RAG
- **openapidocs/extraction-plan.yaml**: OpenAI 相关文档

### 状态类型

- **pending**: 待处理
- **in_progress**: 进行中
- **completed**: 已完成
- **failed**: 提取失败
- **skipped**: 已跳过

### 使用方式

#### 添加新文章

1. **General 主题**：
   - 直接在主计划文件的 `general.pending` 中添加
   - 提取完成后在 `general.completed` 中记录

2. **其他主题**：
   - 在对应主题目录下的 `extraction-plan.yaml` 的 `pending` 中添加
   - 提取完成后在该文件的 `completed` 中记录

#### 更新统计

定期更新主计划文件的统计信息：
1. 更新 `summary` 部分的全局统计
2. 更新 `subplans[].summary` 中各主题的统计
3. 保持与子计划文件的一致性

#### 批量处理流程

用户说"继续提取"或"处理待提取文章"时：
1. 读取主计划文件查看全局状态
2. 确定要处理的主题
3. 读取对应主题的子计划文件
4. 从 `pending` 列表取第一个任务
5. 移至 `in_progress`
6. 执行提取流程
7. 完成后移至 `completed` 并记录文件路径
8. 更新主计划文件的统计信息

## 注意事项

- 正文文件末尾可以保留原作者来源说明（如：`*来源：XXX 的 "YYY" 活动*`），但不包含元数据引用
- 元数据文件的 `content_file` 必须使用正确的相对路径 `./文章名.md`
- 主题和子主题的划分应根据内容的相关性和数量来决定
- 验证内容完整性时，应对照原始来源检查是否有遗漏
- 提取任务过程中及时更新 `extraction-plan.yaml` 的状态
