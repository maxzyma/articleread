# GitHub 图床使用指南

## 快速开始

### 1. 配置 GitHub Token

首次使用需要配置 GitHub Personal Access Token。详见：[GITHUB_TOKEN_SETUP.md](./GITHUB_TOKEN_SETUP.md)

```bash
# 在 ~/.zshrc 中添加
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxx"
export GITHUB_IMAGE_REPO="maxzyma/articleread"
```

### 2. 上传图片

```bash
# 上传单张图片
python3 upload_to_github.py "https://mmbiz.qpic.cn/xxx.jpg" wechat

# 输出: https://cdn.jsdelivr.net/gh/maxzyma/articleread/assets/images/wechat/2026-01/uuid.jpg
```

### 3. 在 Markdown 中使用

```markdown
![图片说明](https://cdn.jsdelivr.net/gh/maxzyma/articleread/assets/images/wechat/2026-01/uuid.jpg)
```

---

## 使用场景

### 场景 1：提取微信公众号文章

```bash
# 1. 提取微信图片 URL
# 2. 批量上传到 GitHub
for url in "${IMAGE_URLS[@]}"; do
  python3 upload_to_github.py "$url" wechat
done
```

### 场景 2：在 article-parser 中使用

图片会自动上传到 GitHub 图床，并返回 CDN 加速的 URL。

### 场景 3：手动上传图片

```bash
# 上传本地图片
python3 upload_to_github.py "/path/to/image.jpg" wechat
```

---

## CDN 加速说明

所有上传的图片都会自动使用 jsDelivr CDN 加速：

| 访问方式 | URL | 速度 |
|---------|-----|------|
| 原始链接 | `raw.githubusercontent.com` | 慢（国内访问受限） |
| CDN 链接 | `cdn.jsdelivr.net` | 快（全球加速） |

脚本会自动返回 CDN 链接。

---

## 存储结构

```
maxzyma/articleread 仓库
└── assets/
    └── images/
        ├── wechat/
        │   ├── 2026-01/
        │   │   ├── uuid-1.jpg
        │   │   └── uuid-2.jpg
        │   └── 2026-02/
        │       └── uuid-3.jpg
        └── xiaohongshu/
            └── 2026-01/
                └── uuid-4.jpg
```

- 按平台分类（wechat / xiaohongshu）
- 按月份组织（YYYY-MM）
- 使用 UUID 命名（避免冲突）

---

## 故障排查

### Token 无效

```bash
# 检查 token 是否设置
echo $GITHUB_TOKEN

# 如果为空，重新加载配置
source ~/.zshrc
```

### 上传失败

```bash
# 检查网络连接
ping github.com

# 检查文件大小（GitHub 限制 25MB）
ls -lh /path/to/image.jpg
```

### 图片无法访问

1. 检查 CDN URL 是否正确
2. 等待 1-2 分钟（CDN 缓存刷新）
3. 尝试直接访问 raw URL

---

## 相关文档

- [GitHub Token 配置指南](./GITHUB_TOKEN_SETUP.md)
- [article-parser 技能文档](../../SKILL.md)

---

## 技术支持

如有问题，请查看：
1. [常见问题 FAQ](./GITHUB_TOKEN_SETUP.md#常见问题)
2. [GitHub 官方文档](https://docs.github.com/)
3. [jsDelivr 文档](https://www.jsdelivr.com/)
