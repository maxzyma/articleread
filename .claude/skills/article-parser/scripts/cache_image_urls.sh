#!/bin/bash
# 图片URL缓存管理器 + 描述性命名生成器
# 用法:
#   ./cache_image_urls.sh <article_url> <action> [urls...]
#   ./cache_image_urls.sh <article_url> download <context_json>
#
# action: get (获取缓存), save (保存URL到缓存), clear (清除缓存)
#         download (下载图片，使用描述性命名)

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
CACHE_DIR="$PROJECT_ROOT/.cache/xiaohongshu"

ARTICLE_URL="$1"
ACTION="$2"

if [ -z "$ARTICLE_URL" ] || [ -z "$ACTION" ]; then
    echo "用法: $0 <article_url> <action> [urls...]" >&2
    echo "action: get, save, clear, download" >&2
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

# 生成描述性名称
generate_name() {
    local context="$1"
    local index="$2"

    # 清理HTML标签
    local clean_context=$(echo "$context" | sed 's/<[^>]*>//g' | sed 's/&nbsp;/ /g' | tr -s ' ' '\n' | grep -v '^$' | tr '\n' ' ')

    # 提取关键词
    local keywords=$(echo "$clean_context" | grep -oE '[A-Za-z]{3,}([ -][A-Za-z]{3,}){0,3}' | \
        head -5 | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-' | head -c 50 | sed 's/-$//')

    if [ -z "$keywords" ] || [ ${#keywords} -lt 3 ]; then
        echo "image-${index}"
    else
        echo "$keywords"
    fi
}

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

    download)
        # 下载图片并使用描述性命名
        shift 2
        local context_json="$1"

        if [ -z "$context_json" ]; then
            echo "错误: download 操作需要提供上下文 JSON" >&2
            exit 1
        fi

        # 解析 JSON 获取 URL 和 上下文
        # 格式: [{"url":"...","context":"..."},{"url":"...","context":"..."}]
        local urls=$(echo "$context_json" | grep -oE '"url":"[^"]+"' | sed 's/"url":"//;s/"$//')
        local index=0

        echo "$urls" | while read -r url; do
            ((index++))
            if [ -n "$url" ]; then
                # 获取上下文
                local context=$(echo "$context_json" | grep -oE "\"$url\"[^}]*" | grep -oE '"context":"[^"]*"' | sed 's/"context":"//;s/"$//')

                # 生成描述性名称
                local name=$(generate_name "$context" "$index")
                local extension="${url##*.}"
                # 限制扩展名长度
                extension="${extension:0:4}"
                local filename="${name}.${extension}"

                echo "下载: $filename"

                # 下载图片
                curl -s -L -A "Mozilla/5.0" \
                    -H "Referer: https://mp.weixin.qq.com/" \
                    "$url" -o "$filename" 2>/dev/null || \
                    echo -e "${YELLOW}下载失败: $url${NC}" >&2
            fi
        done
        ;;

    *)
        echo "错误: 未知的 action '$ACTION'" >&2
        echo "支持的 action: get, save, clear, download" >&2
        exit 1
        ;;
esac
