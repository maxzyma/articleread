# 文章解析归档

此项目用于从各种来源（小红书、Twitter、博客等）提取、整理和归档有价值的文章内容。

## 目录结构

```
articleread/
├── knowledge&memory/              # 知识与记忆主题
│   ├── basics/                    # 基础概念
│   ├── solutions/                 # 解决方案
│   └── comparison/                # 对比分析
│
├── general/                       # 通用主题（未分类）
│   └── article-name/
│       ├── article-name.md        # 正文内容
│       ├── article-name.metadata.yaml  # 元数据
│       └── images/                # 图片资源（可选）
│
└── extraction-plan.yaml           # 提取计划管理
```

## 文章组织原则

- **按主题分类**：文章按主题归入不同目录
- **按子主题组织**：每个主题下可根据内容类型划分子主题
- **元数据同级**：文章和元数据放在同一目录，便于管理和引用

## 图片托管

### GitHub + jsDelivr CDN

项目使用 GitHub 仓库托管图片，通过 jsDelivr CDN 加速访问。

### CDN 链接格式

```
https://cdn.jsdelivr.net/gh/[用户名]/[仓库名]/[文件在仓库中的路径]
```

### 示例

对于文件 `general/boris-claude-code-workflow/images/00_cover.jpg`：

```
https://cdn.jsdelivr.net/gh/maxzyma/articleread/general/boris-claude-code-workflow/images/00_cover.jpg
```

### 在 Markdown 中使用

```markdown
![封面](https://cdn.jsdelivr.net/gh/maxzyma/articleread/general/article-name/images/00_cover.jpg)
```

### 快速生成 CDN 链接

1. **基础 URL**: `https://cdn.jsdelivr.net/gh/maxzyma/articleread/`
2. **文件路径**: 仓库根目录后的完整路径
3. **拼接**: 基础 URL + 文件路径

> 注意：图片推送到 GitHub 后，CDN 首次访问可能需要 1-2 分钟生效。

## 添加新文章

详细规则请参考项目内的 `CLAUDE.md` 文档。

简要流程：
1. 确定主题和子主题目录
2. 提取并整理文章内容（翻译成中文）
3. 创建正文 `.md` 和元数据 `.metadata.yaml` 文件
4. 如有图片，创建 `images/` 目录存放
5. 使用 CDN 链接在正文中引用图片
6. 更新 `extraction-plan.yaml` 记录提取状态

## 项目配置

- **提取规则**: `CLAUDE.md`
- **提取计划**: `extraction-plan.yaml`
- **图片忽略**: `.gitignore`（已配置启用 images 目录）
