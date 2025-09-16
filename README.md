# 🌤️ WeatherStar 4000+ Python Edition

A faithful Python recreation of the iconic Weather Channel WeatherStar 4000 system from the late 1990s, bringing nostalgic weather displays to modern hardware.

## 📺 What is WeatherStar 4000?

The WeatherStar 4000 was the computer system used by The Weather Channel from 1990-1998 to generate local weather information for cable TV viewers. This project recreates that classic experience with authentic graphics, fonts, music, and display modes.

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

### 🆕 Enhanced Features (New!)
- **Marine/Beach Forecast** - Coastal conditions, tides, wave heights
- **Air Quality & Health** - AQI, pollen counts, health recommendations
- **7-Day Temperature Graph** - Visual temperature trends
- **Weather Records** - Historical comparisons
- **Sun & Moon Data** - Detailed astronomy information
- **Wind & Pressure Analysis** - Detailed atmospheric conditions
- **Weekend Forecast** - Focused weekend weather
- **Monthly Outlook** - Extended 30-day trends

### 🎵 Nostalgic Experience
- Authentic smooth jazz background music from the 90s
- Original Star4000 fonts
- Classic blue gradient backgrounds
- Smooth transitions between displays
- Bottom scroll with current conditions

### 📊 Smart Features
- **Weather Trend Arrows** - Rising/falling indicators for temperature and pressure
- **Historical Comparisons** - Current vs. 30-year averages
- **Precipitation Tracking** - 24hr, 7-day, monthly accumulation
- **Right-Click Settings Menu** - Customize display options
- **Auto Location Detection** - Uses IP geolocation or manual entry

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Windows, Mac, or Linux (Raspberry Pi supported!)

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