# 文章解析归档

此目录用于存储从各种来源提取、整理的文章内容。

## 目录结构

```
read/
├── articles/                      # 可分享的正文内容
│   └── YYYY-MM-DD/
│       ├── article-slug.md
│       └── other-article.md
│
└── metadata/                      # 内部管理（来源、验证、对照）
    └── YYYY-MM-DD/
        ├── article-slug.yaml
        └── other-article.yaml
```

## 使用说明

- **articles/**：干净的正文内容，可直接分享
- **metadata/**：元数据文件，包含来源URL、提取方法、验证状态等
- **按日期组织**：同一天的文章和元数据在对应目录下

## 添加新文章

1. 在 `articles/YYYY-MM-DD/` 创建正文 `.md` 文件
2. 在 `metadata/YYYY-MM-DD/` 创建对应的 `.yaml` 文件
3. 元数据中的 `content_file` 字段使用相对路径指向正文
