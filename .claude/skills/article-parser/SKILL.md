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

**推荐策略（优先级从高到低）**：

| 优先级 | 存储方式 | 适用场景 | 优点 | 缺点 |
|--------|---------|---------|------|------|
| 🥇 1 | **GitHub 图床** | 微信、小红书等有防盗链的图片 | 免费稳定、CDN加速、版本控制 | 需要配置 token |
| 🥈 2 | 远程链接 | GitHub、Imgur、Unsplash 等无防盗链图片 | 节省空间、无需上传 | 依赖外部服务 |
| 🥉 3 | 本地存储 | 图床上传失败时的降级方案 | 独立稳定 | 占用空间、不在版本控制中 |

**GitHub 图床使用方式**：

```bash
# 上传单张图片
python3 .claude/skills/article-parser/scripts/upload_to_github.py \
  "https://mmbiz.qpic.cn/xxx.jpg" \
  wechat

# 输出: https://cdn.jsdelivr.net/gh/maxzyma/articleread/assets/images/wechat/2026-01/uuid.jpg
```

**配置要求**：

```bash
# 1. 创建 GitHub Personal Access Token
# 访问: https://github.com/settings/tokens
# 权限: repo (full control)

# 2. 设置环境变量（在 ~/.zshrc 或 ~/.bashrc 中添加）
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxx"
export GITHUB_IMAGE_REPO="maxzyma/articleread"
```

**本地图片目录结构**（仅作为降级方案）：
- 存储位置：`文章目录/images/`
- 命名格式：`image_1.jpg`, `image_2.png`, ...
- 仅在图床上传失败时使用
- 已在 `.gitignore` 中排除（避免提交大文件）

**建议**：
- ✅ 优先使用 GitHub 图床（免费、稳定、CDN 加速）
- ✅ 远程链接图片无需上传
- ⚠️ 本地存储仅作为降级方案

**⚠️ 微信公众号图片提取最佳实践（重要）**

根据实际案例（Boris Cherny Claude Code 工作流文章提取），总结了以下关键教训：

**问题1：懒加载导致图片不完整**
- **原因**：微信公众号使用懒加载，初始状态下只有首屏图片加载
- **解决**：必须先滚动到页面底部触发所有懒加载，再提取图片URL
- **操作**：
  ```javascript
  // 滚动到页面底部
  window.scrollTo(0, document.body.scrollHeight);
  // 等待2秒让图片加载
  await new Promise(resolve => setTimeout(resolve, 2000));
  // 再提取图片
  ```

**问题2：占位符 SVG 被误认为真实图片**
- **原因**：未加载的图片显示为 `data:image/svg+xml` 占位符
- **解决**：过滤掉所有 SVG 图片，只保留 `mmbiz.qpic.cn` 的真实图片
- **判断条件**：
  ```javascript
  // ✅ 保留：真实微信图片
  url.includes('mmbiz.qpic.cn') && !url.includes('svg')
  // ❌ 排除：占位符
  url.includes('data:image/svg')
  ```

**问题3：imgIndex 编号不连续**
- **原因**：微信图片的 `#imgIndex=N` 编号不一定连续
- **陷阱**：imgIndex 可能是 0,1,2,3,4,5,6,7（跳过某些数字）
- **解决**：不要假设 imgIndex 连续，必须通过 URL 中的 imgIndex 参数匹配章节

**问题4：广告图片被误当作正文内容**
- **原因**：文章末尾的"推荐阅读"图片也是 mmbiz 域名
- **识别**：通常在倒数第二、第三个 H3 标题之后出现
- **解决**：
  - 检查图片位置：如果在"结语"或"关于作者"之后，很可能是广告
  - 查看图片上下文：如果有链接到其他文章，是推荐图片
  - 人工确认：用 `take_screenshot` 查看图片内容

**问题5：图片位置与章节对应混乱**
- **原因**：图片的 DOM 顺序与文本顺序不一定一致
- **解决方法**：
  1. **方法A：按 imgIndex 匹配**（推荐）
     ```javascript
     // 提取所有图片的 imgIndex
     const imgIndex = url.match(/imgIndex=(\d+)/)?.[1];
     // 按章节顺序分配图片
     ```
  2. **方法B：截图验证**
     - 对每个章节使用 `take_screenshot` 确认是否有图片
     - 逐个对比，确保图片位置正确

**问题6：部分图片需要多次检查**
- **现象**：第03节和第05节最初检查显示"无图片"，但实际有图片
- **原因**：可能是懒加载触发时机不对，或者检查方法有误
- **解决**：
  - 用户反馈"图片遗漏"时，重新用截图验证
  - 使用 `take_snapshot` 查看该章节的完整内容
  - 滚动到该章节位置后再检查

**完整提取流程（推荐）**：

```javascript
// 步骤1：滚动页面触发懒加载
window.scrollTo(0, document.body.scrollHeight);
await new Promise(resolve => setTimeout(resolve, 2000));
window.scrollTo(0, 0);

// 步骤2：提取所有图片URL
const content = document.querySelector('#js_content');
const images = Array.from(content.querySelectorAll('img'));

const mmbizImages = images
  .map((img, idx) => {
    const url = img['data-src'] || img.src;
    const imgIndex = url.match(/imgIndex=(\d+)/)?.[1];
    return {
      index: idx,
      imgIndex: imgIndex,
      url: url,
      isMmbiz: url.includes('mmbiz.qpic.cn') && !url.includes('svg'),
      isPlaceholder: url.includes('data:image/svg')
    };
  })
  .filter(img => img.isMmbiz && !img.isPlaceholder);

// 步骤3：下载图片到本地（带 referer）
// 步骤4：逐个章节截图验证图片位置
// 步骤5：人工确认广告图片并移除
```

**检查清单**：
- [ ] 滚动页面触发懒加载
- [ ] 过滤掉 SVG 占位符
- [ ] 提取所有真实 mmbiz 图片
- [ ] 下载图片到本地并重命名（按 imgIndex）
- [ ] 逐个章节截图验证图片位置
- [ ] 移除文章末尾的广告图片
- [ ] 让用户验证结果

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

### 1.5 验证环节（Validation）⭐ 重要

**目的**：在内容整理之前，对照原文验证提取结果的完整性和准确性，及时发现并修复问题。

#### 验证流程（三步走）

```
提取内容 → 自动验证 → 发现问题 → 修复问题 → 重新验证 → 完成
```

#### 步骤1：自动验证检查清单

**A. 基础信息验证**

```javascript
// 检查标题、作者、发布时间是否完整
const validation = {
  hasTitle: articleContent.includes('## ') || articleContent.includes('# '),
  hasSource: articleContent.includes('> 来源：'),
  hasAuthor: articleContent.includes('作者') || articleContent.includes('原创'),
  hasDate: articleContent.match(/\d{4}年\d{1,2}月/),
};
```

**检查项**：
- [ ] 标题是否提取（一级标题）
- [ ] 来源信息是否完整（平台、作者、时间）
- [ ] 原文链接是否包含

**B. 章节完整性验证**

```javascript
// 检查章节是否完整（以微信公众号为例）
const sections = articleContent.match(/## \d+｜.+/g);
const expectedSectionCount = 9; // 根据原文预期章节数

console.log(`提取章节数: ${sections?.length || 0}，预期: ${expectedSectionCount}`);
```

**检查项**：
- [ ] 章节数量是否合理（不应突然中断）
- [ ] 章节编号是否连续（01, 02, 03...）
- [ ] 是否有截断痕迹（如：段落突然结束）

**C. 图片完整性验证**

```javascript
// 检查图片引用是否正确
const imageRefs = articleContent.match(/!\[.*\]\(\.\/images\/.+\)/g) || [];
const imageFiles = getImageFilesInDirectory(); // 读取 images/ 目录

console.log(`Markdown引用图片: ${imageRefs.length}，实际图片文件: ${imageFiles.length}`);
```

**检查项**：
- [ ] Markdown 中的图片引用数量是否与实际文件数量一致
- [ ] 图片文件是否存在（检查 `./images/xxx.jpg`）
- [ ] 图片命名是否规范（是否有 `image_1_boris_cherny.png` 这样的临时命名）
- [ ] 是否有断开的图片链接（404）

**D. 广告图片检测**

```javascript
// 检测文章末尾可能的广告图片
const lines = articleContent.split('\n');
let foundAdImage = false;
let inConclusion = false;

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (line.includes('## 结语') || line.includes('## 结尾')) {
    inConclusion = true;
  }
  if (inConclusion && line.match(/!\[.*\]\(\.\/images\/.+\)/)) {
    // 结语之后还有图片，可能是广告
    foundAdImage = true;
    console.warn(`发现可能的广告图片（第${i+1}行）: ${line}`);
  }
}
```

**检查项**：
- [ ] "结语"、"关于作者" 之后是否还有图片
- [ ] 倒数第二个章节之后的图片是否为广告
- [ ] 图片上下文是否有链接到其他文章

**E. 文字内容完整性验证**

```javascript
// 检查可能的截断
const lastLines = lines.slice(-10).join('\n');
const truncationPatterns = [
  /…+$/,           // 省略号结尾
  /\[未完\]$/,      // [未完]
  /待续$/,          // 待续
  /\[全文完\]/,     // [全文完]
];

const mightBeTruncated = truncationPatterns.some(p => p.test(lastLines));
```

**检查项**：
- [ ] 文章结尾是否完整（是否有"未完待续"等）
- [ ] 最后一段是否突然中断
- [ ] 是否有明显的截断标记

**F. 格式验证**

```javascript
// 检查 Markdown 格式问题
const formatIssues = [];

// 检查代码块是否闭合
const codeBlocks = articleContent.match(/```/g);
if (codeBlocks && codeBlocks.length % 2 !== 0) {
  formatIssues.push('代码块未闭合');
}

// 检查引用块格式
const quoteMarks = articleContent.match(/^> /gm);
if (quoteMarks && quoteMarks.length > 50) {
  formatIssues.push('引用块可能过长（是否误将正文当作引用？）');
}
```

**检查项**：
- [ ] 代码块是否闭合（``` 成对出现）
- [ ] 引用块格式是否正确
- [ ] 标题层级是否合理（# ## ### 使用正确）

#### 步骤2：发现问题时自动修复

**问题1：图片不完整**
```javascript
// 修复：重新触发懒加载并提取
if (imageFiles.length < expectedImageCount) {
  console.log('⚠️ 图片不完整，重新提取...');
  // 重新滚动页面、提取图片
  await reExtractImages();
}
```

**问题2：章节截断**
```javascript
// 修复：提示需要重新提取文本
if (sections.length < expectedSectionCount - 2) {
  console.log('⚠️ 章节可能截断，请检查原文');
  // 滚动到页面底部重新获取快照
}
```

**问题3：广告图片未移除**
```javascript
// 修复：自动移除结语后的图片
if (foundAdImage) {
  console.log('⚠️ 发现广告图片，自动移除');
  articleContent = removeAdImages(articleContent);
}
```

**问题4：图片引用错误**
```javascript
// 修复：更新图片路径
if (imageRefs.length !== imageFiles.length) {
  console.log('⚠️ 图片引用不匹配，重新命名...');
  await renameAndUpdateImages();
}
```

#### 步骤3：生成验证报告

```javascript
const validationReport = {
  timestamp: new Date().toISOString(),
  articleUrl: currentArticleUrl,
  summary: {
    totalChecks: 20,
    passed: 18,
    failed: 2,
    warnings: 1
  },
  details: {
    basicInfo: { status: 'pass', items: [...] },
    sections: { status: 'pass', count: 9 },
    images: { status: 'fail', expected: 8, found: 6, missing: [3, 5] },
    format: { status: 'pass', issues: [] }
  },
  recommendations: [
    '图片 #3 (第03节) 缺失，建议重新提取',
    '图片 #5 (第05节) 缺失，建议重新提取'
  ]
};
```

#### 自动化验证脚本（参考）

```bash
#!/bin/bash
# validate_article.sh

echo "🔍 开始验证文章提取结果..."

ARTICLE_FILE="$1"
IMAGES_DIR="$(dirname "$ARTICLE_FILE")/images"

# 1. 检查图片引用
IMAGE_REFS=$(grep -o '\.\.\/images\/[^)]*' "$ARTICLE_FILE" | sort -u)
IMAGE_COUNT=$(echo "$IMAGE_REFS" | wc -l)
FILE_COUNT=$(ls "$IMAGES_DIR"/*.jpg 2>/dev/null | wc -l)

echo "📊 图片统计：引用 $IMAGE_COUNT 张，实际文件 $FILE_COUNT 个"

if [ $IMAGE_COUNT -ne $FILE_COUNT ]; then
  echo "⚠️  图片数量不匹配！"
  echo "引用的图片："
  echo "$IMAGE_REFS"
  echo "实际的文件："
  ls "$IMAGES_DIR"
fi

# 2. 检查章节完整性
SECTIONS=$(grep -c '^## ' "$ARTICLE_FILE")
echo "📚 章节数：$SECTIONS"

# 3. 检查基础信息
echo "📝 基础信息检查："
grep -q '^# ' "$ARTICLE_FILE" && echo "  ✅ 标题" || echo "  ❌ 缺少标题"
grep -q '> 来源：' "$ARTICLE_FILE" && echo "  ✅ 来源" || echo "  ❌ 缺少来源"

# 4. 检查格式
echo "🎨 格式检查："
grep -c '^```$' "$ARTICLE_FILE" | awk '{if ($1 % 2 == 0) print "  ✅ 代码块闭合"; else print "  ❌ 代码块未闭合"}'

echo "✅ 验证完成"
```

#### 使用场景

**场景1：提取完成后自动验证**
```javascript
// 完成提取后立即验证
await extractArticleContent(url);
const validationResult = await validateArticle(content);

if (validationResult.hasErrors) {
  console.log('发现错误，自动修复...');
  await autoFix(validationResult.issues);
}
```

**场景2：用户反馈问题时重新验证**
```javascript
// 用户说"第3节的图片漏了"
await scrollToSection(3);
const screenshot = await takeScreenshot();
if (screenshot.containsImage()) {
  await downloadImage(3);
  await updateMarkdown();
}
```

**场景3：批量提取时抽检**
```bash
# 随机抽检 10% 的文章
for article in $(find . -name "*.md" | shuf | head -n 5); do
  ./validate_article.sh "$article"
done
```

#### 验证最佳实践

✅ **应该做的**：
- 提取完成后立即验证
- 发现问题立即修复，不要等用户反馈
- 保留验证报告（记录问题和修复过程）
- 对于复杂文章，逐个章节截图对照

❌ **不应该做的**：
- 不要假设第一次提取就是完美的
- 不要跳过验证环节直接提交
- 不要忽略用户的反馈（即使看起来是小问题）
- 不要完全依赖自动化，关键部分需要人工确认

#### 验报告模板

```markdown
## 文章提取验证报告

**文章**：Boris Cherny Claude Code 工作流
**验证时间**：2026-01-20 14:00
**验证者**：Claude Code

### 验证结果

✅ **通过** (18/20)

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 标题 | ✅ | 已提取 |
| 来源 | ✅ | 完整 |
| 章节 | ✅ | 9个章节完整 |
| 图片 | ❌ | 缺少第3、5节图片 |
| 格式 | ✅ | Markdown格式正确 |
| 广告 | ✅ | 已移除 |

### 发现的问题

1. **图片不完整**：缺少第03节和第05节的图片
   - 原因：懒加载未触发
   - 修复：重新滚动页面并下载

2. **图片命名不规范**：存在 `image_1_boris_cherny.png`
   - 修复：重命名为 `03_section03.jpg`

### 修复记录

- 14:05 - 重新提取第03节图片 ✅
- 14:07 - 重新提取第05节图片 ✅
- 14:10 - 更新 Markdown 引用 ✅

### 最终状态

✅ 所有问题已修复，可以提交
```

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
