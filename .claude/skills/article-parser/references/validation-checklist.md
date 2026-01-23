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

### 3. 图片完整性验证

- [ ] **图片数量匹配**：Markdown 引用数量 = `images/` 目录文件数量
- [ ] **图片路径正确**：原始版本使用 `./images/xxx.jpg` 格式
- [ ] **图片文件存在**：所有引用的图片文件都在 `images/` 目录中
- [ ] **图片命名规范**：
  - ✅ 使用描述性名称（`workflow-diagram.png`）或 Media ID（`G_xxx.jpg`）
  - ❌ 避免数字索引（`img-1.jpg`、`image_2.png`）

### 4. 三版本验证

- [ ] **原始版本**：`article-slug.md` 存在
- [ ] **standalone 版本**：`article-slug-standalone.md` 存在，图片使用 base64 格式
- [ ] **remote 版本**：`article-slug-remote.md` 存在，图片使用原始 CDN URL
- [ ] **内容一致性**：三个版本的文字内容完全一致（仅图片路径不同）

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
