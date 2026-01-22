# 图片处理最佳实践

## 核心原则

### 1. 外链友好平台优先使用原始 URL

**适用平台**：Twitter/X、微信公众号、知乎等提供稳定 CDN 的平台

**优点**：
- ✅ 减少本地存储需求
- ✅ 避免下载失败或网络问题
- ✅ 原始 URL 通常包含更多元数据（media ID、格式等）
- ✅ 减少手动编号错误

**示例**：

```markdown
# Twitter/X 文章（推荐：直接使用原始 URL）

![正向反馈](https://pbs.twimg.com/media/G_J8qXqaoAQ2xhu?format=jpg&name=large)

![我的技能库](https://pbs.twimg.com/media/G_J8RtCaoAEX3ST?format=png&name=small)
```

**平台 URL 特征**：

| 平台 | CDN 域名 | URL 特征 | 稳定性 |
|------|---------|---------|--------|
| Twitter/X | `pbs.twimg.com` | 包含 media ID | ⭐⭐⭐⭐⭐ |
| 微信公众号 | `mmbiz.qpic.cn` | 包含 wx_fmt 参数 | ⭐⭐⭐⭐⭐ |
| 知乎 | `zxpic.cn` | 包含图片 ID | ⭐⭐⭐⭐ |

---

## 2. 图片命名策略

### ❌ 不推荐：顺序编号

```markdown
![示例图片](./images/image-01.jpg)
![优势说明](./images/image-02.jpg)
![用户评论](./images/image-03.jpg)  # 容易出错！
```

**问题**：
- 手动编号容易跳号、重号
- 不便于查找和验证
- 插入新图片需要重新编号

### ✅ 推荐：描述性命名或 Media ID

#### 方案 A：使用描述性名称（适合本地保存）

```markdown
![Google 搜索截图](./images/google-search-mp3-to-wav.png)
![Skill 优势说明](./images/skill-advantage.jpg)
![用户评论截图](./images/user-comment-tom.jpg)
```

**命名规则**：
- 使用描述性名称，直接反映图片内容
- 全部小写，空格用连字符替换
- 可以包含来源、场景等信息
- 格式：`{描述}-{来源/场景}.{ext}`

#### 方案 B：使用 Media ID（适合 Twitter 等平台）

```markdown
![正向反馈](./images/G_J8qXqaoAQ2xhu.jpg)
![我的技能库](./images/G_J8RtCaoAEX3ST.png)
```

**优点**：
- Media ID 天然唯一，避免冲突
- 易于从原始 URL 提取
- 便于追溯原文

---

## 3. 缓存映射关系

### 目的

记录原文 URL、图片描述和文件名的对应关系，方便后续验证和追溯。

### 缓存文件结构

```
.claude/skills/article-parser/.cache/
└── images/
    └── {article-slug}/
        └── image-mapping.json
```

### 映射文件格式

```json
{
  "article_url": "https://x.com/Khazix0918/status/2013812311388229792",
  "article_title": "Skills的最正确用法，是将整个Github压缩成你自己的超级技能库",
  "extraction_date": "2026-01-22",
  "images": [
    {
      "index": 1,
      "original_url": "https://pbs.twimg.com/media/G_J7mLHXsAA0gNV?format=png&name=900x900",
      "media_id": "G_J7mLHXsAA0gNV",
      "description": "Google 搜索 MP3 转 WAV",
      "alt_text": "示例图片",
      "context_before": "比如格式转化这破事，没有AI之前，我每次就是去Google搜，MP3转WAV...",
      "context_after": "然后就看着各种各样你也不知道是不是有刺客的链接..."
    },
    {
      "index": 2,
      "original_url": "https://pbs.twimg.com/media/G_J7wRIaoAI5VxQ?format=jpg&name=medium",
      "media_id": "G_J7wRIaoAI5VxQ",
      "description": "skill-creator 打包开源项目",
      "alt_text": "skill-creator",
      "context_before": "skill-creator，打包Github上的开源项目，也是完全没问题的。",
      "context_after": "这种方式，就能最快速度，越过所谓的本地整合包..."
    }
  ]
}
```

**关键字段说明**：

| 字段 | 必填 | 说明 |
|------|-----|------|
| `index` | ✅ | 图片在原文中的顺序 |
| `original_url` | ✅ | 图片原始 URL |
| `media_id` | ⚠️ | Twitter 等平台的媒体 ID |
| `context_before` | ✅ | **图片前的文字**（用于精确定位） |
| `context_after` | ⚠️ | 图片后的文字（辅助验证） |

### 生成映射文件的脚本示例

```python
import json
from datetime import datetime
from pathlib import Path

def create_image_mapping(article_url, images_data, article_dir):
    """创建图片映射缓存文件

    Args:
        article_url: 文章原始 URL
        images_data: 图片信息列表
            [{
                'url': '原始URL',
                'media_id': '媒体ID（如果有）',
                'description': '图片描述',
                'alt_text': 'Alt 文本',
                'position': '在文章中的位置'
            }]
        article_dir: 文章目录路径
    """
    cache_dir = Path('.claude/skills/article-parser/.cache/images')
    cache_dir.mkdir(parents=True, exist_ok=True)

    # 使用文章 slug 作为文件名
    article_slug = Path(article_dir).name
    mapping_file = cache_dir / f'{article_slug}.json'

    mapping = {
        'article_url': article_url,
        'extraction_date': datetime.now().isoformat(),
        'images': []
    }

    for i, img in enumerate(images_data, 1):
        # 从 URL 提取 media_id（Twitter）
        media_id = None
        if 'pbs.twimg.com' in img['url']:
            # Twitter URL: https://pbs.twimg.com/media/G_J8qXqaoAQ2xhu?format=jpg&name=large
            media_id = img['url'].split('/')[-1].split('?')[0]

        # 生成本地文件名（使用 media_id 或描述性名称）
        if media_id:
            local_filename = f"{media_id}.jpg"
        else:
            # 使用描述性名称
            desc = img['description'].lower().replace(' ', '-').replace('/', '-')
            local_filename = f"{desc}.jpg"

        mapping['images'].append({
            'index': i,
            'original_url': img['url'],
            'media_id': media_id,
            'description': img['description'],
            'local_filename': local_filename,
            'alt_text': img.get('alt_text', ''),
            'position_in_article': img.get('position', '')
        })

    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    return mapping_file
```

---

## 4. 常见问题与解决方案

### 问题 1：图片顺序错位（重要！）

**典型错误模式**：

```
原文顺序：                          文章中的错误：
"经典开源项目..." → 无图片          → 放了图片A ❌
"skill-creator"  → 图片A           → 放了图片B ❌
"FFmpeg多模态"   → 图片B           → 放了图片C ❌
"发现评论"       → 图片C           → 放了图片D ❌
```

**图片整体向前错位一位！**

**根本原因**：

1. **图片和文字分离提取**：先拿到所有图片 URL 列表，再单独整理文字，然后靠"感觉"匹配
2. **缺少精确位置锚点**：只记录顺序索引（index: 1, 2, 3...），没有记录图片**紧跟在哪句话后面**
3. **验证环节缺失**：没有逐张对照原文验证"这张图是否紧跟在这段文字后面"

**解决方案：使用上下文锚点**

在缓存映射中记录图片的**上下文文字**，而不仅是顺序号：

```json
{
  "index": 3,
  "media_id": "G_J7wRIaoAI5VxQ",
  "original_url": "https://pbs.twimg.com/media/G_J7wRIaoAI5VxQ?format=jpg",
  "context_before": "skill-creator，打包Github上的开源项目，也是完全没问题的。",
  "context_after": "这种方式，就能最快速度，越过所谓的本地整合包..."
}
```

**验证方法**：

```python
def verify_image_position(markdown_content, image_mapping):
    """通过上下文锚点验证图片位置"""
    for img in image_mapping['images']:
        context_before = img.get('context_before', '')
        image_url = img['original_url']

        # 在 markdown 中查找：context_before 后面是否紧跟着这张图片
        pattern = re.escape(context_before[:50]) + r'.*?' + re.escape(image_url)
        if not re.search(pattern, markdown_content, re.DOTALL):
            print(f"❌ 图片位置错误: {img['media_id']}")
            print(f"   应该在: '{context_before[:30]}...' 之后")
```

**提取时的正确做法**：

1. 在浏览器中滚动原文，**边看边记录**每张图片的上下文
2. 记录格式：`"...这段文字之后" → 图片URL`
3. 整理文章时，通过上下文文字精确定位，而不是靠顺序号

**检查清单**：

- [ ] 每张图片都记录了 `context_before`（图片前的文字）
- [ ] 整理文章时，逐张对照上下文放置图片
- [ ] 完成后运行验证脚本确认位置正确

### 问题 2：外链图片失效

**原因**：某些平台的图片 URL 有时效性。

**解决方案**：
- ✅ 对于 Twitter/X、微信公众号等稳定平台，直接使用原始 URL
- ⚠️ 对于小红书等可能失效的平台，下载到本地并使用描述性命名

### 问题 3：无法追溯图片来源

**原因**：没有记录原文 URL 和图片的对应关系。

**解决方案**：
- ✅ 在 `.cache/` 目录创建映射文件
- ✅ 记录原文 URL、media ID、描述等信息
- ✅ 便于后续验证和补充

---

## 5. 提取工作流程（推荐）

### Twitter/X 文章

```python
# 1. 提取文章内容和图片
article_url = "https://x.com/Khazix0918/status/2013812311388229792"
content = extract_twitter_article(article_url)

# 2. 收集图片信息（保留原始 URL）
images = []
for img in content.images:
    images.append({
        'url': img.url,  # 直接使用原始 URL
        'alt_text': img.alt_text,
        'description': extract_description_from_context(img)
    })

# 3. 创建图片映射缓存
create_image_mapping(article_url, images, article_dir)

# 4. 生成 markdown（直接使用原始 URL）
markdown_content = generate_markdown(content, use_original_urls=True)

# 5. 验证图片顺序
verify_image_order(markdown_content, images)
```

### 小红书图文笔记

```python
# 1. 提取图片 URL
image_urls = extract_xiaohongshu_images(article_url)

# 2. 下载图片并使用描述性命名
for i, url in enumerate(image_urls):
    # 从 OCR 或上下文中提取描述
    description = ocr_image(url)
    filename = f"{description.lower().replace(' ', '-')}.jpg"
    download_image(url, f"images/{filename}")

# 3. 创建缓存映射
create_image_mapping(article_url, image_data, article_dir)

# 4. 生成 markdown
markdown_content = generate_markdown(content, image_dir='images')
```

---

## 6. 验证清单

提取完成后，验证以下检查项：

### 图片完整性

- [ ] 所有图片都有对应的描述
- [ ] 图片顺序与原文一致
- [ ] 没有重复的图片文件名
- [ ] 外链图片 URL 可访问

### 缓存完整性

- [ ] `.cache/` 目录中有映射文件
- [ ] 映射文件包含所有图片信息
- [ ] 原始 URL 记录完整

### 文件组织

- [ ] 图片使用描述性命名或 Media ID
- [ ] 外链友好平台直接使用原始 URL
- [ ] 本地图片有清晰的目录结构

---

## 附录：工具脚本

### verify_images.py

验证文章中的图片引用是否正确：

```python
import re
import json
from pathlib import Path

def verify_images(markdown_file, mapping_file):
    """验证图片引用是否正确"""
    # 读取映射文件
    with open(mapping_file) as f:
        mapping = json.load(f)

    # 读取 markdown 文件
    with open(markdown_file) as f:
        content = f.read()

    # 提取所有图片引用
    images_in_md = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)

    # 验证
    issues = []
    for i, (alt, url) in enumerate(images_in_md, 1):
        # 检查是否有重复
        if images_in_md.count((alt, url)) > 1:
            issues.append(f"重复的图片: {alt} -> {url}")

        # 检查是否在映射中
        found = False
        for img in mapping['images']:
            if img['alt_text'] == alt or img['original_url'] == url:
                found = True
                break

        if not found:
            issues.append(f"未在映射中找到: {alt} -> {url}")

    if issues:
        print("❌ 发现问题：")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ 图片验证通过")
        return True

# 使用示例
verify_images(
    'general/skills-github-toolbox/skills-github-toolbox.md',
    '.claude/skills/article-parser/.cache/images/skills-github-toolbox.json'
)
```

---

## 总结

### 核心建议

1. **外链优先**：Twitter/X、微信公众号等平台直接使用原始 URL
2. **描述命名**：避免 image-01 这种编号，使用描述性名称或 Media ID
3. **缓存映射**：在 `.cache/` 记录图片映射关系，便于追溯和验证
4. **工具验证**：使用脚本自动化验证，避免手动错误

### 对比

| 维度 | 旧方式 | 新方式 |
|------|--------|--------|
| 命名 | `image-01.jpg` | `G_J8qXqaoAQ2xhu.jpg` 或 `user-comment.jpg` |
| 存储 | 必须下载 | 外链平台直接用 URL |
| 追溯 | 无记录 | `.cache/` 映射文件 |
| 验证 | 人工检查 | 脚本自动化 |
