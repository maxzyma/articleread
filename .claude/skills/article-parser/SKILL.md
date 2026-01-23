---
name: article-parser
description: 从多平台提取文章内容并归档。图片/视频平台（小红书、抖音）只提取元数据用于搜索；图文平台（微信、Twitter、Medium、知乎、博客、播客）提取全文。使用时机：用户提供任何平台文章链接或要求"解析/提取XX文章"时。
---

# 文章解析与归档

## 核心 SOP

### 搜索优先策略

**核心原则**：任意平台链接 → 优先搜索文字版本 → 找不到才用原平台提取

1. **搜狗微信搜索** - `<作者名> <标题关键词>`
2. **Google/Bing** - `"<作者名>" "<标题关键词>"`
3. **原平台提取** - 小红书 OCR、抖音视频、Twitter 直接提取

**平台优先级**：微信公众号 > 博客/Medium > Twitter/知乎 > 小红书/抖音

详细搜索流程：见 [跨平台搜索策略](references/platform-search-strategy.md)

---

## 通用约束

### 内容整理
- ✅ 忠于原文，保留技术细节和代码示例
- ❌ 删除"关于作者"、"关注我"、推广信息、二维码

### 文件归档
```
general/article-slug/
├── article-slug.md              # 原始版本（./images/ 相对路径）
├── article-slug-standalone.md   # base64 嵌入版
├── article-slug-remote.md       # jsDelivr CDN 版
├── article-slug.metadata.yaml   # 元数据
└── images/                      # 图片目录
```

### 图片命名
- ✅ 描述性名称：`cover.jpg`、`workflow-diagram.png`
- ✅ Media ID：`G_J8qXqaoAQ2xhu.jpg`
- ❌ 不用编号：`image-01.jpg`

---

## Scripts

| 脚本 | 用途 |
|------|------|
| `scripts/generate_standalone.py <file.md>` | 生成 base64 嵌入版 |
| `scripts/generate_remote.py <file.md>` | 生成 CDN 版本 |
| `scripts/cache_image_urls.sh <url> get/save` | 图片 URL 缓存 |

---

## References

### 元数据提取（图片/视频平台）
- [小红书元数据提取](references/xiaohongshu-metadata-best-practices.md)
- [抖音元数据提取](references/douyin-metadata-best-practices.md)

### 全文提取（图文平台）
- [微信公众号全文提取](references/wechat-article-best-practices.md)
- [Twitter 全文提取](references/twitter-article-best-practices.md)
- [知乎全文提取](references/zhihu-article-best-practices.md)
- [博客/个人站点全文提取](references/blog-article-best-practices.md)

### 通用参考
- [跨平台搜索策略](references/platform-search-strategy.md) - 搜索流程和方法
- [文件归档](references/file-archiving.md) - 三版本策略
- [验证清单](references/validation.md) - 完整性检查
- [元数据模板](references/metadata-template.yaml)
