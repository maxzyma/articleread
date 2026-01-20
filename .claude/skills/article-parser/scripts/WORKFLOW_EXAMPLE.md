# GitHub 图床完整工作流示例

本文档展示如何使用 GitHub 图床和双版本 Markdown 功能来处理文章。

---

## 场景：提取微信公众号文章

### 目标

将微信公众号文章提取到本地，图片上传到 GitHub 图床，生成两个版本的 Markdown 文件。

---

## 步骤 1：配置 GitHub Token

**首次使用需要配置（只需一次）：**

```bash
# 1. 访问 GitHub 创建 Token
# https://github.com/settings/tokens
# 权限：repo (full control)

# 2. 设置环境变量
echo 'export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxx"' >> ~/.zshrc
source ~/.zshrc

# 3. 验证配置
echo $GITHUB_TOKEN
```

---

## 步骤 2：提取文章内容

### 2.1 访问微信文章

```bash
# 使用 chrome-devtools MCP 工具
navigate_page "https://mp.weixin.qq.com/s/fSAgfe2V9dUQimAkrPauqQ"
```

### 2.2 提取图片 URL

```javascript
// 滚动页面触发懒加载
window.scrollTo(0, document.body.scrollHeight);
await new Promise(resolve => setTimeout(resolve, 2000));

// 提取所有图片 URL
const content = document.querySelector('#js_content');
const images = Array.from(content.querySelectorAll('img'));
const mmbizImages = images
  .map(img => img['data-src'] || img.src)
  .filter(url => url.includes('mmbiz.qpic.cn') && !url.includes('svg'));

mmbizImages;
```

**示例输出**：
```javascript
[
  "https://mmbiz.qpic.cn/sz_mmbiz_png/J45kic6nKDdnO5nSpib2IIn7m4xMfBx2LFphItiaLHYEhURg5NyicsZzQ6EwfMAVNI6fnRdU7XR50fDETyFyTFrlHA/640?wx_fmt=png&from=appmsg",
  "https://mmbiz.qpic.cn/sz_mmbiz_png/J45kic6nKDdm4KY5zkhhoxo5JgnJYibKWxdia1ib35APwGCBzbuS7630uYo5qDDILFB9b6FReXVAWtia3SkCvaavnkQ/640?wx_fmt=png&from=appmsg",
  // ... 更多图片
]
```

---

## 步骤 3：上传图片到 GitHub 图床

### 3.1 单张图片上传

```bash
python3 .claude/skills/article-parser/scripts/upload_to_github.py \
  "https://mmbiz.qpic.cn/xxx.jpg" \
  wechat
```

**输出**：
```
正在下载图片: https://mmbiz.qpic.cn/xxx.jpg
正在上传到 GitHub: assets/images/wechat/2026-01/uuid-1.jpg
✅ 上传成功!
原始 URL: https://raw.githubusercontent.com/maxzyma/articleread/main/assets/images/wechat/2026-01/uuid-1.jpg
CDN URL:  https://cdn.jsdelivr.net/gh/maxzyma/articlereq/assets/images/wechat/2026-01/uuid-1.jpg

https://cdn.jsdelivr.net/gh/maxzyma/articleread/assets/images/wechat/2026-01/uuid-1.jpg
```

### 3.2 批量上传（推荐）

创建临时脚本 `upload_images.sh`：

```bash
#!/bin/bash

# 图片 URL 列表
IMAGE_URLS=(
  "https://mmbiz.qpic.cn/sz_mmbiz_png/J45kic6nKDdnO5nSpib2IIn7m4xMfBx2LFphItiaLHYEhURg5NyicsZzQ6EwfMAVNI6fnRdU7XR50fDETyFyTFrlHA/640?wx_fmt=png&from=appmsg"
  "https://mmbiz.qpic.cn/sz_mmbiz_png/J45kic6nKDdm4KY5zkhhoxo5JgnJYibKWxdia1ib35APwGCBzbuS7630uYo5qDDILFB9b6FReXVAWtia3SkCvaavnkQ/640?wx_fmt=png&from=appmsg"
  # ... 更多图片
)

# 上传脚本路径
UPLOAD_SCRIPT="../../.claude/skills/article-parser/scripts/upload_to_github.py"

# 批量上传
declare -a CDN_URLS
for i in "${!IMAGE_URLS[@]}"; do
  echo "上传图片 $((i+1))/${#IMAGE_URLS[@]}..."

  CDN_URL=$(python3 "$UPLOAD_SCRIPT" "${IMAGE_URLS[$i]}" wechat)
  CDN_URLS+=("$CDN_URL")

  echo "✅ 图片 $((i+1)) 上传完成"
  echo ""
done

# 输出所有 CDN URL
echo -e "\n========== CDN URLs =========="
for url in "${CDN_URLS[@]}"; do
  echo "$url"
done
```

运行：

```bash
bash upload_images.sh
```

---

## 步骤 4：创建本地版本 Markdown

创建 `boris-claude-code-workflow.md`：

```markdown
# Claude Code 之父的工作流火了：740 万围观的背后

> 来源：微信公众号 AI信息Gap，2026-01-16
> 原文链接：https://mp.weixin.qq.com/s/fSAgfe2V9dUQimAkrPauqQ

## 核心观点

**Boris Cherny（Claude Code 创造者）在 X 上分享个人工作流...**

---

## 01｜15 个 Claude 并行

Boris 的日常是这样的：终端里开 5 个 Claude Code...

![Boris Cherny 的 Claude Code 工作流](./images/01_section01.jpg)

---

## 02｜用最慢的模型，反而最快

这条可能是整个帖子里最反直觉的...

![Boris 关于使用 Opus 4.5 Thinking 的说明](./images/02_section02.jpg)

---
```

**关键点**：
- 使用本地图片路径：`./images/01_section01.jpg`
- 这个版本用于本地预览和编辑

---

## 步骤 5：生成远程版本 Markdown

### 5.1 使用自动化脚本（推荐）

```bash
bash ../../.claude/skills/article-parser/scripts/generate_dual_version.sh \
  boris-claude-code-workflow.md
```

**输出**：
```
🔍 自动检测 CDN URL...
✅ 检测到 CDN URL: https://cdn.jsdelivr.net/gh/maxzyma/articleread/assets/images/wechat/2026-01

📝 生成远程版本...
  源文件: boris-claude-code-workflow.md
  目标文件: boris-claude-code-workflow-remote.md
  CDN URL: https://cdn.jsdelivr.net/gh/maxzyma/articleread/assets/images/wechat/2026-01

✅ 双版本生成完成！
  📄 本地版本: boris-claude-code-workflow.md
  🖼️  图片数量: 8

💡 提示：
  - 本地版本使用相对路径，适合本地预览
  - 远程版本使用 CDN URL，可以分享给别人
  - 两个版本内容同步，只有图片路径不同

✅ 验证通过：远程版本包含 8 张图片
```

### 5.2 使用 sed 命令

```bash
# 替换图片路径
sed 's|(\./images/|(https://cdn.jsdelivr.net/gh/maxzyma/articleread/assets/images/wechat/2026-01/|g' \
  boris-claude-code-workflow.md \
  > boris-claude-code-workflow-remote.md
```

---

## 步骤 6：验证结果

### 6.1 检查本地版本

```bash
grep -n '\[.*\](./images/' boris-claude-code-workflow.md | head -3
```

**输出**：
```
11:![Boris Cherny 在 X 上分享 Claude Code 工作流](./images/00_cover.jpg)
40:![Boris Cherny 的 Claude Code 工作流](./images/01_section01.jpg)
64:![Boris 关于使用 Opus 4.5 Thinking 的说明](./images/02_section02.jpg)
```

### 6.2 检查远程版本

```bash
grep -n '\[.*\](https://cdn' boris-claude-code-workflow-remote.md | head -3
```

**输出**：
```
11:![Boris Cherny 在 X 上分享 Claude Code 工作流](https://cdn.jsdelivr.net/gh/maxzyma/articleread/assets/images/wechat/2026-01/00_cover.jpg)
40:![Boris Cherny 的 Claude Code 工作流](https://cdn.jsdelivr.net/gh/maxzyma/articleread/assets/images/wechat/2026-01/01_section01.jpg)
64:![Boris 关于使用 Opus 4.5 Thinking 的说明](https://cdn.jsdelivr.net/gh/maxzyma/articleread/assets/images/wechat/2026-01/02_section02.jpg)
```

---

## 步骤 7：提交到 Git

### 7.1 查看文件结构

```bash
ls -la boris-claude-code-workflow/
```

**输出**：
```
-rw-r--r--  1 user  staff  6767 Jan 20 13:52 boris-claude-code-workflow.md
-rw-r--r--  1 user  staff  7311 Jan 20 14:58 boris-claude-code-workflow-remote.md
-rw-r--r--  1 user  staff  1234 Jan 20 14:30 boris-claude-code-workflow.metadata.yaml
drwxr-xr-x  8 user  staff   256 Jan 20 13:52 images/
├── 00_cover.jpg
├── 01_section01.jpg
└── ...
```

### 7.2 提交策略

**方案 A：只提交本地版本**（推荐）

```bash
# .gitignore 已配置忽略 images/ 和 *-remote.md
git add boris-claude-code-workflow.md
git commit -m "Add article: Boris Cherny Claude Code workflow"
```

**方案 B：双版本都提交**

```bash
git add boris-claude-code-workflow.md \
        boris-claude-code-workflow-remote.md \
        boris-claude-code-workflow.metadata.yaml
git commit -m "Add article with local and remote versions"
```

---

## 完整工作流脚本

创建一个完整的工作流脚本 `extract_and_host.sh`：

```bash
#!/bin/bash
set -e

ARTICLE_URL="$1"
ARTICLE_TITLE="$2"

if [ -z "$ARTICLE_URL" ] || [ -z "$ARTICLE_TITLE" ]; then
  echo "使用方式: $0 <文章URL> <文章标题>"
  exit 1
fi

# 1. 创建文章目录
SLUG=$(echo "$ARTICLE_TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g')
ARTICLE_DIR="general/$(date +%Y-%m-%d)/$SLUG"
mkdir -p "$ARTICLE_DIR/images"

echo "📁 创建目录: $ARTICLE_DIR"
cd "$ARTICLE_DIR"

# 2. 提取图片 URL（手动从浏览器执行）
echo ""
echo "📋 请在浏览器中执行以下 JavaScript 代码提取图片 URL："
echo "---"
cat << 'EOF'
const content = document.querySelector('#js_content');
const images = Array.from(content.querySelectorAll('img'));
const mmbizImages = images
  .map(img => img['data-src'] || img.src)
  .filter(url => url.includes('mmbiz.qpic.cn') && !url.includes('svg'));
copy(mmbizImages.join('\n'));
EOF
echo "---"
echo ""
read -p "按 Enter 继续（已复制图片 URL）..."

# 3. 粘贴图片 URL
echo ""
echo "📋 请粘贴提取的图片 URL（每行一个，按 Ctrl+D 结束）："
IMAGE_URLS=()
while IFS= read -r line; do
  [[ -n "$line" ]] && IMAGE_URLS+=("$line")
done

echo "✓ 已获取 ${#IMAGE_URLS[@]} 张图片"

# 4. 批量上传图片
echo ""
echo "☁️  开始上传图片到 GitHub..."
UPLOAD_SCRIPT="../../.claude/skills/article-parser/scripts/upload_to_github.py"
PLATFORM="wechat"

for i in "${!IMAGE_URLS[@]}"; do
  echo "  [$((i+1))/${#IMAGE_URLS[@]}] 上传中..."
  python3 "$UPLOAD_SCRIPT" "${IMAGE_URLS[$i]}" "$PLATFORM" 2>/dev/null | tail -1
done

# 5. 创建本地版本（需要手动编写内容）
echo ""
echo "📝 请创建本地版本 Markdown："
echo "  文件: $SLUG.md"
echo "  图片路径: ./images/00_cover.jpg, ./images/01_section01.jpg, ..."
echo ""
read -p "按 Enter 继续（已创建本地版本）..."

# 6. 生成远程版本
echo ""
echo "🔄 生成远程版本..."
bash ../../.claude/skills/article-parser/scripts/generate_dual_version.sh "$SLUG.md"

# 7. 完成
echo ""
echo "✅ 完成！"
echo ""
echo "📄 文件位置："
echo "  本地版本: $SLUG.md"
echo "  远程版本: $SLUG-remote.md"
echo "  图片目录: images/"
echo ""
echo "📊 统计："
echo "  文章标题: $ARTICLE_TITLE"
echo "  图片数量: ${#IMAGE_URLS[@]}"
echo "  文章URL: $ARTICLE_URL"
echo ""
```

---

## 总结

### 完整流程图

```
提取文章 → 上传图片 → 创建本地版本 → 生成远程版本 → 提交 Git
    ↓           ↓              ↓                ↓              ↓
  浏览器     GitHub      ./images/      -remote.md     git push
           图床
```

### 文件对应关系

| 文件 | 图片路径 | 用途 |
|------|---------|------|
| `article.md` | `./images/xxx.jpg` | 本地查看、编辑 |
| `article-remote.md` | `https://cdn.jsdelivr.net/gh/...` | 分享、发布 |
| `article.metadata.yaml` | - | 元数据 |

### 优势

✅ **本地版本**：
- 快速预览
- 离线查看
- 无网络依赖

✅ **远程版本**：
- 完全可分享
- CDN 加速
- 全球可访问

✅ **自动化**：
- 仓库自动检测
- CDN URL 自动生成
- 一键生成双版本
