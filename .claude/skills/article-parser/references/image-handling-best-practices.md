# 图片处理最佳实践

**本文档是图片处理的唯一真相源（Single Source of Truth）**。

本文档详细说明图片处理的所有高级技术实现，包括：外链策略、命名规范、缓存映射、验证工具等。

## 📋 文档定位

- **本文档**：完整的图片处理指南（唯一真相源）
- **SKILL.md**：快速参考和摘要（指向本文档）

---

## 核心原则

1. **外链友好平台优先使用原始 URL**：Twitter/X、微信公众号、知乎等平台提供稳定 CDN，直接使用原始 URL 可减少本地存储需求。

2. **⚠️ Standalone 版本必须使用 base64 内嵌图片**：无论平台是否支持外链，standalone 版本的图片**必须**使用 base64 数据 URI 嵌入，确保文件完全独立可移植。

**三个版本的图片处理规则**：
- **Original 版本**：使用相对路径或外链 URL（根据平台类型）
- **Standalone 版本**：**强制使用 base64**，不接受外链（这是唯一真正独立的版本）
- **Remote 版本**：使用外链 CDN URL（便于在线分享）

---

## 缓存映射关系（防止图片顺序错位）

### 目的

记录图片与上下文的精确对应关系，防止图片顺序错位。

**核心规则**：使用 `context_before` 和 `context_after` 作为锚点，精确定位图片在文章中的位置。

### 缓存文件结构

```
.claude/skills/article-parser/.cache/images/
└── {article-slug}/
    └── image-mapping.json
```

### 映射文件格式

```json
{
  "article_url": "https://x.com/Khazix0918/status/2013812311388229792",
  "article_title": "Skills的最正确用法",
  "extraction_date": "2026-01-22",
  "images": [
    {
      "index": 1,
      "original_url": "https://pbs.twimg.com/media/G_J7mLHXsAA0gNV?format=png&name=900x900",
      "media_id": "G_J7mLHXsAA0gNV",
      "description": "示例图片 - Google搜索",
      "local_filename": "google-search-mp3-to-wav.png",
      "alt_text": "示例图片",
      "context_before": "skill-creator，打包Github上的开源项目",
      "context_after": "可以快速创建技能包"
    },
    {
      "index": 2,
      "original_url": "https://pbs.twimg.com/media/G_J8qXqaoAQ2xhu?format=jpg&name=large",
      "media_id": "G_J8qXqaoAQ2xhu",
      "description": "正向反馈",
      "local_filename": "G_J8qXqaoAQ2xhu.jpg",
      "alt_text": "正向反馈",
      "context_before": "用户反馈非常好",
      "context_after": "提升了效率"
    }
  ]
}
```

**关键字段**：
- `context_before`（必需）：图片前的文字片段，作为关键锚点
- `context_after`（可选）：图片后的文字片段，辅助验证

### 生成映射文件的脚本

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
                'context_before': '图片前的文字',
                'context_after': '图片后的文字（可选）'
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
            media_id = img['url'].split('/')[-1].split('?')[0]

        # 生成本地文件名（使用 media_id 或描述性名称）
        if media_id:
            local_filename = f"{media_id}.jpg"
        else:
            desc = img['description'].lower().replace(' ', '-').replace('/', '-')
            local_filename = f"{desc}.jpg"

        mapping['images'].append({
            'index': i,
            'original_url': img['url'],
            'media_id': media_id,
            'description': img['description'],
            'local_filename': local_filename,
            'alt_text': img.get('alt_text', ''),
            'context_before': img.get('context_before', ''),
            'context_after': img.get('context_after', '')
        })

    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    return mapping_file
```

---

## 验证工具脚本

### verify_images.py

验证文章中的图片引用是否正确，包括：
- 检查是否有重复的图片引用
- 验证每张图片是否在映射文件中
- 根据 context_before 验证图片位置是否正确

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

    # 1. 检查重复引用
    for i, (alt, url) in enumerate(images_in_md, 1):
        if images_in_md.count((alt, url)) > 1:
            issues.append(f"重复的图片: {alt} -> {url}")

    # 2. 检查是否在映射中
    for alt, url in images_in_md:
        found = False
        for img in mapping['images']:
            if img['alt_text'] == alt or img['original_url'] == url:
                found = True
                break

        if not found:
            issues.append(f"未在映射中找到: {alt} -> {url}")

    # 3. 根据 context_before 验证图片位置
    for img in mapping['images']:
        if img.get('context_before'):
            # 查找 context_before 在文章中出现的位置
            before_pos = content.find(img['context_before'])
            if before_pos == -1:
                issues.append(f"找不到锚点文字: {img['context_before']}")
                continue

            # 查找图片引用的位置
            img_ref = f"![{img['alt_text']}]"
            img_pos = content.find(img_ref, before_pos)

            # 验证图片是否紧跟在锚点文字后面（合理范围内）
            if img_pos == -1 or img_pos - before_pos > 500:
                issues.append(
                    f"图片位置可能不对: {img['alt_text']} "
                    f"（应该在 '{img['context_before']}' 附近）"
                )

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

## 生成 Standalone 版本（Base64 内嵌）

### ⚠️ 关键规则

**Standalone 版本必须使用 base64 内嵌图片，无论平台是否支持外链。**

### Python 实现示例

```python
import base64
import re
from pathlib import Path

def generate_standalone_version(markdown_file, output_file):
    """生成 standalone 版本，将所有图片转换为 base64 内嵌

    Args:
        markdown_file: 原始 markdown 文件路径
        output_file: 输出的 standalone 文件路径
    """
    # 读取原始文件
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取所有图片 URL
    image_urls = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)

    # 为每个图片下载并转换为 base64
    for alt_text, url in image_urls:
        # 跳过已经是 base64 的图片
        if url.startswith('data:'):
            continue

        try:
            # 下载图片
            import requests
            response = requests.get(url)
            response.raise_for_status()

            # 转换为 base64
            image_data = response.content
            # 检测图片类型
            content_type = response.headers.get('content-type', 'image/png')
            base64_data = base64.b64encode(image_data).decode('utf-8')
            data_uri = f"data:{content_type};base64,{base64_data}"

            # 替换 URL 为 data URI
            old_ref = f"[{alt_text}]({url})"
            new_ref = f"[{alt_text}]({data_uri})"
            content = content.replace(old_ref, new_ref)

            print(f"✅ 转换图片: {alt_text}")

        except Exception as e:
            print(f"❌ 转换失败 {alt_text}: {e}")
            # 保留原 URL
            continue

    # 写入 standalone 版本
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Standalone 版本已生成: {output_file}")
    print(f"文件大小: {Path(output_file).stat().st_size / 1024:.1f} KB")

# 使用示例
generate_standalone_version(
    'general/article/article.md',
    'general/article/article-standalone.md'
)
```

### 批量转换脚本

```bash
#!/bin/bash
# convert_to_base64.sh

# 为每个图片 URL 下载并转换为 base64
download_and_convert() {
    local url="$1"
    local output_file="$2"

    # 下载图片
    curl -s \
        -H "Referer: https://mp.weixin.qq.com/" \
        -H "User-Agent: Mozilla/5.0" \
        "$url" \
        -o "$output_file"

    # 转换为 base64
    base64_data=$(base64 -i "$output_file")
    echo "data:image/png;base64,$base64_data" > "${output_file}.b64"
}

# 示例：转换微信文章图片
imgIndex=1
download_and_convert \
    "https://mmbiz.qpic.cn/sz_mmbiz_png/...#imgIndex=${imgIndex}" \
    "image_${imgIndex}.png"
```

### 验证 Standalone 版本

```python
def verify_standalone(markdown_file):
    """验证 standalone 版本是否完全独立

    检查：
    1. 是否有外链 URL（应该为 0）
    2. 所有图片是否为 base64 格式
    3. 文件大小合理（base64 会显著增大）
    """
    with open(markdown_file, 'r') as f:
        content = f.read()

    # 检查外链
    external_links = re.findall(r'!\[([^\]]*)\]\((https?://[^)]+)\)', content)

    # 检查 base64 图片
    base64_images = re.findall(r'!\[([^\]]*)\]\((data:[^)]+)\)', content)

    issues = []

    if external_links:
        issues.append(f"发现 {len(external_links)} 个外链图片（standalone 不应有外链）")

    if not base64_images:
        issues.append("未找到 base64 图片")

    if issues:
        print("❌ Standalone 版本验证失败：")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"✅ Standalone 版本验证通过")
        print(f"  - Base64 图片: {len(base64_images)} 个")
        print(f"  - 外链图片: 0 个")
        print(f"  - 文件大小: {Path(markdown_file).stat().st_size / 1024:.1f} KB")
        return True

# 使用示例
verify_standalone('general/article/article-standalone.md')
```

---

## 提取工作流程示例

### Twitter/X 文章

```python
# 1. 提取文章内容和图片
article_url = "https://x.com/Khazix0918/status/2013812311388229792"
content = extract_twitter_article(article_url)

# 2. 收集图片信息（保留原始 URL，记录上下文）
images = []
for img in content.images:
    # 提取图片前后的文字作为锚点
    context_before = extract_text_before(img)
    context_after = extract_text_after(img)

    images.append({
        'url': img.url,  # 直接使用原始 URL
        'alt_text': img.alt_text,
        'description': extract_description_from_context(img),
        'context_before': context_before,
        'context_after': context_after
    })

# 3. 创建图片映射缓存
create_image_mapping(article_url, images, article_dir)

# 4. 生成 markdown（直接使用原始 URL）
markdown_content = generate_markdown(content, use_original_urls=True)

# 5. 验证图片顺序
verify_images(markdown_file, mapping_file)
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

# 3. 创建缓存映射（记录上下文锚点）
image_data = extract_with_context(article_url)
create_image_mapping(article_url, image_data, article_dir)

# 4. 生成 markdown
markdown_content = generate_markdown(content, image_dir='images')

# 5. 验证图片顺序
verify_images(markdown_file, mapping_file)
```

---

## 总结

### 核心原则

1. **外链优先**：Twitter/X、微信公众号等平台直接使用原始 URL（original 和 remote 版本）
2. **Standalone 强制 base64**：standalone 版本**必须**使用 base64 内嵌，无论平台是否支持外链
3. **上下文锚点**：使用 context_before 精确定位图片位置，防止错位
4. **缓存映射**：在 `.cache/` 记录图片映射关系，便于追溯和验证
5. **工具验证**：使用脚本自动化验证，避免手动错误

### 三个版本的图片策略

| 版本 | 图片来源 | 使用场景 | 示例 |
|------|---------|---------|------|
| **Original** | 相对路径或外链 | 本地归档，保留灵活性 | `./images/image-1.png` 或外链 URL |
| **Standalone** | **Base64 内嵌** | 完全独立的单文件，便于分享 | `data:image/png;base64,iVBORw0KGgo...` |
| **Remote** | CDN 外链 | 在线分享，快速加载 | `https://mmbiz.qpic.cn/...` |

**⚠️ 关键规则**：Standalone 版本**必须**使用 base64，这是唯一确保文件完全独立可移植的方式。即使平台支持外链（如微信、Twitter），standalone 版本也不应使用外链。

### 旧方式 vs 新方式

| 维度 | 旧方式 | 新方式 |
|------|--------|--------|
| 命名 | `image-01.jpg` | `G_J8qXqaoAQ2xhu.jpg` 或 `user-comment.jpg` |
| 存储 | 必须下载 | 外链平台直接用 URL |
| 定位 | 靠顺序号 | context_before 锚点精确定位 |
| 追溯 | 无记录 | `.cache/` 映射文件 |
| 验证 | 人工检查 | 脚本自动化 |

---

### 相关文档

- [validation-checklist.md](validation-checklist.md)：完整的验证清单
- [SKILL.md](../SKILL.md)：快速参考（本文档的摘要版）
- [wechat-article-best-practices.md](wechat-article-best-practices.md)：微信公众号特殊处理
