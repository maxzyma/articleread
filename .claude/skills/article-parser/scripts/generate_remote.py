#!/usr/bin/env python3
"""
将 markdown 中的本地图片引用转换为 jsDelivr CDN URL

用法：
    python generate_remote.py article.md                           # 自动检测仓库信息
    python generate_remote.py article.md -o output.md              # 指定输出文件
    python generate_remote.py article.md --repo user/repo          # 指定仓库
    python generate_remote.py article-dir/ --recursive             # 递归处理

功能：
    - 匹配 ![alt](./images/xxx.jpg) 格式的图片引用
    - 替换为 jsDelivr CDN URL
    - 自动检测 git 仓库信息
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

def find_project_root(start_path: Path = None) -> Path:
    """查找项目根目录（包含 .git 的目录）"""
    if start_path is None:
        start_path = Path(__file__).resolve().parent

    # 从脚本目录向上查找 .git 目录
    current = start_path
    while current != current.parent:
        if (current / '.git').exists():
            return current
        current = current.parent

    # 如果找不到 .git，返回当前工作目录
    return Path.cwd()

def get_git_repo_info(file_path: Path) -> tuple[str, str]:
    """从 git 仓库获取用户名和仓库名

    Returns:
        tuple: (user, repo) 或 (None, None) 如果获取失败
    """
    try:
        # 获取 remote URL
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True,
            text=True,
            cwd=file_path.parent if file_path.is_file() else file_path
        )

        if result.returncode != 0:
            return None, None

        remote_url = result.stdout.strip()

        # 解析 URL (支持 HTTPS 和 SSH 格式)
        # HTTPS: https://github.com/user/repo.git
        # SSH: git@github.com:user/repo.git
        if 'github.com' in remote_url:
            if remote_url.startswith('https://'):
                parts = remote_url.replace('https://github.com/', '').replace('.git', '').split('/')
            elif remote_url.startswith('git@'):
                parts = remote_url.replace('git@github.com:', '').replace('.git', '').split('/')
            else:
                return None, None

            if len(parts) >= 2:
                return parts[0], parts[1]

    except Exception:
        pass

    return None, None

def get_relative_path_from_repo_root(file_path: Path) -> str:
    """获取文件相对于仓库根目录的路径"""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            cwd=file_path.parent if file_path.is_file() else file_path
        )

        if result.returncode == 0:
            repo_root = Path(result.stdout.strip())
            return str(file_path.parent.relative_to(repo_root))

    except Exception:
        pass

    return None

def generate_remote(md_file: Path, output_file: Path = None, repo: str = None) -> dict:
    """将 markdown 中的本地图片引用转换为 jsDelivr CDN URL

    Args:
        md_file: 输入的 markdown 文件路径
        output_file: 输出文件路径，默认为 {原文件名}-remote.md
        repo: GitHub 仓库 (格式: user/repo)

    Returns:
        dict: 处理结果统计
    """
    if output_file is None:
        output_file = md_file.parent / f"{md_file.stem}-remote{md_file.suffix}"

    # 获取仓库信息
    if repo:
        user, repo_name = repo.split('/')
    else:
        user, repo_name = get_git_repo_info(md_file)
        if not user or not repo_name:
            print("  [ERROR] 无法自动检测 git 仓库信息，请使用 --repo 参数指定")
            return {'total': 0, 'converted': 0, 'failed': 1, 'failed_files': ['git info']}

    # 获取相对路径
    rel_path = get_relative_path_from_repo_root(md_file)
    if not rel_path:
        # 尝试从当前工作目录计算相对路径
        try:
            cwd = Path.cwd()
            rel_path = str(md_file.parent.relative_to(cwd))
            print(f"  [INFO] 使用相对于工作目录的路径: {rel_path}")
        except ValueError:
            print("  [WARN] 无法获取相对路径，使用文件所在目录")
            rel_path = md_file.parent.name

    # 构建 CDN base URL
    # jsDelivr 格式: https://cdn.jsdelivr.net/gh/user/repo/path/to/images
    cdn_base = f"https://cdn.jsdelivr.net/gh/{user}/{repo_name}/{rel_path}/images"

    content = md_file.read_text(encoding='utf-8')

    stats = {
        'total': 0,
        'converted': 0,
        'failed': 0,
        'failed_files': [],
        'cdn_base': cdn_base
    }

    # 匹配 ![alt](./images/xxx.jpg) 格式
    pattern = r'!\[([^\]]*)\]\(\./images/([^)]+)\)'

    def replace_image(match):
        alt_text = match.group(1)
        filename = match.group(2)

        stats['total'] += 1
        stats['converted'] += 1

        return f'![{alt_text}]({cdn_base}/{filename})'

    new_content = re.sub(pattern, replace_image, content)
    output_file.write_text(new_content, encoding='utf-8')

    return stats

def process_directory(dir_path: Path, recursive: bool = False, repo: str = None) -> dict:
    """处理目录中的 markdown 文件"""
    pattern = '**/*.md' if recursive else '*.md'
    md_files = list(dir_path.glob(pattern))

    # 排除已有的 -remote.md 和 -standalone.md 文件
    md_files = [f for f in md_files
                if not f.stem.endswith('-remote')
                and not f.stem.endswith('-standalone')]

    total_stats = {'files': 0, 'images': 0, 'converted': 0, 'failed': 0}

    for md_file in md_files:
        images_dir = md_file.parent / 'images'
        if not images_dir.exists():
            continue

        print(f"\n处理: {md_file}")
        stats = generate_remote(md_file, repo=repo)

        if stats['total'] > 0:
            total_stats['files'] += 1
            total_stats['images'] += stats['total']
            total_stats['converted'] += stats['converted']
            total_stats['failed'] += stats['failed']

            print(f"  转换: {stats['converted']}/{stats['total']} 图片")
            if 'cdn_base' in stats:
                print(f"  CDN: {stats['cdn_base']}")

    return total_stats

def main():
    parser = argparse.ArgumentParser(
        description='将 markdown 中的本地图片转换为 jsDelivr CDN URL'
    )
    parser.add_argument('input', help='输入文件或目录')
    parser.add_argument('-o', '--output', help='输出文件（仅单文件模式）')
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='递归处理子目录')
    parser.add_argument('--repo', help='GitHub 仓库 (格式: user/repo)')

    args = parser.parse_args()
    input_path = Path(args.input)

    # 智能路径解析：支持从任意目录运行脚本
    if not input_path.exists():
        # 尝试相对于项目根目录解析
        project_root = find_project_root()
        project_relative = project_root / args.input
        if project_relative.exists():
            input_path = project_relative
        else:
            # 尝试相对于当前工作目录解析
            cwd_relative = Path.cwd() / args.input
            if cwd_relative.exists():
                input_path = cwd_relative
            else:
                print(f"错误: 路径不存在: {args.input}")
                print(f"       项目根目录: {project_root}")
                print(f"       尝试的路径:")
                print(f"         - {input_path}")
                print(f"         - {project_relative}")
                print(f"         - {cwd_relative}")
                sys.exit(1)

    if input_path.is_file():
        # 单文件模式
        output_path = Path(args.output) if args.output else None
        print(f"处理文件: {input_path}")
        stats = generate_remote(input_path, output_path, args.repo)

        output_name = output_path or input_path.parent / f"{input_path.stem}-remote{input_path.suffix}"
        print(f"\n结果:")
        print(f"  输出: {output_name}")
        print(f"  转换: {stats['converted']}/{stats['total']} 图片")
        if 'cdn_base' in stats:
            print(f"  CDN: {stats['cdn_base']}")

        if stats['failed'] > 0:
            sys.exit(1)

    elif input_path.is_dir():
        # 目录模式
        print(f"处理目录: {input_path}")
        print(f"递归: {'是' if args.recursive else '否'}")

        stats = process_directory(input_path, args.recursive, args.repo)

        print(f"\n总计:")
        print(f"  处理文件: {stats['files']}")
        print(f"  转换图片: {stats['converted']}/{stats['images']}")

        if stats['failed'] > 0:
            print(f"  失败: {stats['failed']}")
            sys.exit(1)

if __name__ == '__main__':
    main()
