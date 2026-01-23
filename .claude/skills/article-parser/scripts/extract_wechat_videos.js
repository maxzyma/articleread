/**
 * 微信公众号视频提取脚本
 *
 * 使用方法：
 * 1. 在 Chrome DevTools 中打开微信文章
 * 2. 在 Console 中粘贴并运行此脚本
 * 3. 脚本会输出视频信息，包括 URL、时长、封面
 */

(function() {
  console.log('🔍 开始提取视频...');

  // 查找所有视频元素
  const videos = document.querySelectorAll('#js_content video, video, iframe[src*="v.qq.com"]');
  const result = [];

  videos.forEach((v, i) => {
    if (v.tagName === 'VIDEO') {
      result.push({
        index: i,
        type: 'video',
        src: v.src || v.currentSrc,
        poster: v.poster,
        duration: v.duration ? `${Math.floor(v.duration / 60)}:${String(Math.floor(v.duration % 60)).padStart(2, '0')}` : 'unknown'
      });
    } else if (v.tagName === 'IFRAME') {
      result.push({
        index: i,
        type: 'iframe',
        src: v.src
      });
    }
  });

  if (result.length === 0) {
    console.log('✅ 未发现视频');
    return;
  }

  console.log(`✅ 发现 ${result.length} 个视频：`);
  console.table(result);

  // 输出 Markdown 格式的视频链接
  console.log('\n📝 Markdown 格式：');
  result.forEach(video => {
    if (video.type === 'video') {
      const duration = video.duration !== 'unknown' ? `（时长 ${video.duration}）` : '';
      console.log(`> **演示视频**${duration}\n>\n> [视频](${video.src})\n`);
    }
  });

  // 查找视频周围的文本（上下文）
  console.log('\n📍 视频上下文：');
  result.forEach((video, idx) => {
    if (video.type === 'video') {
      const videoEl = document.querySelectorAll('video')[idx];
      let beforeText = '';

      // 向前查找文本
      let parent = videoEl.parentElement;
      let steps = 0;
      while (parent && steps < 10) {
        const prev = parent.previousElementSibling;
        if (prev && prev.textContent.trim()) {
          beforeText = prev.textContent.trim();
          break;
        }
        parent = prev;
        steps++;
      }

      console.log(`视频 ${idx + 1}: ${beforeText.slice(0, 80)}...`);
    }
  });

  return result;
})();
