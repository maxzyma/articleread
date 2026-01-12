# 小红书文章解析详细工作指南

## 完整工作流程

### 第一步：页面分析

1. **列出浏览器页面**
   ```bash
   使用 mcp__chrome-devtools__list_pages 查看当前打开的页面
   ```

2. **选择小红书页面**
   ```bash
   使用 mcp__chrome-devtools__select_page 选择对应的小红书页面索引
   ```

### 第二步：内容提取

#### 2.1 获取页面快照
```bash
mcp__chrome-devtools__take_snapshot
```
查看页面文本内容，了解文章结构。

#### 2.2 识别图片内容
小红书文章的核心内容通常在图片中：

1. **截取图片**：
   ```bash
   mcp__chrome-devtools__take_screenshot
   ```

2. **提取文字**：
   ```bash
   mcp__4_5v_mcp__analyze_image
   prompt: "提取这张图片中的所有文字内容，保持原有格式和结构"
   ```

3. **多图片处理**：
   - 逐个截取所有图片
   - 按顺序提取文字
   - 拼接成完整内容

### 第三步：内容整理

#### 3.1 创建正文文件

1. **确定日期**：使用当前日期（YYYY-MM-DD）

2. **创建目录**：
   ```bash
   mkdir -p articles/YYYY-MM-DD/
   mkdir -p metadata/YYYY-MM-DD/
   ```

3. **整理内容规则**：
   - 去除转发者评论："大家好"、"关注我"、"点赞收藏"等
   - 保留原创内容：原作者观点、技术要点、引用、比喻
   - 结构化：使用 Markdown 标题（# ## ###）
   - 完整性：确保开头结尾无遗漏

4. **创建正文文件**：`articles/YYYY-MM-DD/article-slug.md`
   - 文件命名：小写字母、连字符、描述性
   - 末尾保留：`*来源：原作者信息*`
   - 不包含：元数据引用

#### 3.2 创建元数据文件

参考 `metadata-template.yaml` 模板，创建 `metadata/YYYY-MM-DD/article-slug.yaml`

**关键字段**：
- `content_file`: 使用相对路径 `../../articles/YYYY-MM-DD/...`
- `extraction_date`: 当前日期
- `verification.status`: "completed"（已验证）或 "pending"（待验证）

### 第四步：完整性验证

对照原始网页检查：

1. **开头检查**：标题、作者、背景介绍是否完整
2. **结尾检查**：引用、比喻、总结是否遗漏
3. **中间检查**：技术要点、步骤说明是否齐全
4. **格式检查**：Markdown 结构是否清晰

发现遗漏时，补充内容并更新 `verification.issues_found_and_fixed`。

## 常见问题

### Q: 如何判断内容是转发者还是原作者？
A: 转发者通常有个人化表述（"大家好，我是XX"），原作者内容更客观专业。

### Q: 图片内容提取不完整怎么办？
A: 使用高分辨率截图，分段提取，手动拼接。

### Q: 元数据文件和正文文件命名不一致会有问题吗？
A: 不会，但建议保持一致便于管理。

### Q: 一天多篇文章如何组织？
A: 在同一天目录下创建多个文件，用描述性名称区分。

## 示例

参考现有示例：
- 正文：`articles/2025-01-11/claude-code-31-tips.md`
- 元数据：`metadata/2025-01-11/claude-code-31-tips.yaml`
