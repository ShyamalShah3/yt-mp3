---
name: yt-mp3
description: "Download YouTube videos as MP3 audio files. Use when the user asks to download a YouTube video, convert YouTube to MP3, extract audio from YouTube, save a YouTube video as audio, or mentions 'yt-mp3'."
version: 1.0.0
metadata:
  openclaw:
    category: "media"
    requires:
      bins: ["yt-mp3"]
    cliHelp: "yt-mp3 --help"
---

# YouTube to MP3 Converter

Convert YouTube videos to MP3 audio files using the `yt-mp3` CLI.

## Prerequisites

The CLI requires `yt-dlp` and `ffmpeg` to be installed:

```bash
pip install yt-dlp
brew install ffmpeg  # macOS
```

Install the CLI itself:

```bash
cd <plugin-root> && pip install -e .
```

## Usage

```bash
yt-mp3 <youtube-url> [-o OUTPUT_DIR] [-n FILENAME]
```

## Flags

| Flag | Description | Default |
|------|-------------|---------|
| `url` | YouTube video URL (required, positional) | — |
| `-o`, `--output-dir` | Directory to save the MP3 file | `~/Downloads` |
| `-n`, `--name` | Custom output filename (include `.mp3`) | Video title |

## Examples

```bash
# Download to ~/Downloads with default name
yt-mp3 "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Download to a specific directory
yt-mp3 "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o ~/Music

# Download with a custom filename
yt-mp3 "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o ~/Music -n "song.mp3"
```

## Workflow

1. User provides a YouTube URL
2. Run `yt-mp3 "<url>"` using the Bash tool
3. The tool downloads the video, extracts audio, converts to MP3, and prints the saved file path
4. Report the file path back to the user

## Error Handling

- If `yt-dlp` or `ffmpeg` is missing, the tool prints install instructions and exits
- If the URL is invalid or the video is unavailable, `yt-dlp` prints an error to stderr
- Always quote the URL in the bash command to handle special characters
