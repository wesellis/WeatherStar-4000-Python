#!/usr/bin/env python3
"""
Convert WOFF fonts to TTF for pygame usage
Note: This requires the fonttools library
"""

import sys
import subprocess
from pathlib import Path

def check_fonttools():
    """Check if fonttools is installed"""
    try:
        import fontTools
        return True
    except ImportError:
        return False

def install_fonttools():
    """Install fonttools"""
    print("Installing fonttools...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'fonttools'])
        print("✓ fonttools installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install fonttools")
        print("  Please install manually: pip install fonttools")
        return False

def convert_woff_to_ttf(woff_path, ttf_path):
    """Convert a WOFF font to TTF"""
    from fontTools import ttLib

    try:
        # Load WOFF font
        font = ttLib.TTFont(woff_path)

        # Save as TTF
        font.save(ttf_path)

        print(f"✓ Converted {woff_path.name} → {ttf_path.name}")
        return True
    except Exception as e:
        print(f"✗ Failed to convert {woff_path.name}: {e}")
        return False

def main():
    print("=" * 50)
    print("Star4000 Font Converter (WOFF → TTF)")
    print("=" * 50)

    # Check for fonttools
    if not check_fonttools():
        print("\nfonttools is required for font conversion")
        response = input("Would you like to install it now? (y/n): ")

        if response.lower() == 'y':
            if not install_fonttools():
                return
        else:
            print("\nPlease install fonttools manually:")
            print("  pip install fonttools")
            return

    # Font paths
    fonts_dir = Path("weatherstar_assets/fonts")

    if not fonts_dir.exists():
        # Try ws4kp fonts directory
        fonts_dir = Path("ws4kp/server/fonts")
        if not fonts_dir.exists():
            print(f"Error: Fonts directory not found")
            print(f"  Looked in: weatherstar_assets/fonts")
            print(f"  Looked in: ws4kp/server/fonts")
            return

    # Find WOFF files
    woff_files = list(fonts_dir.glob("*.woff"))

    if not woff_files:
        print(f"No WOFF files found in {fonts_dir}")
        return

    print(f"\nFound {len(woff_files)} WOFF fonts to convert:")
    for wf in woff_files:
        print(f"  • {wf.name}")

    # Create TTF directory
    ttf_dir = Path("weatherstar_assets/fonts_ttf")
    ttf_dir.mkdir(exist_ok=True, parents=True)

    print(f"\nConverting to TTF in {ttf_dir}...")

    # Convert each font
    success_count = 0
    for woff_file in woff_files:
        ttf_file = ttf_dir / (woff_file.stem.replace(" ", "_").lower() + ".ttf")
        if convert_woff_to_ttf(woff_file, ttf_file):
            success_count += 1

    print(f"\n{success_count}/{len(woff_files)} fonts converted successfully")

    if success_count == len(woff_files):
        print("\n✅ All fonts converted! You can now use them in pygame.")
        print("\nFont files created:")
        for ttf_file in ttf_dir.glob("*.ttf"):
            print(f"  {ttf_file}")
    else:
        print("\n⚠ Some fonts failed to convert.")
        print("You may need to convert them manually using an online converter.")

if __name__ == "__main__":
    main()