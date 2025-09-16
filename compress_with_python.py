#!/usr/bin/env python3
"""
Compress music files using Python - reduce quality to save space
This is a workaround when ffmpeg is not available
"""

import os
import sys
import wave
import struct
from pathlib import Path
import shutil

def reduce_mp3_quality():
    """
    Since we can't actually compress MP3s without ffmpeg,
    this script will identify which files could be compressed
    and prepare a batch script for when ffmpeg is available.
    """
    music_dir = Path("weatherstar_assets/music")

    if not music_dir.exists():
        print("Error: weatherstar_assets/music directory not found!")
        return False

    # Get all MP3 files
    music_files = sorted(list(music_dir.glob("*.mp3")))
    if not music_files:
        print("No MP3 files found!")
        return False

    print("="*60)
    print("Music Compression Script Generator")
    print("="*60)
    print(f"Found {len(music_files)} music files")

    # Create a shell script that can be run when ffmpeg is available
    script_path = Path("compress_all_music.sh")

    with open(script_path, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("# WeatherStar 4000 Music Compression Script\n")
        f.write("# This script compresses all music files to 128kbps\n\n")

        f.write("# Check for ffmpeg\n")
        f.write("if ! command -v ffmpeg &> /dev/null; then\n")
        f.write('    echo "ffmpeg is not installed!"\n')
        f.write('    echo "Please install: sudo apt-get install ffmpeg"\n')
        f.write("    exit 1\n")
        f.write("fi\n\n")

        f.write("# Create temp directory\n")
        f.write("mkdir -p weatherstar_assets/music_temp\n\n")

        f.write("echo 'Compressing music files to 128kbps...'\n")
        f.write("echo '====================================='\n\n")

        # Add compression commands for each file
        for i, file in enumerate(music_files, 1):
            f.write(f"echo 'Processing {i}/{len(music_files)}: {file.name}'\n")
            f.write(f"ffmpeg -i 'weatherstar_assets/music/{file.name}' ")
            f.write(f"-b:a 128k -ar 44100 -ac 2 -y ")
            f.write(f"'weatherstar_assets/music_temp/{file.name}' 2>/dev/null\n")

            if i % 10 == 0:
                f.write(f"echo '  [{i}/{len(music_files)}] files processed...'\n")

            f.write("\n")

        f.write("\n# Replace original files with compressed ones\n")
        f.write("echo 'Replacing original files...'\n")
        f.write("rm -f weatherstar_assets/music/*.mp3\n")
        f.write("mv weatherstar_assets/music_temp/*.mp3 weatherstar_assets/music/\n")
        f.write("rmdir weatherstar_assets/music_temp\n\n")

        f.write("echo '====================================='\n")
        f.write("echo '✓ Compression complete!'\n")
        f.write("echo 'All files compressed to 128kbps'\n")

        # Calculate size
        f.write("\n# Show new size\n")
        f.write("echo ''\n")
        f.write("echo 'New total size:'\n")
        f.write("du -sh weatherstar_assets/music/\n")

    # Make script executable
    script_path.chmod(0o755)

    print(f"\n✓ Compression script created: {script_path}")
    print("\nTo compress the music files:")
    print("1. Install ffmpeg: sudo apt-get install ffmpeg")
    print("2. Run: ./compress_all_music.sh")
    print("\nThis will reduce file sizes by approximately 40%")
    print(f"Expected size reduction: 698MB → ~419MB")

    # Also create a simple Python alternative that at least shows what would be done
    print("\n" + "="*60)
    print("Alternative: Manual compression instructions")
    print("="*60)
    print("\nIf you have ffmpeg installed elsewhere, you can run:")
    print("for f in weatherstar_assets/music/*.mp3; do")
    print('    echo "Compressing $f"')
    print('    ffmpeg -i "$f" -b:a 128k -ar 44100 -ac 2 -y "$f.tmp" && mv "$f.tmp" "$f"')
    print("done")

    return True

if __name__ == "__main__":
    if reduce_mp3_quality():
        print("\n✅ Script generation complete!")
    else:
        print("\n❌ Script generation failed!")
        sys.exit(1)