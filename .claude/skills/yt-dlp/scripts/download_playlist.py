#!/usr/bin/env python3
"""
yt-dlp Playlist Downloader Script

Downloads entire playlists with batch processing support.
Supports index selection, reverse order, and concurrent downloads.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def download_playlist(
    url: str,
    output_dir: str = ".",
    start: int = 1,
    end: int = None,
    reverse: bool = False,
    quality: str = "best",
    format_pref: str = "mp4",
    concurrent_fragments: int = None,
) -> list:
    """
    Download playlist using yt-dlp.

    Args:
        url: Playlist URL
        output_dir: Output directory path
        start: Start index (1-based)
        end: End index (exclusive, None for all)
        reverse: Download in reverse order
        quality: Video quality
        format_pref: Preferred format
        concurrent_fragments: Number of concurrent fragments for HLS/DASH

    Returns:
        List of paths to downloaded files
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Build yt-dlp command
    cmd = ["yt-dlp"]

    # Playlist options
    playlist_items = f"{start}"
    if end:
        playlist_items += f"-{end}"
    cmd.extend(["--playlist-items", playlist_items])

    if reverse:
        cmd.append("--playlist-reverse")

    # Format selection
    if format_pref:
        cmd.extend(["-f", f"{quality}[ext={format_pref}]/{quality}"])

    # Output template (include playlist index and title)
    cmd.extend(["-o", str(output_path / "%(playlist_index)s-%(title)s.%(ext)s")])

    # Concurrent fragments
    if concurrent_fragments:
        cmd.extend(["--concurrent-fragments", str(concurrent_fragments)])

    cmd.append(url)

    # Execute
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        raise RuntimeError(f"Failed to download playlist: {result.stderr}")

    # Find downloaded files
    files = list(output_path.glob("*"))
    video_files = [str(f) for f in files if f.suffix in [".mp4", ".webm", ".mkv", ".mov"]]
    return video_files


def main():
    parser = argparse.ArgumentParser(description="Download playlist using yt-dlp")
    parser.add_argument("url", help="Playlist URL")
    parser.add_argument("-o", "--output-dir", default=".", help="Output directory")
    parser.add_argument("--start", type=int, default=1, help="Start index (1-based)")
    parser.add_argument("--end", type=int, help="End index (exclusive)")
    parser.add_argument("--reverse", action="store_true", help="Download in reverse order")
    parser.add_argument("-q", "--quality", default="best", help="Video quality")
    parser.add_argument("-f", "--format", default="mp4", help="Preferred format")
    parser.add_argument("-c", "--concurrent", type=int, help="Concurrent fragments")

    args = parser.parse_args()

    try:
        video_files = download_playlist(
            url=args.url,
            output_dir=args.output_dir,
            start=args.start,
            end=args.end,
            reverse=args.reverse,
            quality=args.quality,
            format_pref=args.format,
            concurrent_fragments=args.concurrent,
        )
        print(f"\nDownloaded {len(video_files)} video(s)")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
