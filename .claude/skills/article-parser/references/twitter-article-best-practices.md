# Twitter 全文提取最佳实践

## 特点

Twitter 是文字友好平台，提取相对简单。

---

## 提取流程

```bash
# 访问推文/Thread
navigate_page -> <Twitter URL>

# 获取页面快照
take_snapshot
```

---

## 提取内容

| 字段 | 位置 |
|------|------|
| 作者 | 用户名和显示名 |
| 时间 | 发布时间戳 |
| 正文 | 推文内容 |
| 图片 | 嵌入图片 |
| Thread | 多条连续推文 |

---

## Thread 处理

1. 展开所有 "Show this thread"
2. 按时间顺序提取所有推文
3. 合并为完整文章

---

## 图片提取

Twitter 图片通常可以直接引用：
```
https://pbs.twimg.com/media/xxxxx.jpg
```

### 图片命名
使用 Media ID：`G_J8qXqaoAQ2xhu.jpg`

---

## 注意事项

- ✅ Thread 需要完整展开
- ✅ 保留嵌入的代码块
- ❌ 忽略评论和转发
