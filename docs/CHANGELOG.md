# WeatherStar 4000 Python - Changelog

## Updates - September 16, 2025

### UI/UX Improvements

#### 1. Local News Display
- **Fixed**: City name font size reduced by 50% to prevent overflow with long city names
- **Implementation**: City name now uses smaller font (14px) and is properly centered below "LOCAL NEWS"

#### 2. Local Forecast Layout
- **Fixed**: Column positioning adjusted for better balance
  - TODAY box moved 10px to the right
  - Last column moved 10px to the left
- **Fixed**: Font size reduced from 32px to 24px for forecast text
- **Implementation**: Added new `font_forecast` for better text fitting

#### 3. Animated Weather Icons
- **New Feature**: Full support for animated GIF weather icons
- **Implementation**: Created `animated_icons.py` module with:
  - GIF frame extraction using PIL/Pillow
  - Time-based animation cycling
  - Automatic fallback to static images if PIL not available
  - Icon caching and preloading for performance

#### 4. Radar Display Optimization
- **Fixed**: Radar stuttering issue by preloading radar data
- **Implementation**: Radar image now fetched during weather data update cycle
- **Performance**: Eliminated frame drops when switching to radar view

#### 5. Air Quality & Health Display
- **Fixed**: Pollen count bar alignment issues
- **Fixed**: Health recommendations text overflow
- **Implementation**:
  - Aligned all pollen bars to fixed position
  - Added text wrapping for health recommendations
  - Implemented auto-scrolling for long recommendation lists
  - Using smaller fonts for better fit

#### 6. Sun & Moon Data Display
- **Fixed**: Font overlaps in data columns
- **Implementation**:
  - Reduced font sizes from extended/small to normal/tiny
  - Dynamic label width calculation to prevent overlaps
  - Adjusted line spacing from 28px to 24px

#### 7. Weekend Forecast
- **Fixed**: Layout changed from single column to 2-column display
- **Implementation**:
  - Saturday and Sunday side-by-side columns
  - Hourly forecast background (background '4')
  - Day/Night periods with weather icons
  - Text wrapping for forecast descriptions

#### 8. 7-Day Temperature Graph
- **New Feature**: Color-coded temperature bars
- **Implementation**:
  - Gradient colors from blue (cold) to red (hot)
  - Temperature ranges:
    - < 32°F: Light blue (freezing)
    - 32-50°F: Lighter blue (cold)
    - 50-65°F: Light green (cool)
    - 65-75°F: Yellow (mild)
    - 75-85°F: Orange (warm)
    - > 85°F: Red (hot)
  - Multi-step gradient rendering for smooth color transitions
- **Fixed**: Graph positioning raised 5px
- **Fixed**: Day labels raised 10px closer to graph

### Technical Improvements

1. **Module Organization**:
   - New `animated_icons.py` module for GIF support
   - Improved icon management with caching

2. **Performance Optimizations**:
   - Radar preloading prevents UI stuttering
   - Icon animations use time-based updates
   - Efficient text caching with LRU cache

3. **Code Quality**:
   - Better error handling for missing dependencies
   - Graceful fallbacks for animation support
   - Improved text rendering with dynamic sizing

### Dependencies
- pygame (required)
- PIL/Pillow (optional, for animated GIFs)
- requests (required)

### Compatibility
- Tested on Raspberry Pi 3B+, 4, and Zero 2W
- Python 3.7+
- All fixes maintain backwards compatibility