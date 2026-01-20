# Claude Code 之父的工作流火了：740 万围观的背后

> 来源：微信公众号 AI信息Gap，2026-01-16
> 原文链接：https://mp.weixin.qq.com/s/fSAgfe2V9dUQimAkrPauqQ

## 核心观点

**Boris Cherny（Claude Code 创造者）在 X 上分享个人工作流：15 个 Claude 实例并行、全程使用 Opus 4.5 Thinking 模型、Plan Mode 优先、团队共享 CLAUDE.md 记忆系统。740 万阅读量，引发开发者热议。**

---

## 背景

Boris Cherny 在 X 上发了一条帖子，分享自己怎么用 Claude Code。

740 万阅读量。

![Boris Cherny 在 X 上分享 Claude Code 工作流](https://cdn.jsdelivr.net/gh/maxzyma/articleread/general/boris-claude-code-workflow/images/00_cover.jpg)

Boris 是 Anthropic 的资深工程师，Claude Code 就是他做的。2024 年 9 月加入 Anthropic，从一个内部原型开始，一路把 Claude Code 做到了 6 个月 10 亿美元 ARR。这个速度，放在整个 SaaS 历史上都是现象级的。

所以当他说「分享一下我自己怎么用 Claude Code」的时候，直接火了。

有人说这是 Anthropic 的「ChatGPT 时刻」。

有人说，用了他的方法之后，「感觉更像在玩星际争霸，而不是在写代码」，从敲键盘变成了指挥部队。

但最让人意外的是，他的设置出奇简单。

用他自己的原话说：surprisingly vanilla。

---

## 01｜15 个 Claude 并行

Boris 的日常是这样的：终端里开 5 个 Claude Code，浏览器里再开 5-10 个。

每个标签页编号 1-5，由系统通知告诉他哪个 Claude 需要操作。

![Boris Cherny 的 Claude Code 工作流](https://cdn.jsdelivr.net/gh/maxzyma/articleread/general/boris-claude-code-workflow/images/01_section01.jpg)

一个 Claude 在跑测试，另一个在重构代码，第三个在写文档。

他还会在手机上（用 Claude iOS app）启动几个会话，早上开始，白天随时查看进度。

需要的时候，用 `--teleport` 命令把会话在本地和网页之间来回转移。

这验证了 Anthropic 联合创始人 Daniela Amodei 说的策略：用更好的编排，而不是更多的算力。

---

## 02｜用最慢的模型，反而最快

这条可能是整个帖子里最反直觉的。

Boris 用的是 **Opus 4.5 Thinking**，Anthropic 最大、最慢的模型。

不是 **Sonnet**。不是 **Haiku**。

他的原话：

> 「这是我用过的最好的编程模型。虽然它比 Sonnet 更大更慢，但因为你不需要反复纠正它、它的工具使用能力更强，所以最终几乎总是比用小模型更快。」

![Boris 关于使用 Opus 4.5 Thinking 的说明](https://cdn.jsdelivr.net/gh/maxzyma/articleread/general/boris-claude-code-workflow/images/02_section02.jpg)

表面上慢，实际上省掉了来回调试的时间。

---

## 03｜Plan Mode：先想清楚，再行动

大多数会话，Boris 都从 Plan Mode 开始。

快捷键是 `shift+tab` 按两次。

如果目标是写一个 Pull Request，他会先在 Plan Mode 里和 Claude 反复讨论，直到计划满意。然后切换到自动接受编辑模式，让 Claude 一次性完成。

他说：「一个好的计划非常重要。」

![Plan Mode 工作流程](https://cdn.jsdelivr.net/gh/maxzyma/articleread/general/boris-claude-code-workflow/images/03_section03.jpg)

强烈推荐这个 Plan Mode，谁用都知道！

---

## 04｜CLAUDE.md：团队共享的 AI 记忆

Boris 的团队维护一个 `CLAUDE.md` 文件，提交到 git 里，每周会更新几次。

规则很简单：「每次看到 Claude 做错什么，就加进去。」

这样 Claude 下次就知道不要再犯同样的错误。

代码审查的时候，他经常在同事的 PR 里 @.claude，让 Claude 把某条规则加进 `CLAUDE.md`。他们用 Claude Code 的 GitHub Action 来实现这个流程。

![CLAUDE.md 文件示例](https://cdn.jsdelivr.net/gh/maxzyma/articleread/general/boris-claude-code-workflow/images/04_section04.jpg)

每一个错误都变成了一条规则。团队合作的时间越长，AI 就越聪明。

---

## 05｜快捷命令：把重复的事情自动化

Boris 用快捷命令处理每天要做很多次的「内循环」工作流。

比如他有一个 `/commit-push-pr` 命令，每天要用几十次。这个命令用内联 bash 预先查询 git status 和其他信息，避免和模型来回对话。

![快捷命令配置示例](https://cdn.jsdelivr.net/gh/maxzyma/articleread/general/boris-claude-code-workflow/images/05_section05.jpg)

命令都放在 `.claude/commands/` 目录里，提交到 git，团队共享。

---

## 06｜Subagents：让 AI 互相检查

Boris 用 subagent 来处理开发周期的不同阶段。

`code-simplifier` 负责在主要工作完成后简化代码架构。

`verify-app` 负责端到端测试。

他的代码审查命令会同时启动好几个 subagent：一个检查代码风格，一个查项目历史理解上下文，一个找明显的 bug。第一轮会有误报，所以他再用 5 个 subagent 专门挑第一轮结果的毛病。

![Subagents 目录结构](https://cdn.jsdelivr.net/gh/maxzyma/articleread/general/boris-claude-code-workflow/images/06_section06.jpg)

他说：「最后的结果很棒，能找到所有真正的问题，没有误报。」

---

## 07｜让 Claude 用你的工具

Boris 让 Claude Code 直接使用他日常的工具。

主要通过 MCP server。比如连接 BigQuery 查询回答数据问题。从 Sentry 拉错误日志。

相关的 MCP 配置放在 `.mcp.json` 里，团队共享。

这意味着 Claude 不只是写代码，还能帮你查数据、找 bug。

---

## 08｜权限和 Hooks

Boris 不用 `--dangerously-skip-permissions`。

他用 `/permissions` 预先允许那些他知道安全的常用 bash 命令，避免不必要的权限弹窗。大部分配置放在 `.claude/settings.json` 里，团队共享。

他用 PostToolUse hook 来格式化 Claude 生成的代码。Claude 生成的代码通常格式不错，hook 处理最后 10%，避免 CI 里出格式错误。

对于特别长时间运行的任务，他要么让 Claude 完成后用后台 agent 验证，要么用 Stop hook 更确定地做这件事，要么用一个叫 `ralph-wiggum` 的插件。

![Hooks 配置示例](https://cdn.jsdelivr.net/gh/maxzyma/articleread/general/boris-claude-code-workflow/images/08_section08.jpg)

---

## 09｜验证循环：最重要的一条

Boris 说，如果只能记住一条，记住这条：

> 「给 Claude 一个验证自己工作的方法。如果 Claude 有这个反馈循环，最终结果的质量会提升 2-3 倍。」

他自己的做法是：Claude 用 Chrome 扩展测试每一个提交到 claude.ai/code 的改动。打开浏览器，测试 UI，反复迭代，直到代码能用、体验顺畅。

验证在不同领域看起来不一样。可能是跑一个 bash 命令，可能是跑测试套件，可能是在浏览器或手机模拟器里测应用。

关键是要让这个循环稳定可靠。

---

## 结语

有人问 Boris，为什么要公开分享这些？

他说 Claude Code 没有唯一正确的使用方式。他们故意把它做成可以随意定制和折腾的样子。

740 万阅读量，说明开发者真的很想知道创造这个工具的人，自己是怎么用的。

答案出乎意料地简单。多开几个、用最好的模型、先想清楚再动手、让 AI 能验证自己的工作。

就这些。

---
