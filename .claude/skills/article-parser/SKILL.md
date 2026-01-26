---
name: article-parser
description: 从多平台提取文章内容并归档。图片/视频平台（小红书、抖音）只提取元数据用于搜索；图文平台（微信、Twitter、Medium、知乎、博客、播客）提取全文。使用时机：用户提供任何平台文章链接或要求"解析/提取XX文章"时。
---

# 文章解析与归档

## 核心 SOP

### 平台处理策略

| 平台类型 | 代表平台 | 处理方式 |
|---------|---------|---------|
| 文字平台 | 微信公众号、博客、Medium、Google Docs | 直接提取 ✅ |
| 混合平台 | Twitter、知乎、简书 | 直接提取 ✅ |
| 图片/视频平台 | 小红书、抖音、B站 | 先搜索文字版本 → 找不到才提取 |

**搜索流程**（仅小红书/抖音/B站）：
1. 识别作者/标题
2. 搜狗微信搜索 → 找到？使用微信版本 ✅
3. Google/Bing → 找到？使用文字版本 ✅
4. 都没找到 → 提取原平台内容

详细策略：见 [跨平台搜索策略](references/platform-search-strategy.md)

---

## 通用约束

### 内容整理
- ✅ 忠于原文，保留技术细节和代码示例
- ❌ 删除"关于作者"、"关注我"、推广信息、二维码

### 文件归档（三版本策略）

**必须同时创建三个版本**：

| 版本 | 文件名 | 图片处理 | 适用场景 |
|------|--------|----------|----------|
| 原始版 | `article-slug.md` | `./images/` 相对路径或外链 URL | 日常阅读、编辑 |
| standalone 版 | `article-slug-standalone.md` | **⚠️ 强制 base64 内嵌** | **完全独立、离线分享** |
| remote 版 | `article-slug-remote.md` | 原始 CDN URL | 在线分享、GitHub 预览 |

**⚠️ 关键规则**：Standalone 版本**必须**使用 base64 内嵌图片，无论平台是否支持外链。这是唯一确保文件完全独立可移植的方式。

目录结构：
```
general/article-slug/
├── article-slug.md              # 原始版本
├── article-slug-standalone.md   # standalone 版本
├── article-slug-remote.md       # remote 版本
├── article-slug.metadata.yaml   # 元数据
└── images/                      # 本地图片
```

详见：[文件归档指南](references/file-archiving-guide.md)

### 图片处理

**📘 完整指南**：所有图片处理的详细实现、代码示例、验证工具，见 **[图片处理最佳实践](references/image-handling-best-practices.md)**（唯一真相源）。

---

#### 快速参考（核心规则）

**三版本图片策略**：

| 版本 | 图片处理 | 关键规则 |
|------|---------|---------|
| **Original** | 相对路径或外链 | 外链友好平台用 URL，其他下载到本地 |
| **Standalone** | **Base64 内嵌** | ⚠️ **强制要求**，无论平台是否支持外链 |
| **Remote** | CDN 外链 | 使用原始 URL（便于在线分享） |

**⚠️ 强制规则**：
1. **Standalone 必须用 base64**：唯一确保文件完全独立的方式
2. **必须创建 image-mapping.json**：记录图片上下文，防止顺序错位
3. **外链友好平台优先**：Twitter、微信、知乎 等直接用 URL（original/remote 版）

**外链平台判断**：
- ✅ 外链友好：`pbs.twimg.com`、`mmbiz.qpic.cn`、`zxpic.cn`
- ⚠️ 需下载：小红书、抖音、个人博客

---

#### ⚠️ 微信公众号特殊处理

**问题**：微信使用懒加载，`take_snapshot` 只能看到占位符 SVG（`data:image/svg+xml`）。

**解决方法（按优先级）**：

1. **方法 1：运行脚本**（推荐）
   - 运行 `scripts/extract_wechat_images.js`（必须在 Chrome DevTools Console 手动执行）
   - 脚本会自动滚动页面、提取所有图片、生成 image-mapping.json

2. **方法 2：手动检查占位符**（备用）
   - 检查快照中是否有 `data:image/svg+xml` 的图片元素
   - 如有占位符，说明有未加载的图片
   - 尝试滚动页面后重新快照，或使用其他方法提取

3. **方法 3：序列测试**（最后手段）
   - 尝试访问 imgIndex=1, 2, 3... 的 URL
   - ⚠️ 注意：微信 CDN 可能对所有不存在索引返回同一张默认图片
   - 需要通过 MD5 或内容分析确认是否为不同图片

详见：[微信公众号文章最佳实践](references/wechat-article-best-practices.md)

---

#### 图片命名

| 策略 | 示例 | 场景 |
|------|------|------|
| 描述性 | `workflow-diagram.png` | ✅ 推荐 |
| Media ID | `G_J8qXqaoAQ2xhu.jpg` | Twitter |
| ❌ 数字索引 | `image-01.jpg` | 禁止使用 |

---

#### 顺序验证（防止错位）

**⚠️ 强制要求**：必须记录 `context_before` 和 `context_after`

```json
{
  "context_before": "图片前的文字（关键锚点）",
  "context_after": "图片后的文字（辅助验证）"
}
```

**错误示例**：
```
❌ 靠"感觉"或顺序号 → 图片错位
✅ 根据 context_before 精确定位 → 图片正确
```

---

#### 快速参考总结

✅ **外链友好**：Twitter、微信、知乎 → 用 URL（original/remote 版）
⚠️ **需下载**：小红书、抖音 → 下载到本地
🔒 **Standalone 强制 base64**：所有平台都必须转换

详见：[图片处理最佳实践](references/image-handling-best-practices.md)（完整实现指南）

---

### 视频处理 ⚠️

**📘 完整指南**：所有视频处理的详细实现、代码示例、平台策略，见 **[视频处理最佳实践](references/video-handling-best-practices.md)**。

**⚠️ 核心规则**：视频是文章内容的重要组成部分，必须检测、提取并记录视频链接。

---

#### 快速参考（核心规则）

**视频检测**：
1. 检查 `take_snapshot` 中是否有 "播放视频" 按钮
2. 使用 `evaluate_script` 查找 `<video>` 元素

**平台处理策略**：

| 平台 | 可直接提取 | 处理方式 | 文章格式 |
|------|----------|---------|---------|
| **微信** | ✅ | 提取 MP4/M3U8 | `[视频标题](直接URL)` |
| **小红书** | ❌ | 使用原文链接 | `[查看原视频](原文URL) （需在平台观看）` |
| **抖音** | ❌ | 使用原文链接 | `[查看原视频](原文URL) （需在平台观看）` |
| **Twitter** | ✅ | 提取 MP4 | `[视频标题](直接URL)` |
| **B站** | ✅ | 提取 M3U8 | `[视频标题](直接URL)` |

**文章格式**：
```markdown
> 来源：平台 作者，YYYY-MM-DD
> 原文链接：https://...
> 视频链接：[视频标题或"查看原视频"](视频URL) （观看说明）
>
> **说明**：本文包含视频内容，完整内容请观看原视频
```

**元数据格式**：
```yaml
source:
  video_url: "视频链接或原文链接"
  content_type: "视频" 或 "图文"
  notes: "视频提取说明（如：blob URL 动态加载）"
```

**⚠️ 重要**：
- 小红书/抖音使用 blob URL → 无法提取原始视频，必须提供原文链接
- 必须在文章顶部添加视频链接
- 必须在元数据中记录视频信息

---

### ⚠️ 提取完成验证清单（必查）

**提取完成后必须逐项验证**，确保完整性：

- [ ] **图片映射已创建** ⚠️ 最重要！
  - `.cache/images/{article-slug}/image-mapping.json` 存在
  - 每张图片都有 `context_before` 和 `context_after`
  - 图片位置已根据上下文验证

- [ ] **图片数量验证** ⚠️ **新增关键步骤**
  - **对比快照中的图片元素数量**与实际提取数量
  - 检查快照中是否有 `data:image/svg+xml` 占位符（说明有懒加载图片未提取）
  - **微信文章特别注意**：
    - 统计快照中所有 `uid=*_image` 元素
    - 排除 `data:image/svg+xml` 占位符
    - 确认剩余图片数量与提取数量一致
  - **如有疑问**：询问用户确认是否有遗漏图片

- [ ] 基础信息完整（标题、作者、时间、来源链接）
- [ ] 章节结构完整（无截断）
- [ ] 图片引用正确（数量匹配、路径正确）
- [ ] **视频链接完整**（如有）⚠️
  - 详见：[视频处理最佳实践](references/video-handling-best-practices.md)
  - 检查 `take_snapshot` 中是否有 "播放视频" 按钮
  - 使用 `evaluate_script` 提取 `<video>` 元素
  - 在文章顶部添加视频链接
  - 在元数据中添加 `video_url`、`content_type` 字段
- [ ] 三版本文件齐全（原始、standalone、remote）
  - ⚠️ **standalone 版本仅检查文件存在，不读取内容**（文件太大，会卡死）
- [ ] 元数据文件完整

详见：[验证清单](references/validation-checklist.md)

---

## Scripts

| 脚本 | 用途 |
|------|------|
| `scripts/extract_wechat_images.js` | **微信图片提取**（必须在 Console 运行） |
| `scripts/extract_wechat_videos.js` | **微信视频提取**（必须在 Console 运行） |
| `scripts/generate_standalone.py <file.md>` | **⚠️ 生成 standalone 版本（强制 base64）** |
| `scripts/generate_remote.py <file.md>` | 生成 CDN 版本 |
| `scripts/cache_image_urls.sh <url> get/save` | 图片 URL 缓存 |

### generate_standalone.py 使用说明

**用途**：将文章中的所有图片转换为 base64 内嵌，生成完全独立的 standalone 版本。

**⚠️ 关键规则**：此脚本**必须**用于生成 standalone 版本，无论平台是否支持外链。

**使用方法**：
```bash
# 生成 standalone 版本
python3 scripts/generate_standalone.py general/article/article.md

# 输出文件：general/article/article-standalone.md
# 特点：
#   - 所有图片转为 base64 data URI
#   - 文件大小显著增加（通常 10-50 倍）
#   - 完全独立，无外部依赖
#   - 便于离线分享和归档
```

**验证 standalone 版本**：
```bash
# 检查是否有外链（应该为 0）
grep -c "https://" article-standalone.md

# 检查 base64 图片数量
grep -c "data:image" article-standalone.md
```

### extract_wechat_videos.js 使用说明

**用途**：自动提取微信公众号文章中的视频

**使用方法**：
```bash
# 1. 在 Chrome DevTools 中打开微信文章
navigate_page -> <微信文章URL>

# 2. 打开 Console，运行脚本
evaluate_script -> 复制 extract_wechat_videos.js 全部内容

# 3. 等待脚本执行并输出视频信息
```

**输出内容**：
- 视频 URL、时长、封面
- Markdown 格式的视频链接
- 视频前后的文本上下文

### extract_wechat_images.js 使用说明

**用途**：自动提取微信公众号文章中的所有图片（包括懒加载图片）

**使用方法**：
```bash
# 1. 在 Chrome DevTools 中打开微信文章
navigate_page -> <微信文章URL>

# 2. 打开 Console，运行脚本
evaluate_script -> 复制 extract_wechat_images.js 全部内容

# 3. 等待脚本执行（自动滚动 + 提取）

# 4. 复制输出的下载命令到终端执行
```

---

## 常见错误与规避

### 微信文章图片遗漏 ❌

**症状**：用户指出文章中还有图片，但提取时未发现

**原因**：
- 微信使用懒加载，`take_snapshot` 只能看到占位符 SVG（`data:image/svg+xml`）
- 真实图片 URL 在 `data-src` 属性中，快照无法捕获
- `extract_wechat_images.js` 脚本无法通过 `evaluate_script` 自动执行（JavaScript 语法限制）

**规避**：
1. ⚠️ **主动验证图片数量**：统计快照中所有图片元素，对比实际提取数量
2. ⚠️ **检查占位符**：快照中有 `data:image/svg+xml` 说明有懒加载图片未提取
3. ⚠️ **询问用户确认**：如有疑问，直接询问用户"文章中是否还有其他图片？"
4. 尝试使用多种方法提取（脚本、手动检查、序列测试）

**案例**：Claude in Excel 文章提取时遗漏了第二张图片（Claude 官方推文截图），因为：
- 快照中只显示 1 张真实图片（imgIndex=0）
- 另一张是占位符 SVG（uid=3_13）
- 最终需要用户提供截图才能确认

### 图片位置错放 ❌

**症状**：图片顺序与原文不符，或图片插错位置

**原因**：
- 没有创建 `image-mapping.json`
- 靠"感觉"或数字顺序放置图片
- 没有根据 `context_before` 验证

**规避**：
1. ⚠️ **必须创建 `image-mapping.json`**
2. 记录每张图片的 `context_before` 和 `context_after`
3. 根据上下文精确定位，不要凭感觉

### 微信图片提取失败 ❌

**症状**：只获取到 SVG 占位符，图片 URL 错误

**原因**：
- 使用 `take_snapshot` 而非 JavaScript 脚本
- 只获取 `src` 属性而非 `data-src`
- 未滚动页面触发懒加载

**规避**：
1. 使用 `scripts/extract_wechat_images.js`
2. 在 Console 中手动运行，不要用 `take_snapshot`
3. 脚本会自动滚动和提取

### 跳过验证清单 ❌

**症状**：文件不完整、元数据缺失、视频遗漏

**原因**：
- 提取完成后未逐项检查
- 认为看起来对就行了

**规避**：
1. ⚠️ **必须使用验证清单逐项检查**
2. 特别检查 `image-mapping.json` 是否创建
3. 检查图片数量（对比快照）
4. 检查视频（如有）是否提取

### 章节内容截断 ❌

**症状**：文章末尾内容丢失

**原因**：
- 未滚动到页面底部
- web_reader API 限制（使用中）
- 快照未捕获完整内容

**规避**：
1. 滚动到页面底部再提取
2. 检查文章末尾是否有"点赞/在看"等结束标记
3. 对照原文验证完整性

---

## References

### 通用参考（核心流程）
- [跨平台搜索策略](references/platform-search-strategy.md) - 小红书/抖音搜索流程
- [文件归档指南](references/file-archiving-guide.md) - 三版本策略
- [图片处理最佳实践](references/image-handling-best-practices.md) - 外链策略、命名规范、缓存映射
- [验证清单](references/validation-checklist.md) - 完整性检查
- [元数据模板](references/metadata-template.yaml) - 通用元数据格式

### 平台特定实践

**元数据提取**（图片/视频平台）：
- [小红书元数据提取](references/xiaohongshu-metadata-best-practices.md)
- [抖音元数据提取](references/douyin-metadata-best-practices.md)

**全文提取**（图文平台）：
- [Google Docs 全文提取](references/google-docs-best-practices.md)
- [微信公众号全文提取](references/wechat-article-best-practices.md)
- [Twitter 全文提取](references/twitter-article-best-practices.md)
- [知乎全文提取](references/zhihu-article-best-practices.md)
- [博客/个人站点全文提取](references/blog-article-best-practices.md)

---

## 常见错误与规避

### 未保存 image-mapping.json ❌

**症状**：图片位置错放，无法验证图片是否在正确位置

**原因**：
- 运行脚本后没有复制 image-mapping.json
- 以为下载图片就够了，不需要映射文件

**规避**：
1. ⚠️ **必须**复制并保存 image-mapping.json
2. 保存到 `.cache/images/{article-slug}/image-mapping.json`
3. 根据映射文件中的 context_before 精确定位图片

### 图片位置错放 ❌

**症状**：图片顺序与原文不符，或图片插错位置

**原因**：
- 没有创建 `image-mapping.json`
- 靠"感觉"或数字顺序放置图片
- 没有根据 `context_before` 验证

**规避**：
1. ⚠️ **必须**创建 `image-mapping.json`
2. 记录每张图片的 `context_before` 和 `context_after`
3. 根据上下文精确定位，不要凭感觉

### 微信图片提取失败 ❌

**症状**：只获取到 SVG 占位符，图片 URL 错误

**原因**：
- 使用 `take_snapshot` 而非 JavaScript 脚本
- 只获取 `src` 属性而非 `data-src`
- 未滚动页面触发懒加载

**规避**：
1. 使用 `scripts/extract_wechat_images.js`
2. 在 Console 中运行，不要用 `take_snapshot`
3. 脚本会自动滚动和提取

### 跳过验证清单 ❌

**症状**：文件不完整、元数据缺失、视频遗漏

**原因**：
- 提取完成后未逐项检查
- 认为看起来对就行了

**规避**：
1. ⚠️ **必须**使用验证清单逐项检查
2. 特别检查 `image-mapping.json` 是否创建
3. 检查视频（如有）是否提取

### 章节内容截断 ❌

**症状**：文章末尾内容丢失

**原因**：
- 未滚动到页面底部
- web_reader API 限制（使用中）
- 快照未捕获完整内容

**规避**：
1. 滚动到页面底部再提取
2. 检查文章末尾是否有"点赞/在看"等结束标记
3. 对照原文验证完整性

