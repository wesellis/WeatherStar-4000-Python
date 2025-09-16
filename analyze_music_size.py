#!/usr/bin/env python3
"""
Analyze music file sizes and estimate compression savings
Shows what compression to 128kbps would save
"""

import os
from pathlib import Path

def analyze_music_files():
    """Analyze music file sizes and estimate compression savings"""
    music_dir = Path("weatherstar_assets/music")

    if not music_dir.exists():
        print("Error: weatherstar_assets/music directory not found!")
        return

    # Get all MP3 files
    music_files = list(music_dir.glob("*.mp3"))
    if not music_files:
        print("No MP3 files found!")
        return

    print("="*60)
    print("WeatherStar 4000 Music File Analysis")
    print("="*60)
    print(f"\nFound {len(music_files)} music files")

    # Calculate current sizes
    total_size = 0
    file_sizes = []

    for file in music_files:
        size_mb = file.stat().st_size / 1024 / 1024
        total_size += size_mb
        file_sizes.append((file.name, size_mb))

    # Sort by size
    file_sizes.sort(key=lambda x: x[1], reverse=True)

    print(f"\nCurrent total size: {total_size:.1f}MB")
    print(f"Average file size: {total_size/len(music_files):.1f}MB")

    # Show largest files
    print("\nLargest files:")
    for name, size in file_sizes[:10]:
        print(f"  {name:<25} {size:6.1f}MB")

    # Estimate compression savings
    # Most MP3s are 192-320kbps, compression to 128kbps typically saves 30-50%
    estimated_compressed = total_size * 0.6  # Conservative 40% reduction
    estimated_savings = total_size - estimated_compressed

    print("\n" + "="*60)
    print("Compression Estimates (128kbps target):")
    print("="*60)
    print(f"Current size:     {total_size:7.1f}MB")
    print(f"After compression: {estimated_compressed:7.1f}MB (estimated)")
    print(f"Space saved:      {estimated_savings:7.1f}MB (~{(estimated_savings/total_size)*100:.0f}%)")

    print("\n" + "="*60)
    print("To actually compress the files:")
    print("="*60)
    print("1. Install ffmpeg:")
    print("   Ubuntu/Debian: sudo apt-get install ffmpeg")
    print("   Mac: brew install ffmpeg")
    print("   Windows: Download from https://ffmpeg.org")
    print("\n2. Run the compress_music.py script")
    print("\nNote: The files have already been renamed to simple names!")
    print("(smooth_jazz_01.mp3 through smooth_jazz_75.mp3)")

if __name__ == "__main__":
    analyze_music_files()