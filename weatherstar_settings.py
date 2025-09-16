#!/usr/bin/env python3
"""
WeatherStar 4000 Settings Manager
Handles saving and loading user preferences
"""

import json
import os
from pathlib import Path

SETTINGS_FILE = Path.home() / ".weatherstar4000_settings.json"

def load_settings():
    """Load saved settings or return defaults"""
    defaults = {
        'location': {
            'auto_detect': True,
            'lat': None,
            'lon': None,
            'zip': None,
            'description': None
        },
        'display': {
            'show_marine': False,
            'show_trends': True,
            'show_historical': True,
            'show_msn': True,
            'show_reddit': True,
            'music_volume': 0.3
        }
    }

    try:
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, 'r') as f:
                saved = json.load(f)
                # Merge with defaults to handle missing keys
                for key in defaults:
                    if key in saved:
                        defaults[key].update(saved[key])
                return defaults
    except Exception as e:
        print(f"Error loading settings: {e}")

    return defaults

def save_settings(settings):
    """Save settings to file"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving settings: {e}")
        return False

def get_saved_location():
    """Get saved location if available"""
    settings = load_settings()
    location = settings.get('location', {})

    if not location.get('auto_detect', True):
        # Use saved manual location
        lat = location.get('lat')
        lon = location.get('lon')
        if lat and lon:
            return lat, lon, location.get('description', f"{lat}, {lon}")

    return None  # Use auto-detect

def save_location(lat, lon, description=None, auto_detect=False):
    """Save a location preference"""
    settings = load_settings()
    settings['location'] = {
        'auto_detect': auto_detect,
        'lat': lat,
        'lon': lon,
        'description': description or f"{lat:.4f}, {lon:.4f}"
    }
    return save_settings(settings)

def save_display_preferences(prefs):
    """Save display preferences"""
    settings = load_settings()
    settings['display'].update(prefs)
    return save_settings(settings)

def get_display_preferences():
    """Get display preferences"""
    settings = load_settings()
    return settings.get('display', {})