# Claude Developer Guide 中文翻译

> 按照 `read` 项目标准组织的 Claude 开发者文档中文翻译

## 📁 目录结构

```
developer-guide/
├── articles/          # 干净的 Markdown 正文（可分享）
│   └── build-with-claude-overview.md
├── metadata/          # YAML 元数据文件
│   └── build-with-claude-overview.yaml
└── README.md
```

## 📝 文件说明

### articles/
干净的 Markdown 文件，包含中文翻译内容，可直接分享。

**格式特点**：
- 核心总结（顶部）
- 元数据（分类、主题、日期、原文链接）
- 中文翻译内容
- 技术术语格式：中文（英文）
- 底部来源说明

### metadata/
YAML 格式的元数据文件，用于内部管理。

**包含字段**：
- `title`, `original_title`
- `extraction_date`
- `source` (platform, url, language, translation_note)
- `original_author`
- `content` (type, topic, format, sections, section_list)
- `extraction_method`
- `verification`
- `content_file`
- `tags`
- `notes`

## 🎯 翻译规则

1. **全文翻译**：内容翻译成中文
2. **技术术语**：中文（英文）
   - token（词元）
   - RAG（检索增强生成）
   - MCP（Model Context Protocol）
3. **专有名词**：保留原文
   - Claude、API、Sonnet、Opus、Haiku
   - Amazon Bedrock、Vertex AI、Microsoft Foundry

## 📊 翻译进度

### build-with-claude (37 页)
- ✅ overview (1/37)
- ⏳ 待处理：36 页

### agents-and-tools (17 页)
- ⏳ 待提取和翻译

### agent-sdk (6 页)
- ⏳ 待提取和翻译

### api (1 页)
- ⏳ 待提取和翻译

### test-and-evaluate (10 页)
- ⏳ 待提取和翻译

**总计**：1/71 页已完成

## 🚀 使用说明

### 查看已翻译文档
```bash
cd articles/
ls *.md
```

### 查看元数据
```bash
cd metadata/
ls *.yaml
```

## 📖 原文来源

- **网站**：https://platform.claude.com/docs/en/home
- **文档**：Claude Developer Guide
- **作者**：Anthropic

## 📅 更新日期

2025-01-12
