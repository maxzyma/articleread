# 视频处理最佳实践

提取文章时，如果发现视频内容，必须按照本文档的规则处理视频链接。

---

## 核心规则 ⚠️

**视频是文章内容的重要组成部分，必须提取并记录视频链接。**

- [ ] **检测视频**：检查页面是否包含视频元素
- [ ] **提取链接**：根据平台类型提取视频 URL
- [ ] **添加到文章**：在文章顶部添加视频链接
- [ ] **更新元数据**：在元数据中记录视频信息

---

## 视频检测

### 1. 快速检测

使用 `take_snapshot` 检查页面：

```
查找以下元素：
- "播放视频" 按钮
- uid=xxx Video 元素
- <video> 标签
```

### 2. JavaScript 检测

使用 `evaluate_script` 查找视频：

```javascript
() => {
  const videos = document.querySelectorAll('video');
  return {
    hasVideo: videos.length > 0,
    videoCount: videos.length,
    firstVideoSrc: videos[0]?.src || videos[0]?.currentSrc
  };
}
```

---

## 平台视频提取策略

| 平台类型 | 代表平台 | 视频提取方式 | 难度 |
|---------|---------|------------|------|
| **直接链接** | 微信、Twitter、B站 | 可提取直接 MP4/M3U8 链接 | ✅ 简单 |
| **Blob URL** | 小红书、抖音 | 使用 blob URL，无法直接提取 | ⚠️ 需特殊处理 |
| **嵌入式** | 博客、Medium | 通常有直接链接或 iframe | ✅ 中等 |

---

## 视频链接格式

### 文章中的格式

在文章顶部的来源信息下方添加：

```markdown
> 来源：平台名称 作者名称，YYYY-MM-DD
> 原文链接：https://...
> 视频链接：[视频标题或"查看原视频"](视频URL) （如需登录或其他说明）
>
> **说明**：本文包含视频内容，完整内容请观看原视频
```

**示例**：

```markdown
> 来源：小红书 产品君，2025-01-25
> 原文链接：https://www.xiaohongshu.com/explore/69761dbe000000000a0314c0
> 视频链接：[查看原视频](https://www.xiaohongshu.com/explore/69761dbe000000000a0314c0) （需在小红书平台观看）
>
> **说明**：本文为视频内容的文字提取整理版，完整内容请观看原视频
```

### 元数据中的格式

在 `source` 部分添加视频相关字段：

```yaml
source:
  platform: "平台名称"
  url: "原文链接"
  video_url: "视频链接或原文链接"
  video_id: "视频ID（如有）"
  content_type: "视频" 或 "图文"
  notes: "视频提取说明（如：使用 blob URL 动态加载）"
```

**示例**：

```yaml
source:
  platform: "小红书"
  url: "https://www.xiaohongshu.com/explore/69761dbe000000000a0314c0"
  video_url: "https://www.xiaohongshu.com/explore/69761dbe000000000a0314c0"
  video_id: "69761dbe000000000a0314c0"
  content_type: "视频"
  notes: "视频使用 blob URL 动态加载，需在小红书平台观看"
```

---

## 各平台详细处理

### 1. 微信公众号 ✅

**特点**：视频通常有直接链接

**提取方法**：
1. 查找页面中的 `<video>` 元素
2. 获取 `src` 属性
3. 或运行 `extract_wechat_videos.js` 脚本

**JavaScript 提取**：
```javascript
() => {
  const videos = document.querySelectorAll('video');
  return Array.from(videos).map((v, i) => ({
    index: i,
    src: v.src,
    poster: v.poster,
    duration: v.duration
  }));
}
```

**链接格式**：
- 直接 MP4 链接：`https://mpvideo.qpic.cn/...`
- M3U8 流媒体链接：`https://vspx.tencent.com/...`

---

### 2. 小红书 ⚠️

**特点**：使用 blob URL 动态加载，无法直接提取原始视频

**检测方法**：
```javascript
() => {
  const video = document.querySelector('video');
  return {
    hasVideo: !!video,
    src: video?.src,  // 通常是 blob:https://...
    isBlob: video?.src?.startsWith('blob:')
  };
}
```

**处理方案**：
1. **文章中**：添加原文链接，说明需在平台观看
2. **元数据中**：
   - `video_url`: 原文链接
   - `content_type`: "视频"
   - `notes`: "视频使用 blob URL 动态加载，需在小红书平台观看"

**完整示例**：
```markdown
> 来源：小红书 产品君，2025-01-25
> 原文链接：https://www.xiaohongshu.com/explore/69761dbe000000000a0314c0
> 视频链接：[查看原视频](https://www.xiaohongshu.com/explore/69761dbe000000000a0314c0) （需在小红书平台观看）
>
> **说明**：本文为视频内容的文字提取整理版，完整内容请观看原视频
```

---

### 3. 抖音 ⚠️

**特点**：类似小红书，使用动态加载

**处理方案**：同小红书

---

### 4. Twitter ✅

**特点**：视频通常有直接链接

**提取方法**：
1. 查找 `<video>` 元素
2. 或从网络请求中查找 `.mp4` 链接

**链接格式**：
- `https://video.twimg.com/ext_tw_video/.../.../.../...mp4`

**处理方案**：
- 文章中添加直接视频链接
- 元数据中记录 video_url

---

### 5. B站 ✅

**特点**：通常有直接视频链接

**提取方法**：
1. 查找页面中的视频信息
2. 从 `__INITIAL_STATE__` 或类似数据中提取

**链接格式**：
- M3U8 链接：`https://cn-hk-eq-01-09.bilivideo.com/.../index.m3u8`

---

### 6. 博客/Medium ✅

**特点**：视频可能是嵌入的 YouTube/Vimeo

**提取方法**：
1. 查找 `<iframe>` 元素
2. 提取 YouTube/Vimeo 的视频 ID
3. 生成视频链接

**YouTube 示例**：
```markdown
> 视频链接：[观看 YouTube 视频](https://www.youtube.com/watch?v=VIDEO_ID)
```

---

## 常见问题

### Q1: 如何判断是否需要提取视频？

**A**: 检查页面是否有以下特征：
- `take_snapshot` 中有 "播放视频" 按钮
- 页面有 `<video>` 元素
- 页面有视频播放器（iframe）
- 文章标题或内容提到"视频"、"演示"

### Q2: blob URL 无法下载怎么办？

**A**: 对于 blob URL（小红书、抖音）：
1. **无法提取原始视频文件**（这是平台限制）
2. **提供原文链接**，让用户在平台观看
3. **在文章和元数据中明确说明**

### Q3: 如何验证视频链接是否有效？

**A**:
- **直接链接**：在浏览器中打开验证
- **Blob URL**：检查原文链接是否可访问
- **嵌入视频**：检查嵌入平台是否可访问

### Q4: 视频链接应该放在文章的哪里？

**A**: 在文章顶部，来源信息下方：

```markdown
# 文章标题

> 来源：平台 作者，日期
> 原文链接：https://...
> 视频链接：[...](...)

## 正文开始
```

---

## 验证清单

提取完成后，验证以下项目：

- [ ] **视频已检测**：确认页面包含视频元素
- [ ] **链接已提取**：根据平台类型提取了视频链接
- [ ] **文章已添加**：在文章顶部添加了视频链接
- [ ] **说明已添加**：添加了必要的说明文字
- [ ] **元数据已更新**：
  - [ ] `video_url` 字段已添加
  - [ ] `content_type` 已设置为 "视频"
  - [ ] `notes` 字段说明了视频提取方式
- [ ] **链接有效**：视频链接可访问或原文链接可访问

---

## 快速参考表

| 平台 | 可直接提取 | 处理方式 | 文章格式 | 元数据字段 |
|------|----------|---------|---------|-----------|
| **微信** | ✅ | 提取 MP4/M3U8 | `[视频标题](直接URL)` | `video_url`: 直接URL |
| **小红书** | ❌ | 使用原文链接 | `[查看原视频](原文URL)` + 说明 | `video_url`: 原文URL<br>`notes`: blob URL说明 |
| **抖音** | ❌ | 使用原文链接 | `[查看原视频](原文URL)` + 说明 | `video_url`: 原文URL<br>`notes`: blob URL说明 |
| **Twitter** | ✅ | 提取 MP4 | `[视频标题](直接URL)` | `video_url`: 直接URL |
| **B站** | ✅ | 提取 M3U8 | `[视频标题](直接URL)` | `video_url`: 直接URL |
| **博客** | ✅ | 提取嵌入链接 | `[观看视频](平台URL)` | `video_url`: 嵌入URL |

---

## 总结

**核心原则**：
1. **视频是文章的一部分**，必须记录
2. **根据平台特性**选择合适的处理方式
3. **在文章和元数据中**都添加视频信息
4. **明确说明视频的获取方式**

**验证清单是强制性的**：
- 每次提取完成后必须验证视频链接是否完整
- 遗漏视频链接 = 提取不完整
