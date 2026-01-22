---
name: yt-dlp
description: "Comprehensive video and audio downloader supporting 1000+ platforms including YouTube, Twitter, TikTok, Instagram, 小红书, Vimeo, Twitch, and more. Use when you need to download videos from websites, extract audio from videos (MP3, M4A, FLAC), download subtitles in multiple languages, download entire playlists, get video metadata without downloading, or handle age-restricted or authenticated content. This skill provides Python scripts for common tasks and references for advanced options."
---

# yt-dlp

## Overview

yt-dlp is a powerful command-line tool for downloading videos and audio from the web. This skill provides convenient Python scripts and reference documentation for common download tasks.

**When to use this skill:**
- User provides a video/audio URL and asks to download, extract, or process it
- User mentions YouTube, Twitter, TikTok, 小红书, or other supported platforms
- User wants subtitles, audio extraction, or playlist downloads
- User needs video metadata or information without downloading

**When NOT to use:**
- User wants to analyze, transcribe, or process already-downloaded media files
- User asks about video editing, conversion, or manipulation (use video/audio tools instead)

## Quick Start

### Check Platform Support

First, verify the platform is supported:

```bash
yt-dlp --simulate "URL"
```

For a list of all supported platforms:

```bash
yt-dlp --list-extractors
```

### Download a Video

Use the `download_video.py` script:

```bash
cd scripts
python download_video.py "URL" -o output_dir -q best -f mp4
```

Parameters:
- `-o OUTPUT_DIR`: Output directory (default: current directory)
- `-q QUALITY`: Video quality (default: best)
- `-f FORMAT`: Preferred format (default: mp4)
- `-s LANGS`: Subtitle languages (comma-separated, e.g., en,zh)
- `--embed-subs`: Embed subtitles in video
- `--no-playlist`: Download single video from playlist

### Extract Audio

Use the `extract_audio.py` script:

```bash
cd scripts
python extract_audio.py "URL" -o output_dir -f mp3 -q 192
```

Parameters:
- `-o OUTPUT_DIR`: Output directory (default: current directory)
- `-f FORMAT`: Audio format (mp3, m4a, flac, wav)
- `-q QUALITY`: Audio quality in kbps (default: 192)
- `-t TEMPLATE`: Custom output filename template

### Download Subtitles

Use the `download_subs.py` script:

```bash
cd scripts
python download_subs.py "URL" -o output_dir -l en,zh -f srt
```

Parameters:
- `-o OUTPUT_DIR`: Output directory (default: current directory)
- `-l LANGUAGES`: Language codes (default: en)
- `-f FORMAT`: Subtitle format (srt, vtt, ass)
- `--auto-subs`: Download auto-generated subtitles
- `--embed`: Embed subtitles in video

### Download Playlist

Use the `download_playlist.py` script:

```bash
cd scripts
python download_playlist.py "URL" -o output_dir --start 1 --end 10
```

Parameters:
- `-o OUTPUT_DIR`: Output directory (default: current directory)
- `--start N`: Start index (1-based, default: 1)
- `--end N`: End index (exclusive)
- `--reverse`: Download in reverse order
- `-q QUALITY`: Video quality (default: best)
- `-f FORMAT`: Preferred format (default: mp4)
- `-c N`: Concurrent fragments for HLS/DASH

## Common Workflows

### 1. Download YouTube Video with Subtitles

```bash
cd scripts
python download_video.py "https://youtube.com/watch?v=VIDEO_ID" \
  -o ./videos \
  -s en,zh \
  --embed-subs
```

### 2. Extract Audio as High-Quality MP3

```bash
cd scripts
python extract_audio.py "URL" \
  -o ./audio \
  -f mp3 \
  -q 320
```

### 3. Download Entire Playlist

```bash
cd scripts
python download_playlist.py "https://youtube.com/playlist?list=PLAYLIST_ID" \
  -o ./playlist
```

### 4. Download Specific Playlist Range

```bash
cd scripts
python download_playlist.py "URL" \
  -o ./videos \
  --start 5 \
  --end 15
```

### 5. Get Video Metadata Without Downloading

```bash
yt-dlp --skip-download --write-info-json "URL"
```

Or as JSON:

```bash
yt-dlp -j "URL"
```

## Platform-Specific Notes

### 小红书 (Xiaohongshu)

```bash
cd scripts
python download_video.py "https://www.xiaohongshu.com/explore/VIDEO_ID" \
  -o ./xiaohongshu
```

### Twitter/X

```bash
cd scripts
python download_video.py "https://twitter.com/user/status/TWEET_ID" \
  -o ./twitter
```

### YouTube Shorts

```bash
cd scripts
python download_video.py "https://youtube.com/shorts/VIDEO_ID" \
  -o ./shorts
```

### TikTok (Without Watermark)

```bash
yt-dlp -o "%(title)s.%(ext)s" "URL"
```

## Authentication

For age-restricted or paid content, use browser cookies:

```bash
# Export cookies using browser extension, then:
yt-dlp --cookies cookies.txt "URL"
```

Or use cookies from browser directly:

```bash
yt-dlp --cookies-from-browser chrome "URL"
```

Supported browsers: chrome, firefox, safari, edge, opera, brave

## Output Templates

Control output filenames with templates:

| Template | Description |
|----------|-------------|
| `%(title)s.%(ext)s` | Video title with extension |
| `%(id)s.%(ext)s` | Video ID with extension |
| `%(uploader)s-%(title)s.%(ext)s` | Uploader and title |
| `%(upload_date)s-%(title)s.%(ext)s` | Date and title (YYYYMMDD) |

Example:

```bash
yt-dlp -o "%(uploader)s/%(upload_date)s-%(title)s.%(ext)s" "URL"
```

## Quality Selection

Use the `--list-formats` option to see available formats:

```bash
yt-dlp --list-formats "URL"
```

Common quality selectors:

| Selector | Description |
|----------|-------------|
| `best` | Best quality (single file) |
| `worst` | Worst quality |
| `bestvideo+bestaudio` | Best video and audio (merges if needed) |
| `height<=720` | Resolution up to 720p |
| `filesize<100M` | Files smaller than 100MB |

Example:

```bash
yt-dlp -f "height<=1080" "URL"
```

## References

### [platforms.md](references/platforms.md)
Complete list of supported platforms, including:
- Video platforms (YouTube, Vimeo, Dailymotion)
- Social media (Twitter, TikTok, Instagram, Reddit, 小红书)
- Educational platforms (Coursera, edX, Udemy)
- Live streaming (Twitch, YouTube Live)

### [common-options.md](references/common-options.md)
Comprehensive reference for yt-dlp options:
- Quality selection
- Output templates
- Playlist handling
- Subtitle options
- Audio extraction
- Authentication
- Advanced features

## Troubleshooting

### Video Not Downloading

1. Check platform support: `yt-dlp --simulate "URL"`
2. Update yt-dlp: `pip install -U yt-dlp`
3. Check authentication requirements
4. Try with cookies: `--cookies-from-browser chrome`

### Format Not Available

1. List available formats: `yt-dlp --list-formats "URL"`
2. Use format selector: `yt-dlp -f "bestvideo+bestaudio" "URL"`
3. Specify merge format: `yt-dlp --merge-output-format mp4 "URL"`

### Subtitle Issues

1. List available subtitles: `yt-dlp --list-subs "URL"`
2. Try auto-generated: `--write-auto-subs`
3. Specify language: `--sub-lang en,zh`

## Scripts Summary

| Script | Purpose |
|--------|---------|
| `download_video.py` | Download videos with quality/format control |
| `extract_audio.py` | Extract audio from videos |
| `download_subs.py` | Download subtitles separately |
| `download_playlist.py` | Download entire playlists |
