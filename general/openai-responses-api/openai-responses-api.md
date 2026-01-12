# 为什么我们构建 Responses API

> **核心总结**：随着 GPT-5 的发布，Responses API 为推理模型（Reasoning Models）和智能体（Agent）未来提供了最佳集成方式。相比 Chat Completions API，Responses API 提供了持久推理（Persistent Reasoning）、托管工具（Hosted Tools）和多模态工作流（Multimodal Workflows）支持。它是一个有状态的智能体循环（Agentic Loop），能够保留推理状态（Reasoning State）跨多个轮次，在 TAUBench 上提升 5% 性能，缓存利用率提高 40-80%。

**发布日期：** 2025 年 9 月 22 日
**分类：** OpenAI / API 设计 / GPT-5
**作者：** Steve Coffey, Prashant Mital
**来源：** [OpenAI Developer Blog](https://developers.openai.com/blog/responses-api/)

---

## 引言

随着 GPT-5 的发布，我们想要给出更多关于集成它的最佳方式的背景，**响应 API（Responses API）**，以及为什么 Responses 是为推理模型（Reasoning Models）和智能体（Agent）未来量身定制的。

OpenAI API 的每一代都是围绕同一个问题构建的：**开发者与模型交谈的最简单、最强大的方式是什么？**

我们的 API 设计始终由模型本身的工作方式指导。最初的 `/v1/completions` 端点很简单，但有限制：你给模型一个提示（Prompt），它只会完成你的想法。通过少样本提示（Few-shot Prompting）等技术，开发者可以尝试引导模型做诸如输出 JSON 和回答问题之类的事情，但这些模型远不如我们今天习惯的那么强大。

然后来了 RLHF、ChatGPT 和后训练（Post-training）时代。突然间模型不只是完成你半写成的散文——它们像对话伙伴一样**响应（Responding）**。为了跟上步伐，我们构建了 `/v1/chat/completions`（**著名的在一个周末内完成**）。通过赋予 system、user、assistant 等角色，我们提供了快速构建具有自定义指令和上下文的聊天界面的脚手架。

我们的模型不断变得更好。很快，它们开始看、听和说。2023 年末的函数调用（Function-calling）成为我们最受喜爱的功能之一。大约同时，我们推出了测试版的助手 API（Assistants API）：我们第一次尝试完全智能体（Agent）界面，带有代码解释器（Code Interpreter）和文件搜索（File Search）等托管工具。一些开发者喜欢它，但由于相对于 Chat Completions 限制性强且难以采用的 API 设计，它从未实现大规模采用。

到 2024 年末，显然我们需要统一：像 Chat Completions 一样平易近人，像 Assistants 一样强大，但专门为多模态（Multimodal）和推理模型（Reasoning Models）构建。进入 `/v1/responses`。

---

## /v1/responses 是一个智能体循环（Agentic Loop）

Chat Completions 为你提供了一个简单的基于回合的聊天界面。Responses 相反为你提供了一个用于推理和行动的结构化循环。把它想象成与侦探一起工作：你给他们证据，他们调查，他们可能咨询专家（工具），最后他们回报。侦探在步骤之间保留他们的私人笔记（推理状态，Reasoning State），但从不将它们交给客户。

这就是推理模型（Reasoning Models）真正发光的地方：Responses 在这些轮次之间保留模型的**推理状态（Reasoning State）**。在 Chat Completions 中，推理在调用之间被丢弃，就像侦探每次离开房间都忘记线索一样。Responses 保持笔记本打开；逐步的思维过程实际上存活到下一轮。这体现在基准测试中（TAUBench +5%）以及更高效的缓存利用率和延迟中。

Responses 还可以发出多个输出项（Output Items）：不仅是模型**说了什么**，还有它**做了什么**。你获得收据——工具调用（Tool Calls）、结构化输出（Structured Outputs）、中间步骤（Intermediate Steps）。这就像得到完成的论文和草稿本数学。对调试、审计和构建更丰富的 UI 很有用。

**Chat Completions 示例：**
```json
{
  "message": {
    "role": "assistant",
    "content": "我要使用 get_weather 工具来查找天气。",
    "tool_calls": [
      {
        "id": "call_88O3ElkW2RrSdRTNeeP1PZkm",
        "type": "function",
        "function": {
          "name": "get_weather",
          "arguments": "{\"location\":\"New York, NY\",\"unit\":\"f\"}"
        }
      }
    ],
    "refusal": null,
    "annotations": []
  }
}
```

**Responses 示例：**
```json
[
  {
    "id": "rs_6888f6d0606c819aa8205ecee386963f0e683233d39188e7",
    "type": "reasoning",
    "summary": [
      {
        "type": "summary_text",
        "text": "**确定天气响应**\n\n我需要回答用户关于旧金山天气的问题。..."
      }
    ]
  },
  {
    "id": "msg_6888f6d83acc819a978b51e772f0a5f40e683233d39188e7",
    "type": "message",
    "status": "completed",
    "content": [
      {
        "type": "output_text",
        "text": "我将检查实时天气服务以获取旧金山的当前状况，以华氏度和摄氏度提供温度，以符合您的偏好。"
      }
    ],
    "role": "assistant"
  },
  {
    "id": "fc_6888f6d86e28819aaaa1ba69cca766b70e683233d39188e7",
    "type": "function_call",
    "status": "completed",
    "arguments": "{\"location\":\"San Francisco, CA\",\"unit\":\"f\"}",
    "call_id": "call_XOnF4B9DvB8EJVB3JvWnGg83",
    "name": "get_weather"
  }
]
```

Chat Completions 每个请求发出一个**消息（Message）**。消息的结构是有限的：消息还是函数调用先来？

Responses 发出**多态项（Polymorphic Items）**列表。模型采取的行动顺序是清晰的。作为开发者，你可以选择要显示、记录或完全忽略其中的哪些。

---

## 使用托管工具（Hosted Tools）向上堆栈移动

在函数调用的早期，我们注意到一个关键模式：开发者使用模型既调用 API，也搜索文档存储以引入外部数据源——现在称为检索增强生成（RAG）。但是，如果你是一个刚刚开始的开发者，从头开始构建检索管道是一项令人生畏且昂贵的工作。使用 Assistants，我们推出了我们的第一个**托管工具**：`file_search` 和 `code_interpreter`，允许模型做检索增强生成（RAG）并编写代码来解决你问它的问题。

在 Responses 中，我们更进一步，添加了网络搜索（Web Search）、图像生成（Image Gen）和模型上下文协议（MCP）。而且由于工具执行通过代码解释器或 MCP 等托管工具在服务器端发生，你不是每次调用都通过自己的后端反弹，确保更好的延迟和往返成本。

---

## 安全地保留推理（Preserving Reasoning Safely）

那么为什么要费尽心思混淆模型的原始思维链（Chain-of-Thought, CoT）？公开思维链并让客户端将它们视为与其他模型输出类似不是更容易吗？简短的回答是，公开原始思维链有许多风险：比如幻觉（Hallucinations）、在最终响应中不会生成的有害内容，以及对 OpenAI 来说，开放竞争风险。

当我们去年末发布 o1-preview 时，我们的首席科学家 Jakub Pachocki 在我们的博客中写道：

> "我们认为，隐藏的思维链为监控模型提供了独特的机会。假设它是忠实的和可读的，隐藏的思维链允许我们'读取模型的思想'并理解其思维过程。例如，在未来，我们可能希望监控思维链以寻找操纵用户的迹象。然而，为了使这工作，模型必须有自由地以未改变的形式表达其思想，所以我们不能对思维链训练任何策略合规性或用户偏好。我们也不想使未对齐的思维链直接对用户可见。"

Responses 通过以下方式解决了这个问题：
- 在内部保留推理，加密并对客户端隐藏
- 通过 `previous_response_id` 或推理项目（Reasoning Items）允许安全继续，而不暴露原始思维链

---

## 为什么 /v1/responses 是最佳构建方式

我们将 Responses 设计为**有状态（Stateful）、多模态（Multimodal）和高效（Efficient）**。

**智能体工具使用（Agentic Tool-Use）：** Responses API 使你能够轻松地使用文件搜索（File Search）、图像生成（Image Gen）、代码解释器（Code Interpreter）和模型上下文协议（MCP）等工具增强智能体（Agent）工作流。

**默认有状态（Stateful-by-Default）。** 对话和工具状态自动跟踪。这使推理和多轮工作流戏剧性地更容易。通过 Responses 集成的 GPT-5 在 TAUBench 上比 Chat Completions 得分高 5%，纯粹通过利用保留的推理。

**从根本上多模态（Multimodal from the Ground Up）。** 文本、图像、音频、函数调用（Function Calls）——都是一等公民。我们没有将模态螺栓连接到文本 API 上；我们从第一天起就设计了足够的卧室。

**更低的成本，更好的性能。** 内部基准测试显示，与 Chat Completions 相比，缓存利用率提高 40-80%。这意味着更低的延迟和更低的成本。

**更好的设计：** 我们从 Chat Completions 和 Assistants API 学到了很多东西，并在 Responses API 和 SDK 中做了一些小的生活质量改进，包括：
- 语义流事件（Semantic Streaming Events）
- 内部标记的多态性（Internally-tagged Polymorphism）
- SDK 中的 `output_text` 助手（不再需要 `choices.[0].message.content`）
- 更好的多模态和推理参数组织

---

## Chat Completions 怎么样？

Chat Completions 不会消失。如果它对你有用，继续使用它。但是，如果你想要持久推理（Persistent Reasoning）、感觉原生的多模态交互，以及不需要胶带的智能体循环（Agentic Loop）——Responses 是前进的道路。

---

## 展望未来

正如 Chat Completions 取代了 Completions，我们期望 Responses 成为开发者构建 OpenAI 模型的默认方式。它在需要时简单，在想要时强大，并且足够灵活以处理下一个范式抛给我们的任何东西。

这是我们在未来几年将构建的 API。

---

*来源：OpenAI Developer Blog*
