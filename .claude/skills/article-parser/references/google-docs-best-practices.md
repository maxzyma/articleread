# Google Docs 全文提取指南

## 概述

Google Docs 是一个特殊的平台，内容在 iframe 和 Canvas 中渲染，无法直接使用常规的 `take_snapshot` 方法提取。本文档介绍 Google Docs 的最佳提取方法。

---

## 推荐方法：导出 API

**✅ 最佳实践：使用 Google Docs 导出 API**

### 方法 1：curl 直接下载（推荐）

```bash
# 提取文档 ID
# URL 格式：https://docs.google.com/document/d/{DOCUMENT_ID}/edit
curl -L "https://docs.google.com/document/d/{DOCUMENT_ID}/export?format=md" \
  -o /tmp/article.md
```

**支持的导出格式**：
- `md` - Markdown（推荐，保留格式）
- `txt` - 纯文本
- `html` - HTML（带样式）
- `docx` - Microsoft Word

**优点**：
- ✅ 简单直接，一行命令完成
- ✅ 获取完整内容，无渲染限制
- ✅ Markdown 格式便于后续处理
- ✅ 无需浏览器，无网络延迟

**缺点**：
- ❌ 无法提取实时协作状态
- ❌ 无法提取评论/建议（如有需要，使用其他格式）

### 方法 2：Chrome DevTools 导出菜单

当无法直接使用 curl 时（如需要身份验证），可通过浏览器 UI 导出：

```bash
# 1. 使用 Chrome DevTools 打开文档
navigate_page -> https://docs.google.com/document/d/{DOCUMENT_ID}/edit

# 2. 点击 File 菜单
click -> File menuitem

# 3. 点击 Download 子菜单
click -> Download menuitem

# 4. 选择格式（如 Markdown）
click -> Markdown (.md) menuitem
```

**优点**：
- ✅ 使用用户已有的身份验证
- ✅ 可通过 UI 验证导出成功

**缺点**：
- ❌ 需要浏览器交互
- ❌ 文件下载到默认目录，需要定位

---

## 不推荐的方法

### ❌ 方法：Canvas/iframe 提取

**为什么不行**：
- Google Docs 内容在 Canvas 元素中渲染
- 使用 `take_snapshot` 只能看到 UI 框架，无法获取正文
- iframe 内容受跨域限制，无法直接访问

**错误示例**：
```javascript
// 这无法获取文档内容
const content = document.querySelector('.kix-appview').innerText;
```

---

## 完整工作流程

### 标准提取流程

```bash
# 1. 提取文档 ID
DOCUMENT_ID=$(echo "$URL" | sed -n 's/.*\/document\/d\/\([^\/]*\).*/\1/p')

# 2. 下载为 Markdown
curl -L "https://docs.google.com/document/d/$DOCUMENT_ID/export?format=md" \
  -o /tmp/article.md

# 3. 验证内容
head -20 /tmp/article.md

# 4. 复制到工作目录
cp /tmp/article.md general/article-slug/article-slug.md
```

### 处理身份验证的文档

如果文档需要身份验证（非公开链接）：

```bash
# 使用 Chrome DevTools 方法
# 1. 打开文档（用户已登录）
navigate_page -> <Google Docs URL>

# 2. 通过导出菜单下载
click -> File -> Download -> Markdown

# 3. 检查网络请求获取下载 URL
list_network_requests -> resource_type: "document"

# 4. 找到导出请求并复制 URL
get_network_request -> <reqid>
```

---

## 内容处理

### Markdown 后处理

导出的 Markdown 可能包含：
- ✅ 标题结构（H1-H6）
- ✅ 列表（有序/无序）
- ✅ 链接（自动转换）
- ⚠️ 图片（可能为 Google Docs 内部 URL）

**图片处理**：
```bash
# 检查图片 URL
grep -E '!\[.*\]\(.*\)' article.md

# 如果是 Google Docs 内部 URL，需要手动提取
# 或使用 html 格式导出后解析
```

### 格式清理

```bash
# 移除多余空行
sed -i '' '/^$/N;/^\n$/D' article.md

# 统一换行符
dos2unix article.md
```

---

## 验证清单

提取完成后验证：

- [ ] **文件大小合理**（> 1KB 表示有内容）
- [ ] **包含标题**（第一行应为文档标题）
- [ ] **包含正文**（不是空白或仅包含框架文本）
- [ ] **链接完整**（如有链接，格式正确）
- [ ] **列表格式**（有序/无序列表正确）
- [ ] **无截断**（文档末尾完整，无省略号）

---

## 常见问题

### 1. curl 返回 HTML 登录页面

**症状**：下载的文件是 HTML，包含"Sign in"等文本

**原因**：文档非公开，需要身份验证

**解决方案**：
- 使用 Chrome DevTools 方法（通过已登录浏览器）
- 或请求用户提供公开链接

### 2. 导出的 Markdown 乱码

**症状**：中文或特殊字符显示为乱码

**原因**：编码问题

**解决方案**：
```bash
# 转换编码
iconv -f UTF-8 -t UTF-8 article.md > article-fixed.md
```

### 3. 图片无法显示

**症状**：图片链接为 Google Docs 内部 URL

**原因**：导出 API 不包含外部图片 URL

**解决方案**：
- 使用 `format=html` 导出
- 从 HTML 中提取真实图片 URL
- 或手动截图保存

---

## 示例

### 完整提取示例

```bash
# 提取 Clawdbot 趋势分析文档
URL="https://docs.google.com/document/d/1Mz4xt1yAqb2gDxjr0Vs_YOu9EeO-6JYQMSx4WWI8KUA/edit"

# 提取文档 ID
DOC_ID=$(echo $URL | cut -d'/' -f6)

# 下载 Markdown
curl -L "https://docs.google.com/document/d/$DOC_ID/export?format=md" \
  -o /tmp/clawdbot.md

# 验证
echo "文件大小: $(wc -c < /tmp/clawdbot.md) bytes"
head -5 /tmp/clawdbot.md

# 输出：
# 文件大小: 40256 bytes
# Clawdbot Trend Analysis - Comprehensive Findings
#
# Analysis Date: 2026-01-25
```

---

## 总结

| 方法 | 适用场景 | 推荐度 |
|------|---------|--------|
| **curl + 导出 API** | 公开文档 | ⭐⭐⭐⭐⭐ |
| **Chrome DevTools UI** | 需要身份验证 | ⭐⭐⭐⭐ |
| Canvas/iframe 提取 | 不适用 | ❌ |

**核心建议**：
1. ✅ 优先使用 curl + 导出 API（最快最可靠）
2. ✅ Markdown 格式便于后续处理
3. ✅ 验证文件大小和内容头部
4. ❌ 避免使用 Canvas/iframe 方法（无法获取内容）
