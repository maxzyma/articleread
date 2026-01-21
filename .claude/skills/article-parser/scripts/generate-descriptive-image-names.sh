#!/bin/bash
# 生成描述性图片名称
# 功能：根据文章上下文自动生成描述性的图片文件名
# 用法: ./generate-descriptive-image-names.sh <article_slug> <context_file> <image_index> <img_url>
# 示例: ./generate-descriptive-image-names.sh "cursor-long-running" "article.md" 3 "https://mmbiz.qpic.cn/..."

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 清理HTML标签，提取纯文本
strip_html() {
    echo "$1" | sed 's/<[^>]*>//g' | sed 's/&nbsp;/ /g' | sed 's/&lt;/</g' | sed 's/&gt;/>/g' | sed 's/&amp;/\&/g' | tr -s ' ' '\n' | grep -v '^$' | tr '\n' ' '
}

# 从上下文生成名称
generate_name() {
    local article_slug="$1"
    local context="$2"
    local index="$3"

    # 提取上下文中的关键词
    # 移除HTML标签
    local clean_context=$(strip_html "$context")

    # 提取关键短语（2-4个词）
    local keywords=$(echo "$clean_context" | \
        grep -oE '[A-Za-z0-9]{3,}([ -][A-Za-z0-9]{3,}){0,3}' | \
        head -5 | \
        tr '[:upper:]' '[:lower:]' | \
        tr ' ' '-' | \
        tr -cd 'a-z0-9-')

    # 如果没有提取到关键词，使用通用名称
    if [ -z "$keywords" ] || [ ${#keywords} -lt 3 ]; then
        # 使用章节位置作为后备
        echo "${article_slug}-${index}"
    else
        # 限制长度并清理
        local name=$(echo "$keywords" | head -c 50 | sed 's/-$//')
        # 确保名称唯一且不重复
        if [ ${#name} -lt 5 ]; then
            echo "${article_slug}-${index}"
        else
            echo "$name"
        fi
    fi
}

# 主函数
main() {
    local article_slug="${1:-}"
    local context="${2:-}"
    local index="${3:-0}"

    if [ -z "$article_slug" ] || [ -z "$context" ]; then
        echo "用法: $0 <article_slug> <context_text> <image_index>" >&2
        echo "示例: $0 'cursor-long-running' '从 Solid 迁移到 React 的代码合并请求' 3" >&2
        exit 1
    fi

    # 生成名称
    local name=$(generate_name "$article_slug" "$context" "$index")

    # 输出结果（文件名，不含扩展名）
    echo "$name"
}

# 如果直接运行脚本
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
