# 微信公众号全文提取最佳实践

## 提取流程

```
访问文章 → 滚动触发懒加载 → 提取文本 → 提取图片 → 验证完整性
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
```javascript
const adKeywords = [
  '进群后', '关注我们', '扫码加入',
  '更多阅读', '推荐阅读', '长按识别'
];
// 检查图片前后文本是否包含这些关键词
```

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
