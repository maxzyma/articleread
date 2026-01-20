---
name: article-parser
description: 从多个平台提取和整理文章内容到本地文档系统。**核心策略**：遇到小红书/抖音等图片/视频平台链接时，优先搜索同作者/同标题的微信公众号版本。如无微信公众号版本，再使用原平台提取流程。使用时机：用户提供任何平台文章链接、要求提取文章内容或"解析XX文章"时。
---

# 文章解析与归档

## 核心工作流程

### 🎯 优先搜索策略（最重要）

**当用户提供文章链接时，按以下顺序处理**：

#### 情况 1：用户提供小红书/抖音/图片视频平台链接

```
1. 识别作者/标题
   ↓
2. 搜索微信公众号（同作者 + 同标题）
   ↓
3a. 找到 → 使用微信公众号版本 ✅
   ↓
3b. 未找到 → 使用原平台提取 ⚠️
```

**示例流程**：

用户给：小红书链接 `https://www.xiaohongshu.com/explore/69698507000000001a0335b1`

处理步骤：
1. 访问小红书链接，提取：作者="AI信息Gap"，标题="Claude Code之父的工作流火了"
2. 搜索微信公众号：`site:mp.weixin.qq.com "AI信息Gap" "Claude Code"`
3. 找到微信版本 → 使用微信版本（纯文本，更准确）

#### 情况 2：用户直接提供微信公众号链接

直接使用微信版本提取（最优）

#### 情况 3：用户直接提供博客/官网链接

直接提取（通常无引用限制）

---

## 平台优先级

| 优先级 | 平台 | 内容格式 | 提取难度 | 推荐度 |
|-------|------|----------|----------|--------|
| 🥇 1 | 微信公众号 | 纯文本/HTML | ⭐ 简单 | ✅✅✅ 强烈推荐 |
| 🥈 2 | 个人博客/官网 | 纯文本/HTML | ⭐ 简单 | ✅✅ 推荐 |
| 🥉 3 | Medium/Dev.to | 纯文本/HTML | ⭐ 简单 | ✅✅ 推荐 |
| 4 | 知乎/简书 | 纯文本/HTML | ⭐⭐ 中等 | ✅ 可用 |
| 5 | 小红书 | 图片 | ⭐⭐⭐⭐ 复杂 | ⚠️ 备选 |
| 6 | 抖音/B站 | 视频 | ⭐⭐⭐⭐⭐ 最复杂 | ⚠️ 最后选择 |

**原则**：
- ✅ 优先使用文字友好的平台
- ✅ 图片/视频平台仅作为备选
- ✅ 同一内容优先选择文字版本

---

## 优先级原则：微信公众号 > 小红书

**重要**：在提取任何文章前，优先检查是否有微信公众号版本，原因：

| 特性 | 微信公众号 | 小红书 |
|------|-----------|--------|
| 内容格式 | 纯文本/HTML | 图片 |
| 提取难度 | ⭐ 简单 | ⭐⭐⭐⭐ 复杂 |
| 准确性 | ✅ 100% | ⚠️ 依赖OCR |
| 速度 | ⚡ 快速 | 🐌 需要多步处理 |
| 完整性 | ✅ 无遗漏 | ⚠️ 可能遗漏 |

### 0. 优先搜索微信公众号

#### 0.1 搜索流程

**步骤1：使用搜狗微信搜索**

```bash
# 1. 访问搜狗微信搜索
navigate_page -> https://weixin.sogou.com/

# 2. 填写搜索框
fill -> 搜索框
value: "<公众号名称> <文章关键词>"
# 示例：AI信息Gap Claude Code

# 3. 点击搜索按钮
click -> "搜文章"
```

**步骤2：识别目标文章**

从搜索结果中找到目标文章，检查：
- ✅ 公众号名称匹配
- ✅ 文章标题关键词匹配
- ✅ 发布时间合理
- ✅ 内容摘要匹配

**步骤3：访问并提取内容**

```bash
# 直接访问微信公众号文章链接
navigate_page -> <微信文章URL>

# 获取完整内容
take_snapshot -> 提取所有文本内容
```

**步骤4：提取并保存必要配图**

对于非图片/视频识别的文章（如微信公众号），提取并保存必要的配图：

```javascript
// 使用 JavaScript 获取文章中的所有图片
const images = Array.from(document.querySelectorAll('img'));
const articleImages = images
  .map(img => ({
    url: img.src || img['data-src'],
    alt: img.alt || '',
    width: img.width || img.naturalWidth || 0,
    height: img.height || img.naturalHeight || 0
  }))
  .filter(img => img.url && (img.url.includes('mmbiz') || img.url.includes('wx_fmt')));
articleImages;
```

**判断是否为必要配图**：

✅ **应该保留的配图**：
- 技术架构图、流程图
- 界面截图、代码运行效果图
- 数据图表、统计图
- 示意图、说明图
- 文章中的关键配图

❌ **应该忽略的图片**：
- 作者头像
- 公众号二维码
- 分享引导图（"关注我"、"点赞"等）
- 装饰性小图标
- 尺寸过小的图片（宽度 < 200px）
- 明显的广告图片

**判断图片引用限制**：

根据图片来源判断是否需要下载：

| 图片来源 | 是否受限 | 处理方式 |
|---------|---------|---------|
| `mmbiz.qpic.cn` | ✅ 有防盗链 | 下载到本地 |
| `sns-*pic.xhscdn.com` | ✅ 有防盗链 | 下载到本地 |
| `github.com` | ❌ 无限制 | 保留链接 |
| `imgur.com` | ❌ 无限制 | 保留链接 |
| `unsplash.com` | ❌ 无限制 | 保留链接 |
| CDN 链接（`cdn.*`） | ⚠️ 待确认 | 先尝试链接 |
| 其他 | ⚠️ 待确认 | 先尝试链接 |

**处理配图（分两种情况）**：

**情况1：无引用限制 - 保留链接**

```markdown
## 正文内容

![配图说明](https://example.com/image.jpg)

继续文本内容...
```

**情况2：有引用限制 - 下载到本地**

```bash
# 1. 创建图片目录（仅在有需要时创建）
mkdir -p general/YYYY-MM-DD/article-slug/images/

# 2. 下载受限制的图片到本地
for img_url in "${RESTRICTED_IMAGES[@]}"; do
  # 使用 curl 下载，添加正确的 referer
  curl -s \
    -H "Referer: https://mp.weixin.qq.com/" \
    -H "User-Agent: Mozilla/5.0" \
    "$img_url" \
    -o "general/YYYY-MM-DD/article-slug/images/image_${index}.jpg"
done
```

**在 Markdown 中引用本地图片**：

```markdown
## 正文内容

![配图说明](./images/image_1.jpg)

继续文本内容...
```

**图片存储规则**：

| 存储方式 | 适用场景 | 优点 | 缺点 |
|---------|---------|------|------|
| 远程链接 | GitHub、Imgur、Unsplash 等 | 节省空间 | 依赖外部服务 |
| 本地存储 | 微信图片、小红书图片 | 独立稳定 | 占用空间 |

**本地图片目录结构**：
- 存储位置：`文章目录/images/`
- 命名格式：`image_1.jpg`, `image_2.png`, ...
- 仅在必要时创建（有受限制图片时）
- 已在 `.gitignore` 中排除（避免提交大文件）

**建议**：
- 优先使用远程链接（快速、节省空间）
- 仅对有防盗链的图片使用本地存储
- 大文件可考虑上传到图床后使用远程链接

#### 0.2 搜索技巧和具体方法

**从小红书/抖音链接寻找微信公众号版本**：

```bash
# 步骤 1：访问原链接提取基本信息
navigate_page -> <小红书/抖音链接>
take_snapshot -> 提取作者名和标题关键词

# 步骤 2：使用搜狗微信搜索
navigate_page -> https://weixin.sogou.com/
fill -> 搜索框
value: "<作者名> <标题关键词>"
click -> "搜文章"

# 步骤 3：检查搜索结果
# 查找公众号名称和标题都匹配的结果
# 如果找到，点击进入并使用微信版本
# 如果未找到，继续使用原平台提取流程
```

**搜索策略表**：

| 场景 | 搜索策略 | 示例 |
|------|---------|------|
| 小红书链接 | 搜索"作者 + 标题关键词" | `AI信息Gap Claude Code` |
| 抖音链接 | 搜索"作者 + 标题关键词" | `湾仔码农 ralph loop` |
| 知道作者 | `公众号名 关键词` | `AI信息Gap Claude` |
| 知道标题 | 直接搜索标题关键词 | `Claude Code 工作流` |
| 按时间排序 | 找到最新发布的文章 | 搜狗支持时间筛选 |
| 技术文章 | 优先搜微信公众号 | `site:mp.weixin.qq.com "技术关键词"` |

**跨平台搜索优先级**：

1. **搜狗微信搜索**（最推荐）
   - https://weixin.sogou.com/
   - 覆盖最全
   - 更新及时

2. **Google/Bing 高级搜索**
   ```
   site:mp.weixin.qq.com "作者名" "标题关键词"
   "作者名" "标题关键词" 公众号
   ```

3. **微信 APP 搜一搜**
   - 最准确
   - 需要手动操作
   - 适合验证

4. **第三方聚合平台**
   - 新榜：https://www.newrank.cn/
   - 清博：https://www.gsdata.cn/

#### 0.3 备选搜索方案

如果搜狗搜索没有找到，尝试：

1. **Google/Bing 高级搜索**：
   ```
   site:mp.weixin.qq.com "关键词"
   site:mp.weixin.qq.com "作者名" "关键词"
   ```

2. **直接在微信中搜索**：
   - 打开微信 APP
   - 点击"搜一搜"
   - 输入关键词
   - 选择"文章"分类

3. **其他文字友好的平台**：
   - 个人博客/官网
   - Medium/Dev.to（英文）
   - 知乎/简书
   - Medium/Dev.to（英文技术文章）
   - 知乎、简书等

#### 0.4 何时使用小红书流程

只有在以下情况才使用小红书提取流程：
- ❌ 微信公众号没有该文章
- ❌ 其他平台也没有完整版本
- ✅ 用户明确要求从小红书提取
- ✅ 内容是小红书原创（如独家图文/视频笔记）

#### 0.5 小红书访问绕过方法

**问题**：直接访问小红书链接经常被封锁（404, error_code=300031）

**解决方案**：通过首页搜索结果访问（自动添加 xsec_token）

```bash
# 步骤 1：访问小红书首页
navigate_page -> https://www.xiaohongshu.com/

# 步骤 2：使用搜索框搜索
fill -> 搜索框
value: "<作者名> <标题关键词>"

# 步骤 3：按 Enter 执行搜索
press_key -> "Enter"

# 步骤 4：从搜索结果中点击目标文章
click -> <文章标题链接>

# 步骤 5：页面会自动包含 xsec_token 参数，成功访问
```

**关键原理**：
- 直接访问：`https://www.xiaohongshu.com/explore/69698507000000001a0335b1` ❌ 被封锁
- 搜索访问：`https://www.xiaohongshu.com/explore/69698507000000001a0335b1?xsec_token=xxx&xsec_source=pc_search` ✅ 成功

**URL 参数说明**：
- `xsec_token`: 小红书安全令牌，通过搜索结果页面自动生成
- `xsec_source`: 来源标识（如 `pc_search`）

**提取流程调整**：
1. 优先尝试通过首页搜索找到目标文章
2. 点击搜索结果链接（自动带 token）
3. 如果搜索未找到，再尝试直接访问原始链接
4. 如果仍然被封锁，建议寻找其他平台的版本

---

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
- **删除非核心内容**：
  - ❌ "关于作者"部分（个人简介、职位、学历等）
  - ❌ "关注我"、"点赞"、"在看"等引导语
  - ❌ 公众号二维码、推广信息
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
