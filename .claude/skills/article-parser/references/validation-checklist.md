# 验证清单

提取完成后必须进行验证，确保内容完整性和准确性。

## 验证流程

```
提取内容 → 自动验证 → 发现问题 → 修复问题 → 重新验证 → 完成
```

## 核心验证项

### 1. 基础信息验证

- [ ] **标题**：是否有一级标题 `#`
- [ ] **来源信息**：是否包含引用块 `> 来源：平台 作者，YYYY-MM-DD`
- [ ] **原文链接**：是否包含 `> 原文链接：https://...`
- [ ] **作者信息**：是否准确提取作者姓名/职位

### 2. 内容完整性验证

- [ ] **章节完整**：检查章节数量是否合理，编号是否连续
- [ ] **无截断痕迹**：文章结尾是否完整，无"未完待续"等标记
- [ ] **技术细节保留**：代码示例、技术栈、流程步骤是否完整
- [ ] **引用和比喻**：是否遗漏作者的引用或比喻

### 3. 图片和视频完整性验证

#### 图片验证

- [ ] **图片数量匹配**：Markdown 引用数量 = `images/` 目录文件数量
- [ ] **图片路径正确**：原始版本使用 `./images/xxx.jpg` 格式
- [ ] **图片文件存在**：所有引用的图片文件都在 `images/` 目录中
- [ ] **图片命名规范**：
  - ✅ 使用描述性名称（`workflow-diagram.png`）或 Media ID（`G_xxx.jpg`）
  - ❌ 避免数字索引（`img-1.jpg`、`image_2.png`）

#### 视频验证 ⚠️

**⚠️ 重要规则：视频是文章内容的重要组成部分，必须提取并记录视频链接。**

详见：[视频处理最佳实践](video-handling-best-practices.md)

**验证流程**：
1. [ ] **检测视频**：`take_snapshot` 中是否有 "播放视频" 按钮或 `<video>` 元素
2. [ ] **提取链接**：根据平台类型提取视频 URL（详见平台策略）
3. [ ] **添加到文章**：在文章顶部添加视频链接
4. [ ] **更新元数据**：添加 `video_url`、`content_type` 等字段

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
  notes: "视频提取说明"
```

**平台处理策略**：

| 平台 | 可直接提取 | 处理方式 | 文章格式 |
|------|----------|---------|---------|
| **微信** | ✅ | 提取 MP4/M3U8 | `[视频标题](直接URL)` |
| **小红书** | ❌ | 使用原文链接 | `[查看原视频](原文URL) （需在平台观看）` |
| **抖音** | ❌ | 使用原文链接 | `[查看原视频](原文URL) （需在平台观看）` |
| **Twitter** | ✅ | 提取 MP4 | `[视频标题](直接URL)` |
| **B站** | ✅ | 提取 M3U8 | `[视频标题](直接URL)` |

**常见遗漏**：
- ❌ 只看 `take_snapshot` → 忽略视频内容
- ❌ 未运行 `evaluate_script` → 无法获取视频 URL
- ❌ 小红书/抖音未添加链接 → blob URL 无法提取但必须提供原文链接

### 微信公众号特有验证 ⚠️

**微信公众号文章必须使用 JavaScript 提取，不要只用 `take_snapshot`！**

- [ ] **使用 JavaScript 提取**：运行 `extract_wechat_images.js` 脚本
- [ ] **检查 data-src 属性**：确保从 `data-src` 而非 `src` 获取图片 URL
- [ ] **验证 imgIndex 连续性**：检查 imgIndex 参数是否连续（0, 1, 2, ...）
- [ ] **触发懒加载**：滚动到页面底部后再提取图片
- [ ] **过滤占位符**：排除 `data:image/svg` 的占位符图片

**常见错误**：
- ❌ 使用 `take_snapshot` 提取 → 只能获取 `src` 属性（占位符）
- ❌ 未滚动页面 → 懒加载图片未触发
- ❌ 忽略 `data-src` → 遗漏真实图片 URL

**正确流程**：
1. 打开微信文章
2. 运行 `extract_wechat_images.js`
3. 检查输出的图片数量和 URL
4. 复制下载命令批量下载
5. 验证图片完整性

### 4. 三版本验证

- [ ] **原始版本**：`article-slug.md` 存在
- [ ] **standalone 版本**：`article-slug-standalone.md` 存在（⚠️ **不读取验证**：文件可能很大，会导致卡死）
- [ ] **remote 版本**：`article-slug-remote.md` 存在，图片使用原始 CDN URL
- [ ] **内容一致性**：原始版本和 remote 版本的文字内容一致（仅图片路径不同）

> **为什么 standalone 版本不读取验证？**
> standalone 版本使用 base64 嵌入图片，文件可能达到数 MB。读取验证会消耗大量内存和上下文，导致响应卡死。验证时仅检查文件存在性即可。

### 5. 格式验证

- [ ] **代码块闭合**：所有 ``` 成对出现
- [ ] **引用块格式正确**：`>` 使用合理，未将正文误标为引用
- [ ] **标题层级合理**：`#` `##` `###` 使用正确
- [ ] **列表格式正确**：无断行、缩进正确

### 6. 元数据验证

- [ ] **元数据文件存在**：`article-slug.metadata.yaml` 存在
- [ ] **必填字段完整**：
  - `title`、`extraction_date`
  - `source.platform`、`source.url`
  - `content_file` 路径正确（`./article-slug.md`）
- [ ] **提取方法记录**：`extraction_method` 准确记录使用的工具
- [ ] **验证状态标记**：`verification.status` 设为 `completed`

### 7. 内容清理验证

- [ ] **无广告图片**："结语"、"关于作者"之后无多余图片
- [ ] **无推广信息**：已删除"关注我"、二维码、推广链接
- [ ] **无评论区内容**：已删除观众反馈、评论区互动
- [ ] **无冗余信息**：已删除点赞数、收藏数、互动数据

## 自动验证检查（可选）

如果使用脚本验证，可以参考以下检查逻辑：

### A. 基础信息检查

```javascript
const validation = {
  hasTitle: content.includes('# '),
  hasSource: content.includes('> 来源：'),
  hasLink: content.includes('> 原文链接：'),
  hasDate: content.match(/\d{4}-\d{2}-\d{2}/),
};
```

### B. 章节完整性检查

```javascript
const sections = content.match(/## \d+[｜|].+/g);
console.log(`提取章节数: ${sections?.length || 0}`);
```

### C. 图片完整性检查

```javascript
const imageRefs = content.match(/!\[.*\]\(\.\/images\/.+\)/g) || [];
const imageFiles = fs.readdirSync('./images/');
console.log(`引用: ${imageRefs.length}，文件: ${imageFiles.length}`);
```

### D. 三版本检查

```javascript
const hasOriginal = fs.existsSync('article-slug.md');
const hasStandalone = fs.existsSync('article-slug-standalone.md');
const hasRemote = fs.existsSync('article-slug-remote.md');
console.log(`原始: ${hasOriginal}, standalone: ${hasStandalone}, remote: ${hasRemote}`);
```

## 发现问题时的处理

| 问题类型 | 处理方式 |
|---------|---------|
| 图片不完整 | 重新提取图片，检查是否有懒加载未触发 |
| 章节截断 | 滚动到页面底部，重新获取内容 |
| 广告图片未移除 | 手动删除"结语"之后的图片和推广信息 |
| 图片引用错误 | 检查文件名，更新 Markdown 引用 |
| 三版本缺失 | 运行 `generate_standalone.py` 和 `generate_remote.py` |
| 元数据缺失字段 | 根据模板补充必填字段 |

## 验证完成标记

所有验证项通过后：

1. 在元数据中标记验证完成：
   ```yaml
   verification:
     status: "completed"
     verified_against: "原始网页"
     issues_found_and_fixed:
       - "无"
   ```

2. 提交到 Git：
   ```bash
   git add general/article-slug/
   git commit -m "Add: 文章标题（验证完成）"
   ```

## 平台特定验证

不同平台可能有额外的验证要求，详见各平台的 best-practices 文档：

- [小红书特定验证](xiaohongshu-metadata-best-practices.md)
- [抖音特定验证](douyin-metadata-best-practices.md)
- [微信公众号特定验证](wechat-article-best-practices.md)
- [Twitter 特定验证](twitter-article-best-practices.md)
- [知乎特定验证](zhihu-article-best-practices.md)
- [博客特定验证](blog-article-best-practices.md)
