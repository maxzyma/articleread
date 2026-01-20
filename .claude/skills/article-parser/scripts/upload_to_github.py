#!/usr/bin/env python3
"""
将图片上传到 GitHub 图床（带 jsDelivr CDN 加速）

使用方式：
    python3 upload_to_github.py <image_url_or_path> [platform]

参数：
    image_url_or_path: 图片 URL 或本地路径
    platform: 平台类型（wechat | xiaohongshu），默认为 wechat

环境变量：
    GITHUB_TOKEN: GitHub Personal Access Token（必需）
    GITHUB_IMAGE_REPO: 仓库名称（可选，默认自动检测当前 git 仓库）

仓库检测优先级：
    1. 参数传入的 repo
    2. 环境变量 GITHUB_IMAGE_REPO
    3. 自动检测当前 git 仓库的 origin remote

输出：
    CDN 加速的图片 URL

示例：
    # 在 git 仓库中运行（自动检测仓库）
    python3 upload_to_github.py "https://mmbiz.qpic.cn/xxx.jpg" wechat

    # 手动指定仓库
    python3 upload_to_github.py "https://mmbiz.qpic.cn/xxx.jpg" wechat --repo username/repo
"""

import sys
import os
import subprocess
import requests
import base64
import uuid
from datetime import datetime

class GitHubImageHost:
    """GitHub 图床上传器"""

    def __init__(self, token=None, repo=None, branch='main'):
        """
        初始化 GitHub 图床

        Args:
            token: GitHub Personal Access Token（从环境变量读取）
            repo: 仓库名称，格式 "username/repo"（从环境变量读取或自动检测）
            branch: 分支名，默认 'main'
        """
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("缺少 GITHUB_TOKEN 环境变量。请先设置：export GITHUB_TOKEN=\"ghp_xxx\"")

        # 优先级：参数传入 > 环境变量 > 自动检测 git remote
        self.repo = repo or os.getenv('GITHUB_IMAGE_REPO') or self._detect_git_repo()
        if not self.repo or self.repo == 'unknown/unknown':
            raise ValueError("无法检测到 git 仓库。请设置 GITHUB_IMAGE_REPO 环境变量或在 git 仓库中运行此脚本")

        self.branch = branch
        self.api_base = "https://api.github.com"

    def _detect_git_repo(self):
        """
        自动检测当前 git 仓库信息

        Returns:
            仓库名称，格式 "username/repo"
            如果检测失败，返回 None
        """
        try:
            # 获取 git remote 信息
            result = subprocess.run(
                ['git', 'remote', '-v'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                return None

            # 解析输出，找到 origin
            for line in result.stdout.split('\n'):
                if line.startswith('origin\t'):
                    # 格式: origin  https://github.com/username/repo.git (fetch)
                    #       origin  git@github.com:username/repo.git (fetch)
                    url = line.split()[1]
                    repo = self._parse_github_url(url)
                    if repo:
                        print(f"自动检测到仓库: {repo}")
                        return repo

            return None

        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return None

    def _parse_github_url(self, url):
        """
        解析 GitHub URL，提取 username/repo

        Args:
            url: git remote URL

        Returns:
            仓库名称 "username/repo" 或 None
        """
        # HTTPS 格式: https://github.com/username/repo.git
        if 'github.com/' in url:
            parts = url.split('github.com/')[1].split('/')
            if len(parts) >= 2:
                repo_name = parts[1].replace('.git', '')
                return repo_name

        # SSH 格式: git@github.com:username/repo.git
        elif url.startswith('git@github.com:'):
            parts = url.split(':')[1].split('/')
            if len(parts) >= 1:
                repo_name = parts[0].replace('.git', '')
                return repo_name

        return None

    def upload_image(self, image_path_or_url, platform='wechat'):
        """
        上传图片到 GitHub

        Args:
            image_path_or_url: 本地路径或远程 URL
            platform: 'wechat' | 'xiaohongshu'

        Returns:
            图片 URL（使用 jsDelivr CDN 加速）
        """
        # 生成唯一文件名
        date_str = datetime.now().strftime('%Y-%m')
        filename = f"{uuid.uuid4()}.jpg"
        path = f"assets/images/{platform}/{date_str}/{filename}"

        # 获取图片内容
        if image_path_or_url.startswith('http'):
            content = self._download_image(image_path_or_url, platform)
        else:
            with open(image_path_or_url, 'rb') as f:
                content = f.read()

        # 检查文件大小（GitHub 限制 25MB）
        if len(content) > 25 * 1024 * 1024:
            raise ValueError(f"图片过大: {len(content) / 1024 / 1024:.2f}MB，超过 25MB 限制")

        # 上传到 GitHub
        return self._upload_to_github(path, content, platform)

    def _download_image(self, url, platform):
        """
        下载远程图片（带 referer 处理防盗链）

        Args:
            url: 图片 URL
            platform: 平台类型

        Returns:
            图片二进制内容
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        # 根据平台设置 referer
        if platform == 'wechat':
            headers['Referer'] = 'https://mp.weixin.qq.com/'
        elif platform == 'xiaohongshu':
            headers['Referer'] = 'https://www.xiaohongshu.com/'

        print(f"正在下载图片: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        return response.content

    def _upload_to_github(self, path, content, platform):
        """
        上传到 GitHub API

        Args:
            path: 文件路径
            content: 文件内容
            platform: 平台类型

        Returns:
            CDN 加速的图片 URL
        """
        url = f"{self.api_base}/repos/{self.repo}/contents/{path}"
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        # 转换为 base64
        content_b64 = base64.b64encode(content).decode()

        data = {
            'message': f'Add image for {platform} article ({datetime.now().strftime("%Y-%m-%d")})',
            'content': content_b64,
            'branch': self.branch
        }

        print(f"正在上传到 GitHub: {path}")
        response = requests.put(url, json=data, headers=headers)

        # 检查响应
        if response.status_code not in [200, 201]:
            error_msg = response.json().get('message', 'Unknown error')
            raise Exception(f"GitHub API 错误: {error_msg}")

        response.raise_for_status()

        # 返回 CDN 加速的 URL
        raw_url = response.json()['content']['download_url']
        cdn_url = self._convert_to_cdn(raw_url)

        print(f"✅ 上传成功!")
        print(f"原始 URL: {raw_url}")
        print(f"CDN URL:  {cdn_url}")

        return cdn_url

    def _convert_to_cdn(self, raw_url):
        """
        转换为 jsDelivr CDN URL

        Args:
            raw_url: GitHub raw URL

        Returns:
            CDN URL

        示例:
            https://raw.githubusercontent.com/user/repo/main/path/file.jpg
            → https://cdn.jsdelivr.net/gh/user/repo/path/file.jpg
        """
        # 移除 /main/ 分支名（jsDelivr 会自动处理）
        return raw_url.replace(
            'https://raw.githubusercontent.com',
            'https://cdn.jsdelivr.net/gh'
        ).replace(f'/{self.branch}/', '/')


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    image_path_or_url = sys.argv[1]
    platform = sys.argv[2] if len(sys.argv) > 2 else 'wechat'

    try:
        # 创建上传器
        host = GitHubImageHost()

        # 上传图片
        cdn_url = host.upload_image(image_path_or_url, platform)

        # 输出 CDN URL
        print(f"\n{cdn_url}")

    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
