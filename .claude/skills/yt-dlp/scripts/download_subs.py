#!/usr/bin/env python3
"""
yt-dlp Subtitle Downloader Script

Downloads subtitles from videos in various formats.
Supports auto-generated subtitles and multiple languages.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def download_subtitles(
    url: str,
    output_dir: str = ".",
    languages: str = "en",
    format: str = "srt",
    auto_subs: bool = True,
    write_auto_subs: bool = False,
    embed_subs: bool = False,
) -> list:
    """
    Download subtitles from video using yt-dlp.

    Args:
        url: Video URL
        output_dir: Output directory path
        languages: Comma-separated language codes (e.g., "en,zh")
        format: Subtitle format (srt/vtt/ass/etc.)
        auto_subs: Download auto-generated subtitles if manual not available
        write_auto_subs: Write auto-generated subtitles separately
        embed_subs: Embed subtitles in video file (requires video download)

    Returns:
        List of paths to downloaded subtitle files
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Build yt-dlp command
    cmd = [
        "yt-dlp",
        "--write-subs",
        "--sub-lang", languages,
        "--sub-format", format,
        "-o", str(output_path / "%(title)s.%(ext)s"),
    ]

    if auto_subs:
        cmd.append("--write-auto-subs")

    if write_auto_subs:
        cmd.append("--write-auto-subs")

    if embed_subs:
        cmd.append("--embed-subs")
        cmd.append("--embed-thumbnail")

    cmd.append(url)

    # Execute
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        raise RuntimeError(f"Failed to download subtitles: {result.stderr}")

    # Find subtitle files
    sub_files = list(output_path.glob(f"*.{format}"))
    return [str(f) for f in sub_files]


def main():
    parser = argparse.ArgumentParser(description="Download subtitles using yt-dlp")
    parser.add_argument("url", help="Video URL")
    parser.add_argument("-o", "--output-dir", default=".", help="Output directory")
    parser.add_argument("-l", "--languages", default="en", help="Comma-separated language codes")
    parser.add_argument("-f", "--format", default="srt", help="Subtitle format (srt/vtt/ass)")
    parser.add_argument("--auto-subs", action="store_true", help="Download auto-generated subtitles")
    parser.add_argument("--write-auto", action="store_true", help="Write auto-generated subs separately")
    parser.add_argument("--embed", action="store_true", help="Embed subtitles in video")

    args = parser.parse_args()

    try:
        sub_files = download_subtitles(
            url=args.url,
            output_dir=args.output_dir,
            languages=args.languages,
            format=args.format,
            auto_subs=args.auto_subs,
            write_auto_subs=args.write_auto,
            embed_subs=args.embed,
        )
        if sub_files:
            print(f"\nDownloaded {len(sub_files)} subtitle file(s):")
            for f in sub_files:
                print(f"  - {f}")
        else:
            print("\nNo subtitle files found (might not be available for this video)")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
