#!/usr/bin/env python3
"""YouTube to MP3 converter CLI."""

import argparse
import os
import subprocess
import sys


def check_dependencies():
    """Check that yt-dlp and ffmpeg are installed."""
    missing = []
    for cmd in ("yt-dlp", "ffmpeg"):
        if subprocess.run(
            ["which", cmd], capture_output=True, text=True
        ).returncode != 0:
            missing.append(cmd)
    if missing:
        print(f"Error: missing required dependencies: {', '.join(missing)}")
        print("Install with:")
        if "yt-dlp" in missing:
            print("  pip install yt-dlp")
        if "ffmpeg" in missing:
            print("  brew install ffmpeg  (macOS)")
            print("  sudo apt install ffmpeg  (Linux)")
        sys.exit(1)


def download(url: str, output_dir: str, filename: str | None = None) -> str:
    """Download a YouTube video as MP3.

    Returns the path to the downloaded file.
    """
    check_dependencies()

    output_dir = os.path.expanduser(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    template = os.path.join(output_dir, filename) if filename else os.path.join(output_dir, "%(title)s.%(ext)s")

    cmd = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",  # best quality
        "--output", template,
        "--no-playlist",
        "--print", "after_move:filepath",
        url,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

    filepath = result.stdout.strip().splitlines()[-1]
    return filepath


def main():
    parser = argparse.ArgumentParser(
        prog="yt-mp3",
        description="Download YouTube videos as MP3 files.",
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "-o", "--output-dir",
        default="~/Downloads",
        help="Output directory (default: ~/Downloads)",
    )
    parser.add_argument(
        "-n", "--name",
        default=None,
        help="Output filename (default: video title). Include .mp3 extension.",
    )

    args = parser.parse_args()

    print(f"Downloading: {args.url}")
    filepath = download(args.url, args.output_dir, args.name)
    print(f"Saved: {filepath}")


if __name__ == "__main__":
    main()
