
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

**G. Remote 版本验证** ⭐ 重要

```javascript
// 检查 remote 版本是否已创建
const fs = require('fs');
const path = require('path');

const remoteFilePath = path.join(
  articleDir,
  articleSlug + '-remote.md'
);

const hasRemoteVersion = fs.existsSync(remoteFilePath);

if (!hasRemoteVersion) {
  console.error('❌ 缺少 remote 版本！');
  console.error('   必须创建 ' + articleSlug + '-remote.md');
  console.error('   图片使用原始 CDN URL，用于在线分享');
} else {
  // 检查 remote 版本中的图片链接是否正确
  const remoteContent = fs.readFileSync(remoteFilePath, 'utf8');
  const cdnImageLinks = remoteContent.match(/https:\/\/mmbiz\.qpic\.cn\/[^)]+/g) || [];

  if (cdnImageLinks.length === 0) {
    console.warn('⚠️ remote 版本未使用 CDN URL');
  }
}
```

**检查项**：
- [ ] remote 版本文件是否存在（`article-slug-remote.md`）
- [ ] remote 版本是否使用原始 CDN URL（不是 `./images/`）
- [ ] remote 版本内容是否与本地版本一致（除图片路径外）

**重要**：remote 版本不是可选的，必须创建！

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
