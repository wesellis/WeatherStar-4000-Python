#!/usr/bin/env python3
"""
WeatherStar 4000 Launcher
Checks dependencies and runs the weather display
"""

import sys
import subprocess
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    missing = []

    # Check pygame
    try:
        import pygame
    except ImportError:
        missing.append('pygame')

    # Check requests
    try:
        import requests
    except ImportError:
        missing.append('requests')

    return missing

def install_dependencies(packages):
    """Try to install missing packages"""
    print("Installing missing packages...")
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")
            print(f"  Please install manually: pip install {package}")
            return False
    return True

def main():
    print("=" * 50)
    print("WeatherStar 4000+ Python Version")
    print("=" * 50)

    # Check for missing dependencies
    missing = check_dependencies()

    if missing:
        print(f"\nMissing dependencies: {', '.join(missing)}")
        response = input("Would you like to install them now? (y/n): ")

        if response.lower() == 'y':
            if not install_dependencies(missing):
                print("\nPlease install dependencies manually:")
                print(f"  pip install {' '.join(missing)}")
                input("\nPress Enter to exit...")
                sys.exit(1)
        else:
            print("\nPlease install dependencies manually:")
            print(f"  pip install {' '.join(missing)}")
            input("\nPress Enter to exit...")
            sys.exit(1)

    # Get location
    print("\n" + "=" * 50)
    print("Location Setup")
    print("=" * 50)
    print("Enter your location (or press Enter to auto-detect)")
    print("You can find your coordinates at: https://www.latlong.net/")

    lat_input = input("Latitude [auto-detect]: ").strip()
    lon_input = input("Longitude [auto-detect]: ").strip()

    if lat_input and lon_input:
        lat = float(lat_input)
        lon = float(lon_input)
        print(f"\nStarting WeatherStar 4000 for {lat}, {lon}...")
    else:
        print("\nAuto-detecting location...")
        lat = None
        lon = None
        print("Starting WeatherStar 4000...")
    print("Controls:")
    print("  Space - Pause/Resume auto-play")
    print("  Arrow Keys - Navigate displays")
    print("  Right Click or M - Settings Menu")
    print("  Escape - Exit")
    print("")

    # Check for the main WeatherStar 4000 script
    if Path("weatherstar4000.py").exists():
        script = "weatherstar4000.py"
        print("\nStarting WeatherStar 4000...")
        print("Logs will be saved to 'logs' directory")
    else:
        print("Error: weatherstar4000.py not found!")
        input("Press Enter to exit...")
        sys.exit(1)

    # Run the weather display
    try:
        if lat is not None and lon is not None:
            subprocess.run([sys.executable, script, '--lat', str(lat), '--lon', str(lon)])
        else:
            # Let the script auto-detect location
            subprocess.run([sys.executable, script])
    except KeyboardInterrupt:
        print("\n\nWeatherStar 4000 closed.")
    except Exception as e:
        print(f"\nError running WeatherStar: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()