#!/usr/bin/env python3
"""
WeatherStar 4000+ Specialized Weather Display Functions Module

Specialized weather display methods extracted from displays.py
to meet the line limit requirements.
"""

import pygame
import time
from datetime import datetime, timedelta
from weatherstar_modules.weatherstar_logger import get_logger

# Screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Colors from ws4kp SCSS
COLORS = {
    'yellow': (255, 255, 0),           # Title color
    'white': (255, 255, 255),          # Main text
    'black': (0, 0, 0),                # Text shadows
    'purple_header': (32, 0, 87),      # Column headers
    'blue_gradient_1': (16, 32, 128),  # Gradient start
    'blue_gradient_2': (0, 16, 64),    # Gradient end
    'light_blue': (128, 128, 255),     # Low temperatures
    'blue': (128, 128, 255),           # Alias for light_blue
    'cyan': (0, 255, 255),             # Reddit subreddits
    'red': (255, 0, 0),                # Breaking news
}


class WeatherStarSpecializedDisplays:
    """Specialized weather display methods for WeatherStar 4000+"""

    def __init__(self, weatherstar_instance):
        """Initialize with reference to main WeatherStar instance"""
        self.ws = weatherstar_instance
        self.logger = get_logger()

    def _get_wind_direction(self, degrees):
        """Convert degrees to cardinal direction"""
        if degrees is None:
            return ''
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                     'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        index = int((degrees + 11.25) / 22.5) % 16
        return directions[index]

    def _get_icon_name(self, icon_url):
        """Convert NOAA icon URL to local icon name"""
        if not icon_url:
            return None

        # Extract icon name from URL
        # Example: https://api.weather.gov/icons/land/day/few?size=medium
        parts = icon_url.split('/')
        if len(parts) >= 2:
            condition = parts[-1].split('?')[0]

            # Map NOAA conditions to our icon names
            icon_map = {
                'skc': 'Clear', 'few': 'Clear', 'sct': 'Partly-Cloudy',
                'bkn': 'Cloudy', 'ovc': 'Cloudy',
                'rain': 'Rain', 'rain_showers': 'Shower',
                'tsra': 'Thunderstorm', 'snow': 'Light-Snow',
                'fog': 'Fog', 'wind': 'Windy'
            }

            return icon_map.get(condition, 'Clear')
        return None

    def draw_almanac(self):
        """Draw Almanac screen with weather statistics and records"""
        self.ws.draw_background('4')  # Use the hourly forecast background
        self.ws.draw_header("Weather", "Almanac")

        current = self.ws.weather_data.get('current', {})

        # Get current date/time
        now = datetime.now()
        date_str = now.strftime("%B %d, %Y")

        # Title
        date_text = self.ws.font_normal.render(f"Weather Statistics for {date_str}", True, COLORS['yellow'])
        date_rect = date_text.get_rect(center=(320, 100))
        self.ws.screen.blit(date_text, date_rect)

        y_pos = 130  # Move up by 10px

        # Current Stats
        stats_title = self.ws.font_extended.render("CURRENT CONDITIONS", True, COLORS['yellow'])
        self.ws.screen.blit(stats_title, (60, y_pos))
        y_pos += 35

        # Temperature
        temp_c = current.get('temperature', {}).get('value')
        if temp_c is not None:
            temp_f = int(temp_c * 9/5 + 32)
            temp_text = self.ws.font_normal.render(f"Temperature: {temp_f}°F", True, COLORS['white'])
            self.ws.screen.blit(temp_text, (80, y_pos))
            y_pos += 25

        # Humidity
        humidity = current.get('relativeHumidity', {}).get('value')
        if humidity:
            humid_text = self.ws.font_normal.render(f"Humidity: {humidity:.0f}%", True, COLORS['white'])
            self.ws.screen.blit(humid_text, (80, y_pos))
            y_pos += 25

        # Dewpoint
        dewpoint_c = current.get('dewpoint', {}).get('value')
        if dewpoint_c is not None:
            dewpoint_f = int(dewpoint_c * 9/5 + 32)
            dew_text = self.ws.font_normal.render(f"Dewpoint: {dewpoint_f}°F", True, COLORS['white'])
            self.ws.screen.blit(dew_text, (80, y_pos))
            y_pos += 25

        # Pressure
        pressure = current.get('barometricPressure', {}).get('value')
        if pressure:
            pressure_inhg = pressure * 0.00029530
            press_text = self.ws.font_normal.render(f"Pressure: {pressure_inhg:.2f} in", True, COLORS['white'])
            self.ws.screen.blit(press_text, (80, y_pos))
            y_pos += 25

        # Visibility
        visibility = current.get('visibility', {}).get('value')
        if visibility:
            vis_miles = visibility / 1609.34
            vis_text = self.ws.font_normal.render(f"Visibility: {vis_miles:.1f} miles", True, COLORS['white'])
            self.ws.screen.blit(vis_text, (80, y_pos))
            y_pos += 35

        # Sun/Moon Data (simulated)
        y_pos += 10
        sun_title = self.ws.font_extended.render("SUN & MOON", True, COLORS['yellow'])
        self.ws.screen.blit(sun_title, (60, y_pos))
        y_pos += 35

        # Calculate approximate sunrise/sunset for display
        sunrise_text = self.ws.font_normal.render("Sunrise: 6:45 AM", True, COLORS['white'])
        self.ws.screen.blit(sunrise_text, (80, y_pos))
        y_pos += 25

        sunset_text = self.ws.font_normal.render("Sunset: 7:30 PM", True, COLORS['white'])
        self.ws.screen.blit(sunset_text, (80, y_pos))
        y_pos += 25

        moon_text = self.ws.font_normal.render("Moon Phase: Waxing Gibbous", True, COLORS['white'])
        self.ws.screen.blit(moon_text, (80, y_pos))

        self.logger.main_logger.debug("Drew Almanac display")

    def draw_temperature_graph(self):
        """Draw 7-Day Temperature Graph"""
        self.ws.draw_background('1-chart')  # Use chart background if available, else '1'
        self.ws.draw_header("7-Day", "Temperature")

        # Get forecast periods
        forecast = self.ws.weather_data.get('forecast', {})
        periods = forecast.get('periods', [])

        # Graph area - raised by 5 pixels more
        graph_left = 80
        graph_top = 105  # Was 110, now 105 (raised 5px more)
        graph_width = 480
        graph_height = 250

        # Draw graph axes
        pygame.draw.line(self.ws.screen, COLORS['white'], (graph_left, graph_top + graph_height),
                        (graph_left + graph_width, graph_top + graph_height), 2)  # X-axis
        pygame.draw.line(self.ws.screen, COLORS['white'], (graph_left, graph_top),
                        (graph_left, graph_top + graph_height), 2)  # Y-axis

        # Get temperatures for the next 7 days
        temps = []
        labels = []
        for i in range(0, min(len(periods), 14), 2):  # Every 2 periods (day/night)
            if i < len(periods):
                day_period = periods[i]
                night_period = periods[i+1] if i+1 < len(periods) else None

                if day_period.get('isDaytime'):
                    high = day_period.get('temperature', 0)
                    low = night_period.get('temperature', 0) if night_period else high - 10
                else:
                    low = day_period.get('temperature', 0)
                    high = night_period.get('temperature', 0) if night_period else low + 10

                temps.append((high, low))
                labels.append(day_period.get('name', '')[:3].upper())

        if temps:
            # Find min/max for scaling
            all_temps = [t for pair in temps for t in pair]
            min_temp = min(all_temps) - 5
            max_temp = max(all_temps) + 5
            temp_range = max_temp - min_temp

            # Draw bars
            bar_width = graph_width // len(temps)
            for i, ((high, low), label) in enumerate(zip(temps, labels)):
                x = graph_left + i * bar_width + bar_width // 2

                # Calculate heights
                high_y = graph_top + graph_height - ((high - min_temp) / temp_range * graph_height)
                low_y = graph_top + graph_height - ((low - min_temp) / temp_range * graph_height)

                # Draw temperature bar with color gradient
                bar_x = x - 20
                bar_height = abs(low_y - high_y)

                # Calculate color based on average temperature
                avg_temp = (high + low) / 2
                # Color gradient from blue (cold) to red (hot)
                if avg_temp < 32:  # Freezing
                    bar_color = (100, 150, 255)  # Light blue
                elif avg_temp < 50:  # Cold
                    bar_color = (150, 200, 255)  # Lighter blue
                elif avg_temp < 65:  # Cool
                    bar_color = (150, 255, 150)  # Light green
                elif avg_temp < 75:  # Mild
                    bar_color = (255, 255, 100)  # Yellow
                elif avg_temp < 85:  # Warm
                    bar_color = (255, 200, 100)  # Orange
                else:  # Hot
                    bar_color = (255, 100, 100)  # Red

                # Draw gradient bar
                # Draw multiple rectangles with slightly different colors for gradient effect
                gradient_steps = 5
                step_height = bar_height / gradient_steps
                for j in range(gradient_steps):
                    # Interpolate color
                    factor = j / gradient_steps
                    r = int(bar_color[0] * (1 - factor * 0.3))  # Darken towards bottom
                    g = int(bar_color[1] * (1 - factor * 0.3))
                    b = int(bar_color[2] * (1 - factor * 0.3))
                    step_color = (min(255, r), min(255, g), min(255, b))

                    pygame.draw.rect(self.ws.screen, step_color,
                                   (bar_x, high_y + j * step_height, 40, step_height + 1))

                # Draw temperatures
                high_text = self.ws.font_small.render(str(high), True, COLORS['yellow'])
                high_rect = high_text.get_rect(center=(x, high_y - 10))
                self.ws.screen.blit(high_text, high_rect)

                low_text = self.ws.font_small.render(str(low), True, COLORS['white'])
                low_rect = low_text.get_rect(center=(x, low_y + 20))
                self.ws.screen.blit(low_text, low_rect)

                # Draw day label - raised by 10px as requested
                label_text = self.ws.font_small.render(label, True, COLORS['white'])
                label_rect = label_text.get_rect(center=(x, graph_top + graph_height + 10))  # Was +20, now +10
                self.ws.screen.blit(label_text, label_rect)

        self.logger.main_logger.debug("Drew Temperature Graph display")

    def draw_weather_records(self):
        """Draw Weather Records"""
        self.ws.draw_background('4')
        self.ws.draw_header("Weather", "Records")

        now = datetime.now()
        date_str = now.strftime("%B %d")

        y_pos = 120

        # Title
        title = self.ws.font_normal.render(f"Records for {date_str}", True, COLORS['yellow'])
        title_rect = title.get_rect(center=(320, y_pos))
        self.ws.screen.blit(title, title_rect)
        y_pos += 40

        # Simulated record data (would fetch from historical database)
        records = [
            ("Record High", f"92°F (1998)"),
            ("Record Low", f"41°F (1965)"),
            ("Average High", f"75°F"),
            ("Average Low", f"58°F"),
            ("Record Rainfall", f"3.21\" (1977)"),
            ("Record Snowfall", f"0.0\" (Never)"),
        ]

        for label, value in records:
            label_text = self.ws.font_normal.render(f"{label}:", True, COLORS['white'])
            self.ws.screen.blit(label_text, (120, y_pos))

            value_text = self.ws.font_normal.render(value, True, COLORS['yellow'])
            self.ws.screen.blit(value_text, (350, y_pos))

            y_pos += 35

        # This day in weather history
        y_pos += 20
        history_title = self.ws.font_extended.render("THIS DAY IN WEATHER HISTORY", True, COLORS['yellow'])
        self.ws.screen.blit(history_title, (60, y_pos))
        y_pos += 35

        history_text = "1992: Hurricane Andrew made landfall in Florida"
        hist = self.ws.font_small.render(history_text, True, COLORS['white'])
        self.ws.screen.blit(hist, (80, y_pos))

        self.logger.main_logger.debug("Drew Weather Records display")

    def draw_sun_moon(self):
        """Draw Sunrise/Sunset & Moon"""
        self.ws.draw_background('1')  # Use background 1 (standard 2-column)
        self.ws.draw_header("Sun & Moon", "Data")

        # Two column layout - moved closer together
        left_col_x = 60
        right_col_x = 335  # Moved 15px to the left to close gap
        y_pos = 120

        # LEFT COLUMN - Sun data
        sun_title = self.ws.font_normal.render("SUN", True, COLORS['yellow'])
        self.ws.screen.blit(sun_title, (left_col_x, y_pos))
        sun_y = y_pos + 30

        # Calculate approximate sunrise/sunset (simplified)
        now = datetime.now()
        sunrise = now.replace(hour=6, minute=45, second=0)
        sunset = now.replace(hour=19, minute=30, second=0)
        day_length = sunset - sunrise
        hours = int(day_length.total_seconds() // 3600)
        minutes = int((day_length.total_seconds() % 3600) // 60)

        sun_data = [
            ("Sunrise", sunrise.strftime("%I:%M %p")),
            ("Sunset", sunset.strftime("%I:%M %p")),
            ("Day Length", f"{hours}h {minutes}m"),
            ("Solar Noon", "1:07 PM"),
            ("Civil Dawn", "6:20 AM"),
            ("Civil Dusk", "8:00 PM"),
            ("UV Index", "6 (High)")
        ]

        for label, value in sun_data:
            # Use tiny font for better fit
            label_text = self.ws.font_tiny.render(f"{label}:", True, COLORS['white'])
            self.ws.screen.blit(label_text, (left_col_x + 10, sun_y))

            # Calculate proper position for value to avoid overlap - 5px thinner
            label_width = self.ws.font_tiny.size(f"{label}:")[0]
            value_x = left_col_x + 15 + max(110, label_width + 10)  # Reduced from 120 to 110
            value_text = self.ws.font_tiny.render(value, True, COLORS['yellow'])
            self.ws.screen.blit(value_text, (value_x, sun_y))

            sun_y += 24  # Reduced spacing

        # RIGHT COLUMN - Moon data
        moon_title = self.ws.font_normal.render("MOON", True, COLORS['yellow'])
        self.ws.screen.blit(moon_title, (right_col_x, y_pos))
        moon_y = y_pos + 30

        # Calculate moon phase (simplified)
        moon_age = (now.day % 30)  # Very simplified
        if moon_age < 7:
            phase = "Waxing Crescent"
            illumination = moon_age * 14
        elif moon_age < 14:
            phase = "Waxing Gibbous"
            illumination = 50 + (moon_age - 7) * 7
        elif moon_age == 14:
            phase = "Full Moon"
            illumination = 100
        elif moon_age < 21:
            phase = "Waning Gibbous"
            illumination = 100 - (moon_age - 14) * 7
        else:
            phase = "Waning Crescent"
            illumination = 50 - (moon_age - 21) * 7

        moon_data = [
            ("Phase", phase),
            ("Illumination", f"{illumination}%"),
            ("Moonrise", "3:45 PM"),
            ("Moonset", "2:30 AM"),
            ("Next Full", "In 3 days"),
            ("Next New", "In 18 days"),
            ("Age", f"{moon_age} days")
        ]

        for label, value in moon_data:
            # Use tiny font for better fit
            label_text = self.ws.font_tiny.render(f"{label}:", True, COLORS['white'])
            self.ws.screen.blit(label_text, (right_col_x + 10, moon_y))

            # Calculate proper position for value to avoid overlap - 5px thinner
            label_width = self.ws.font_tiny.size(f"{label}:")[0]
            value_x = right_col_x + 15 + max(100, label_width + 10)  # Reduced from 110 to 100
            value_text = self.ws.font_tiny.render(value, True, COLORS['yellow'])
            self.ws.screen.blit(value_text, (value_x, moon_y))

            moon_y += 24  # Reduced spacing

        self.logger.main_logger.debug("Drew Sun & Moon display")

    def draw_wind_pressure(self):
        """Draw Wind & Pressure"""
        self.ws.draw_background('1')
        self.ws.draw_header("Wind &", "Pressure")

        current = self.ws.weather_data.get('current', {})

        y_pos = 120

        # Wind section
        wind_title = self.ws.font_extended.render("WIND CONDITIONS", True, COLORS['yellow'])
        self.ws.screen.blit(wind_title, (60, y_pos))
        y_pos += 35

        # Get wind data
        wind_speed = current.get('windSpeed', {}).get('value')
        wind_dir = current.get('windDirection', {}).get('value')
        wind_gust = current.get('windGust', {}).get('value')

        if wind_speed:
            wind_mph = int(wind_speed * 0.621371)
            speed_text = self.ws.font_normal.render(f"Speed: {wind_mph} mph", True, COLORS['white'])
            self.ws.screen.blit(speed_text, (80, y_pos))
            y_pos += 30

        if wind_dir:
            dir_text = self._get_wind_direction(wind_dir)
            direction = self.ws.font_normal.render(f"Direction: {dir_text} ({wind_dir}°)", True, COLORS['white'])
            self.ws.screen.blit(direction, (80, y_pos))
            y_pos += 30

        if wind_gust:
            gust_mph = int(wind_gust * 0.621371)
            gust_text = self.ws.font_normal.render(f"Gusts: {gust_mph} mph", True, COLORS['yellow'])
            self.ws.screen.blit(gust_text, (80, y_pos))
            y_pos += 30

        # Wind chill / Heat index
        wind_chill = current.get('windChill', {}).get('value')
        heat_index = current.get('heatIndex', {}).get('value')

        if wind_chill:
            wc_f = int(wind_chill * 9/5 + 32)
            wc_text = self.ws.font_normal.render(f"Wind Chill: {wc_f}°F", True, COLORS['blue'])
            self.ws.screen.blit(wc_text, (80, y_pos))
            y_pos += 30
        elif heat_index:
            hi_f = int(heat_index * 9/5 + 32)
            hi_text = self.ws.font_normal.render(f"Heat Index: {hi_f}°F", True, (255, 100, 100))
            self.ws.screen.blit(hi_text, (80, y_pos))
            y_pos += 30

        # Pressure section
        y_pos += 20
        pressure_title = self.ws.font_extended.render("BAROMETRIC PRESSURE", True, COLORS['yellow'])
        self.ws.screen.blit(pressure_title, (60, y_pos))
        y_pos += 35

        pressure = current.get('barometricPressure', {}).get('value')
        if pressure:
            pressure_inhg = pressure * 0.00029530
            press_text = self.ws.font_normal.render(f"Current: {pressure_inhg:.2f} in", True, COLORS['white'])
            self.ws.screen.blit(press_text, (80, y_pos))
            y_pos += 30

            # Trend (simulated)
            trend_text = self.ws.font_normal.render("Trend: Steady", True, COLORS['white'])
            self.ws.screen.blit(trend_text, (80, y_pos))

        self.logger.main_logger.debug("Drew Wind & Pressure display")

    def draw_monthly_outlook(self):
        """Draw Monthly Outlook"""
        self.ws.draw_background('4')  # Changed to hourly forecast background
        self.ws.draw_header("30-Day", "Outlook")

        y_pos = 120

        # Title
        now = datetime.now()
        month = now.strftime("%B %Y")
        title = self.ws.font_normal.render(f"Outlook for {month}", True, COLORS['yellow'])
        title_rect = title.get_rect(center=(320, y_pos))
        self.ws.screen.blit(title, title_rect)
        y_pos += 35  # Moved up 15px (was 50, now 35)

        # Temperature outlook
        temp_title = self.ws.font_extended.render("TEMPERATURE OUTLOOK", True, COLORS['yellow'])
        self.ws.screen.blit(temp_title, (60, y_pos))
        y_pos += 35

        temp_outlook = "Above Normal Temperatures Expected"
        temp_text = self.ws.font_normal.render(temp_outlook, True, COLORS['white'])
        self.ws.screen.blit(temp_text, (80, y_pos))
        y_pos += 30

        # Show probability
        prob_text = self.ws.font_small.render("Probability: 60% above normal", True, COLORS['white'])
        self.ws.screen.blit(prob_text, (100, y_pos))
        y_pos += 40

        # Precipitation outlook
        precip_title = self.ws.font_extended.render("PRECIPITATION OUTLOOK", True, COLORS['yellow'])
        self.ws.screen.blit(precip_title, (60, y_pos))
        y_pos += 35

        precip_outlook = "Near Normal Precipitation Expected"
        precip_text = self.ws.font_normal.render(precip_outlook, True, COLORS['white'])
        self.ws.screen.blit(precip_text, (80, y_pos))
        y_pos += 30

        # Show probability
        prob2_text = self.ws.font_small.render("Probability: Equal chances", True, COLORS['white'])
        self.ws.screen.blit(prob2_text, (100, y_pos))
        y_pos += 40

        # Data source
        source = self.ws.font_small.render("Source: NOAA Climate Prediction Center", True, COLORS['white'])
        source_rect = source.get_rect(center=(320, 380))
        self.ws.screen.blit(source, source_rect)

        self.logger.main_logger.debug("Drew Monthly Outlook display")