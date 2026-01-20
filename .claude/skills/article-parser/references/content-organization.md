# 4. 检查格式
echo "🎨 格式检查："
grep -c '^```$' "$ARTICLE_FILE" | awk '{if ($1 % 2 == 0) print "  ✅ 代码块闭合"; else print "  ❌ 代码块未闭合"}'

echo "✅ 验证完成"
```

#### 使用场景

**场景1：提取完成后自动验证**
```javascript
// 完成提取后立即验证
await extractArticleContent(url);
const validationResult = await validateArticle(content);

if (validationResult.hasErrors) {
  console.log('发现错误，自动修复...');
  await autoFix(validationResult.issues);
}
```

**场景2：用户反馈问题时重新验证**
```javascript
// 用户说"第3节的图片漏了"
await scrollToSection(3);
const screenshot = await takeScreenshot();
if (screenshot.containsImage()) {
  await downloadImage(3);
  await updateMarkdown();
}
```

**场景3：批量提取时抽检**
```bash
# 随机抽检 10% 的文章
for article in $(find . -name "*.md" | shuf | head -n 5); do
  ./validate_article.sh "$article"
done
```

#### 验证最佳实践

✅ **应该做的**：
