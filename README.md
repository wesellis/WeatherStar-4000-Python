# 📺 WeatherStar 4000 Python Recreation

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-00AA00?style=for-the-badge&logo=python&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white)
![NOAA](https://img.shields.io/badge/NOAA%20API-003087?style=for-the-badge&logo=gov&logoColor=white)
![CRT](https://img.shields.io/badge/CRT%20TV-Ready-orange?style=for-the-badge)

### **Authentic 1990s Weather Channel Experience**
*A pixel-perfect recreation of the iconic WeatherStar 4000 for Raspberry Pi and CRT TVs*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![CRT Compatible](https://img.shields.io/badge/4:3%20CRT-Compatible-green.svg)](https://en.wikipedia.org/wiki/Cathode-ray_tube)

[Features](#-features) • [Quick Start](#-quick-start) • [Raspberry Pi](#-raspberry-pi--crt-tv-setup) • [Screenshots](#-screenshots) • [Documentation](#-documentation)

</div>

---

## 🎯 **Project Overview**

The WeatherStar 4000 was the iconic weather information system used by The Weather Channel throughout the 1990s. This Python recreation brings that nostalgic experience to modern hardware, **optimized for Raspberry Pi and authentic display on 4:3 CRT televisions**.

### **Perfect for:**
- 📺 **CRT TV collectors** - Native 640x480 resolution perfect for 4:3 displays
- 🖥️ **Retro computing enthusiasts** - Authentic 90s experience
- 🌡️ **Weather monitoring stations** - Professional weather display
- 🏫 **Educational displays** - Museums, schools, maker spaces
- 🎮 **Nostalgia projects** - Relive the 90s Weather Channel

## ✨ Features

### 🎨 Authentic Display Modes
- **Current Conditions** - Temperature, humidity, wind, pressure with trends
- **Local Forecast** - 3-column scrolling text forecast
- **Extended Forecast** - 7-day outlook with conditions
- **Hourly Forecast** - Next 24 hours with scrolling display
- **Regional Observations** - Nearby city conditions
- **Travel Cities** - Major US city weather
- **Weather Almanac** - Records, sunrise/sunset, precipitation totals
- **Local Radar** - Animated radar imagery
- **Hazards & Warnings** - Active weather alerts

### 🆕 Enhanced Features (New in v1.0!)
- **Air Quality & Health** - Real-time AQI, pollen counts, health recommendations
- **7-Day Temperature Graph** - Color-coded temperature trends (blue=cold to red=hot)
- **Weather Records** - Historical comparisons
- **Sun & Moon Data** - Detailed astronomy information
- **Wind & Pressure Analysis** - Barometric trends
- **Weekend Forecast** - 2-column Saturday/Sunday display
- **Animated Weather Icons** - GIF animations for rain, snow, storms
- **News Integration** - MSN, Reddit, and REAL local news headlines
- **Clickable Headlines** - Open news articles in browser

### 🎵 Authentic Experience
- **75+ Smooth Jazz Tracks** - Hours of period-correct background music
- **Original Star4000 Fonts** - Pixel-perfect bitmap fonts
- **Classic Backgrounds** - Blue gradients and authentic layouts
- **Smooth Transitions** - Auto-cycling through all displays
- **Scrolling Ticker** - Classic bottom banner with conditions

### 📊 Smart Features
- **Weather Trend Arrows** - Rising/falling indicators for temperature and pressure
- **Historical Comparisons** - Current vs. 30-year averages
- **Precipitation Tracking** - 24hr, 7-day, monthly accumulation
- **Right-Click Settings Menu** - Customize display options
- **Auto Location Detection** - Uses IP geolocation or manual entry

## 🚀 Quick Start

### System Requirements
- Python 3.7 or higher
- 1GB RAM minimum (2GB recommended)
- Internet connection for weather data
- **Perfect for Raspberry Pi 3B+, 4, or Zero 2W**

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/WeatherStar-4000-Python.git
cd WeatherStar-4000-Python
```

2. **Install dependencies:**
```bash
pip install pygame requests
```

3. **Run WeatherStar 4000:**

**Windows:**
```bash
run_weatherstar.bat
```

**Linux/Mac:**
```bash
./run_weatherstar.sh
```

**Or directly with Python:**
```bash
python run_weatherstar.py
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| **Space** | Pause/Resume auto-play |
| **←/→** | Navigate displays manually |
| **Right-Click** or **M** | Open settings menu |
| **Escape** | Exit |

### Settings Menu Options
1. **Toggle Marine Forecast** - Show/hide coastal conditions
2. **Toggle Weather Trends** - Show/hide trend arrows
3. **Toggle Historical Data** - Show/hide comparisons
4. **Music Volume** - Adjust background music (0-100%)
5. **Refresh Weather Data** - Force update

## 🗂️ Project Structure

```
WeatherStar-4000-Python/
├── weatherstar4000.py          # Main application
├── weatherstar_logger.py       # Logging utilities
├── run_weatherstar.py          # Python launcher
├── run_weatherstar.bat         # Windows launcher
├── run_weatherstar.sh          # Linux/Mac launcher
├── convert_fonts.py            # Font conversion utility
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
├── README.md                   # Documentation
├── .gitignore                  # Git ignore rules
├── weatherstar_assets/         # All assets
│   ├── fonts/                  # Original WOFF fonts
│   ├── fonts_ttf/              # Converted TTF fonts
│   ├── music/                  # 75+ background tracks
│   ├── icons/                  # Weather condition icons
│   ├── logos/                  # WeatherStar logos
│   └── backgrounds/            # Display backgrounds
└── logs/                       # Runtime logs (auto-created)
```

## 🛠️ Configuration

### Manual Location
When prompted, enter your latitude and longitude:
```
Latitude: 40.7128
Longitude: -74.0060
```

Find your coordinates at [LatLong.net](https://www.latlong.net/)

### Auto-Detection
Press Enter when prompted to use IP-based location detection.

## 📝 Logging

Comprehensive logging is saved to the `logs/` directory:
- `weatherstar_main.log` - General application logs
- `weatherstar_display.log` - Display mode changes
- `weatherstar_weather.log` - Weather API interactions
- `weatherstar_error.log` - Error tracking

## 🌐 Data Sources

- **Weather Data**: [NOAA/NWS API](https://api.weather.gov) (US only)
- **Radar Images**: [Iowa State Mesonet](https://mesonet.agron.iastate.edu)
- **Location Detection**: [ipapi.co](https://ipapi.co)

## 🏗️ Building from Source

### Converting Fonts
If you need to convert WOFF fonts to TTF:
```bash
python convert_fonts.py
```

### Installing Optional Dependencies
For enhanced astronomy calculations:
```bash
pip install ephem
```

## 🐛 Troubleshooting

### No Sound/Music
- Check music files exist in `weatherstar_assets/music/`
- Verify pygame mixer initialized (check logs)
- Adjust volume in settings menu (Right-click → 4)

### Display Issues
- Ensure 640x480 resolution is supported
- Check all assets are in `weatherstar_assets/`
- Review error logs in `logs/weatherstar_error.log`

### Weather Data Not Loading
- Verify internet connection
- Check location is within the US (NOAA API limitation)
- Review API logs in `logs/weatherstar_weather.log`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Bug fixes
- New display modes
- International weather API support
- Performance improvements
- Additional nostalgic music tracks

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Original WeatherStar 4000 by The Weather Channel
- [ws4kp](https://github.com/netbymatt/ws4kp) JavaScript implementation for reference
- NOAA/NWS for weather data API
- The Weather Channel music composers of the 1990s

## 🎯 Roadmap

- [ ] International weather support (non-US locations)
- [ ] Custom color themes
- [ ] Weather history graphs
- [ ] Severe weather animations
- [ ] Voice narration option
- [ ] Web interface for remote viewing
- [ ] Mobile companion app

## 📺 Screenshots

### Current Conditions
![Current Conditions](weatherstar_assets/screenshots/current.png)

### Local Forecast
![Local Forecast](weatherstar_assets/screenshots/forecast.png)

### Local Radar
![Radar](weatherstar_assets/screenshots/radar.png)

---

**Made with ❤️ for weather enthusiasts and 90s nostalgia lovers**

*Not affiliated with The Weather Channel or IBM*