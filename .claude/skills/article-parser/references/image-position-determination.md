**微信公众号图片位置确定的最佳实践（2026-01-20 更新）**：

根据实战经验，总结了以下关键原则和命名规范：

**核心原则**：

> 图片的位置由它们在文章中出现的顺序决定，而不是由图片内容决定。
> 图片的名称应该描述其内容，而非使用数字索引。

**❌ 旧方式（不推荐）**：
```
img-0.gif, img-1.jpg, img-2.jpg, img-3.jpg, img-4.jpg
```
- 顺序调整时容易混淆
- 插入/删除图片需要重新编号
- 文件名无语义，无法从名称知道内容

**✅ 推荐方式：描述性命名**：
```
stripe-ceo-evaluation.png      # Stripe CEO 评价
solid-react-migration.png       # Solid→React 迁移
agent-testing-demo.png          # Agent 测试动图
failure-modes-summary.png       # 四种失败模式
michael-truell-response.png     # Michael Truell 回应
```
- 文件名直接对应内容含义
- 顺序调整不影响文件语义
- 更清晰、更易维护

**命名最佳实践**：

1. **短格式**（3-5个词）
   ```
   stripe-ceo.png, migration-solid-react.png
   ```

2. **全部小写**，空格用连字符替换
   ```
   agent-testing-demo.png（不是 Agent Testing Demo.png）
   ```

3. **避免特殊字符**，只使用字母、数字、连字符
   ```
   solid-react-migration.png（不是 solid_react@migration.png）
   ```

4. **保持简洁但有意义**
   ```
   video-render-optimization.png（不是 long-video-rendering-module-optimization-with-rust-language-performance-improvement.png）
   ```

5. **必要时添加序号区分**
   ```
   comparison-chart-1.png, comparison-chart-2.png
   ```

**工作流程**：

```bash
# 1. 提取图片 URL 和 imgIndex
js: getImagesWithIndex()

# 2. 查看网页快照，确定每张图片的上下文
take_snapshot → 找到每张图片前后的文本

# 3. 根据上下文生成描述性名称
# 示例：图片前后文本提到 "Stripe CEO 对这项研究的评价"
# 生成名称：stripe-ceo-evaluation.png

# 4. 下载并命名图片
curl -H "Referer: https://mp.weixin.qq.com/" \
  "url_with_imgIndex=2" -o stripe-ceo-evaluation.png

# 5. 在 Markdown 中按正确位置引用
![Stripe CEO 对这项研究的评价](./images/stripe-ceo-evaluation.png)
```

**图片位置确定方法**：

| 方法 | 步骤 | 准确率 | 推荐 |
|------|------|--------|------|
| ✅ 网页结构分析 | 1. 提取 imgIndex<br>2. 查看网页快照<br>3. 按文本位置确定 | ~100% | ✅ 强烈推荐 |
| ❌ 图片内容分析 | 1. OCR 分析每张图片<br>2. 理解图片内容<br>3. 推断章节对应关系 | ~70% | ❌ 不推荐 |

**广告图片过滤**：

在确定图片位置前，先过滤掉非正文图片：

```javascript
// 过滤规则
const isAdImage = (img, context) => {
    // 1. 尺寸过小（可能是二维码/Logo）
    if (img.naturalWidth < 100) return true;

    // 2. 上下文包含广告关键词
    const adKeywords = ['进群后', '更多阅读', '推荐阅读', '扫码关注'];
    if (adKeywords.some(k => context.includes(k))) return true;

    return false;
};
```

**快速参考：命名模板**

| 场景 | 命名示例 |
|------|----------|
| 人物评价/回应 | `{name}-response.png`, `{name}-evaluation.png` |
| 代码迁移 | `{from}-to-{to}-migration.png` |
| 性能对比 | `{metric}-comparison.png`, `{before}-vs-{after}.png` |
| 架构图 | system-architecture.png, component-diagram.png |
| 流程图 | workflow-diagram.png, process-flow.png |
| 测试截图 | testing-demo.png, verification-result.png |
| 失败模式 | failure-modes.png, error-summary.png |
