#!/usr/bin/env python3
"""
Compress already-renamed music files to 128kbps
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil

def compress_music_files():
    """Compress music files to 128kbps (files already renamed)"""
    music_dir = Path("weatherstar_assets/music")
    temp_dir = Path("weatherstar_assets/music_compressed")

    # Check for local ffmpeg
    ffmpeg_cmd = './ffmpeg' if Path('./ffmpeg').exists() else 'ffmpeg'

    # Test ffmpeg
    try:
        subprocess.run([ffmpeg_cmd, '-version'], capture_output=True, check=True)
    except:
        print("Error: ffmpeg not found!")
        return False

    # Get all MP3 files
    music_files = sorted(list(music_dir.glob("smooth_jazz_*.mp3")))
    if not music_files:
        print("No music files found!")
        return False

    print(f"Found {len(music_files)} music files to compress")
    print("Target: 128kbps (reducing size by ~40%)")

    # Create temp directory
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True)

    # Track sizes
    original_total = 0
    compressed_total = 0

    print("\nCompressing files...")
    print("="*50)

    for i, file in enumerate(music_files, 1):
        output_path = temp_dir / file.name

        print(f"[{i:2d}/{len(music_files)}] {file.name}", end=" ... ")

        # Compress using ffmpeg
        cmd = [
            ffmpeg_cmd,
            '-i', str(file),
            '-b:a', '128k',  # 128kbps bitrate
            '-ar', '44100',   # 44.1kHz sample rate
            '-ac', '2',       # Stereo
            '-y',             # Overwrite output
            '-loglevel', 'error',
            str(output_path)
        ]

        try:
            subprocess.run(cmd, check=True)

            # Get file sizes
            original_size = file.stat().st_size / 1024 / 1024  # MB
            new_size = output_path.stat().st_size / 1024 / 1024  # MB
            original_total += original_size
            compressed_total += new_size
            reduction = (1 - new_size/original_size) * 100

            print(f"{original_size:.1f}MB → {new_size:.1f}MB (-{reduction:.0f}%)")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to compress")
            return False

    print("="*50)
    print(f"\nOriginal total:   {original_total:.1f}MB")
    print(f"Compressed total: {compressed_total:.1f}MB")
    print(f"Space saved:      {original_total - compressed_total:.1f}MB ({((original_total - compressed_total)/original_total)*100:.0f}%)")

    print("\nReplacing original files with compressed versions...")

    # Replace original files
    for file in music_dir.glob("smooth_jazz_*.mp3"):
        file.unlink()

    # Move compressed files
    for file in temp_dir.glob("*.mp3"):
        shutil.move(str(file), music_dir / file.name)

    # Clean up
    temp_dir.rmdir()

    print("✓ Compression complete!")
    return True

if __name__ == "__main__":
    print("="*50)
    print("WeatherStar 4000 Music Compression")
    print("="*50)

    if compress_music_files():
        print("\n✅ All files successfully compressed!")
    else:
        print("\n❌ Compression failed!")
        sys.exit(1)