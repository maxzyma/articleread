# 微信公众号全文提取最佳实践

## ⚠️ 重要：图片提取必须使用 JavaScript

**微信公众号使用图片懒加载，不能只依赖 `take_snapshot`！**

- ❌ **错误**：使用 `take_snapshot` → 只能获取占位符 SVG
- ✅ **正确**：运行 `extract_wechat_images.js` → 获取真实图片 URL

**原因**：微信图片的真实 URL 存储在 `data-src` 属性中，`src` 是占位符。

---

## 提取流程

```
访问文章 → 滚动触发懒加载 → 提取文本 → 提取图片 → 验证完整性
```

### 快速开始（推荐）

**使用自动化脚本**：
```bash
# 1. 打开微信文章
navigate_page -> <微信文章URL>

# 2. 运行图片提取脚本
evaluate_script -> 复制 scripts/extract_wechat_images.js 全部内容

# 3. 脚本会自动：
#    - 滚动页面触发懒加载
#    - 提取所有图片 URL（包括 data-src）
#    - 输出下载命令
#    - 生成一键下载脚本

# 4. 复制下载命令到终端执行
```

---

## 访问与加载

### 1. 访问文章
```bash
navigate_page -> <微信文章URL>
```

### 2. 触发懒加载（关键）
```javascript
// 滚动到页面底部
window.scrollTo(0, document.body.scrollHeight);
// 等待2秒让图片加载
await new Promise(resolve => setTimeout(resolve, 2000));
```

---

## 图片提取

### 提取脚本
```javascript
const images = Array.from(document.querySelectorAll('img'));
const articleImages = images
  .map(img => {
    const url = img.src || img['data-src'];
    const match = url.match(/imgIndex=(\d+)/);
    return {
      url: url,
      imgIndex: match ? match[1] : 'cover'
    };
  })
  .filter(img => img.url &&
    img.url.includes('mmbiz.qpic.cn') &&
    !img.url.includes('data:image/svg'));
```

### 图片位置确定
- ✅ 按 `imgIndex` 参数顺序确定位置
- ❌ 不要通过分析图片内容推断位置

### 过滤规则
| 保留 | 过滤 |
|------|------|
| 技术架构图、流程图 | 作者头像 |
| 界面截图、代码效果图 | 公众号二维码 |
| 数据图表 | 分享引导图 |
| 文章关键配图 | 宽度 < 200px 的小图 |

### 广告图片识别

**关键词列表**：
```javascript
const adKeywords = [
  // 交流群相关
  '进群后', '扫码加入', '欢迎加入', '交流群', '学习进步',
  // 知识星球/付费社群
  '知识星球', '请加入', 'AI工具实战派',
  // 推广引导
  '关注我们', '更多阅读', '推荐阅读', '长按识别',
  // 公众号推广
  '本文完整版详见', '文章精校版参见', '公众号：', '未来的回响'
];
```

**图片上下文检查**：
```javascript
// 检查图片前后文本是否包含广告关键词
function isAdImage(imgElement) {
  const beforeText = getPreviousText(imgElement, 100);
  const afterText = getNextText(imgElement, 100);
  const combined = beforeText + ' ' + afterText;

  return adKeywords.some(keyword => combined.includes(keyword));
}
```

---

## 视频提取 ⚠️

### 重要：`take_snapshot` 无法提取视频

**微信公众号文章中的视频 `<video>` 元素不会在 `take_snapshot` 中显示 URL！**

- ❌ **错误**：使用 `take_snapshot` → 只能看到 "播放视频" 按钮，看不到视频 URL
- ✅ **正确**：运行 `evaluate_script` 查找 `<video>` 元素

**原因**：`take_snapshot` 返回的是无障碍树（a11y tree），视频元素可能只显示为播放按钮。

### 提取流程

```javascript
// 1. 查找所有视频元素
const videos = document.querySelectorAll('#js_content video, video, iframe[src*="v.qq.com"]');
const result = [];

videos.forEach((v, i) => {
  if (v.tagName === 'VIDEO') {
    result.push({
      type: 'video',
      src: v.src || v.currentSrc,
      poster: v.poster,
      duration: v.duration
    });
  } else if (v.tagName === 'IFRAME') {
    result.push({
      type: 'iframe',
      src: v.src
    });
  }
});

JSON.stringify(result, null, 2);
```

### 添加到文章

在适当位置添加视频链接：

```markdown
> **演示视频**（时长 01:14）
>
> [安装使用演示视频](https://mpvideo.qpic.cn/...mp4)
```

### 验证清单

- [ ] 检查 `take_snapshot` 中是否有 "播放视频" 按钮
- [ ] 使用 `evaluate_script` 查找 `<video>` 元素
- [ ] 提取视频 URL 和元数据（时长、封面）
- [ ] 在文章中添加视频链接

---

## 广告内容剔除策略

### 常见广告位置模式

**文末推广区域**（常见结构）：
```
[正文结束]
---
更多关于...请持续关注后续分享！
本文完整版详见公众号：XXX
文章精校版参见知识星球：XXX

【限时开放】欢迎加入XXX交流群一起学习进步～
[二维码图片 - 交流群]

AI编程、AI运营、工具资料分享
请加入知识星球
[二维码图片 - 知识星球]

---
- **推荐阅读** -
```

### 剔除规则

| 内容类型 | 是否保留 | 说明 |
|---------|---------|------|
| 正文技术内容 | ✅ 保留 | 文章核心价值 |
| 数据来源说明 | ✅ 保留 | 如"数据来源：SkillsMP · 2026年1月19日" |
| 公众号名称（来源） | ✅ 保留 | 保留在元数据中，正文中低调呈现 |
| 二维码图片 | ❌ 剔除 | 交流群、知识星球等 |
| "推荐阅读" | ❌ 剔除 | 推广性质的链接列表 |
| "限时开放"引导 | ❌ 剔除 | 加群引导语 |
| "请持续关注" | ❌ 剔除 | 关注引导语 |

### 保留边界案例

**可以保留的边缘内容**：
- ✅ "本文数据截至2026年1月19日，Stars数会持续变动"（时效性说明）
- ✅ "类型 | 链接"等资源表格（技术资源）
- ✅ 作者版权声明（如非过度推广）

**必须剔除的内容**：
- ❌ "扫码加入交流群"
- ❌ "请加入知识星球"
- ❌ 二维码图片（交流群、知识星球、公众号）
- ❌ "- **推荐阅读** -" 及其后的链接列表

### 实施步骤

1. **识别广告区域**：
   - 从文末向前扫描
   - 查找关键词："欢迎加入"、"知识星球"、"推荐阅读"
   - 确定广告区域的起始位置

2. **移除广告内容**：
   - 删除二维码图片引用
   - 删除推广性文字
   - 截断到正文结束位置

3. **验证完整性**：
   - 确保正文内容完整
   - 检查是否误删了有用的资源链接
   - 保留必要的时效性说明

---

## 图片存储

### 优先级
1. **GitHub 图床** → `cdn.jsdelivr.net/gh/user/repo/path`
2. **远程链接** → 无防盗链的直接引用
3. **本地存储** → 降级方案

### 下载命令
```bash
curl -s \
  -H "Referer: https://mp.weixin.qq.com/" \
  -H "User-Agent: Mozilla/5.0" \
  "$img_url" \
  -o "general/article-slug/images/image_${index}.jpg"
```

### 命名规则
- ✅ 描述性：`stripe-ceo-evaluation.png`
- ✅ Media ID：按 imgIndex 命名
- ❌ 纯编号：`image-01.jpg`

---

## 常见问题

### 问题1：图片不完整
- **原因**：未触发懒加载
- **解决**：滚动到底部后再提取

### 问题2：占位符 SVG
- **原因**：图片未加载
- **解决**：过滤 `data:image/svg`

### 问题3：图片位置错乱
- **原因**：DOM 顺序与显示顺序不一致
- **解决**：按 `imgIndex` 参数排序
