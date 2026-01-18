#!/bin/bash
# 小红书资源下载器（带缓存）
# 用法: ./download_resource.sh <url> [extension] [max_retries]
# 输出: 返回本地缓存文件路径

set -e

# 缓存目录
CACHE_DIR="/tmp/claude/xiaohongshu/cache"

URL="$1"
EXTENSION="${2:-}"  # 可选：文件扩展名（如 jpg, mp4）
MAX_RETRIES="${3:-3}"

if [ -z "$URL" ]; then
    echo "用法: $0 <url> [extension] [max_retries]" >&2
    exit 1
fi

# 创建缓存目录
mkdir -p "$CACHE_DIR"

# 从 URL 生成唯一标识（MD5）
url_hash() {
    # 移除 URL 中的查询参数和特殊字符，生成稳定的 hash
    local clean_url="$1"
    # 移除查询参数
    clean_url="${clean_url%%\?*}"
    # 移除片段标识符
    clean_url="${clean_url%%#*}"
    # 使用 md5sum 生成 hash
    echo -n "$clean_url" | md5sum | cut -d' ' -f1
}

# 从 URL 推断扩展名
infer_extension() {
    local url="$1"
    local provided_ext="$2"

    # 如果提供了扩展名，直接使用
    if [ -n "$provided_ext" ]; then
        echo "$provided_ext"
        return
    fi

    # 从 URL 提取扩展名
    if echo "$url" | grep -qE '\.(jpg|jpeg|png|webp|gif|mp4|webm)'; then
        echo "$url" | grep -oE '\.(jpg|jpeg|png|webp|gif|mp4|webm)$' | sed 's/^.//'
    else
        echo "bin"  # 默认扩展名
    fi
}

# 生成缓存文件路径
URL_HASH=$(url_hash "$URL")
EXTENSION=$(infer_extension "$URL" "$EXTENSION")
CACHE_FILE="$CACHE_DIR/${URL_HASH}.${EXTENSION}"

# 检查缓存
if [ -f "$CACHE_FILE" ]; then
    # 验证文件是否有效（非空且可读）
    if [ -s "$CACHE_FILE" ]; then
        echo "使用缓存: $CACHE_FILE" >&2
        echo "$CACHE_FILE"
        exit 0
    else
        # 缓存文件无效，删除
        echo "缓存文件无效，重新下载: $CACHE_FILE" >&2
        rm -f "$CACHE_FILE"
    fi
fi

# 下载函数
download_with_retry() {
    local url="$1"
    local output="$2"
    local max_retries="$3"
    local attempt=1

    while [ $attempt -le $max_retries ]; do
        echo "下载中 ($attempt/$max_retries): $url" >&2

        # 使用 curl 下载，添加 User-Agent 避免被拦截
        if curl -L -f -o "$output" \
            -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1" \
            -H "Referer: https://www.xiaohongshu.com/" \
            --connect-timeout 30 \
            --max-time 300 \
            "$url"; then
            echo "下载成功: $output" >&2
            return 0
        else
            echo "下载失败 (尝试 $attempt/$max_retries)" >&2
            if [ $attempt -lt $max_retries ]; then
                sleep 2
            fi
        fi
        ((attempt++))
    done

    echo "下载失败，已达到最大重试次数" >&2
    # 清理失败的文件
    rm -f "$output"
    return 1
}

# 执行下载
download_with_retry "$URL" "$CACHE_FILE" "$MAX_RETRIES"

# 输出缓存文件路径
echo "$CACHE_FILE"
