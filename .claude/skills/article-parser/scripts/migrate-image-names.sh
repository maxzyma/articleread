#!/bin/bash
# 迁移旧项目的图片命名从数字索引到描述性命名
# 用法: ./migrate-image-names.sh <article_dir>
# 示例: ./migrate-image-names.sh general/long-running-agents-cursor-anthropic

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "$1" ]; then
    echo "用法: $0 <article_dir>" >&2
    echo "示例: $0 general/long-running-agents-cursor-anthropic" >&2
    echo "" >&2
    echo "此脚本将:" >&2
    echo "1. 扫描指定目录中的 img-*.jpg/png/gif 文件" >&2
    echo "2. 根据 md 文件中的图片引用上下文生成新名称" >&2
    echo "3. 重命名图片文件" >&2
    echo "4. 更新 md 文件中的图片引用" >&2
    exit 1
fi

ARTICLE_DIR="$1"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
FULL_PATH="$PROJECT_ROOT/$ARTICLE_DIR"

if [ ! -d "$FULL_PATH" ]; then
    echo -e "${RED}错误: 目录不存在: $FULL_PATH${NC}" >&2
    exit 1
fi

IMAGES_DIR="$FULL_PATH/images"
if [ ! -d "$IMAGES_DIR" ]; then
    echo -e "${RED}错误: images 目录不存在: $IMAGES_DIR${NC}" >&2
    exit 1
fi

echo -e "${GREEN}开始迁移图片命名...${NC}"
echo "目录: $ARTICLE_DIR"
echo ""

# 查找所有数字命名的图片
OLD_IMAGES=$(find "$IMAGES_DIR" -type f \( -name "img-*.jpg" -o -name "img-*.png" -o -name "img-*.gif" -o -name "image_*.jpg" -o -name "image_*.png" -o -name "image_*.gif" \) 2>/dev/null | sort)

if [ -z "$OLD_IMAGES" ]; then
    echo -e "${YELLOW}未找到需要迁移的图片文件${NC}"
    exit 0
fi

echo "找到以下需要迁移的图片:"
echo "$OLD_IMAGES" | while read -r img; do
    echo "  - $(basename "$img")"
done
echo ""

# 查找 md 文件
MD_FILES=$(find "$FULL_PATH" -maxdepth 1 -name "*.md" -type f)
if [ -z "$MD_FILES" ]; then
    echo -e "${RED}错误: 未找到 md 文件${NC}" >&2
    exit 1
fi

# 迁移每个图片
echo "$OLD_IMAGES" | while read -r old_img; do
    filename=$(basename "$old_img")
    extension="${filename##*.}"

    # 从 md 文件中查找图片的上下文
    context=""
    for md_file in $MD_FILES; do
        # 查找图片引用及其前后文本
        line_num=0
        while IFS= read -r line; do
            ((line_num++))
            if [[ "$line" == *"$filename"* ]]; then
                # 找到引用行，获取前后各3行的上下文
                start=$((line_num > 3 ? line_num - 3 : 1))
                end=$((line_num + 3))

                context=$(sed -n "${start},${end}p" "$md_file" | grep -oE '[a-zA-Z][a-zA-Z0-9 -]{3,50}' | head -5 | tr '\n' ' ' | sed 's/  */ /g' | sed 's/ $//')
                break 2
            fi
        done < "$md_file"
    done

    # 生成新名称
    if [ -n "$context" ]; then
        # 从上下文中提取关键词
        new_name=$(echo "$context" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-' | head -c 50 | sed 's/-$//')
    fi

    # 如果无法生成描述性名称，使用通用名称
    if [ -z "$new_name" ] || [ ${#new_name} -lt 5 ]; then
        # 提取原文件中的数字
        num=$(echo "$filename" | grep -oE '\d+' | head -1)
        if [ -n "$num" ]; then
            new_name="image-${num}"
        else
            new_name="image-$(date +%s)"
        fi
    fi

    new_img="$IMAGES_DIR/${new_name}.${extension}"

    # 如果新名称已存在，添加序号
    if [ -f "$new_img" ] && [ "$new_img" != "$old_img" ]; then
        counter=1
        while [ -f "$IMAGES_DIR/${new_name}-${counter}.${extension}" ]; do
            ((counter++))
        done
        new_img="$IMAGES_DIR/${new_name}-${counter}.${extension}"
        new_name="${new_name}-${counter}"
    fi

    echo "迁移: $filename -> ${new_name}.${extension}"

    # 重命名文件
    mv "$old_img" "$new_img"

    # 更新 md 文件中的引用
    for md_file in $MD_FILES; do
        sed -i '' "s|$filename|${new_name}.${extension}|g" "$md_file" 2>/dev/null || \
        sed -i "s|$filename|${new_name}.${extension}|g" "$md_file"
    done
done

echo ""
echo -e "${GREEN}迁移完成！${NC}"
echo ""
echo "注意事项:"
echo "1. 请检查生成的名称是否准确"
echo "2. 如果名称不合适，可以手动重命名并更新 md 文件"
echo "3. 提交更改前请运行验证脚本检查完整性"
