/**
 * 微信公众号图片提取脚本
 *
 * 功能：
 * 1. 滚动页面触发懒加载
 * 2. 提取所有图片 URL（包括 data-src 属性）
 * 3. 按 imgIndex 排序
 * 4. 输出可下载的图片列表
 *
 * 使用方法：
 * 1. 在 Chrome DevTools 中打开微信公众号文章
 * 2. 在 Console 中运行此脚本
 * 3. 复制输出的图片 URL 列表
 * 4. 使用 curl 批量下载
 */

(function() {
  console.log('🔍 开始提取微信公众号图片...\n');

  // 1. 滚动到页面底部触发懒加载
  console.log('⬇️  滚动到页面底部触发懒加载...');
  window.scrollTo(0, document.body.scrollHeight);

  // 2. 等待图片加载
  setTimeout(() => {
    console.log('⏳ 等待图片加载完成...\n');

    // 3. 提取所有图片
    const allImages = Array.from(document.querySelectorAll('img'));

    const articleImages = allImages
      .map((img, domIndex) => {
        // 优先使用 data-src（微信懒加载），其次使用 src
        const url = img.dataset?.src || img.src;

        // 从 URL 或 data-index 属性获取图片索引
        const indexMatch = url.match(/imgIndex=(\d+)/);
        const dataIndex = img.getAttribute('data-index');
        const imgIndex = indexMatch?.[1] || dataIndex || domIndex;

        return {
          url: url,
          imgIndex: parseInt(imgIndex),
          width: img.width || img.getAttribute('data-width') || 0,
          height: img.height || img.getAttribute('data-height') || 0,
          className: img.className,
          isPlaceholder: url.includes('data:image/svg'),
          isWeixinImage: url.includes('mmbiz.qpic.cn')
        };
      })
      .filter(img => {
        // 过滤掉：
        // 1. 占位符 SVG
        // 2. 空URL
        // 3. 非微信图片（如广告、头像等，可根据需要调整）
        return img.url &&
               !img.isPlaceholder &&
               img.isWeixinImage &&
               img.width > 200; // 只保留宽度 > 200px 的图片
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
      height: img.height
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

    // 统计信息
    console.log('\n========== 统计信息 ==========\n');
    console.log(`总图片数: ${articleImages.length}`);
    console.log(`imgIndex 范围: ${articleImages[0].imgIndex} - ${articleImages[articleImages.length - 1].imgIndex}`);
    console.log(`总尺寸估算: ${(articleImages.reduce((sum, img) => sum + (img.width * img.height), 0) / 1000000).toFixed(2)} MP`);

    // 检查是否有遗漏的图片
    const expectedCount = articleImages[articleImages.length - 1].imgIndex + 1;
    if (expectedCount !== articleImages.length) {
      console.warn(`\n⚠️  警告：imgIndex 不连续！`);
      console.warn(`   期望 ${expectedCount} 张图片，实际找到 ${articleImages.length} 张`);
      console.warn(`   可能原因：部分图片未加载或被过滤`);
    }

    console.log('\n✨ 提取完成！\n');

  }, 2500); // 等待 2.5 秒让图片加载

})();
