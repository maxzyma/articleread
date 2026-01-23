# 脚本使用指南

## 核心脚本

### extract_wechat_images.js ⚠️ 微信公众号专用

**重要**：提取微信公众号文章图片时，必须使用此脚本！

**问题**：微信公众号使用图片懒加载，`take_snapshot` 只能获取占位符。

**解决**：此脚本自动滚动页面触发懒加载，从 `data-src` 属性提取真实图片 URL。

**使用方法**：

```javascript
// 1. 在 Chrome DevTools 中打开微信文章
navigate_page -> <微信文章URL>

// 2. 打开 Console，运行脚本
// 复制 extract_wechat_images.js 全部内容到 Console

// 3. 脚本会自动：
//    - 滚动页面触发懒加载
//    - 提取所有图片 URL
//    - 按 imgIndex 排序
//    - 输出下载命令

// 4. 复制输出的下载命令到终端执行
```

**输出内容**：
- 图片信息列表（URL、尺寸、imgIndex）
- 逐个下载命令
- 批量下载 Shell 脚本
- JSON 格式数据

详见：[微信公众号全文提取最佳实践](../references/wechat-article-best-practices.md)

---

### generate_standalone.py

将原始版本（`./images/` 路径）转换为 standalone 版本（base64 嵌入）。

**用法**：

```bash
python3 generate_standalone.py article-slug/article-slug.md
python3 generate_standalone.py article-slug/ --recursive
```

**支持格式**：jpg, jpeg, png, gif, webp, svg, bmp

### generate_remote.py

将原始版本（`./images/` 路径）转换为 remote 版本（jsDelivr CDN URL）。

**用法**：

```bash
# 自动检测仓库信息
python3 generate_remote.py article-slug/article-slug.md

# 指定仓库
python3 generate_remote.py article-slug/article-slug.md --repo user/repo

# 批量处理
python3 generate_remote.py article-slug/ --recursive
```

**输出示例**：

```
处理文件: article-slug/article-slug.md

结果:
  输出: article-slug/article-slug-remote.md
  转换: 5/5 图片
  CDN: https://cdn.jsdelivr.net/gh/user/repo/general/article-slug/images
```

### cache_image_urls.sh

图片/视频 URL 缓存管理脚本，避免重复提取。

**用法**：

```bash
./cache_image_urls.sh <文章URL> get           # 获取缓存
./cache_image_urls.sh <文章URL> save <URLS>   # 保存URL
```

---

## 可选：GitHub 图床上传

> **注意**：新的三版本策略中，remote 版本自动使用 jsDelivr CDN 引用仓库中的图片，无需单独上传到图床。以下内容仅供特殊情况参考。

### 1. 配置 GitHub Token

首次使用需要配置 GitHub Personal Access Token。详见：[GITHUB_TOKEN_SETUP.md](./GITHUB_TOKEN_SETUP.md)

```bash
# 在 ~/.zshrc 中添加
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxx"
```

**注意**：`GITHUB_IMAGE_REPO` 是可选的！脚本会自动检测当前 git 仓库。

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
