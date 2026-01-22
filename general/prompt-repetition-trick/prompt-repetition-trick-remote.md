# 一个被忽视的 Prompt 技巧：重复提示词

> 来源：微信公众号 数字生命卡兹克，2026-01-22
> 原文链接：https://mp.weixin.qq.com/s/jlpaO-piFqvnxAgVJ47wyw

## 核心观点

**通过重复输入提示词，可以将非推理类大语言模型（LLM）的准确率从 21.33% 提高到 97.33%。**这个简单的"复制粘贴大法"（Ctrl C + Ctrl V）在 70 个测试任务中赢了 47 次，0 次失败。

![论文封面](https://mmbiz.qpic.cn/mmbiz_png/OjgKEXmLURpSib6zyXsy8qgZEWaLzWmujgGZmgUic31pdZxUAeWgNNT7E5tsibibkRR0ul0Z2Mn4ib6iaOp3ficQYEQnw/640?wx_fmt=png)

---

## 背景：Google 的新研究

这个技巧出自 Google 的论文《Prompt Repetition Improves Non-Reasoning LLMs》，翻译过来就是：**重复你的问题，能让 AI 变得更聪明。**

### 什么是非推理模型？

- **非推理模型**：没有深度思考功能，直接生成答案（速度快，但准确率相对较低）
  - 示例：Gemini 2.0 Flash、GPT-4o、Claude 3 Haiku、DeepSeek V3
- **推理模型**：有思维链（Chain of Thought），会"思考"（速度慢，但准确率高）
  - 示例：DeepSeek R1、GPT-5.2 Thinking

![测试模型列表](https://mmbiz.qpic.cn/mmbiz_png/OjgKEXmLURpSib6zyXsy8qgZEWaLzWmujwrdDSfokrsYAl02e8b8uHpYTyz6Tw80xJQnDEic7NyS0uibzsEoTOljQ/640?wx_fmt=png)

---

## 核心实验：重复提示词的效果

### 实验设计

Google 测试了 7 个主流非推理模型：
- Gemini 2.0 Flash & Flash Lite
- GPT-4o & 4o-mini
- Claude 3 Haiku & 3.7 Sonnet
- DeepSeek V3

测试基准包括：
- ARC、OpenBookQA、GSM8K、MMLU-Pro、MATH 等常见测试集
- 两个自创测试：NameIndex（姓名索引法）和 MiddleMatch（中间匹配法）

![测试方法图示](https://mmbiz.qpic.cn/mmbiz_png/OjgKEXmLURpSib6zyXsy8qgZEWaLzWmujAFAojymHmSIdmT44ARoJxQ24V6RY7aMPa5wzyykHleFGHZiaJkJibm6g/640?wx_fmt=png)

### 对比方式

**传统方式**：
```
<问题>
```

**重复方式**：
```
<问题><问题>
```

**不加解释，不说 please，不加"think step by step"，不做任何修饰，只是原封不动地重复一遍。**

### 实验结果

![重复提示词对比](https://mmbiz.qpic.cn/mmbiz_png/OjgKEXmLURpSib6zyXsy8qgZEWaLzWmujliccibibP6iaxVZanDBwuNbpwvsXu6gicEVZ4bp3icSRoDlQD8qx1RWw9qCA/640?wx_fmt=png)

在 70 组对比中：
- **赢 47 次**（准确率显著提升）
- **平 23 次**
- **输 0 次**

某些任务上，准确率从 21% 飙升到 97%。

---

## 技术原理：为什么重复有效？

### 因果语言模型的局限性

大模型是"因果语言模型"（Causal Language Model），从左到右逐词预测。当前的 token 只能看到之前的内容，无法提前看到后面的。

### 重复的作用

当问题从 `Q` 变成 `Q1Q2` 时：
- `Q2` 里的每个字在计算时，都能"回头看" `Q1` 的所有内容
- 等于给了 AI 一次"重新思考"的机会

### 通俗示例

假设给 AI 一个选择题：

**问题**：
```
选项：
A. 把蓝色方块放到红色方块左边
B. 把红色方块放到蓝色方块左边

场景说明：现在红色在左，蓝色在右。
问题：哪一个选项会改变画面？只输出 A 或 B
```

**不重复时**：读到 A、B 时，模型还不知道场景信息，第一印象很空。等读到后面时，已经无法"倒带"重新理解 A、B。

**重复后**：第二遍的 A、B 出现时，已经包含了第一遍的完整信息，模型能带着场景条件生成选项表征，准确率大幅提升。

---

## 为什么对推理模型无效？

因为推理模型（如 DeepSeek R1）已经通过强化学习（RL）自动学会这个技巧了。

它们在推理时，第一反应就是**复述问题**：
- "题目问的是……"
- "我们需要求解的是……"
- "首先我们需要理解题目给出的条件……"

本质上，它们已经在自动"多抄一遍题目"给自己排版了。

![DeepSeek R1 推理示例](https://mmbiz.qpic.cn/mmbiz_png/OjgKEXmLURpSib6zyXsy8qgZEWaLzWmujKEUdQwHicic7YHJndNoU6ZD6iasfedDWzdl3ZTE6yrl4CCHo02aJlk3xw/640?wx_fmt=png)

---

## 实践启示

### 1. 简短问答场景

对于纯粹的问答任务（尤其是短问题），不需要复杂的 Prompt 工程：
- ❌ 不需要复杂的结构、角色、规则、上下文、格式
- ✅ 只要把题目重复一遍，就是极强的优化

### 2. 适用场景

| 模型类型 | 是否适用 | 原因 |
|---------|---------|------|
| 非推理模型 | ✅ 适用 | 速度快，重复可弥补准确率 |
| 推理模型 | ❌ 不适用 | 已自动学会复述技巧 |

### 3. 使用建议

- 适用于需要快速响应的场景
- 适用于短问题、选择题、事实性问答
- 不适用于需要复杂推理的任务（直接用推理模型更好）

---

## 更深层的思考

### Prompt 工程的本质

我们过去对 Prompt 工程的想象太浪漫了：
- 总觉得需要结构清晰、层层递进、有角色有规则
- 把写提示词当成"下咒语"，要讲究格式、口气、敬语

但事实证明，**对很多场景，模型压根不需要你在提示词上搞太多花活**。

### 重复的意义

人类社会一直在用"复制粘贴"，只是给它起了体面的名字：
- 复述、强调、排比、朗诵、咏唱、抄经、背诵、晨读……

**人类的很多情感，都是靠重复才能构筑的。**

### 生活启示

> "爱一个人是日常的复制粘贴，专业是一辈子的复制粘贴，写作是对一些想法一遍又一遍的复制粘贴，直到有一天，这些东西都不需要你刻意想起，它们自动从你的手指和眼神里长出来。"

> "从一堆 token 里看到真正的重点，需要的是几次重复后的清晰。而从一地鸡毛里看到一点点意义，生活，很多时候也是这样。"

---

## 技术要点总结

| 维度 | 说明 |
|------|------|
| **核心技巧** | 将提示词重复一遍（Ctrl C + Ctrl V） |
| **适用模型** | 非推理模型（如 GPT-4o、Claude 3、Gemini Flash） |
| **提升幅度** | 最高可达 21% → 97% |
| **实现方式** | 不加任何修饰，原封不动重复 |
| **不适用场景** | 推理模型（已自动学会此技巧） |

---

## 未来方向

Google 论文中提到的优化方向：
1. 把重复提示写入模型训练流程
2. 只在 KV cache 里保留第二遍提示（不影响推理性能）
3. 只重复提示词的一部分（而非整段）
4. 扩展到多模态（图像、视频的重复）

---

**高山之流水，万物皆重复。**
