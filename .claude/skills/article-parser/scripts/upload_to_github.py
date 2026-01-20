#!/usr/bin/env python3
"""
将图片上传到 GitHub 图床（带 jsDelivr CDN 加速）

使用方式：
    python3 upload_to_github.py <image_url_or_path> [platform]

参数：
    image_url_or_path: 图片 URL 或本地路径
    platform: 平台类型（wechat | xiaohongshu），默认为 wechat

环境变量：
    GITHUB_TOKEN: GitHub Personal Access Token
    GITHUB_IMAGE_REPO: 仓库名称（默认：maxzyma/articleread）

输出：
    CDN 加速的图片 URL

示例：
    python3 upload_to_github.py "https://mmbiz.qpic.cn/xxx.jpg" wechat
    # 输出: https://cdn.jsdelivr.net/gh/maxzyma/articleread/assets/images/wechat/2026-01/uuid.jpg
"""

import sys
import os
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
            repo: 仓库名称，格式 "username/repo"（从环境变量读取）
            branch: 分支名，默认 'main'
        """
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("缺少 GITHUB_TOKEN 环境变量")

        self.repo = repo or os.getenv('GITHUB_IMAGE_REPO', 'maxzyma/articleread')
        self.branch = branch
        self.api_base = "https://api.github.com"

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
