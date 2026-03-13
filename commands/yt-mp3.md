---
description: Download a YouTube video as an MP3 file
argument-hint: <youtube-url> [output-dir]
allowed-tools: [Bash, Read]
---

# Download YouTube Video as MP3

The user wants to download a YouTube video as an MP3 file.

## Arguments

$ARGUMENTS

## Instructions

1. Parse the arguments: the first argument is the YouTube URL, the optional second argument is the output directory (default: `~/Downloads`)
2. Run the download command using the Bash tool:

```bash
yt-mp3 "<url>" -o "<output-dir>"
```

3. If `yt-mp3` is not installed, install it first:

```bash
pip install -e /Users/shyamal/Documents/Development/claude/github/yt-mp3
```

4. Report the saved file path to the user
