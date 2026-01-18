---
name: xiaohongshu-parser
description: 从小红书提取和整理文章内容到本地文档系统。支持图文笔记和视频笔记。**重要特性**：自动下载图片/视频到本地以绕过小红书防爬机制。使用时机：用户提供小红书链接、说"从小红书提取这篇文章"或"解析小红书内容"时。
---

# 小红书文章解析

## 内容类型识别

在开始提取前，先判断内容类型：

- **图文笔记**：URL 中不含 `type` 参数或 `type=image`，页面包含多张图片
- **视频笔记**：URL 中包含 `type=video`，页面包含视频播放器

## 工作流程

### 1. 内容提取

#### 1.1 图文笔记

**步骤1：获取图片URL**
- 使用 `take_snapshot` 获取页面文本（标题、作者、标签等）
- 从 snapshot 中找到图片元素的 URL
- 使用 JavaScript 获取所有图片 URL：
  ```javascript
  // 获取所有图片URL
  const slides = Array.from(document.querySelectorAll('.swiper-slide img, [class*="slide"] img'));
  const imageUrls = slides
    .map(img => img.src)
    .filter(src => src.includes('sns-webpic') && (src.includes('spectrum') || src.includes('notes_pre_post')))
    .filter((v, i, a) => a.indexOf(v) === i);
  imageUrls
  ```

**步骤2：缓存图片URL**
- 使用 `scripts/cache_image_urls.sh` 缓存图片 URL 列表：
  ```bash
  # 检查是否有缓存
  CACHED_URLS=$(.claude/skills/xiaohongshu-parser/scripts/cache_image_urls.sh \
    "<文章URL>" "get")

  if [ $? -eq 0 ]; then
    # 使用缓存的 URL
    IMAGE_URLS=($CACHED_URLS)
    echo "使用缓存的 ${#IMAGE_URLS[@]} 个图片 URL"
  else
    # 从页面提取 URL 并保存到缓存
    # 假设 IMAGE_URLS 是从 JavaScript 提取的数组
    .claude/skills/xiaohongshu-parser/scripts/cache_image_urls.sh \
      "<文章URL>" "save" "${IMAGE_URLS[@]}"
  fi
  ```
- **缓存机制**：基于文章 URL 的 MD5 哈希生成缓存文件
  - 相同文章不会重复提取 URL
  - 跨任务、跨会话共享缓存
  - 缓存位置：项目目录 `.cache/xiaohongshu/{hash}_image_urls.txt`
  - 已在 `.gitignore` 中，不会被提交到 git

**步骤3：图片文字提取**
- 使用 `mcp__4_5v_mcp__analyze_image` 分析图片（使用原始 URL）
- 提示词：`"Extract all text content from this image, preserving the original structure and formatting. Be thorough and complete."`
- 逐个处理所有图片 URL
- **防爬注意事项**：如果遇到 403 错误或访问失败，可能需要：
  - 使用 `take_screenshot` 工具截取页面图片，然后进行 OCR
  - 或者等待一段时间后重试

**关键要点**：
- 核心内容通常在图片中，不是 HTML 文本
- 缓存图片 URL 可以避免重复提取，提高效率
- 小红书有防爬机制，如果直接访问图片 URL 失败，使用截图方式
- 图片内容要完整提取，保留原文结构

#### 1.2 视频笔记

**步骤1：获取视频URL和文本内容**
- 使用 `take_snapshot` 获取标题、作者、描述、标签等文本信息
- 导航到小红书视频页面
- 使用 `list_network_requests` 监听网络请求（过滤 `media`、`xhr`、`fetch` 类型）
- 查找以 `sns-video-al.xhscdn.com` 或 `sns-video-hw.xhscdn.com` 开头的 MP4 请求
- 使用 `get_network_request` 获取详细信息并提取视频 URL

**步骤2：缓存视频URL**
- 使用 `scripts/cache_image_urls.sh` 缓存视频 URL（复用同一个脚本）：
  ```bash
  # 保存视频 URL 到缓存
  .claude/skills/xiaohongshu-parser/scripts/cache_image_urls.sh \
    "<文章URL>" "save" "<视频URL>"

  # 或检查缓存
  CACHED_URL=$(.claude/skills/xiaohongshu-parser/scripts/cache_image_urls.sh \
    "<文章URL>" "get")
  ```
- **缓存机制**：基于文章 URL 的 MD5 哈希生成缓存文件
  - 相同文章不会重复提取 URL
  - 跨任务、跨会话共享缓存
  - 缓存位置：项目目录 `.cache/xiaohongshu/{hash}_image_urls.txt`
  - 已在 `.gitignore` 中，不会被提交到 git

**关键要点**：
- 视频使用 blob URL，必须通过监听网络请求获取真实 URL
- 视频笔记的主要内容通常在文本信息中（标题、作者、描述、标签）
- 缓存视频 URL 可以避免重复提取，提高效率
- 元数据中记录视频 URL 供后续查看或下载

### 2. 内容整理

#### 2.1 图文笔记

将提取的内容整理为干净的 Markdown 文档：

- **去除转发者**：删除"大家好，我是XX"、"关注我"等中间人评论
- **保留原文**：完整保留图片中的文字内容，不要总结或改写
  - 逐段记录图片中的文字
  - 保留原始的结构和层级
  - 保留重要的引用、比喻、案例
  - 不要简化或概括技术细节
- **结构化**：使用 Markdown 标题层级组织内容（# ## ###）
- **完整对照**：确保没有遗漏段落，特别是结尾的引用或比喻

**重要原则**：图文笔记的核心价值在图片内容中，必须完整、忠实地提取所有文字，不要因为内容"多"或"杂"而省略或总结。

#### 2.2 视频笔记

**目标受众**：技术人员，需要高效、直接的技术干货。

**内容取舍原则**：

✅ **保留**：
- 技术栈（框架、库、工具）
- 实现流程/步骤
- 核心概念和技术原理
- 代码示例或伪代码
- 视频链接（观看 + 下载）
- 技术限制和注意事项

❌ **删除**：
- 观众反馈、评论区的非技术讨论
- 互动数据（点赞、收藏数）
- 发布时间、标签等非技术信息
- 学习建议、推荐语
- emoji 和非技术化表述

**评论区使用**：
- ✅ 提取：技术栈、实现细节、作者补充说明
- ❌ 忽略：观众评价、使用体验、讨论热度

**标题优化**：
- 去掉 emoji
- 使用技术化表述
- 示例：`"新流派！Vibe Animation教程公开🎏"` → `"Vibe Animation：AI + 手势识别的矢量动画新流派"`

**内容提取**：
- 优先从视频和描述中提取技术信息
- 如无法提取完整代码/步骤，标注为 `pending` 状态
- 在元数据中记录"待完善内容"

### 3. 完整性验证

#### 3.1 图文笔记

对照原始网页检查内容：

- 检查开头和结尾是否完整
- 验证引用、比喻是否遗漏
- 确认技术要点无缺失

#### 3.2 视频笔记

对照原始视频和页面检查：

- 验证视频 URL 可访问性
- 检查文字信息完整性（标题、作者、描述、标签）
- 确认元数据中的视频信息准确（格式、大小）
- 如果视频包含教学内容，验证关键步骤是否已记录

### 4. 文件归档

按照项目 CLAUDE.md 中定义的结构创建文件：

```
general/YYYY-MM-DD/article-slug.md              # 正文
general/YYYY-MM-DD/article-slug.metadata.yaml    # 元数据（与正文同目录）
```

**重要**：
- 元数据和正文放在同一目录，便于管理
- 正文末尾保留原作者来源说明
- 元数据的 `content_file` 使用相对路径 `./article-slug.md`

**文件命名**：使用小写字母、连字符（如 `vibe-animation-tutorial.md`）

## 资源

### scripts/

- **cache_image_urls.sh**：图片/视频 URL 缓存管理脚本
  - 用法：`./cache_image_urls.sh <文章URL> <action> [urls...]`
  - action: `get` (获取缓存), `save` (保存URL), `clear` (清除缓存)
  - 基于文章 URL 的 MD5 哈希生成缓存文件

### references/

- **metadata-template.yaml**：元数据文件模板，包含所有必需字段
- **workflow-guide.md**：详细的分步工作指南和常见问题

### 示例

- **图文笔记**：`general/claude-code-31-tips/` - Claude Code 使用技巧
- **视频笔记**：`general/2026-01-16/vibe-animation-tutorial/` - Vibe Animation 技术教程

参考这些示例了解内容组织和格式规范。
