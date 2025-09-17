# WeatherStar 4000+ v2.1.0 - Real Radar Update

## 🌩️ Release Date: September 16, 2025

### ✨ Major Features
- **Real NOAA Weather Radar** - Live radar from weather.gov with automatic zoom to your location
- **Improved News Displays** - MSN & Reddit with colored categories and smooth scrolling
- **Enhanced Image Quality** - High-quality radar with LANCZOS resampling and smoothing
- **Modularized Architecture** - Cleaner codebase split into logical modules

### 🎯 Key Improvements
- ✅ Real-time animated radar (6 frames) from NOAA
- ✅ Automatic location detection and regional zoom
- ✅ Fixed Weekend Forecast icon aspect ratios
- ✅ Proper news text sizing and margins
- ✅ Scrolling ticker positioned correctly (20px from bottom)
- ✅ Removed artificial scanlines for authentic CRT display
- ✅ Security updates for all dependencies

### 🔧 Technical Changes
- Fetches radar from `weather.gov/ridge` API
- Intelligent crop and zoom based on lat/lon coordinates
- PIL/Pillow integration for superior image processing
- Modular code organization (displays, data fetchers, news, weather)
- Updated to latest secure package versions

### 📦 Requirements
- Python 3.7+
- pygame 2.6.0
- requests 2.32.3
- Pillow 10.4.0
- ephem 4.1.0+ (optional)

### 🚀 Installation
```bash
git clone https://github.com/wesellis/WeatherStar-4000-Python.git
cd WeatherStar-4000-Python
pip install -r requirements.txt
python weatherstar4000.py
```

### 🎮 Perfect for
- Raspberry Pi projects
- Retro weather displays
- CRT TV installations
- Weather enthusiasts
- 90s nostalgia lovers

---
*Recreating the authentic 1990s Weather Channel experience with modern data!*