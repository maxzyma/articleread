#!/bin/bash
# 小红书图片URL缓存管理器
# 用法: ./cache_image_urls.sh <article_url> <action> [urls...]
# action: get (获取缓存), save (保存URL到缓存), clear (清除缓存)

set -e

# 缓存目录（项目目录下）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
CACHE_DIR="$PROJECT_ROOT/.cache/xiaohongshu"

ARTICLE_URL="$1"
ACTION="$2"

if [ -z "$ARTICLE_URL" ] || [ -z "$ACTION" ]; then
    echo "用法: $0 <article_url> <action> [urls...]" >&2
    echo "action: get, save, clear" >&2
    exit 1
fi

# 从文章URL生成缓存目录名
url_hash() {
    local clean_url="$1"
    clean_url="${clean_url%%\?*}"
    clean_url="${clean_url%%#*}"
    echo -n "$clean_url" | md5sum | cut -d' ' -f1
}

URL_HASH=$(url_hash "$ARTICLE_URL")
CACHE_FILE="$CACHE_DIR/${URL_HASH}_image_urls.txt"

# 创建缓存目录
mkdir -p "$CACHE_DIR"

case "$ACTION" in
    get)
        # 获取缓存的URL列表
        if [ -f "$CACHE_FILE" ]; then
            cat "$CACHE_FILE"
        else
            exit 1  # 无缓存
        fi
        ;;

    save)
        # 保存URL列表到缓存
        shift 2
        if [ $# -eq 0 ]; then
            echo "错误: save 操作需要提供 URL 列表" >&2
            exit 1
        fi

        # 清空旧缓存并写入新URL
        > "$CACHE_FILE"
        for url in "$@"; do
            echo "$url" >> "$CACHE_FILE"
        done
        echo "已缓存 $# 个图片URL到: $CACHE_FILE" >&2
        ;;

    clear)
        # 清除缓存
        rm -f "$CACHE_FILE"
        echo "已清除缓存: $CACHE_FILE" >&2
        ;;

    *)
        echo "错误: 未知的 action '$ACTION'" >&2
        echo "支持的 action: get, save, clear" >&2
        exit 1
        ;;
esac
