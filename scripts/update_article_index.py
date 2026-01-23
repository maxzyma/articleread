#!/usr/bin/env python3
"""
自动更新 article-index.md

用法：
    python scripts/update_article_index.py
"""

import yaml
from pathlib import Path
from datetime import datetime


def load_articles():
    """加载所有文章元数据"""
    articles = []

    for meta_file in Path('.').rglob('*.metadata.yaml'):
        try:
            with open(meta_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if not data or 'title' not in data:
                continue

            title = data.get('title', 'Untitled')
            extraction_date = data.get('extraction_date', '1970-01-01')
            source = data.get('source', {})
            platform = source.get('platform', 'Unknown')

            # 获取目录路径
            dir_path = str(meta_file.parent)

            # 获取主 markdown 文件名
            content_file = data.get('content_file', '')
            if content_file.startswith('./'):
                content_file = content_file[2:]

            articles.append({
                'title': title,
                'date': extraction_date,
                'platform': platform,
                'dir': dir_path,
                'file': content_file
            })
        except Exception as e:
            print(f"[WARN] 跳过 {meta_file}: {e}")

    return articles


def generate_index(articles):
    """生成 Markdown 索引"""
    # 按日期倒序排序
    articles.sort(key=lambda x: x['date'], reverse=True)

    lines = []
    lines.append("# 文章索引\n")
    lines.append(f"**更新时间**: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"**总计**: {len(articles)} 篇\n")
    lines.append("---\n")

    # 按年月分组
    current_year_month = None

    for article in articles:
        date = article['date']
        year_month = date[:7]  # YYYY-MM

        # 新的月份标题
        if year_month != current_year_month:
            current_year_month = year_month
            lines.append(f"\n## {year_month}\n")
            lines.append("| 日期 | 标题 | 来源 | 文件路径 |")
            lines.append("|------|------|------|----------|")

        # 表格行
        month_day = date[5:]  # MM-DD
        title_link = f"[{article['title']}]({article['dir']}/{article['file']})"
        dir_short = article['dir'].split('/')[-1]  # 只显示最后一层目录

        lines.append(f"| {month_day} | {title_link} | {article['platform']} | `{dir_short}/` |")

    # 统计信息
    lines.append("\n---\n")
    lines.append("## 按主题统计\n")

    general_count = sum(1 for a in articles if a['dir'].startswith('general/'))
    memory_count = sum(1 for a in articles if a['dir'].startswith('knowledge&memory/'))

    lines.append(f"- **General (通用)**: {general_count} 篇")
    lines.append(f"- **Knowledge & Memory (知识与记忆)**: {memory_count} 篇")

    lines.append("\n---\n")
    lines.append("**说明**：此索引由脚本自动生成。更新命令：\n")
    lines.append("```bash\npython3 scripts/update_article_index.py\n```\n")

    return '\n'.join(lines)


if __name__ == '__main__':
    articles = load_articles()
    index_content = generate_index(articles)

    index_file = Path('article-index.md')
    index_file.write_text(index_content, encoding='utf-8')

    print(f"✓ 索引已更新: {index_file}")
    print(f"  总计: {len(articles)} 篇")
