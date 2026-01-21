# Claude 降临：Claude Code 31 天实战指南 (Advent of Claude)

> 来源：微信公众号「AI实用工具汇」译者：雷小锋，2026-01-13
> 原作者：Ado Kukic (Anthropic 开发者关系负责人)
> 原文活动：Advent of Claude: 31 Days of Claude Code (2024年12月)
> 原文链接：https://mp.weixin.qq.com/s/qCsfa5oxXeAEMwwKtoI4bg
>
> **注意**：微信公众号文章链接为临时链接，可能随时间失效。如无法访问，请通过搜狗微信搜索或关注公众号「AI实用工具汇」查找原文。

---

## 核心观点

**Claude Code 是一个可深度定制、可自动化、可编程的开发环境**，而不仅仅是一个 AI 编程助手。通过掌握 31 个实战技巧，从 `/init` 自动入职到 Agent Skills 和 MCP 集成，开发者可以构建属于自己的 AI 辅助开发工作流。

---

## 背景：什么是 Advent of Claude？

在刚刚过去的 12 月，Anthropic 的开发者关系负责人 Ado Kukic 发起了一项名为 "Advent of Claude"（Claude 降临）的活动。

他每天在 X/Twitter 和 LinkedIn 上分享一个 Claude Code 的使用技巧，连更 31 天。起初这只是一个简单的降临节日历（Advent Calendar），最终变成了一张描绘那些彻底改变软件开发方式的功能图谱。

这篇文章将 31 个技巧汇编成综合指南，按照从入门到精通的顺序重新编排。

---

## 一、让 AI 快速了解你的项目

### 1. `/init`：让 Claude 自动入职你的项目

**每个人都需要入职文档**。有了 `/init`，Claude 会自己编写它。

Claude 会读取你的代码库并生成一个 `CLAUDE.md` 文件，其中包含：
- 构建和测试命令
- 关键目录及其用途
- 代码规范和模式
- 重要的架构决策

**这是我在任何新项目中运行的第一条命令。**

对于大型项目，你还可以创建一个 `.claude/rules/` 目录，用于存放模块化的、特定主题的指令。该目录中的每个 `.md` 文件都会作为 Project Memory（项目记忆）与 `CLAUDE.md` 一起自动加载。

你甚至可以使用 YAML Frontmatter 根据文件路径有条件地应用规则：

```yaml
---
paths:
  - src/api/**/*.ts
---

# API Development Rules

All API endpoints must include input validation
```

**把 `CLAUDE.md` 想象成你的通用项目指南**，而把 `.claude/rules/` 想象成针对测试、安全性、API 设计或任何其他值得单独列出的内容的专项补充。

---

### 2. Memory Updates：动态更新记忆

想在不手动编辑 `CLAUDE.md` 的情况下保存某些内容到 Claude 的记忆中吗？

直接告诉 Claude 更新文件即可：

```
Update Claude.md: always use bun instead of npm in this project
```

保持编码流畅，不要打断你的心流。

---

### 3. `@` Mentions：即时添加上下文

**`@` 提及是给 Claude 提供上下文的最快方式**：

- `@src/auth.ts` — 将文件即时添加到上下文
- `@src/components/` — 引用整个目录
- `@mcp:github` — 启用或禁用 MCP servers

在 Git 仓库中，文件建议的速度提高了约 3 倍，并且支持模糊匹配。

**`@` 是从"我需要上下文"到"Claude 已获取上下文"的最短路径。**

---

## 二、必备快捷键

这些是你会频繁使用的命令。请将它们刻入肌肉记忆。

---

### 4. `!` 前缀：即时运行 Bash

不要浪费 Token 去问"你能运行 git status 吗？"。只需键入 `!` 加上你的 Bash 命令：

```bash
! git status
! npm test
! ls -la src/
```

`!` 前缀会立即执行 Bash 并将输出注入到上下文中：
- 没有模型处理延迟
- 没有 Token 浪费
- 不需要切换多个终端窗口

**这看起来很微小，直到你发现自己每天要用它五十次。**

---

### 5. Double Esc（双击 Esc）：倒带 (Rewind)

想尝试一种"如果我们这样...会怎样"的方法，但又不想承诺后果？

**尽管去试。如果情况变得奇怪，按两次 `Esc` 键跳回到干净的检查点 (Checkpoint)。**

你可以回滚对话、代码更改，或者两者都回滚。需要注意的是，通过 Bash 运行的命令无法撤销。

---

### 6. Ctrl + R：反向搜索 (Reverse Search)

你可以搜索过去的 Prompt：

| 按键 | 动作 |
|------|------|
| Ctrl+R | 开始反向搜索 |
| Ctrl+R (再次) | 循环浏览匹配项 |
| Enter | 运行它 |
| Tab | 编辑选中的内容 |

**不要重新输入。使用回溯。** 这也适用于 Slash 命令。

---

### 7. Prompt Stashing：暂存

这就像 `git stash`，但是用于你的 Prompt。

`Ctrl+S` 保存你的草稿。发送其他内容。当你准备好时，你的草稿会自动恢复。

**再也不用复制到临时记事本了。再也不会在对话中途打断思路了。**

---

### 8. Prompt Suggestions：智能建议

Claude 可以预测你接下来要问什么。完成一个任务后，有时你会看到一个灰色的后续建议出现：

- `Tab`：接受并编辑
- `Enter`：接受并立即运行

以前 `Tab` 用于自动补全你的代码。**现在它自动补全你的工作流。** 可以通过 `/config` 切换此功能。

---

## 三、会话管理

**Claude Code 是一个持久化的开发环境**，针对你的工作流进行优化可以让你事半功倍。

---

### 9. 继续上次的工作

不小心关闭了终端？笔记本电脑中途没电了？没问题。

```bash
claude --continue          # 立即恢复你上一次的对话
claude --resume            # 显示一个选择器，选择任何过去的会话
```

上下文得以保留。势头得以恢复。你的工作永远不会丢失。

你还可以通过 `cleanupPeriodDays` 设置自定义会话保留时间。默认为 30 天，但你可以将其设置为任意时长，如果不希望保留会话，甚至可以设置为 0。

---

### 10. Named Sessions：命名会话

**你的 Git 分支有名字。你的 Claude 会话也应该有。**

```bash
/rename api-migration           # 为当前会话命名
/resume api-migration           # 按名称恢复
claude --resume api-migration   # 从命令行也可以工作
```

`/resume` 界面会对 Fork 的会话进行分组，并支持快捷键：
- `P`：预览
- `R`：重命名

---

### 11. Claude Code Remote：远程模式

在网页上开始任务，在终端里完成：

```bash
# 在 claude.ai/code 上，开启一个 Claude Code 会话
# 当你离开时它在后台运行

# 稍后，在你的终端：
claude --teleport session_abc123
```

这会将远程会话拉取并恢复到本地。无论在家还是在路上，Claude 都在。

这也支持通过 iOS 和 Android 的 Claude 移动应用以及 Claude Desktop 应用程序使用。

---

### 12. `/export`：获取凭证

有时你需要一份发生过的事情的记录。

`/export` 将你的整个对话导出为 Markdown：
- 你发送的每一个 Prompt
- Claude 给出的每一个回复
- 每一次工具调用及其输出

非常适合用于文档编写、培训，或者向过去的自己证明，是的，你确实已经尝试过那种方法了。

---

## 四、生产力功能

这些功能消除了摩擦，帮助你行动得更快。

---

### 13. Vim Mode

厌倦了伸手去拿鼠标来编辑 Prompt？

输入 `/vim` 解锁完整的 Vim 风格编辑：

- `h j k l`：导航
- `ciw`：更改单词
- `dd`：删除行
- `w b`：按单词跳转
- `A`：在行尾追加

**以思维的速度编辑 Prompt。** 你几十年 Vim 使用积累的肌肉记忆终于在 AI 工具中得到了回报。

退出 Vim 模式也从未如此简单，只需再次输入 `/vim`。

---

### 14. `/statusline`：自定义你的视图

Claude Code 在终端底部有一个可自定义的状态栏。

`/statusline` 允许你配置那里显示的内容：
- Git 分支和状态
- 当前模型
- Token 使用情况
- Context Window（上下文窗口）百分比
- 自定义脚本

**一目了然的信息意味着更少的手动检查中断。**

---

### 15. `/context`：Token 的 X 射线视觉

想知道是什么在吞噬你的上下文窗口吗？

输入 `/context` 准确查看是什么在消耗 Token：
- System prompt 大小
- MCP server prompts
- Memory files (`CLAUDE.md`)
- 加载的 Skills 和 Agents
- 对话历史

**当你的上下文开始填满时，这就是你找出它去向的方法。**

---

### 16. `/stats`：你的使用仪表板

> 2023: "Check out my GitHub contribution graph"<br/>
> 2025: "Check out my Claude Code stats"

输入 `/stats` 查看你的使用模式、最常用的模型、使用连胜纪录等。**橙色是新的绿色。**

---

### 17. `/usage`：了解你的极限

"我快达到限额了吗？"

```bash
/usage         # 通过可视化进度条检查当前使用情况
/extra-usage   # 购买额外容量
```

**了解你的极限。然后超越它们。**

---

## 五、思考与规划

控制 Claude 处理问题的方式。

---

### 18. Ultrathink：深度思考

通过单个关键字按需触发扩展思考：

```
> ultrathink: design a caching layer for our API
```

当你在 Prompt 中包含 `ultrathink` 时，Claude 在响应之前会分配最多 32k token 进行内部推理。

**对于复杂的架构决策或棘手的调试会话**，这可能是肤浅答案与真正洞察力之间的区别。

> **注意**：过去你可以指定 `think`、`think harder` 和 `ultrathink` 来分配不同数量的思考 Token，但现在我们将其简化为一个单一的思考预算。仅当未设置 `MAX_THINKING_TOKENS` 时，`ultrathink` 关键字才起作用。配置 `MAX_THINKING_TOKENS` 后，它将优先控制所有请求的思考预算。

---

### 19. Plan Mode：规划模式

先清除战争迷雾。

按 `Shift+Tab` 两次进入 Plan 模式。Claude 可以：
- 阅读和搜索你的代码库
- 分析架构
- 探索依赖关系
- 起草实施计划

**但在你批准计划之前，它不会编辑任何内容。**

**三思而后行 (Think twice. Execute once)。**

我有 90% 的时间默认使用 Plan 模式。最新版本允许你在拒绝计划时提供反馈，使迭代更快。

---

### 20. Extended Thinking (API)

直接使用 Claude API 时，你可以启用扩展思考以查看 Claude 的逐步推理：

```javascript
thinking: {
  type: "enabled",
  budget_tokens: 5000
}
```

Claude 在响应之前会在 Thinking Block 中展示其推理过程。

**这对于调试复杂逻辑或理解 Claude 的决策非常有用。**

---

## 六、权限与安全

**没有控制的权力只是混乱**。这些功能让你设定界限。

---

### 21. Sandbox Mode：沙盒模式

```
"Can I run npm install?" [Allow]
"Can I run npm test?" [Allow]
"Can I cat this file?" [Allow]
"Can I pet that dawg?" [Allow] ×100
```

`/sandbox` 让你一次性定义边界。Claude 在其中自由工作。

**你获得了速度，同时拥有真正的安全性。** 最新版本支持通配符语法，如 `mcp__server__*`，用于允许整个 MCP server。

---

### 22. YOLO Mode

厌倦了 Claude Code 为每件事都请求许可？

```bash
claude --dangerously-skip-permissions
```

这个标志对一切说 Yes。**它的名字里有"danger（危险）"是有原因的**——请明智地使用它，最好是在隔离环境或受信任的操作中使用。

---

### 23. Hooks：钩子

Hooks 是在预定的生命周期事件中运行的 Shell 命令：

- `PreToolUse` / `PostToolUse`：工具执行前后
- `PermissionRequest`：自动批准或拒绝许可请求
- `Notification`：对 Claude 的通知做出反应
- `SubagentStart` / `SubagentStop`：监控 Agent 的生成

通过 `/hooks` 或在 `.claude/settings.json` 中配置它们。

**使用 Hooks 阻止危险命令、发送通知、记录操作或与外部系统集成。这是对概率性 AI 的确定性控制。**

---

## 七、自动化与 CI/CD

Claude Code 的工作不仅仅局限于交互式会话。

---

### 24. Headless Mode：无头模式

你可以将 Claude Code 用作强大的 CLI 工具来进行脚本编写和自动化：

```bash
claude -p "Fix the lint errors"
claude -p "List all the functions" | grep "async"
git diff | claude -p "Explain these changes"
echo "Review this PR" | claude -p --json
```

**管道中的 AI。**

`-p` 标志以非交互方式运行 Claude 并直接输出到标准输出 (stdout)。

---

### 25. Commands：可重用提示

将任何 Prompt 保存为可重用的命令：

```markdown
<!-- .claude/commands/daily-standup.md -->
Generate a daily standup summary based on recent git commits...
```

创建一个 Markdown 文件，它就会变成一个 Slash 命令，并且可以额外接受参数：

```bash
/daily-standup                    # 运行你的早会流程 Prompt
/explain $ARGUMENTS               # /explain src/auth.ts
```

**停止重复自己。你最好的 Prompts 值得被重用。**

---

## 八、浏览器集成

Claude Code 可以看到并在浏览器中交互。

---

### 26. Claude Code + Chrome

Claude 现在可以直接与 Chrome 交互：
- 导航页面
- 点击按钮并填写表单
- 读取控制台错误
- 检查 DOM
- 截图

**"修复 Bug 并验证它能工作"现在只需一个 Prompt。**

从 `claude.ai/chrome` 安装 Chrome 扩展。

---

## 九、高级功能：Agents 与扩展性

这是 Claude Code 真正变得强大的地方。

---

### 27. Subagents：子智能体

**圣诞老人不会自己包装每一个礼物。他有精灵。**

Subagents 就是 Claude 的精灵。每一个都：
- 拥有自己的 200k Context Window
- 执行专门的任务
- 与其他 Agent 并行运行
- 将输出合并回主 Agent

**像圣诞老人一样授权。** Subagents 可以在后台运行，而你继续工作，并且它们拥有对 MCP 工具的完全访问权限。

---

### 28. Agent Skills：技能

Skills 是包含指令、脚本和资源的文件夹，用于教授 Claude 专门的任务。

它们一次打包，随处可用。而且由于 Agent Skills 现在是一个开放标准，它们可以在任何支持它们的工具中工作。

**把 Skills 想象成给 Claude 按需提供的专业知识**。无论是你公司特定的部署流程、测试方法，还是文档标准。

---

### 29. Plugins：插件

还记得分享 Claude Code 设置意味着要在 12 个目录中发送 47 个文件吗？

**那个时代结束了。**

```bash
/plugin install my-setup
```

Plugins 将 Commands、Agents、Skills、Hooks 和 MCP servers 捆绑在一个包中。通过市场发现新的工作流，其中包括搜索过滤以便更容易发现。

---

### 30. Language Server Protocol (LSP) 集成

LSP 支持赋予了 Claude IDE 级别的代码智能：

- **即时诊断**：Claude 在每次编辑后立即看到错误和警告
- **代码导航**：跳转到定义、查找引用和悬停信息
- **语言感知**：代码符号的类型信息和文档

**Claude Code 现在像你的 IDE 一样理解你的代码。**

---

### 31. Claude Agent SDK

驱动 Claude Code 的相同 Agent 循环、工具和上下文管理现在作为 SDK 提供。

**只需 10 行代码即可构建像 Claude Code 一样工作的 Agent：**

```javascript
import { query } from '@anthropic-ai/claude-agent-sdk';

for await (const msg of query({
  prompt: "Generate markdown API docs for all public functions in src/",
  options: {
    allowedTools: ["Read", "Write", "Glob"],
    permissionMode: "acceptEdits"
  }
})) {
  if (msg.type === 'result') {
    console.log("Docs generated:", msg.result);
  }
}
```

**这仅仅是个开始。**

---

## 快速参考

### Keyboard Shortcuts（键盘快捷键）

| 快捷键 | 动作 |
|--------|------|
| `!command` | 立即执行 Bash |
| `Esc Esc` | 倒带对话/代码 |
| `Ctrl+R` | 反向搜索历史 |
| `Ctrl+S` | 暂存当前 Prompt |
| `Shift+Tab` (×2) | 切换 Plan 模式 |
| `Alt+P` / `Option+P` | 切换模型 |
| `Ctrl+O` | 切换详细模式 |
| `Tab` / `Enter` | 接受 Prompt 建议 |

---

### Essential Commands（必备命令）

| 命令 | 用途 |
|------|------|
| `/init` | 为你的项目生成 CLAUDE.md |
| `/context` | 查看 Token 消耗 |
| `/stats` | 查看使用统计 |
| `/usage` | 检查速率限制 |
| `/vim` | 启用 Vim 模式 |
| `/config` | 打开配置 |
| `/hooks` | 配置生命周期钩子 |
| `/sandbox` | 设置权限边界 |
| `/export` | 导出对话为 Markdown |
| `/resume` | 恢复过去的会话 |
| `/rename` | 命名当前会话 |
| `/theme` | 打开主题选择器 |
| `/terminal-setup` | 配置终端集成 |

---

### CLI Flags（命令行标志）

| 标志 | 用途 |
|------|------|
| `-p "prompt"` | 无头/打印模式 |
| `--continue` | 恢复上一次会话 |
| `--resume` | 选择要恢复的会话 |
| `--resume name` | 按名称恢复会话 |
| `--teleport id` | 恢复网页会话 |
| `--dangerously-skip-permissions` | YOLO 模式 |

---

## 结语

当我开始这个降临日历时，我以为我只是在分享技巧。但回顾这 31 天，我看到了更多的东西：**一种人机协作的哲学。**

Claude Code 最好的功能在于给你控制权。Plan Mode、Agent Skills、Hooks、Sandbox 边界、Session Management。

**这些是与 AI 合作的工具，而不是向它投降。**

那些从 Claude Code 中获得最大收益的开发者，并不是那些输入"为我做所有事"的人。而是那些学会了：
- 何时使用 Plan Mode
- 如何构建 Prompt
- 何时调用 Ultrathink
- 如何设置 Hooks 以在错误发生前捕获它们

**AI 是一个杠杆。这些功能帮助你找到正确的抓手。**

致 2026。

---

*来源：Ado Kukic 的 "Advent of Claude: 31 Days of Claude Code" 活动*
