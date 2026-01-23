---
name: article-parser
description: 从多平台提取文章内容并归档。图片/视频平台（小红书、抖音）只提取元数据用于搜索；图文平台（微信、Twitter、Medium、知乎、博客、播客）提取全文。使用时机：用户提供任何平台文章链接或要求"解析/提取XX文章"时。
---

# 文章解析与归档

## 核心 SOP

### 平台处理策略

| 平台类型 | 代表平台 | 处理方式 |
|---------|---------|---------|
| 文字平台 | 微信公众号、博客、Medium | 直接提取 ✅ |
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
| 原始版 | `article-slug.md` | `./images/` 相对路径 | 日常阅读、编辑 |
| standalone 版 | `article-slug-standalone.md` | base64 嵌入 | 离线分享、归档 |
| remote 版 | `article-slug-remote.md` | 原始 CDN URL | 在线分享、GitHub 预览 |

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
- ✅ 所有平台图片都下载到 `images/` 目录
- ✅ 使用描述性名称：`cover.jpg`、`workflow-diagram.png`
- ✅ 或使用 Media ID：`G_J8qXqaoAQ2xhu.jpg`
- ❌ 不用数字索引：`image-01.jpg`、`img-1.png`

### 验证清单

提取完成后必须验证：

- [ ] 基础信息完整（标题、作者、时间、来源链接）
- [ ] 章节结构完整（无截断）
- [ ] 图片引用正确（数量匹配、路径正确）
- [ ] 三版本文件齐全（原始、standalone、remote）
- [ ] 元数据文件完整

详见：[验证清单](references/validation-checklist.md)

---

## Scripts

| 脚本 | 用途 |
|------|------|
| `scripts/generate_standalone.py <file.md>` | 生成 base64 嵌入版 |
| `scripts/generate_remote.py <file.md>` | 生成 CDN 版本 |
| `scripts/cache_image_urls.sh <url> get/save` | 图片 URL 缓存 |

---

## References

### 通用参考（核心流程）
- [跨平台搜索策略](references/platform-search-strategy.md) - 小红书/抖音搜索流程
- [文件归档指南](references/file-archiving-guide.md) - 三版本策略
- [验证清单](references/validation-checklist.md) - 完整性检查
- [元数据模板](references/metadata-template.yaml) - 通用元数据格式

### 平台特定实践

**元数据提取**（图片/视频平台）：
- [小红书元数据提取](references/xiaohongshu-metadata-best-practices.md)
- [抖音元数据提取](references/douyin-metadata-best-practices.md)

**全文提取**（图文平台）：
- [微信公众号全文提取](references/wechat-article-best-practices.md)
- [Twitter 全文提取](references/twitter-article-best-practices.md)
- [知乎全文提取](references/zhihu-article-best-practices.md)
- [博客/个人站点全文提取](references/blog-article-best-practices.md)
