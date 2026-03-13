#!/usr/bin/env python3
"""YouTube to MP3 converter CLI."""

import argparse
import os
import shutil
import subprocess
import sys

EXTRA_PATHS = [
    os.path.expanduser("~/Library/Python/3.13/bin"),
    os.path.expanduser("~/Library/Python/3.12/bin"),
    os.path.expanduser("~/.local/bin"),
    os.path.expanduser("~/.deno/bin"),
    "/opt/homebrew/bin",
    "/usr/local/bin",
]


def _find(cmd: str) -> str | None:
    """Find a command on PATH or in common install locations."""
    path = shutil.which(cmd)
    if path:
        return path
    for d in EXTRA_PATHS:
        p = os.path.join(d, cmd)
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    # Fallback: try static_ffmpeg package for ffmpeg/ffprobe
    if cmd in ("ffmpeg", "ffprobe"):
        try:
            import static_ffmpeg
            static_ffmpeg.add_paths()
            return shutil.which(cmd)
        except ImportError:
            pass
    return None


def check_dependencies() -> dict[str, str]:
    """Return resolved paths for yt-dlp and ffmpeg, or exit with install instructions."""
    paths = {}
    missing = []
    for cmd in ("yt-dlp", "ffmpeg"):
        p = _find(cmd)
        if p:
            paths[cmd] = p
        else:
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
    return paths


def download(url: str, output_dir: str, filename: str | None = None) -> str:
    """Download a YouTube video as MP3.

    Returns the path to the downloaded file.
    """
    paths = check_dependencies()

    output_dir = os.path.realpath(os.path.expanduser(output_dir))
    try:
        os.makedirs(output_dir, exist_ok=True)
    except (FileExistsError, OSError):
        pass  # directory exists but may be sandboxed

    template = os.path.join(output_dir, filename) if filename else os.path.join(output_dir, "%(title)s.%(ext)s")

    cmd = [
        paths["yt-dlp"],
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",  # best quality
        "--ffmpeg-location", os.path.dirname(paths["ffmpeg"]),
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
        help="Output filename (default: video title). .mp3 extension added automatically.",
    )

    args = parser.parse_args()

    name = args.name
    if name and not name.endswith(".mp3"):
        name += ".mp3"

    print(f"Downloading: {args.url}")
    filepath = download(args.url, args.output_dir, name)
    print(f"Saved: {filepath}")


if __name__ == "__main__":
    main()
