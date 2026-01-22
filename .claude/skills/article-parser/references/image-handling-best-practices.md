# 图片处理最佳实践

## 核心原则

### 三版本策略

所有文章创建三个版本：

| 版本 | 文件名 | 图片处理 | 适用场景 |
|------|--------|----------|----------|
| **原始版** | `article.md` | `./images/` 相对路径 | 日常阅读、编辑、本地预览 |
| **standalone 版** | `article-standalone.md` | base64 嵌入 | 离线分享、长期归档 |
| **remote 版** | `article-remote.md` | jsDelivr CDN URL | 在线分享、博客发布 |

**工作流程**：

```
1. 下载所有图片 → images/
2. 创建原始版本 → article.md（引用 ./images/）
3. 生成 standalone 版本 → article-standalone.md（base64 嵌入）
4. 生成 remote 版本 → article-remote.md（jsDelivr CDN）
```

### 统一下载策略

**所有平台都下载图片到本地** `images/` 目录：

```
article-slug/
├── article-slug.md              # 原始版本
├── article-slug-standalone.md   # standalone 版本
├── article-slug.metadata.yaml
└── images/
    ├── G_J7mLHXsAA0gNV.jpg     # Twitter media ID
    ├── google-search.png        # 描述性命名
    └── ...
```

**优点**：
- ✅ 避免外链失效风险
- ✅ 统一的工作流程
- ✅ 便于生成 standalone 版本
- ✅ 本地预览不依赖网络

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
- ✅ **统一下载到本地** `images/` 目录（不再区分平台）
- ✅ 原始版本使用 `./images/` 相对路径
- ✅ standalone 版本嵌入 base64 数据

### 问题 3：无法追溯图片来源

**原因**：没有记录原文 URL 和图片的对应关系。

**解决方案**：
- ✅ 在 `.cache/` 目录创建映射文件
- ✅ 记录原文 URL、media ID、描述等信息
- ✅ 便于后续验证和补充

---

## 5. 提取工作流程（双版本策略）

### 通用工作流程

```python
import base64
import hashlib
from pathlib import Path

def extract_article(article_url, article_dir):
    """统一的文章提取工作流程"""

    # 1. 提取文章内容和图片 URL
    content = extract_article_content(article_url)

    # 2. 下载所有图片到 images/ 目录
    images_dir = Path(article_dir) / 'images'
    images_dir.mkdir(exist_ok=True)

    image_mapping = []
    for i, img in enumerate(content.images, 1):
        # 生成文件名（Media ID 或描述性命名）
        if 'pbs.twimg.com' in img.url:
            media_id = img.url.split('/')[-1].split('?')[0]
            filename = f"{media_id}.jpg"
        else:
            url_hash = hashlib.md5(img.url.encode()).hexdigest()[:12]
            filename = f"{url_hash}.jpg"

        # 下载图片
        download_image(img.url, images_dir / filename)

        # 记录映射
        image_mapping.append({
            'index': i,
            'original_url': img.url,
            'local_filename': filename,
            'context_before': img.context_before,  # 重要！
            'alt_text': img.alt_text
        })

    # 3. 创建缓存映射
    create_image_mapping(article_url, image_mapping, article_dir)

    # 4. 生成原始版本（使用 ./images/ 路径）
    original_md = generate_markdown(content, image_prefix='./images/')
    write_file(article_dir / 'article.md', original_md)

    # 5. 生成 standalone 版本（嵌入 base64）
    standalone_md = convert_to_base64(original_md, images_dir)
    write_file(article_dir / 'article-standalone.md', standalone_md)

    # 6. 生成 remote 版本（jsDelivr CDN）
    remote_md = convert_to_cdn(original_md, user, repo, rel_path)
    write_file(article_dir / 'article-remote.md', remote_md)

    # 7. 验证
    verify_image_positions(original_md, image_mapping)

def convert_to_base64(markdown_content, images_dir):
    """将 markdown 中的本地图片转换为 base64"""
    import re

    def replace_image(match):
        alt_text = match.group(1)
        image_path = match.group(2)

        if image_path.startswith('./images/'):
            filename = image_path.replace('./images/', '')
            full_path = images_dir / filename

            if full_path.exists():
                with open(full_path, 'rb') as f:
                    data = base64.b64encode(f.read()).decode('utf-8')

                # 确定 MIME 类型
                suffix = full_path.suffix.lower()
                mime_map = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                           '.png': 'image/png', '.gif': 'image/gif',
                           '.webp': 'image/webp'}
                mime_type = mime_map.get(suffix, 'image/jpeg')

                return f'![{alt_text}](data:{mime_type};base64,{data})'

        return match.group(0)

    return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, markdown_content)
```

### 使用脚本生成版本

```bash
# 生成 standalone 版本（base64 嵌入）
python scripts/generate_standalone.py article-slug/article-slug.md

# 生成 remote 版本（jsDelivr CDN）
python scripts/generate_remote.py article-slug/article-slug.md

# 批量处理目录
python scripts/generate_standalone.py article-slug/ --recursive
python scripts/generate_remote.py article-slug/ --recursive
```

---

## 6. 验证清单

提取完成后，验证以下检查项：

### 图片完整性

- [ ] 所有图片都已下载到 `images/` 目录
- [ ] 所有图片都有对应的描述
- [ ] 图片顺序与原文一致
- [ ] 没有重复的图片文件名

### 缓存完整性

- [ ] `.cache/` 目录中有映射文件
- [ ] 映射文件包含所有图片的 `context_before`
- [ ] 原始 URL 记录完整

### 三版本验证

- [ ] 原始版本 `article.md` 图片引用 `./images/` 路径
- [ ] standalone 版本 `article-standalone.md` 图片嵌入 base64
- [ ] remote 版本 `article-remote.md` 图片使用 jsDelivr CDN URL
- [ ] 三个版本的图片数量一致
- [ ] standalone 版本文件大小合理（检查是否有图片遗漏）

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

1. **统一下载**：所有平台图片都下载到本地 `images/` 目录
2. **三版本输出**：原始版本（本地路径）、standalone（base64）、remote（CDN）
3. **描述命名**：避免 image-01 这种编号，使用描述性名称或 Media ID
4. **缓存映射**：在 `.cache/` 记录图片映射关系，包含 `context_before` 便于验证
5. **工具验证**：使用脚本自动化生成版本和验证

### 策略对比

| 维度 | 旧方式（外链优先） | 新方式（统一下载） |
|------|--------|--------|
| 命名 | `image-01.jpg` | `G_J8qXqaoAQ2xhu.jpg` 或描述性命名 |
| 存储 | 外链平台直接用 URL | 统一下载到 `images/` |
| 版本 | local / remote | original / standalone / remote |
| 离线分享 | ❌ 不支持 | ✅ standalone 版本 |
| 在线分享 | 依赖外链稳定性 | ✅ remote 版本（jsDelivr CDN） |
| 追溯 | 无记录 | `.cache/` 映射文件 |
| 验证 | 人工检查 | 脚本自动化 |
