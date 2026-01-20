# GitHub Personal Access Token 配置指南

本文档说明如何创建和配置 GitHub Personal Access Token，用于上传图片到 GitHub 图床。

---

## 步骤 1：创建 Personal Access Token

### 1.1 访问 GitHub 设置

1. 登录 GitHub：https://github.com
2. 点击右上角头像 → **Settings**
3. 左侧菜单最下方 → **Developer settings**

### 1.2 生成 Token

1. 点击 **Personal access tokens** → **Tokens (classic)**
2. 点击 **Generate new token** → **Generate new token (classic)**

### 1.3 配置 Token

**Note（备注）**：
```
Article Parser Image Upload
```

**Expiration（过期时间）**：
- 建议选择：No expiration（永不过期）
- 或选择 90 days、1 year 等

**Select scopes（权限勾选）**：
- ✅ **repo** (Full control of private repositories)
  - repo:status
  - repo_deployment
  - public_repo
  - repo:invite
  - security_events

![Token 配置示例](https://docs.github.com/assets/cb-43758/more-button-more-options-rest-api.png)

### 1.4 生成并复制 Token

1. 点击页面底部的 **Generate token**
2. **重要**：立即复制 token（只显示一次！）
3. 保存到安全的位置（密码管理器）

生成的 token 格式类似：
```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 步骤 2：设置环境变量

### 2.1 打开 Shell 配置文件

**macOS / Linux**：
```bash
# 使用 zsh（默认）
nano ~/.zshrc

# 或使用 bash
nano ~/.bashrc
```

**Windows（WSL 或 Git Bash）**：
```bash
nano ~/.bashrc
```

### 2.2 添加环境变量

在文件末尾添加：

```bash
# GitHub Image Host Configuration
export GITHUB_TOKEN="ghp_你的token"
```

**重要**：只需要配置 `GITHUB_TOKEN`！`GITHUB_IMAGE_REPO` 会自动检测当前 git 仓库。

### 2.3 保存并生效

```bash
# 保存文件：Ctrl+O，Enter
# 退出：Ctrl+X

# 重新加载配置
source ~/.zshrc   # zsh
# 或
source ~/.bashrc  # bash
```

### 2.4 验证配置

```bash
# 检查环境变量是否设置成功
echo $GITHUB_TOKEN

# 检查能否自动检测仓库
cd /path/to/your/git/repo
git remote -v

# 应该输出你的 token 和 git remote 信息
```

### 关于仓库自动检测

脚本会自动从当前 git 仓库的 `origin` remote 中提取仓库信息：

```bash
# 自动检测支持的 URL 格式：
# HTTPS: https://github.com/username/repo.git
# SSH:   git@github.com:username/repo.git
```

**优先级**：
1. 手动传入参数（`--repo username/repo`）
2. 环境变量 `GITHUB_IMAGE_REPO`
3. 自动检测 git 仓库（推荐）

---

## 步骤 3：测试上传功能

### 3.1 测试单张图片上传

```bash
cd /Users/magooup/workspace/default/research/articleread

# 测试上传（使用任意公开图片 URL）
python3 .claude/skills/article-parser/scripts/upload_to_github.py \
  "https://github.github.io/assets/images/logo.png" \
  wechat
```

### 3.2 预期输出

```
正在下载图片: https://github.github.com/assets/images/logo.png
正在上传到 GitHub: assets/images/wechat/2026-01/uuid.jpg
✅ 上传成功!
原始 URL: https://raw.githubusercontent.com/maxzyma/articleread/main/assets/images/wechat/2026-01/uuid.jpg
CDN URL:  https://cdn.jsdelivr.net/gh/maxzyma/articleread/assets/images/wechat/2026-01/uuid.jpg

https://cdn.jsdelivr.net/gh/maxzyma/articlereq/assets/images/wechat/2026-01/uuid.jpg
```

### 3.3 验证图片可访问

1. 复制输出的 CDN URL
2. 在浏览器中打开
3. 确认图片能正常显示

---

## 常见问题

### Q1: Token 无效或过期

**错误信息**：
```
❌ 错误: GitHub API 错误: Bad credentials
```

**解决方法**：
1. 检查 token 是否正确复制（无多余空格）
2. 如果过期，重新生成 token
3. 确认环境变量生效：`echo $GITHUB_TOKEN`

### Q2: 权限不足

**错误信息**：
```
❌ 错误: GitHub API 错误: Resource not accessible by integration
```

**解决方法**：
1. 重新生成 token
2. 确保勾选了 `repo` 权限
3. 更新环境变量

### Q3: 仓库不存在

**错误信息**：
```
❌ 错误: GitHub API 错误: Not Found
```

**解决方法**：
1. 检查仓库名称是否正确：`用户名/仓库名`
2. 确认仓库已创建
3. 确认 token 有权限访问该仓库

### Q4: 图片过大

**错误信息**：
```
❌ 错误: 图片过大: 26.5MB，超过 25MB 限制
```

**解决方法**：
1. 压缩图片后再上传
2. 或使用本地存储作为降级方案

### Q5: 环境变量未生效

**症状**：`echo $GITHUB_TOKEN` 输出为空

**解决方法**：
```bash
# 确认文件已编辑
cat ~/.zshrc | grep GITHUB_TOKEN

# 重新加载
source ~/.zshrc

# 如果还是不行，检查使用的 shell
echo $SHELL
```

---

## 安全建议

### ✅ 推荐做法

1. **定期轮换 token**：每 6-12 个月更换一次
2. **使用最小权限**：只勾选必要的权限（repo）
3. **妥善保管**：使用密码管理器存储
4. **监控使用情况**：在 GitHub 设置中查看 token 使用记录

### ❌ 避免的做法

1. ❌ 不要在代码中硬编码 token
2. ❌ 不要将 token 提交到 git 仓库
3. ❌ 不要在不安全的渠道分享 token
4. ❌ 不要使用过期或泄露的 token

---

## 相关链接

- [GitHub Personal Access Tokens 官方文档](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [jsDelivr CDN 文档](https://www.jsdelivr.com/)
- [GitHub API 文档](https://docs.github.com/en/rest)

---

## 需要帮助？

如果遇到问题：

1. 检查本文档的"常见问题"部分
2. 查看 GitHub 官方文档
3. 检查环境变量和脚本权限

提示：确保 `upload_to_github.py` 有执行权限：
```bash
chmod +x .claude/skills/article-parser/scripts/upload_to_github.py
```
