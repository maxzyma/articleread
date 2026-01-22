# Supported Platforms

yt-dlp supports thousands of websites. Below are commonly used platforms:

## Video Platforms

| Platform | URL Pattern | Notes |
|----------|-------------|-------|
| YouTube | `youtube.com/watch?v=...` | Full support including playlists, subtitles |
| YouTube Shorts | `youtube.com/shorts/...` | Automatic extraction |
| Vimeo | `vimeo.com/...` | Various quality levels |
| Dailymotion | `dailymotion.com/video/...` | Standard support |
| Twitch | `twitch.tv/videos/...` | VODs and clips |

## Social Media

| Platform | URL Pattern | Notes |
|----------|-------------|-------|
| Twitter/X | `twitter.com/.../status/...` | Videos and GIFs |
| TikTok | `tiktok.com/@user/video/...` | Without watermark recommended |
| Instagram | `instagram.com/p/...` | Requires authentication for some content |
| Facebook | `facebook.com/.../videos/...` | May require authentication |
| Reddit | `reddit.com/r/.../comments/...` | Videos and GIFs |
| 小红书 (Xiaohongshu) | `xiaohongshu.com/...` | Experimental support |

## Educational & Professional

| Platform | URL Pattern | Notes |
|----------|-------------|-------|
| Coursera | `coursera.org/learn/...` | Requires authentication |
| edX | `edx.org/course/...` | Requires authentication |
| Udemy | `udemy.com/course/...` | Requires authentication |
| LinkedIn Learning | `linkedin.com/learning/...` | Requires authentication |
| Khan Academy | `khanacademy.org/...` | Full support |

## Live Streaming

| Platform | URL Pattern | Notes |
|----------|-------------|-------|
| Twitch | `twitch.tv/...` | Live streams (use `--live-from-start`) |
| YouTube Live | `youtube.com/watch?v=...` | Live streams |
| Bilibili | `bilibili.com/video/...` | Some content requires region |

## Checking Platform Support

To check if a URL is supported:

```bash
yt-dlp --list-extractors | grep platform_name
```

To test a URL without downloading:

```bash
yt-dlp --simulate "URL"
```

## Authentication Required

Some platforms require authentication (cookies, login):

- **Paid course platforms** (Coursera, edX, Udemy)
- **Private/age-restricted content**
- **Region-locked content**

Use browser cookies for authentication:

```bash
yt-dlp --cookies cookies.txt "URL"
```

Export cookies from browser using browser extensions like "Get cookies.txt LOCALLY".
