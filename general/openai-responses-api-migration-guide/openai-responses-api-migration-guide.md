# 迁移到 Responses API 指南

> 来源：OpenAI 官方文档，2026-01-20
> 原文链接：https://platform.openai.com/docs/guides/migrate-to-responses

## 核心观点

**Responses API 是 OpenAI 新一代 API 原语，是 Chat Completions API 的演进版本**，提供更简洁的接口和强大的智能体（Agent）能力。虽然 Chat Completions API 仍受支持，但所有新项目推荐使用 Responses API。

---

## 关于 Responses API

Responses API 是一个统一接口，用于构建强大的、类似智能体的应用程序。它包含：

### 核心能力

- **内置工具**：网络搜索（Web Search）、文件搜索（File Search）、计算机使用（Computer Use）、代码解释器（Code Interpreter）、远程 MCP（Remote MCPs）
- **无缝多轮交互**：允许传递之前的响应以获得更高准确率的推理结果
- **原生多模态支持**：原生支持文本和图像

---

## Responses API 的优势

与 Chat Completions API 相比，Responses API 具有以下优势：

### 1. 更好的性能

使用推理模型（如 GPT-5）时，Responses API 相比 Chat Completions API 能获得更好的模型智能表现。内部评估显示，在相同提示词和设置下，SWE-bench 性能提升 **3%**。

### 2. 默认智能体化

Responses API 是一个智能体循环，允许模型在一次 API 请求中调用多个工具，包括：
- `web_search`（网络搜索）
- `image_generation`（图像生成）
- `file_search`（文件搜索）
- `code_interpreter`（代码解释器）
- 远程 MCP 服务器
- 您的自定义函数

### 3. 更低的成本

由于改进的缓存利用率，成本降低。内部测试显示，相比 Chat Completions API，缓存利用率提升 **40% 到 80%**。

### 4. 有状态的上下文

使用 `store: true` 在轮次之间维护状态，保留推理和工具上下文。

### 5. 灵活的输入

- 可以传递字符串输入或消息列表
- 使用指令（instructions）进行系统级指导

### 6. 加密推理

可以选择退出有状态性，同时仍从高级推理中受益。

### 7. 面向未来

为即将推出的模型做好了准备。

---

## 功能对比

| 功能 | Chat Completions API | Responses API |
|------|---------------------|---------------|
| 文本生成 | ✅ | ✅ |
| 音频（Audio） | ✅ | 即将推出 |
| 视觉（Vision） | ✅ | ✅ |
| 结构化输出 | ✅ | ✅ |
| 函数调用 | ✅ | ✅ |
| 网络搜索 | ❌ | ✅ |
| 文件搜索 | ❌ | ✅ |
| 计算机使用 | ❌ | ✅ |
| 代码解释器 | ❌ | ✅ |
| MCP | ❌ | ✅ |
| 图像生成 | ❌ | ✅ |
| 推理摘要 | ❌ | ✅ |

---

## 与 Chat Completions API 的对比

### Messages vs. Items

两个 API 都可以轻松从模型生成输出。

- **Chat Completions API**：输入和结果是 **Messages（消息）** 数组
- **Responses API**：使用 **Items（项目）** 数组

Item 是多种类型的联合体，代表模型操作的可能范围。**Message（消息）** 是一种 Item，**function_call（函数调用）** 和 **function_call_output（函数调用输出）** 也是。

与 Chat Completions Message（将多个关注点粘合到一个对象中）不同，Items 彼此独立，更好地代表了模型上下文的基本单元。

### 并行生成差异

- **Chat Completions**：可以使用 `n` 参数返回多个并行生成（`choices`）
- **Responses**：移除了此参数，只保留一个生成

### 请求示例对比

**Chat Completions API：**

```python
from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-5",
  messages=[
      {
          "role": "user",
          "content": "Write a one-sentence bedtime story about a unicorn."
      }
  ]
)

print(completion.choices[0].message.content)
```

**Responses API：**

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
  model="gpt-5",
  input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
```

### 响应对象差异

当从 Responses API 获得响应时，字段略有不同：

- **Chat Completions**：返回 `message`
- **Responses**：返回类型化的 `response` 对象，具有自己的 `id`
  - 默认情况下，Responses 被存储
  - 要禁用存储，设置 `store: false`

**Chat Completions 响应结构：**

```json
{
  "id": "chatcmpl-C9EDpkjH60VPPIB86j2zIhiR8kWiC",
  "object": "chat.completion",
  "created": 1756315657,
  "model": "gpt-5-2025-08-07",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Under a blanket of starlight...",
        "refusal": null,
        "annotations": []
      },
      "finish_reason": "stop"
    }
  ]
}
```

**Responses API 响应结构：**

```json
{
  "id": "resp_68af4030592c81938ec0a5fbab4a3e9f05438e46b5f69a3b",
  "object": "response",
  "created_at": 1756315696,
  "model": "gpt-5-2025-08-07",
  "output": [
    {
      "id": "rs_68af4030baa48193b0b43b4c2a176a1a05438e46b5f69a3b",
      "type": "reasoning",
      "content": [],
      "summary": []
    },
    {
      "id": "msg_68af40337e58819392e935fb404414d005438e46b5f69a3b",
      "type": "message",
      "status": "completed",
      "content": [
        {
          "type": "output_text",
          "annotations": [],
          "logprobs": [],
          "text": "Under a quilt of moonlight..."
        }
      ],
      "role": "assistant"
    }
  ]
}
```

---

## 其他差异

### 1. 存储默认值

- **Responses**：默认存储
- **Chat Completions**：新账户默认存储
- **禁用存储**：设置 `store: false`

### 2. 推理模型体验

推理模型在 Responses API 中有更丰富的体验，包括改进的工具使用。

### 3. 结构化输出 API 形状

- **Chat Completions**：使用 `response_format`
- **Responses**：使用 `text.format`
  - 详见[结构化输出指南](https://platform.openai.com/docs/guides/structured-outputs)

### 4. 函数调用 API 形状

函数调用的 API 形状不同，包括请求上的函数配置和响应中发送的函数调用。详见[函数调用指南](https://platform.openai.com/docs/guides/function-calling)。

### 5. 辅助方法

Responses SDK 提供 `output_text` 辅助方法，而 Chat Completions SDK 没有此方法。

### 6. 对话状态管理

- **Chat Completions**：必须手动管理对话状态
- **Responses**：与 Conversations API 兼容（支持持久化对话），或传递 `previous_response_id` 轻松链接响应

---

## 从 Chat Completions 迁移

### 步骤 1：更新生成端点

将生成端点从 `POST /v1/chat/completions` 更新到 `POST /v1/responses`。

如果不使用函数或多模态输入，迁移就完成了！简单的消息输入在两个 API 之间兼容：

**Chat Completions：**

```javascript
const context = [
  { role: 'system', content: 'You are a helpful assistant.' },
  { role: 'user', content: 'Hello!' }
];

const completion = await client.chat.completions.create({
  model: 'gpt-5',
  messages: messages
});
```

**Responses：**

```javascript
const response = await client.responses.create({
  model: "gpt-5",
  input: context
});
```

### 步骤 2：更新项目定义

在 Chat Completions 中，需要创建指定不同角色和内容的消息数组。

**生成文本示例：**

```javascript
import OpenAI from 'openai';

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

const completion = await client.chat.completions.create({
  model: 'gpt-5',
  messages: [
    { 'role': 'system', 'content': 'You are a helpful assistant.' },
    { 'role': 'user', 'content': 'Hello!' }
  ]
});

console.log(completion.choices[0].message.content);
```

### 步骤 3：更新多轮对话

如果应用程序中有多轮对话，请更新上下文逻辑。

**Chat Completions（需要手动管理上下文）：**

```javascript
let messages = [
    { 'role': 'system', 'content': 'You are a helpful assistant.' },
    { 'role': 'user', 'content': 'What is the capital of France?' }
  ];

const res1 = await client.chat.completions.create({
  model: 'gpt-5',
  messages
});

messages = messages.concat([res1.choices[0].message]);
messages.push({ 'role': 'user', 'content': 'And its population?' });

const res2 = await client.chat.completions.create({
  model: 'gpt-5',
  messages
});
```

**Responses（支持自动上下文管理）：**

使用 Responses API 的 `previous_response_id` 或 Conversations API，可以更轻松地管理多轮对话。

### 步骤 4：决定何时使用有状态性

某些组织（如具有零数据保留（ZDR）要求的组织）由于合规性或数据保留策略，无法以有状态方式使用 Responses API。为了支持这些情况，OpenAI 提供加密推理项目，允许您保持工作流无状态，同时仍从推理项目中受益。

**要禁用有状态性但仍利用推理：**

1. 在 **store 字段**设置 `store: false`
2. 添加 `["reasoning.encrypted_content"]` 到 **include 字段**

API 将返回推理令牌的加密版本，可以像常规推理项目一样在未来的请求中传递回来。

**对于 ZDR 组织**：
- OpenAI 自动强制执行 `store=false`
- 当请求包含 `encrypted_content` 时，它在内存中解密（永不写入磁盘），用于生成下一个响应，然后安全丢弃
- 任何新的推理令牌立即加密并返回给您，确保不会持久化任何中间状态

### 步骤 5：更新函数定义

Chat Completions 和 Responses 之间的函数定义有两个微小但显着的差异：

#### 差异 1：标记方式

- **Chat Completions**：使用**外部标记**的多态性
- **Responses**：使用**内部标记**的多态性

#### 差异 2：严格模式

- **Chat Completions**：函数默认**非严格**
- **Responses**：函数默认**严格**

**函数定义对比：**

**Chat Completions API：**

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Determine weather in my location",
    "strict": true,
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string"
        }
      },
      "additionalProperties": false,
      "required": [
        "location",
        "unit"
      ]
    }
  }
}
```

**Responses API：**

```json
{
  "type": "function",
  "name": "get_weather",
  "description": "Determine weather in my location",
  "parameters": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string"
      }
    },
    "additionalProperties": false,
    "required": [
      "location",
      "unit"
    ]
  }
}
```

### 步骤 6：更新结构化输出定义

在 Responses API 中，定义结构化输出已从 `response_format` 移至 `text.format`：

**Chat Completions：**

```javascript
const completion = await openai.chat.completions.create({
  model: "gpt-5",
  messages: [
    {
      "role": "user",
      "content": "Jane, 54 years old"
    }
  ],
  response_format: {
    type: "json_schema",
    json_schema: {
      name: "person",
      strict: true,
      schema: {
        type: "object",
        properties: {
          name: {
            type: "string",
            minLength: 1
          },
          age: {
            type: "number",
            minimum: 0,
            maximum: 130
          }
        },
        required: ["name", "age"],
        additionalProperties: false
      }
    }
  }
});
```

**Responses API：**

```javascript
const response = await openai.responses.create({
  model: "gpt-5",
  input: [
    {
      "role": "user",
      "content": "Jane, 54 years old"
    }
  ],
  text: {
    format: {
      type: "json_schema",
      json_schema: {
        name: "person",
        strict: true,
        schema: {
          type: "object",
          properties: {
            name: {
              type: "string",
              minLength: 1
            },
            age: {
              type: "number",
              minimum: 0,
              maximum: 130
            }
          },
          required: ["name", "age"],
          additionalProperties: false
        }
      }
    }
  }
});
```

### 步骤 7：升级到原生工具

如果您的应用程序有可以从 OpenAI 原生工具中受益的用例，可以更新工具调用以直接使用 OpenAI 的工具。

**Chat Completions（需要自己实现）：**

```javascript
async function web_search(query) {
    const fetch = (await import('node-fetch')).default;
    const res = await fetch(`https://api.example.com/search?q=${query}`);
    const data = await res.json();
    return data.results;
}

const completion = await client.chat.completions.create({
  model: 'gpt-5',
  messages: [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'Who is the current president of France?' }
  ],
  functions: [
    {
      name: 'web_search',
      description: 'Search the web for information',
      parameters: {
        type: 'object',
        properties: { query: { type: 'string' } },
        required: ['query']
      }
    }
  ]
});
```

**Responses（直接使用原生工具）：**

```javascript
const response = await client.responses.create({
  model: 'gpt-5',
  input: [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'Who is the current president of France?' }
  ],
  tools: [
    {
      type: 'web_search'
    }
  ]
});
```

---

## 增量迁移

Responses API 是 Chat Completions API 的超集。Chat Completions API 也将继续受到支持。因此，如果需要，可以增量采用 Responses API。

**迁移策略**：
- 将受益于改进推理模型的用户流程迁移到 Responses API
- 其他流程保持在 Chat Completions API 上，直到准备好完全迁移

**最佳实践**：鼓励所有用户迁移到 Responses API，以利用 OpenAI 的最新功能和改进。

---

## Assistants API 说明

基于开发者在 Assistants API Beta 中的反馈，OpenAI 在 Responses API 中集成了关键改进，使其更加灵活、快速和易于使用。

**重要信息**：
- Responses API 代表在 OpenAI 上构建智能体的未来方向
- Responses API 现在具有类似 Assistant 和 Thread 的对象
- 详见[迁移指南](https://platform.openai.com/docs/guides/assistants/migration)

**弃用时间线**：
- **2025年8月26日**：开始弃用 Assistants API
- **2026年8月26日**：Assistants API 正式退役

---

## 技术启示

对于正在使用 OpenAI API 的开发者：

### 1. 立即行动

- **新项目**：直接使用 Responses API
- **现有项目**：开始规划迁移路径

### 2. 优先迁移的场景

- 需要复杂推理的应用
- 需要多工具调用的智能体应用
- 对成本敏感的应用（缓存优化）
- 需要多轮对话的应用

### 3. 迁移建议

- **增量迁移**：按用户流程逐步迁移，降低风险
- **测试验证**：在迁移前后对比结果，确保功能一致
- **利用新功能**：迁移后充分利用原生工具和状态管理

### 4. Assistants API 用户

- 如果使用 Assistants API，必须在 **2026年8月26日** 前完成迁移
- 查看官方迁移指南，了解具体的迁移步骤
- Responses API 提供了更灵活和强大的替代方案

---

## 参考资源

- [Responses API 参考](https://platform.openai.com/docs/api-reference/responses)
- [函数调用指南](https://platform.openai.com/docs/guides/function-calling)
- [结构化输出指南](https://platform.openai.com/docs/guides/structured-outputs)
- [工具使用指南](https://platform.openai.com/docs/guides/tools)
- [Assistants API 迁移指南](https://platform.openai.com/docs/guides/assistants/migration)
