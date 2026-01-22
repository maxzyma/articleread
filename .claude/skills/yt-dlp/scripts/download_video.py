#!/usr/bin/env python3
"""
yt-dlp Video Downloader Script

Downloads videos from various platforms using yt-dlp.
Supports quality selection, format preferences, and output customization.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def download_video(
    url: str,
    output_dir: str = ".",
    quality: str = "best",
    format_pref: str = "mp4",
    subtitle_langs: str = None,
    embed_subs: bool = False,
    no_playlist: bool = False,
) -> str:
    """
    Download a video using yt-dlp.

    Args:
        url: Video URL
        output_dir: Output directory path
        quality: Video quality (best/worst/bestvideo+bestaudio/etc.)
        format_pref: Preferred format (mp4/webm/mkv/etc.)
        subtitle_langs: Comma-separated subtitle languages (e.g., "en,zh")
        embed_subs: Whether to embed subtitles in video
        no_playlist: If True, download only single video from playlist

    Returns:
        Path to downloaded file
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Build yt-dlp command
    cmd = ["yt-dlp"]

    # Format selection
    if format_pref:
        cmd.extend(["-f", f"{quality}[ext={format_pref}]/{quality}"])

    # Output template
    cmd.extend(["-o", str(output_path / "%(title)s.%(ext)s")])

    # Subtitles
    if subtitle_langs:
        cmd.append("--write-subs")
        cmd.append("--sub-lang")
        cmd.append(subtitle_langs)
        if embed_subs:
            cmd.append("--embed-subs")

    # No playlist
    if no_playlist:
        cmd.append("--no-playlist")

    # URL
    cmd.append(url)

    # Execute
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        raise RuntimeError(f"Failed to download video: {result.stderr}")

    # Extract filename from output
    output_lines = result.stdout.split('\n')
    for line in output_lines:
        if '[download] Destination:' in line:
            return line.split('[download] Destination:')[-1].strip()

    # Fallback: find newest file in output directory
    files = list(output_path.glob("*"))
    if files:
        return str(max(files, key=lambda p: p.stat().st_mtime))

    raise RuntimeError("Could not determine output file path")


def main():
    parser = argparse.ArgumentParser(description="Download video using yt-dlp")
    parser.add_argument("url", help="Video URL")
    parser.add_argument("-o", "--output-dir", default=".", help="Output directory")
    parser.add_argument("-q", "--quality", default="best", help="Video quality")
    parser.add_argument("-f", "--format", default="mp4", help="Preferred format")
    parser.add_argument("-s", "--subs", help="Subtitle languages (comma-separated)")
    parser.add_argument("--embed-subs", action="store_true", help="Embed subtitles")
    parser.add_argument("--no-playlist", action="store_true", help="Download single video only")

    args = parser.parse_args()

    try:
        output_path = download_video(
            url=args.url,
            output_dir=args.output_dir,
            quality=args.quality,
            format_pref=args.format,
            subtitle_langs=args.subs,
            embed_subs=args.embed_subs,
            no_playlist=args.no_playlist,
        )
        print(f"\nDownloaded to: {output_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
