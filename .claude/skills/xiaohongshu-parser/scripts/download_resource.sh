#!/bin/bash
# 下载小红书资源到本地
# 用法: ./download_resource.sh <url> <output_path> [max_retries]

set -e

URL="$1"
OUTPUT_PATH="$2"
MAX_RETRIES="${3:-3}"

if [ -z "$URL" ] || [ -z "$OUTPUT_PATH" ]; then
    echo "用法: $0 <url> <output_path> [max_retries]"
    exit 1
fi

# 创建输出目录
mkdir -p "$(dirname "$OUTPUT_PATH")"

# 下载函数
download_with_retry() {
    local url="$1"
    local output="$2"
    local max_retries="$3"
    local attempt=1

    while [ $attempt -le $max_retries ]; do
        echo "尝试下载 ($attempt/$max_retries): $url"

        # 使用 curl 下载，添加 User-Agent 避免被拦截
        if curl -L -f -o "$output" \
            -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1" \
            -H "Referer: https://www.xiaohongshu.com/" \
            --connect-timeout 30 \
            --max-time 300 \
            "$url"; then
            echo "下载成功: $output"
            return 0
        else
            echo "下载失败 (尝试 $attempt/$max_retries)"
            if [ $attempt -lt $max_retries ]; then
                sleep 2
            fi
        fi
        ((attempt++))
    done

    echo "下载失败，已达到最大重试次数"
    return 1
}

# 执行下载
download_with_retry "$URL" "$OUTPUT_PATH" "$MAX_RETRIES"
