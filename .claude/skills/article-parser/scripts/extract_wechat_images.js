/**
 * 微信公众号图片提取脚本（增强版）
 *
 * 功能：
 * 1. 滚动页面触发懒加载
 * 2. 提取所有图片 URL（包括 data-src 属性）
 * 3. 提取每张图片的上下文（context_before 和 context_after）
 * 4. 按 imgIndex 排序
 * 5. 输出可下载的图片列表
 * 6. 生成 image-mapping.json（用于验证图片位置）
 *
 * 使用方法：
 * 1. 在 Chrome DevTools 中打开微信公众号文章
 * 2. 在 Console 中运行此脚本
 * 3. 复制输出的图片 URL 列表和 image-mapping.json
 * 4. 将 image-mapping.json 保存到 .cache/images/{article-slug}/
 */

(function() {
  console.log('🔍 开始提取微信公众号图片...\n');

  // 1. 滚动到页面底部触发懒加载
  console.log('⬇️  滚动到页面底部触发懒加载...');
  window.scrollTo(0, document.body.scrollHeight);

  // 广告图片关键词（用于识别和过滤广告图片）
  const adKeywords = [
    // 交流群相关
    '进群后', '扫码加入', '欢迎加入', '交流群', '学习进步',
    // 知识星球/付费社群
    '知识星球', '请加入', 'AI工具实战派',
    // 推广引导
    '关注我们', '更多阅读', '推荐阅读', '长按识别',
    // 公众号推广
    '本文完整版详见', '文章精校版参见', '公众号：',
    // 常见广告词
    '限时开放', '请持续关注', '未来的回响'
  ];

  // 提取图片前后的文本（用于定位和广告识别）
  function getImageContext(imgElement, maxChars = 150) {
    function getText(node, accumulated = '') {
      if (!node || accumulated.length > maxChars) return accumulated;

      if (node.nodeType === Node.TEXT_NODE) {
        return accumulated + node.textContent.trim();
      }

      if (node.nodeType === Node.ELEMENT_NODE) {
        // 跳过图片、视频等元素
        if (['IMG', 'VIDEO', 'IFRAME', 'SCRIPT', 'STYLE'].includes(node.tagName)) {
          return accumulated;
        }
        // 遍历子节点
        for (let child of node.childNodes) {
          accumulated = getText(child, accumulated);
          if (accumulated.length >= maxChars) break;
        }
      }
      return accumulated;
    }

    // 获取图片之前的文本
    let beforeText = '';
    let current = imgElement.previousSibling;
    while (current && beforeText.length < maxChars) {
      beforeText = getText(current) + beforeText;
      current = current.previousSibling;
    }
    beforeText = beforeText.trim().slice(-maxChars);

    // 获取图片之后的文本
    let afterText = '';
    current = imgElement.nextSibling;
    while (current && afterText.length < maxChars) {
      afterText += getText(current);
      current = current.nextSibling;
      if (afterText.length >= maxChars) break;
    }
    afterText = afterText.trim().slice(0, maxChars);

    return { before: beforeText, after: afterText };
  }

  // 检查是否为广告图片
  function isAdImage(context) {
    const combined = context.before + ' ' + context.after;
    return adKeywords.some(keyword => combined.includes(keyword));
  }

  // 2. 等待图片加载
  setTimeout(() => {
    console.log('⏳ 等待图片加载完成...\n');

    // 3. 提取所有图片
    const allImages = Array.from(document.querySelectorAll('img'));
    const articleUrl = window.location.href;
    const extractionDate = new Date().toISOString().split('T')[0];

    const articleImages = allImages
      .map((img, domIndex) => {
        // 优先使用 data-src（微信懒加载），其次使用 src
        const url = img.dataset?.src || img.src;

        // 从 URL 或 data-index 属性获取图片索引
        const indexMatch = url.match(/imgIndex=(\d+)/);
        const dataIndex = img.getAttribute('data-index');
        const imgIndex = indexMatch?.[1] || dataIndex || domIndex;

        // 提取图片上下文
        const context = getImageContext(img);
        const isAd = isAdImage(context);

        return {
          url: url,
          imgIndex: parseInt(imgIndex),
          width: img.width || img.getAttribute('data-width') || 0,
          height: img.height || img.getAttribute('data-height') || 0,
          className: img.className,
          isPlaceholder: url.includes('data:image/svg'),
          isWeixinImage: url.includes('mmbiz.qpic.cn'),
          context: context,
          isAd: isAd,
          adReason: isAd ? '上下文包含广告关键词' : null
        };
      })
      .filter(img => {
        // 过滤掉：
        // 1. 占位符 SVG
        // 2. 空URL
        // 3. 非微信图片（如广告、头像等，可根据需要调整）
        // 4. 广告图片（上下文包含广告关键词）
        return img.url &&
               !img.isPlaceholder &&
               img.isWeixinImage &&
               img.width > 200 && // 只保留宽度 > 200px 的图片
               !img.isAd; // 过滤广告图片
      })
      .sort((a, b) => a.imgIndex - b.imgIndex);

    // 4. 输出结果
    if (articleImages.length === 0) {
      console.warn('⚠️  未找到任何文章图片！');
      console.log('💡 提示：可能是图片还在加载中，请稍后重新运行此脚本');
      return;
    }

    console.log(`✅ 找到 ${articleImages.length} 张图片：\n`);

    // 输出图片列表（用于下载）
    console.log('========== 图片信息 ==========\n');
    articleImages.forEach((img, index) => {
      console.log(`图片 ${index + 1} (imgIndex=${img.imgIndex}):`);
      console.log(`  URL: ${img.url}`);
      console.log(`  尺寸: ${img.width} x ${img.height}`);
      console.log(`  前文: ${img.context.before.slice(0, 80)}...`);
      console.log(`  后文: ${img.context.after.slice(0, 80)}...`);
      console.log('');
    });

    // 输出下载命令
    console.log('========== 下载命令 ==========\n');
    console.log('# 方法1：逐个下载（推荐，可以重命名）');
    articleImages.forEach((img, index) => {
      const filename = `image_${String(index + 1).padStart(2, '0')}.png`;
      console.log(`curl -s -L "${img.url}" -o "${filename}"`);
    });

    console.log('\n# 方法2：批量下载（使用图片序号）');
    articleImages.forEach(img => {
      const filename = `image_${String(img.imgIndex).padStart(2, '0')}.png`;
      console.log(`curl -s -L "${img.url}" -o "${filename}"`);
    });

    // 输出 JSON 格式（用于程序处理）
    console.log('\n========== JSON 格式 ==========\n');
    console.log(JSON.stringify(articleImages.map((img, index) => ({
      index: index + 1,
      imgIndex: img.imgIndex,
      url: img.url,
      filename: `image_${String(index + 1).padStart(2, '0')}.png`,
      width: img.width,
      height: img.height,
      context_before: img.context.before,
      context_after: img.context.after
    })), null, 2));

    // 输出 Bash 脚本（一键下载所有图片）
    console.log('\n========== 一键下载脚本 ==========\n');
    console.log('#!/bin/bash');
    console.log('# 保存为 download_images.sh 后运行');
    console.log('mkdir -p images');
    console.log('');
    articleImages.forEach((img, index) => {
      const filename = `images/image_${String(index + 1).padStart(2, '0')}.png`;
      console.log(`curl -s -L "${img.url}" -o "${filename}"`);
      console.log(`echo "✓ 下载完成: ${filename}"`);
    });
    console.log('\necho "✓ 所有图片下载完成！"');

    // ⚠️ 重要：生成 image-mapping.json
    console.log('\n========== image-mapping.json ==========\n');
    console.log('⚠️  将以下 JSON 保存到 .cache/images/{article-slug}/image-mapping.json');
    console.log('⚠️  这是验证图片位置的关键文件，不要跳过！\n');

    const imageMapping = {
      article_url: articleUrl,
      extraction_date: extractionDate,
      images: articleImages.map((img, index) => ({
        index: index + 1,
        original_url: img.url,
        filename: `image_${String(index + 1).padStart(2, '0')}.png`,
        description: `图片 ${index + 1}`,
        context_before: img.context.before,
        context_after: img.context.after,
        placement: `根据 context_before: "${img.context.before.slice(0, 50)}..." 定位`
      }))
    };

    console.log(JSON.stringify(imageMapping, null, 2));

    // 统计信息
    console.log('\n========== 统计信息 ==========\n');
    console.log(`总图片数: ${articleImages.length}`);
    console.log(`imgIndex 范围: ${articleImages[0].imgIndex} - ${articleImages[articleImages.length - 1].imgIndex}`);
    console.log(`总尺寸估算: ${(articleImages.reduce((sum, img) => sum + (img.width * img.height), 0) / 1000000).toFixed(2)} MP`);
    console.log(`文章 URL: ${articleUrl}`);
    console.log(`提取日期: ${extractionDate}`);

    // 检查是否有遗漏的图片
    const expectedCount = articleImages[articleImages.length - 1].imgIndex + 1;
    if (expectedCount !== articleImages.length) {
      console.warn(`\n⚠️  警告：imgIndex 不连续！`);
      console.warn(`   期望 ${expectedCount} 张图片，实际找到 ${articleImages.length} 张`);
      console.warn(`   可能原因：部分图片未加载或被过滤（包括广告图片）`);
    }

    console.log('\n✨ 提取完成！\n');
    console.log('💡 提示：');
    console.log('   1. 复制 image-mapping.json 并保存到 .cache/images/{article-slug}/');
    console.log('   2. 下载图片后，根据 context_before 精确定位图片位置');
    console.log('   3. 广告图片已自动过滤，如有误判请手动调整\n');

  }, 2500); // 等待 2.5 秒让图片加载

})();
