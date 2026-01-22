# Common Options Reference

## Quality Selection

| Option | Description | Example |
|--------|-------------|---------|
| `-f best` | Best quality (single file) | `yt-dlp -f best "URL"` |
| `-f worst` | Worst quality | `yt-dlp -f worst "URL"` |
| `-f bestvideo+bestaudio` | Best video + audio (may merge) | `yt-dlp -f "bestvideo+bestaudio" "URL"` |
| `-f 720p` | Specific resolution | `yt-dlp -f "height<=720" "URL"` |
| `--format-sort` | Sort by preferences | `yt-dlp --format-sort "+res" "URL"` |

## Output Options

| Option | Description | Example |
|--------|-------------|---------|
| `-o TEMPLATE` | Output filename template | `yt-dlp -o "%(title)s.%(ext)s" "URL"` |
| `--output-na-placeholder` | Placeholder for missing metadata | `yt-dlp --output-na-placeholder "NA" "URL"` |
| `--restrict-filenames` | Safe filenames (ASCII only) | `yt-dlp --restrict-filenames "URL"` |
| `-a FILE` | Batch download from file | `yt-dlp -a urls.txt` |

### Output Template Fields

| Field | Description |
|-------|-------------|
| `%(title)s` | Video title |
| `%(id)s` | Video ID |
| `%(ext)s` | File extension |
| `%(uploader)s` | Uploader name |
| `%(duration)s` | Duration in seconds |
| `%(view_count)s` | View count |
| `%(upload_date)s` | Upload date (YYYYMMDD) |
| `%(playlist_index)s` | Position in playlist |

## Playlist Options

| Option | Description | Example |
|--------|-------------|---------|
| `--no-playlist` | Download single video only | `yt-dlp --no-playlist "URL"` |
| `--playlist-items RANGE` | Specific items (1-5,3,7) | `yt-dlp --playlist-items 1-5 "URL"` |
| `--playlist-reverse` | Reverse order | `yt-dlp --playlist-reverse "URL"` |
| `--playlist-end N` | Stop at N | `yt-dlp --playlist-end 10 "URL"` |

## Subtitle Options

| Option | Description | Example |
|--------|-------------|---------|
| `--write-subs` | Download subtitles | `yt-dlp --write-subs --sub-lang en "URL"` |
| `--write-auto-subs` | Auto-generated subtitles | `yt-dlp --write-auto-subs "URL"` |
| `--sub-lang LANGS` | Language codes | `yt-dlp --sub-lang en,zh "URL"` |
| `--sub-format FORMAT` | Format (srt/vtt/ass) | `yt-dlp --sub-format srt "URL"` |
| `--embed-subs` | Embed in video | `yt-dlp --embed-subs "URL"` |
| `--list-subs` | List available subs | `yt-dlp --list-subs "URL"` |

## Audio Extraction

| Option | Description | Example |
|--------|-------------|---------|
| `-x` | Extract audio only | `yt-dlp -x "URL"` |
| `--audio-format FORMAT` | Audio format | `yt-dlp -x --audio-format mp3 "URL"` |
| `--audio-quality QUALITY` | Quality (kbps) | `yt-dlp -x --audio-quality 320 "URL"` |

## Download Behavior

| Option | Description | Example |
|--------|-------------|---------|
| `--no-overwrites` | Skip existing files | `yt-dlp --no-overwrites "URL"` |
| `--continue` | Continue incomplete downloads | `yt-dlp --continue "URL"` |
| `--concurrent-fragments N` | Concurrent fragments | `yt-dlp --concurrent-fragments 4 "URL"` |
| `--limit-rate RATE` | Rate limit (e.g., 50M) | `yt-dlp --limit-rate 50M "URL"` |
| `--retry-times N` | Retry attempts | `yt-dlp --retry-times 3 "URL"` |

## Information & Metadata

| Option | Description | Example |
|--------|-------------|---------|
| `--list-formats` | List available formats | `yt-dlp --list-formats "URL"` |
| `--list-thumbnails` | List thumbnails | `yt-dlp --list-thumbnails "URL"` |
| `--write-info-json` | Write video metadata | `yt-dlp --write-info-json "URL"` |
| `--write-description` | Write description | `yt-dlp --write-description "URL"` |
| `--write-thumbnail` | Write thumbnail | `yt-dlp --write-thumbnail "URL"` |
| `--skip-download` | Get metadata only | `yt-dlp --skip-download "URL"` |
| `-j` | Output JSON metadata | `yt-dlp -j "URL"` |

## Authentication

| Option | Description | Example |
|--------|-------------|---------|
| `-u USER` | Username | `yt-dlp -u user -p pass "URL"` |
| `-p PASS` | Password | `yt-dlp -u user -p pass "URL"` |
| `--cookies FILE` | Cookies file | `yt-dlp --cookies cookies.txt "URL"` |
| `--cookies-from-browser BROWSER` | Use browser cookies | `yt-dlp --cookies-from-browser chrome "URL"` |

## Advanced

| Option | Description | Example |
|--------|-------------|---------|
| `--concat-playlist` | Concatenate playlist items | `yt-dlp --concat-playlist "URL"` |
| `--merge-output-format FORMAT` | Merge to specific format | `yt-dlp --merge-output-format mp4 "URL"` |
| `--postprocessor-args ARGS` | PP arguments | `yt-dlp --postprocessor-args "ffmpeg:-threads 4" "URL"` |
| `--exec CMD` | Run command after download | `yt-dlp --exec "mv {} /videos/" "URL"` |
| `--print FILE` | Print downloaded file path | `yt-dlp --print "%(filename)s" "URL"` |

## Live Streams

| Option | Description | Example |
|--------|-------------|---------|
| `--live-from-start` | Download from start | `yt-dlp --live-from-start "URL"` |
| `--wait-for-video MIN` | Wait if not started | `yt-dlp --wait-for-video 10 "URL"` |
| `--hls-use-mpegts` | Use MPEG-TS format | `yt-dlp --hls-use-mpegts "URL"` |
