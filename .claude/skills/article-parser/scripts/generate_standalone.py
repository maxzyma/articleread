#!/usr/bin/env python3
"""
将 markdown 中的本地图片引用转换为 base64 嵌入

用法：
    python generate_standalone.py article.md                    # 输出到 article-standalone.md
    python generate_standalone.py article.md -o output.md       # 指定输出文件
    python generate_standalone.py article-dir/                  # 处理目录
    python generate_standalone.py article-dir/ --recursive      # 递归处理

功能：
    - 匹配 ![alt](./images/xxx.jpg) 格式的图片引用
    - 将图片转换为 base64 data URI
    - 支持 jpg, png, gif, webp, svg, bmp 格式
"""

import argparse
import base64
import re
import sys
from pathlib import Path

MIME_MAP = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.svg': 'image/svg+xml',
    '.bmp': 'image/bmp',
}

def image_to_base64(image_path: Path) -> tuple[str, str]:
    """将图片文件转换为 base64 编码

    Returns:
        tuple: (base64_data, mime_type)
    """
    suffix = image_path.suffix.lower()
    mime_type = MIME_MAP.get(suffix, 'image/jpeg')

    with open(image_path, 'rb') as f:
        data = f.read()

    b64 = base64.b64encode(data).decode('utf-8')
    return b64, mime_type

def generate_standalone(md_file: Path, output_file: Path = None) -> dict:
    """将 markdown 中的本地图片引用转换为 base64

    Args:
        md_file: 输入的 markdown 文件路径
        output_file: 输出文件路径，默认为 {原文件名}-standalone.md

    Returns:
        dict: 处理结果统计
    """
    if output_file is None:
        output_file = md_file.parent / f"{md_file.stem}-standalone{md_file.suffix}"

    content = md_file.read_text(encoding='utf-8')
    images_dir = md_file.parent / 'images'

    stats = {
        'total': 0,
        'converted': 0,
        'failed': 0,
        'failed_files': []
    }

    # 匹配 ![alt](./images/xxx.jpg) 格式
    pattern = r'!\[([^\]]*)\]\(\./images/([^)]+)\)'

    def replace_image(match):
        alt_text = match.group(1)
        filename = match.group(2)
        image_path = images_dir / filename

        stats['total'] += 1

        if not image_path.exists():
            stats['failed'] += 1
            stats['failed_files'].append(filename)
            print(f"  [WARN] 图片不存在: {filename}")
            return match.group(0)  # 保持原样

        try:
            b64_data, mime_type = image_to_base64(image_path)
            stats['converted'] += 1
            return f'![{alt_text}](data:{mime_type};base64,{b64_data})'
        except Exception as e:
            stats['failed'] += 1
            stats['failed_files'].append(filename)
            print(f"  [ERROR] 转换失败 {filename}: {e}")
            return match.group(0)

    new_content = re.sub(pattern, replace_image, content)
    output_file.write_text(new_content, encoding='utf-8')

    return stats

def process_directory(dir_path: Path, recursive: bool = False) -> dict:
    """处理目录中的 markdown 文件

    Args:
        dir_path: 目录路径
        recursive: 是否递归处理子目录
    """
    pattern = '**/*.md' if recursive else '*.md'
    md_files = list(dir_path.glob(pattern))

    # 排除已有的 -standalone.md 文件
    md_files = [f for f in md_files if not f.stem.endswith('-standalone')]

    total_stats = {'files': 0, 'images': 0, 'converted': 0, 'failed': 0}

    for md_file in md_files:
        images_dir = md_file.parent / 'images'
        if not images_dir.exists():
            continue

        print(f"\n处理: {md_file}")
        stats = generate_standalone(md_file)

        if stats['total'] > 0:
            total_stats['files'] += 1
            total_stats['images'] += stats['total']
            total_stats['converted'] += stats['converted']
            total_stats['failed'] += stats['failed']

            print(f"  转换: {stats['converted']}/{stats['total']} 图片")

    return total_stats

def main():
    parser = argparse.ArgumentParser(
        description='将 markdown 中的本地图片转换为 base64 嵌入'
    )
    parser.add_argument('input', help='输入文件或目录')
    parser.add_argument('-o', '--output', help='输出文件（仅单文件模式）')
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='递归处理子目录')

    args = parser.parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"错误: 路径不存在: {input_path}")
        sys.exit(1)

    if input_path.is_file():
        # 单文件模式
        output_path = Path(args.output) if args.output else None
        print(f"处理文件: {input_path}")
        stats = generate_standalone(input_path, output_path)

        output_name = output_path or input_path.parent / f"{input_path.stem}-standalone{input_path.suffix}"
        print(f"\n结果:")
        print(f"  输出: {output_name}")
        print(f"  转换: {stats['converted']}/{stats['total']} 图片")

        if stats['failed'] > 0:
            print(f"  失败: {stats['failed']} ({', '.join(stats['failed_files'])})")
            sys.exit(1)

    elif input_path.is_dir():
        # 目录模式
        print(f"处理目录: {input_path}")
        print(f"递归: {'是' if args.recursive else '否'}")

        stats = process_directory(input_path, args.recursive)

        print(f"\n总计:")
        print(f"  处理文件: {stats['files']}")
        print(f"  转换图片: {stats['converted']}/{stats['images']}")

        if stats['failed'] > 0:
            print(f"  失败: {stats['failed']}")
            sys.exit(1)

if __name__ == '__main__':
    main()
