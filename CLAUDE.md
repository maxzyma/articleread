# 文章解析归档项目

## 自动提交规则

**重要规则：静默自动提交到 GitHub**

- 在合适的时机自动提交并推送到 GitHub
- 无需询问用户或通知
- 提交时机包括：
  - 完成重要工作后
  - 创建或修改文档后
  - 记录讨论内容后
  - 其他有意义的变更

## 项目概述

此项目用于从各种来源（小红书、Twitter、博客等）提取、整理和归档有价值的文章内容。

## 核心规则

### 目录结构

```
articleread/
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
└── general/                     # 通用主题（未分类）
    └── (预留)
```

### 设计原则

1. **按主题分类**：文章按主题归入不同目录（如 `knowledge&memory`）
2. **按子主题组织**：每个主题下可根据内容类型划分子主题（如 `basics`、`solutions`、`comparison`）
3. **同级目录平铺**：若无子主题，文章直接放在主题目录下平铺
4. **元数据同级**：文章和元数据放在同一目录，便于管理和引用
5. **相对路径引用**：元数据中的 `content_file` 使用相对路径 `./文章名.md`

### 添加新文章工作流程

当用户要求添加新文章时：

1. **确定主题**：根据文章内容选择合适的主题目录
   - `knowledge&memory` - 知识图谱、记忆、RAG
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

6. **更新索引**（重要）：
   - 运行 `python3 scripts/update_article_index.py` 更新 `article-index.md`
   - 索引包含：日期、标题、来源、文件路径
   - 按时间倒序排列，方便查找

### 文章格式规范

**目标受众**：技术人员，希望高效获取新知识

**核心原则**：
- ✅ 高效直白，开篇即核心观点
- ✅ 结构化信息（表格、列表、分节）
- ✅ 聚焦技术价值和可操作建议
- ✅ 来源放在标题下方，使用引用格式（低调呈现）
- ❌ 移除评论区、观众反馈等非技术细节
- ❌ 避免冗长的提取说明

#### 正文文件格式模板

```markdown
# 文章标题

> 来源：平台名称 作者名称，YYYY-MM-DD
> 原文链接：https://...

## 核心观点

[一句话总结文章核心价值，加粗关键信息]

---

## 背景：什么是 XXX？

[简要介绍相关概念或背景，2-3句话]

---

## 主要分析

[使用分节、列表、表格等结构化方式组织内容]

### 1. **小节标题**
- 要点1
- 要点2

### 2. **小节标题**
- 要点1
- 要点2

---

## 对比/总结

| 维度 | 说明 |
|------|------|
| 项目1 | 说明 |
| 项目2 | 说明 |

---

## 技术启示

对于正在 XXX 的开发者：

1. **建议1**: 具体建议
2. **建议2**: 具体建议
3. **建议3**: 具体建议
```

#### 格式要点

1. **标题**：简洁直接，聚焦主题
2. **来源**：使用引用块（`>`）放在标题下方、正文之前
3. **开篇**：核心观点立即呈现，无需铺垫
4. **结构**：
   - 使用 `---` 分隔主要章节
   - 使用列表提高可读性
   - 使用表格对比信息
5. **技术术语**：中文在前，英文在后括号标注（如：智能体 Agent）
6. **移除内容**：
   - ❌ 评论区/观众反馈
   - ❌ 详细的互动数据（播放量、点赞数等）
   - ❌ 作者粉丝数等无关信息
   - ❌ 冗长的"如何提取"说明

#### 元数据文件格式模板（简化版）

```yaml
---
title: "文章标题"
original_title: "原标题（如果不同）"
extraction_date: "YYYY-MM-DD"

source:
  platform: "平台名称"
  url: "原始URL"
  video_id: "视频ID（如有）"
  author: "作者名称"
  publish_date: "YYYY-MM-DD"

content:
  type: "技术观点/教程/分析"
  topic: "主题分类"
  core_point: "一句话总结核心观点"
  key_topics:
    - "关键主题1"
    - "关键主题2"
    - "关键主题3"

extraction_method:
  - "提取方法"

verification:
  status: "completed"
  verified_against: "验证来源"
  notes: "简短说明"

content_file: "./文章名.md"

tags:
  - "标签1"
  - "标签2"
  - "标签3"

notes: |
  核心观点：[一句话总结]

  技术背景：
  - 要点1
  - 要点2

  目标受众：[明确受众群体]
```

#### 元数据简化要点

- ✅ 保留：核心观点、关键主题、技术背景
- ❌ 移除：详细的互动数据、作者粉丝数、冗余字段
- ✅ 聚焦：技术价值和目标受众

### 元数据文件模板（旧版，仅供参考）

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

### 文件和目录命名规范

**基本规则**：使用小写字母、数字、连字符（`-`），避免特殊字符和空格

#### 目录层级

1. **主题目录**：如 `knowledge&memory/`、`general/`
   - 使用短名称，可包含 `&` 等符号
   - 代表大的知识领域

2. **子主题目录**（可选）：如 `basics/`、`solutions/`、`comparison/`
   - 使用小写字母
   - 按内容类型细分

3. **文章独立目录**：如 `claude-code-31-tips/`、`manus-claude-best-agent-model/`
   - 每篇文章包含正文 `.md` 和元数据 `.metadata.yaml` 两个文件时，创建独立目录
   - 目录名基于文章标题转换：小写、连字符替空格、移除特殊字符
   - 示例：
     - `Claude Code 31条秘籍` → `claude-code-31-tips/`
     - `Manus创始人：Claude是做Agent的最佳模型` → `manus-claude-best-agent-model/`

#### 文件命名

- **正文文件**：与目录同名，扩展名 `.md`
  - 如 `claude-code-31-tips.md`
- **元数据文件**：与目录同名，扩展名 `.metadata.yaml`
  - 如 `claude-code-31-tips.metadata.yaml`

#### 完整示例

```
general/
├── claude-code-31-tips/
│   ├── claude-code-31-tips.md
│   └── claude-code-31-tips.metadata.yaml
├── manus-claude-best-agent-model/
│   ├── manus-claude-best-agent-model.md
│   └── manus-claude-best-agent-model.metadata.yaml
└── ralph-loop-claude-code/
    ├── ralph-loop-claude-code.md
    └── ralph-loop-claude-code.metadata.yaml
```

### 示例

**主题目录示例：**
- `knowledge&memory/` - 知识与记忆

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
└── knowledge&memory/
    └── extraction-plan.yaml          # 知识与记忆子计划
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
- **knowledge&memory/extraction-plan.yaml**: 知识图谱、记忆与 RAG

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
9. **更新文章索引**：运行 `python3 scripts/update_article_index.py`

## 注意事项

- 正文文件末尾可以保留原作者来源说明（如：`*来源：XXX 的 "YYY" 活动*`），但不包含元数据引用
- 元数据文件的 `content_file` 必须使用正确的相对路径 `./文章名.md`
- 主题和子主题的划分应根据内容的相关性和数量来决定
- 验证内容完整性时，应对照原始来源检查是否有遗漏
- 提取任务过程中及时更新 `extraction-plan.yaml` 的状态
- **每次新增文章后必须更新 `article-index.md`**，保持索引同步

## 技能管理

### 创建/更新技能的规则

**重要**：创建或更新技能时，必须使用 `skill-creator` 技能。

❌ **错误做法**：直接编辑 `.claude/skills/` 下的文件
✅ **正确做法**：调用 `/skill-creator` 技能，按其指导操作

**理由**：
1. skill-creator 提供标准化的创建流程
2. 自动验证技能结构和质量
3. 确保符合技能最佳实践
4. 生成可分发的 .skill 文件

**操作流程**：
1. 调用 `skill-creator` 技能
2. 描述需要的技能或更新内容
3. 按照 skill-creator 的指导进行操作
4. 使用其提供的 `package_skill.py` 验证和打包

**示例**：
- 创建新技能：使用 `init_skill.py` 脚本
- 更新现有技能：编辑后使用 `package_skill.py` 验证打包
- 分发技能：分享生成的 .skill 文件

**相关文档**：
- skill-creator 技能路径：`.claude/skills/skill-creator/`
- 技能示例：`xiaohongshu-parser.skill`（已打包）

## Ralph Loop 集成

article-parser 技能与 Ralph Loop 可以配合使用，实现自动化迭代提取。

### 适用场景

| 场景 | 说明 | 推荐迭代次数 |
|------|------|------------|
| **批量处理待提取文章** | 持续处理 extraction-plan.yaml 中的 pending 列表 | 10-20 次 |
| **单个复杂文章** | 针对难以提取的文章多次尝试和优化 | 5-10 次 |
| **质量优化迭代** | 重新提取和改进已存在文章的格式、翻译或结构 | 3-5 次 |
| **监控特定平台** | 持续监控并提取特定平台（小红书、Twitter）的新文章 | 无限制（使用完成信号） |

### 使用示例

#### 1. 批量处理待提取文章

```bash
/ralph-loop "使用 article-parser 技能继续处理 extraction-plan.yaml 中的待提取文章列表。完成后输出 <promise>批量提取完成</promise>。" --completion-promise "批量提取完成" --max-iterations 10
```

#### 2. 复杂网页多次尝试

```bash
/ralph-loop "使用 article-parser 技能提取 https://example.com/article。如果提取失败，分析原因并调整策略继续提取。输出 <promise>文章提取完成</promise>。" --completion-promise "文章提取完成" --max-iterations 5
```

#### 3. 优化已有文章

```bash
/ralph-loop "使用 article-parser 技能重新提取并优化已提取文章的格式和质量。输出 <promise>优化完成</promise>。" --completion-promise "优化完成" --max-iterations 3
```

#### 4. 无限制迭代（仅依赖完成信号）

```bash
/ralph-loop "使用 article-parser 技能处理所有待提取文章，直到 extraction-plan.yaml 中没有 pending 状态的任务。输出 <promise>所有文章已提取完成</promise>。" --completion-promise "所有文章已提取完成"
```

### 工作原理

1. **迭代改进**：Ralph Loop 重复相同提示词，每次迭代都能看到上次的文件修改
2. **自动重试**：如果提取失败（网络问题、格式错误等），下次迭代会继续尝试
3. **进度跟踪**：通过修改 `extraction-plan.yaml` 和创建文件，每次迭代都能看到进度
4. **完成控制**：
   - 使用 `<promise>` 标签信号停止
   - 使用 `--max-iterations` 设置最大迭代次数
   - 两者满足任一条件即可停止

### 注意事项

✅ **推荐使用 Ralph Loop 的场景**：
- 需要多次尝试的复杂提取任务
- 批量处理多个文章
- 需要迭代优化格式和质量的场景
- 网络不稳定可能导致重试的任务

❌ **不推荐使用 Ralph Loop 的场景**：
- 简单的单次提取任务（直接使用 article-parser 更高效）
- 需要人工判断或设计决策的任务
- 一次性操作
- 不明确成功标准的调试任务

### 最佳实践

1. **设置合理的迭代次数**：根据任务复杂度设置 `--max-iterations`，避免无限循环
2. **使用明确的完成信号**：提供清晰的 `<promise>` 标签内容
3. **监控进度**：Ralph Loop 会自动显示迭代次数，便于跟踪
4. **随时取消**：使用 `/cancel-ralph` 可随时停止循环
5. **结合 extraction-plan**：让 Ralph Loop 通过更新 extraction-plan.yaml 来跟踪进度
