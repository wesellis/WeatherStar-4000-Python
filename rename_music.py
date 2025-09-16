#!/usr/bin/env python3
"""
Rename WeatherStar 4000 music files to simple sequential names
Creates backup before renaming
"""

import os
import sys
from pathlib import Path
import shutil

def rename_music_files():
    """Rename music files with simple sequential names"""
    music_dir = Path("weatherstar_assets/music")
    backup_dir = Path("../weatherstar_music_backup")

    if not music_dir.exists():
        print("Error: weatherstar_assets/music directory not found!")
        return False

    # Get all MP3 files and sort them alphabetically
    music_files = sorted(list(music_dir.glob("*.mp3")))
    if not music_files:
        print("No MP3 files found in music directory!")
        return False

    print(f"Found {len(music_files)} music files to rename")

    # Create backup directory if it doesn't exist
    if not backup_dir.exists():
        print(f"\nCreating backup directory: {backup_dir}")
        backup_dir.mkdir(parents=True)

        # Copy original files to backup
        print("Backing up original files...")
        for file in music_files:
            shutil.copy2(file, backup_dir / file.name)
            print(f"  Backed up: {file.name}")
    else:
        print(f"\nBackup already exists at: {backup_dir}")

    print("\n" + "="*60)
    print("File renaming preview:")
    print("="*60)

    # Show renaming plan
    rename_map = {}
    for i, file in enumerate(music_files, 1):
        new_name = f"smooth_jazz_{i:02d}.mp3"
        rename_map[file] = music_dir / new_name

        # Show first 5 and last 2 as examples
        if i <= 5 or i >= len(music_files) - 1:
            old_display = file.name[:40] + "..." if len(file.name) > 43 else file.name
            print(f"{old_display:<45} → {new_name}")
        elif i == 6:
            print(f"  ... {len(music_files) - 7} more files ...")

    print("\n" + "="*60)

    # Auto-proceed with renaming
    print("\nProceeding with rename operation...")
    print("\nRenaming files...")

    # First pass: rename to temporary names to avoid conflicts
    temp_renames = {}
    for file, new_path in rename_map.items():
        temp_name = file.parent / f"_temp_{file.name}"
        file.rename(temp_name)
        temp_renames[temp_name] = new_path

    # Second pass: rename to final names
    for temp_path, final_path in temp_renames.items():
        temp_path.rename(final_path)
        print(f"  Renamed to: {final_path.name}")

    print("\n" + "="*60)
    print("✓ Music file renaming complete!")
    print(f"✓ Original files backed up to: {backup_dir.absolute()}")
    print(f"✓ {len(music_files)} files renamed:")
    print("  • smooth_jazz_01.mp3 through smooth_jazz_{:02d}.mp3".format(len(music_files)))

    # Calculate total size
    total_size = sum(f.stat().st_size for f in music_dir.glob("*.mp3")) / 1024 / 1024
    print(f"\nTotal music size: {total_size:.0f}MB")
    print("\nNote: Files were renamed only (not compressed)")
    print("To compress files, install ffmpeg and run compress_music.py")

    return True

if __name__ == "__main__":
    print("="*60)
    print("WeatherStar 4000 Music File Renamer")
    print("="*60)

    if rename_music_files():
        print("\nProcess complete!")
    else:
        print("\nProcess failed!")
        sys.exit(1)