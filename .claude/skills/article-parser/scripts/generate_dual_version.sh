#!/bin/bash
#
# 生成双版本 Markdown 文件
#
# 使用方式：
#   bash generate_dual_version.sh <article.md> [cdn_base_url]
#
# 参数：
#   article.md: 本地版本的 Markdown 文件（使用 ./images/ 路径）
#   cdn_base_url: CDN 基础 URL（可选，默认自动检测）
#
# 输出：
#   生成 article-remote.md（使用 CDN URL）
#
# 示例：
#   bash generate_dual_version.sh boris-claude-code-workflow.md
#   bash generate_dual_version.sh article.md "https://cdn.jsdelivr.net/gh/user/repo/assets/images/wechat/2026-01"
#

set -e

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查参数
ARTICLE_FILE="$1"

if [ -z "$ARTICLE_FILE" ]; then
    echo "❌ 错误: 缺少文章文件路径"
    echo ""
    echo "使用方式："
    echo "  bash $0 <article.md> [cdn_base_url]"
    echo ""
    echo "示例："
    echo "  bash $0 boris-claude-code-workflow.md"
    echo "  bash $0 article.md \"https://cdn.jsdelivr.net/gh/user/repo/assets/images/wechat/2026-01\""
    exit 1
fi

# 检查文件是否存在
if [ ! -f "$ARTICLE_FILE" ]; then
    echo "❌ 错误: 文件不存在: $ARTICLE_FILE"
    exit 1
fi

# 提取文件名（不含扩展名）
BASE_NAME="${ARTICLE_FILE%.md}"

# 检测 CDN 基础 URL
if [ -n "$2" ]; then
    # 使用用户提供的 CDN URL
    CDN_BASE_URL="$2"
    echo -e "${BLUE}ℹ️  使用提供的 CDN URL${NC}"
else
    # 自动检测 CDN URL
    echo -e "${BLUE}🔍 自动检测 CDN URL...${NC}"

    # 1. 检测仓库
    REPO_INFO=$(git remote get-url origin 2>/dev/null || echo "")
    if [ -z "$REPO_INFO" ]; then
        echo -e "${YELLOW}⚠️  警告: 无法检测 git 仓库${NC}"
        echo -e "${YELLOW}使用默认 CDN URL（请手动确认是否正确）${NC}"
        REPO_INFO="https://github.com/maxzyma/articleread.git"
    fi

    # 2. 解析仓库名
    if [[ $REPO_INFO =~ github\.com/([^/]+/[^/]+)\.git ]]; then
        REPO_PATH="${BASH_REMATCH[1]}"
    else
        echo -e "${YELLOW}⚠️  警告: 无法解析仓库名${NC}"
        REPO_PATH="maxzyma/articleread"
    fi

    # 3. 检测当前月份
    CURRENT_MONTH=$(date +%Y-%m)

    # 4. 构建完整的 CDN URL
    # 从文章路径或环境变量判断平台
    PLATFORM="${GITHUB_IMAGE_PLATFORM:-wechat}"

    CDN_BASE_URL="https://cdn.jsdelivr.net/gh/${REPO_PATH}/assets/images/${PLATFORM}/${CURRENT_MONTH}"

    echo -e "${GREEN}✅ 检测到 CDN URL:${NC} $CDN_BASE_URL"
fi

# 生成远程版本
REMOTE_FILE="${BASE_NAME}-remote.md"

echo ""
echo -e "${BLUE}📝 生成远程版本...${NC}"
echo "  源文件: $ARTICLE_FILE"
echo "  目标文件: $REMOTE_FILE"
echo "  CDN URL: $CDN_BASE_URL"
echo ""

# 使用 sed 替换图片路径
# 替换模式: (./images/xxx.jpg) -> (https://cdn.jsdelivr.net/gh/.../xxx.jpg)
sed 's|(\./images/|('"$CDN_BASE_URL"'/|g' "$ARTICLE_FILE" > "$REMOTE_FILE"

# 统计替换数量（使用固定的 CDN 域名部分进行匹配）
IMAGE_COUNT=$(grep -o 'cdn\.jsdelivr\.net/gh/[^)]*jpg' "$REMOTE_FILE" 2>/dev/null | wc -l | tr -d ' ')

echo ""
echo -e "${GREEN}✅ 双版本生成完成！${NC}"
echo ""
echo "  📄 本地版本: $ARTICLE_FILE"
echo "  📄 远程版本: $REMOTE_FILE"
echo "  🖼️  图片数量: $IMAGE_COUNT"
echo ""
echo -e "${BLUE}💡 提示：${NC}"
echo "  - 本地版本使用相对路径，适合本地预览"
echo "  - 远程版本使用 CDN URL，可以分享给别人"
echo "  - 两个版本内容同步，只有图片路径不同"
echo ""

# 验证远程版本
if [ "$IMAGE_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✅ 验证通过：远程版本包含 $IMAGE_COUNT 张图片${NC}"
else
    echo -e "${YELLOW}⚠️  警告: 未检测到图片引用${NC}"
    echo "  请确认文章中是否包含图片"
fi
