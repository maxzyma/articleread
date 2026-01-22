#!/usr/bin/env python3
"""
yt-dlp Audio Extractor Script

Extracts audio from videos and saves it in various formats.
Supports quality selection and automatic conversion.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def extract_audio(
    url: str,
    output_dir: str = ".",
    audio_format: str = "mp3",
    audio_quality: str = "192",
    output_template: str = None,
) -> str:
    """
    Extract audio from video using yt-dlp.

    Args:
        url: Video URL
        output_dir: Output directory path
        audio_format: Audio format (mp3/m4a/flac/wav/etc.)
        audio_quality: Audio quality in kbps (for mp3: 64-320, for m4a: 64-256)
        output_template: Custom output template (default: "%(title)s.%(ext)s")

    Returns:
        Path to extracted audio file
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Build yt-dlp command
    cmd = [
        "yt-dlp",
        "-x",  # Extract audio
        "--audio-format", audio_format,
        "--audio-quality", audio_quality,
        "-o", str(output_path / (output_template or "%(title)s.%(ext)s")),
        url,
    ]

    # Execute
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        raise RuntimeError(f"Failed to extract audio: {result.stderr}")

    # Extract filename from output
    output_lines = result.stdout.split('\n')
    for line in output_lines:
        if '[download] Destination:' in line:
            return line.split('[download] Destination:')[-1].strip()

    # Fallback: find newest file in output directory
    files = list(output_path.glob(f"*.{audio_format}"))
    if files:
        return str(max(files, key=lambda p: p.stat().st_mtime))

    raise RuntimeError("Could not determine output file path")


def main():
    parser = argparse.ArgumentParser(description="Extract audio from video using yt-dlp")
    parser.add_argument("url", help="Video URL")
    parser.add_argument("-o", "--output-dir", default=".", help="Output directory")
    parser.add_argument("-f", "--format", default="mp3", help="Audio format (mp3/m4a/flac/wav)")
    parser.add_argument("-q", "--quality", default="192", help="Audio quality in kbps")
    parser.add_argument("-t", "--template", help="Output filename template")

    args = parser.parse_args()

    try:
        output_path = extract_audio(
            url=args.url,
            output_dir=args.output_dir,
            audio_format=args.format,
            audio_quality=args.quality,
            output_template=args.template,
        )
        print(f"\nExtracted audio to: {output_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
