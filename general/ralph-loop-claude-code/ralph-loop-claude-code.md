# 卷死你的 Claude Code，让它彻夜干活：ralph loop 插件一手体验

> 来源：微信公众号 Decoder Only（转载湾仔码农），2026-01-15
> 原文作者：湾仔码农
> 原文链接：https://www.xiaohongshu.com/explore/69683542000000000b00bacb（已失效）

## 核心观点

**Ralph Loop 插件让 Claude Code 实现持续循环执行，在有详细 PRD（产品需求文档）和测试用例的场景下，可自动完成数天的人工工作量。**

核心价值：
- 自动循环迭代：遇到错误自动修复，直到所有测试通过
- 效率提升显著：Claude Code 之父 Boris 一个月提交 259 个 PR，添加 40000 行代码
- 需要前期准备：详细的 PRD + 完整的测试用例是关键前提

---

## 背景：Boris 的惊人产出

最近 Claude Code 之父 Boris 分享了一个数字：

**过去 1 个月内，提交了 259 个 PR，添加了 40000 行代码。**

而这背后，是 Claude Code 不眠不休地在帮他干活。

你可能好奇，怎么让 Claude 持续不间断运行长任务？

这背后的秘密就是 Anthropic 近期开放的插件 —— **ralph wiggum**（最近因为版权原因，改名为 **ralph loop** 了）。

---

## Ralph Loop 的名字由来

**Ralph Wiggum** 是美国动画片《辛普森一家》中的角色，他最大的特点就是智力迟钝但"天真执着"，认定目标后，即使犯错也会不断尝试。

去年，有个澳洲的码农 Geoffrey Huntley（之前一直写代码，最近在澳洲养山羊）在他的一篇博客里最早提出了这个理念。他编写了一个只有 5 行的 Bash 脚本，背后的原理很简单——如果需求没做完，就继续循环做，别扯什么"人在回路（Human in the loop）"。

这个理念很快被 Claude Code 和 Anthropic 效仿，各自发展出一套类似的能力。

---

## 什么时候需要用 Ralph Loop？

你用 Claude Code 或其他 AI 编程工具时，是不是经常一个任务开始跑后，就得时不时去检查，再给它一些反馈？

我最常用的就是 pua 一下"跑完全部单元测试和自动化测试，中间不可以停止"。但这种方式时灵时不灵，最头疼的就是 AI 说"已经完美通过了所有测试"，但你一体验，还是各种 bug。

**Ralph Loop 最厉害的地方**是它会"天真执着"地帮你执行需求，如果没达到终止条件，它可以一直干下去，直到地老天荒，或者把你的套餐的钱全部花光。

---

## 安装配置

### 安装步骤

```bash
# 添加官方市场
/plugin marketplace add anthropics/claude-code

# 安装插件
/plugin install ralph-loop@claude-plugins-official
```

**注意**：要用 `ralph-loop`，而不是 `ralph-wiggum`（旧版名称）。

---

## 实战案例：飞书文档转微信公众号排版工具

### 需求背景

公众号写比较多，每次粘贴到编辑器都想问候产品经理。于是想做一个工具，支持从飞书文档复制粘贴，并且多个模板可以选择。

### 第一步：编写 PRD

用 AI 辅助生成 PRD 初稿，命名为 `prd.md`。核心功能需求：
1. 读取飞书文档内容
2. 解析 Markdown 格式
3. 转换为微信公众号支持的格式
4. 处理图片、代码块、表格等特殊元素
5. 提供多个模板选择

### 第二步：启动 Ralph Loop

```
/ralph-loop:ralph-loop "读取 prd.md，选择 2-3 个最核心的功能实现一个可运行的 MVP。要求：1) 有基本的用户界面 2) 核心功能可以操作 3) 包含基础测试 4) 确保代码可以运行。完成后输出 <promise>MVP_COMPLETE</promise>" --max-iterations 20 --completion-promise "MVP_COMPLETE"
```

### 执行过程

| 轮次 | 耗时 | 说明 |
|------|------|------|
| 1-20 轮 | 9 分 31 秒 | 完整执行 20 轮（stop hook 报错） |

**观察记录**：
- Claude 自己发现语法错误，开始自动修复
- 进入循环模式，持续迭代
- 完成后包含 3 个模板，图片粘贴正常渲染
- 标题格式、分级标题、代码块都已映射
- 但代码块样式不够好看，首行缩进过于传统

### 第三步：迭代优化

```
/ralph-loop:ralph-loop "读取 prd.md，多提供几个模板（10 个），找一下微信上比较流行的模板，各种颜色的组合。代码块样式整专业点，mac terminal 风格，自动换行。所有模板都不要首行缩进了。要求：1) 实现以上需求 2) 核心功能可以操作 3) 包含基础测试 4) 确保代码可以运行。" --max-iterations 20 --completion-promise "TEMPLATE_ENRICH_COMPLETE"
```

结果：5 分多钟就搞完了，10 个模板都已实现。

---

## 提高难度：make it better 测试

前面给的需求比较具体，下面试试"make it better"这种模糊需求：

```
/ralph-loop:ralph-loop "make it better." --max-iterations 20
```

### 执行观察

- 上了个厕所回来，发现 Claude 自己分解了 8 个任务
- 分解的任务包括：字数统计、移动端响应式、常用模板等
- 跑了 4 轮，花了 22 分钟
- 第二天早上发现跑到第 14 轮停了（npm run test 卡死）
- 但 Claude 能自动识别错误并修复，继续第 15 轮

### 验收结果

经过一夜迭代，功能"雕花"到了极致：
- 暗黑模式
- 导入 HTML
- 快捷键
- 模板预览
- 模板搜索
- 常用模板
- 分类筛选
- 字数统计
- 阅读时间
- 底部快捷操作按钮

---

## 小结

**Ralph Loop 最适合的场景**：
> 你有了非常详细的 PRD 和测试用例，但人工执行要非常久的场景。可以让它"笨笨地坚持"、不知疲倦地按照需求干活，不用担心跑偏。

**重要建议**：
1. **最好结合浏览器自动化测试**，进一步验证效果（我这次中间那个错误，就卡在缺了这一步）
2. **Token 消耗可控**：反正人工执行也要花那么多，不用太操心
3. **慎用"make it better"**：可能会给你惊喜，但也可能给你写一堆史上雕花的功能

---

## 资源链接

- [Claude Code](https://claude.ai/code)
- [Ralph Loop 插件](https://github.com/anthropics/claude-code-plugins)
- [Geoffrey Huntley](https://github.com/guysie)
