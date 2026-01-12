# 使用 Messages API

有效使用 Messages API 的实用模式和示例。

本指南涵盖使用 Messages API 的常见模式，包括基本请求、多轮对话、预填充技术和视觉功能。

## 基本请求和响应

### Shell
```bash
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello, Claude"}
    ]
  }'
```

### 响应
```json
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Hello!"
    }
  ],
  "model": "claude-sonnet-4-5",
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 12,
    "output_tokens": 6
  }
}
```

## 多轮对话

Messages API 是无状态的，这意味着您始终要将完整的对话历史发送给 API。

### 示例
```bash
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello, Claude"},
      {"role": "assistant", "content": "Hello!"},
      {"role": "user", "content": "Can you describe LLMs to me?"}
    ]
  }'
```

## 预填充 Claude 的响应

您可以在输入消息列表的最后一个位置预填充 Claude 响应的一部分。

### 示例：获取单选答案
```bash
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --data '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1,
    "messages": [
      {"role": "user", "content": "What is latin for Ant? (A) Apoidea, (B) Rhopalocera, (C) Formicidae"},
      {"role": "assistant", "content": "The answer is ("}
    ]
  }'
```

## 视觉功能

Claude 可以在请求中读取文本和图像。我们支持图像的 base64 和 url 源类型，以及 image/jpeg、image/png、image/gif 和 image/webp 媒体类型。

### 选项 1：Base64 编码图像
```bash
IMAGE_URL="https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
IMAGE_MEDIA_TYPE="image/jpeg"
IMAGE_BASE64=$(curl "$IMAGE_URL" | base64)

curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --data '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": [
        {"type": "image", "source": {
          "type": "base64",
          "media_type": "'$IMAGE_MEDIA_TYPE'",
          "data": "'$IMAGE_BASE64'"
        }},
        {"type": "text", "text": "What is in the above image?"}
      ]}
    ]
  }'
```

### 选项 2：URL 引用图像
```bash
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --data '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": [
        {"type": "image", "source": {
          "type": "url",
          "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
        }},
        {"type": "text", "text": "What is in the above image?"}
      ]}
    ]
  }'
```

## 工具使用和 Computer use

有关如何将工具与 Messages API 一起使用的示例，请参阅我们的工具使用指南。
有关如何使用 Messages API 控制桌面计算机环境的示例，请参阅我们的 computer use 指南。
对于保证的 JSON 输出，请参阅结构化输出。
