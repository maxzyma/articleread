# Anthropic 大佬连发 31 条 Claude Code 秘籍

**Ado Kukic - Anthropic 开发者关系负责人**

**Advent of Claude: 31 Days of Claude Code**

Claude Code 最强大功能的全面指南，从快速快捷键到高级智能体模式。

---

## 背景

在刚刚过去的 12 月，Anthropic 的开发者关系负责人 Ado Kukic 发起了一项名为 "Advent of Claude"（Claude 降临）的活动。

他每天在社交媒体上分享一个 Claude Code 的使用技巧，连更 31 天。Ado Kukic 整理的这 31 条技巧告诉我们：Claude Code 其实是一个可深度定制、可自动化、甚至可编程的开发环境。

---

## 让 AI 快速了解你的项目

### 1. /init：自动生成项目说明书

在一个新项目中，直接运行 /init 命令。Claude 会自动阅读你的代码库，并生成一个 CLAUDE.md 文件。这个文件是你的项目说明书，里面包含了：

- 构建和测试命令
- 目录结构说明
- 代码规范和架构决策
- ...

有了这个文件，Claude 每次启动时都会自动读取。对于大型项目，你还可以创建 .claude/rules/目录，通过 Front Matter 指定规则生效的路径，实现模块化的上下文管理。

### 2. Memory Updates：动态更新记忆

直接告诉 Claude："Update Claude.md: always use bun instead of npm"。它会自动把这条新知识写入记忆文件，不用打断你的心流。

### 3. @ Mentions：极速引用上下文

使用 @ 符号可以像在社交软件里 @ 人一样方便地引用代码：

- **@src/auth.ts**：引用特定文件
- **@src/components/**: 引用整个目录
- **@mcp:github**: 启用或禁用工具（MCP Server）

文件建议支持模糊匹配，这是从"我需要上下文"到"Claude 获得上下文"的最快路径。

---

## 必备快捷键

### 4. ! Prefix：直接运行 Shell

不用切换终端窗口，直接输入 `! git status` 或 `! npm test`。

这不仅是运行命令，更重要的是命令的输出结果会直接进入 Claude 的上下文。Claude 马上就能根据报错信息给出修复建议，无缝衔接。

### 5. Double Esc：时光倒流

尝试了一个新思路，结果代码改乱了？别慌，双击 Esc 键，直接回退到上一个检查点。你可以选择回退对话，或者回退代码变更。

### 6. Ctrl + R：反向搜索

就像 Shell 里的反向搜索一样，按 Ctrl + R 可以搜索你之前的 Prompt（提示词）。

### 7. Prompt Stashing：暂存提示词

打字打到一半想看个别的东西？按 Ctrl + S 暂存当前的 Prompt。等你准备好了，它会自动恢复。再也不用把草稿复制到记事本里了。

### 8. Prompt Suggestions：智能补全

Claude 甚至能预测你接下来想问什么。当你看到灰色的建议文字时，按 Tab 键接受并编辑，或者按 Enter 直接运行。

---

## 会话管理

Claude Code 不仅仅是一次性的对话，它是一个持久的开发环境。

### 9. Continue & Resume：无缝续关

终端意外关闭？电脑没电了？

- **claude --continue**：瞬间恢复上一次的对话。
- **claude --resume**：显示历史会话列表供你选择。

上下文完美保留，工作流永不丢失。

### 10. Named Sessions：给会话起个名

像管理 Git 分支一样管理你的会话：

- **/rename api-migration**：给当前会话命名。
- **/resume api-migration**：按名称恢复会话。

### 11. Claude Code Remote：远程传送

在网页版 claude.ai/code 上开始任务，回家后用 `claude --teleport session_id` 直接把云端会话"拉"到本地终端继续开发。无缝切换设备。

### 12. /export：留下证据

需要记录刚才发生了什么？/export 命令可以将整个对话（包括提示词、回复、工具调用结果）导出为 Markdown 文件。用于写文档或复盘非常完美。

---

## 生产力神器

### 13. Vim Mode: 极客模式

如果你是 Vim 党，输入 /vim 即可开启 Vim 模式。用 h j k l 移动光标，用 ciw 修改单词。在 AI 工具里体验指尖起舞的快感。

### 14. /statusline: 自定义状态栏

底部状态栏显示什么由你定：Git 分支、当前模型、Token 使用量、上下文占用率等。信息一目了然。

### 15. /context: Token 透视眼

担心 Token 用超了？输入 /context，Claude 会列出 System Prompt、MCP Server、记忆文件、对话历史分别占用了多少空间，帮你精准"瘦身"。

### 16. /stats: 使用统计

输入 /stats 查看你的使用习惯、最爱用的模型、连续使用天数等。

### 17. /usage: 额度监控

通过 /usage 随时查看当前的费率限制和使用进度，做到心中有数。

---

## 思考与规划

### 18. ultrathink：深度思考模式

当你需要设计复杂的缓存层或重构架构时，在提示词中加上 ultrathink。Claude 会分配高达 32k 的 Token 进行内部推理。虽然反应慢一点，但逻辑准确率大幅提升。

### 19. Plan Mode：计划模式

按两次 Shift + Tab 进入。

在这个模式下，Claude 会阅读代码、分析架构、起草计划，但绝不修改代码。直到你批准计划，它才会动手。你是架构师，它是执行者。

### 20. Extended Thinking (API)：透明化思考

通过 API 调用时，开启 Extended Thinking 可以看到 Claude 的逐步推理过程（Thinking Blocks）。这对调试复杂逻辑非常有帮助。

---

## 安全与控制

### 21. Sandbox Mode：沙箱模式

用 /sandbox 一次性定义边界。比如：允许读取所有文件，允许运行 npm test，但禁止网络请求。

### 22. YOLO Mode：狂飙模式

如果你在隔离环境或完全信任操作，使用 --dangerously-skip-permissions。

YOLO (You Only Live Once)——它将跳过所有权限询问，直接执行。慎用！

### 23. Hooks：生命周期钩子

你可以在 PreToolUse（工具使用前）、SubagentStart（子智能体启动时）等事件上挂载 Shell 脚本。

比如：每当 Claude 想运行 rm -rf，自动触发脚本拦截并报警。这是对概率性 AI 的确定性控制。

---

## 自动化与 CI/CD

### 24. Headless Mode：无头模式

通过 -p 参数，Claude 可以变成一个 CLI 工具集成到流水线中：

```bash
git diff | claude -p "Explain these changes"
```

它在后台静默运行，结果直接输出到标准输出。

### 25. Commands：可复用指令

把常用的 Prompt 保存为 Markdown 文件，它就变成了自定义命令。

比如写一个 daily-standup.md，以后只需输入 /daily-standup 就能自动运行日报生成流程。

---

## 浏览器集成

### 26. Claude Code + Chrome

安装 Chrome 扩展后，Claude 可以直接操控浏览器：点击按钮、填写表单、查看控制台报错、截图。

"修复 Bug 并验证"现在变成了一个指令。

---

## 进阶：智能体与扩展

### 27. Subagents：子智能体

Claude 可以像圣诞老人分派任务给精灵一样，启动多个"子智能体"并行工作。每个子智能体有独立的 200k 上下文，处理完任务后将结果汇总。

### 28. Agent Skills：技能包

Skills 是打包好的指令和脚本文件夹。你可以把公司的部署流程封装成一个 Skill，团队成员安装后即可直接拥有这项"专家技能"，无需重复教导。

### 29. Plugins：插件市场

不再需要发送几十个文件来分享配置。/plugin install 一键安装打包好的命令、Skill、Hook 和 MCP Server。

### 30. LSP Integration：IDE 级智能

通过集成语言服务器协议（LSP），Claude 现在的代码理解能力达到了 IDE 级别。它能看到实时报错、跳转定义、查看类型信息。

### 31. Claude Agent SDK

Claude Code 的核心能力（Agent Loop、工具管理、上下文管理）现在作为一个 SDK 开放了。你可以用几十行代码构建一个像 Claude Code 一样强大的自定义智能体。

---

## 设计哲学

看完这 31 条技巧，你会发现 Claude Code 的设计哲学非常有意思。

- 通过 Plan Mode，它尊重人的决策权；
- 通过 Hooks 和 Sandbox，它给人提供了控制权；
- 通过 Subagents 和 Automation，它帮人分担了繁琐的执行工作。

正如 Ado Kukic 所说："用得最好的开发者，不是那些把所有事情都丢给 AI 的人，而是那些懂得何时使用计划模式、何时开启深度思考、如何设置安全边界的人。"

Claude Code 不是要取代开发者，而是要放大开发者的能力。

---

*来源：Ado Kukic 的 "Advent of Claude: 31 Days of Claude Code" 活动*
