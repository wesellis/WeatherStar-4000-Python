#!/usr/bin/env python3
"""
Compress and rename WeatherStar 4000 music files
Converts to 128kbps MP3 and renames with simple sequential names
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil

def check_ffmpeg():
    """Check if ffmpeg is installed"""
    # First check for local ffmpeg binary
    local_ffmpeg = Path("./ffmpeg")
    if local_ffmpeg.exists():
        return True
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def compress_and_rename_music():
    """Compress music files to 128kbps and rename with simple names"""
    music_dir = Path("weatherstar_assets/music")
    backup_dir = Path("weatherstar_assets/music_original")
    temp_dir = Path("weatherstar_assets/music_compressed")

    if not music_dir.exists():
        print("Error: weatherstar_assets/music directory not found!")
        return False

    # Check for ffmpeg
    if not check_ffmpeg():
        print("Error: ffmpeg not installed!")
        print("Please install ffmpeg:")
        print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("  Mac: brew install ffmpeg")
        print("  Windows: Download from https://ffmpeg.org/download.html")
        return False

    # Get all MP3 files
    music_files = list(music_dir.glob("*.mp3"))
    if not music_files:
        print("No MP3 files found in music directory!")
        return False

    print(f"Found {len(music_files)} music files to process")

    # Create backup directory
    if not backup_dir.exists():
        print(f"Creating backup directory: {backup_dir}")
        backup_dir.mkdir(parents=True)

        # Copy original files to backup
        print("Backing up original files...")
        for file in music_files:
            shutil.copy2(file, backup_dir / file.name)
            print(f"  Backed up: {file.name}")
    else:
        print(f"Backup already exists at: {backup_dir}")

    # Create temporary directory for compressed files
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True)

    print("\nCompressing and renaming files...")
    print("Target: 128kbps MP3 (reduces size by ~40-50%)")

    # Process each file
    for i, file in enumerate(music_files, 1):
        # Generate simple name
        new_name = f"smooth_jazz_{i:02d}.mp3"
        output_path = temp_dir / new_name

        print(f"\nProcessing {i}/{len(music_files)}: {file.name}")
        print(f"  New name: {new_name}")

        # Compress using ffmpeg (use local binary if available)
        ffmpeg_cmd = './ffmpeg' if Path('./ffmpeg').exists() else 'ffmpeg'
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

            # Get file sizes for comparison
            original_size = file.stat().st_size / 1024 / 1024  # MB
            new_size = output_path.stat().st_size / 1024 / 1024  # MB
            reduction = (1 - new_size/original_size) * 100

            print(f"  Original: {original_size:.1f}MB → Compressed: {new_size:.1f}MB")
            print(f"  Size reduction: {reduction:.0f}%")
        except subprocess.CalledProcessError as e:
            print(f"  ERROR: Failed to compress {file.name}")
            print(f"    {e}")
            continue

    # Replace original files with compressed ones
    print("\n" + "="*50)
    response = input("Replace original files with compressed versions? (y/n): ")

    if response.lower() == 'y':
        # Clear original music directory
        print("\nReplacing files...")
        for file in music_dir.glob("*.mp3"):
            file.unlink()

        # Move compressed files to music directory
        for file in temp_dir.glob("*.mp3"):
            shutil.move(str(file), music_dir / file.name)
            print(f"  Installed: {file.name}")

        # Remove temp directory
        temp_dir.rmdir()

        print("\n" + "="*50)
        print("✓ Music compression complete!")
        print(f"✓ Original files backed up to: {backup_dir}")
        print("✓ 75 files renamed to: smooth_jazz_01.mp3 through smooth_jazz_75.mp3")

        # Calculate total space saved
        original_total = sum(f.stat().st_size for f in backup_dir.glob("*.mp3")) / 1024 / 1024
        new_total = sum(f.stat().st_size for f in music_dir.glob("*.mp3")) / 1024 / 1024
        saved = original_total - new_total

        print(f"\nSpace saved: {saved:.0f}MB ({(saved/original_total)*100:.0f}% reduction)")
        print(f"Original total: {original_total:.0f}MB")
        print(f"New total: {new_total:.0f}MB")
    else:
        print("Compression cancelled. Original files unchanged.")
        print(f"Compressed files available in: {temp_dir}")

    return True

if __name__ == "__main__":
    print("="*50)
    print("WeatherStar 4000 Music Compressor")
    print("="*50)

    if compress_and_rename_music():
        print("\nProcess complete!")
    else:
        print("\nProcess failed!")
        sys.exit(1)