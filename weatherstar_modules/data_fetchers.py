#!/usr/bin/env python3
"""
WeatherStar 4000+ Data Fetching Module

All data fetching and API-related methods extracted from the main weatherstar4000.py file
to reduce the main file size and improve organization.
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import io
import pygame


class WeatherStarDataFetchers:
    """Data fetching methods for WeatherStar 4000+"""

    def __init__(self, weatherstar_instance):
        """Initialize with reference to main WeatherStar instance"""
        self.ws = weatherstar_instance
        # Import logger from main module
        from weatherstar_modules.weatherstar_logger import get_logger
        self.logger = get_logger()

    def get_cached_city_name(self):
        """Get city name with caching to avoid repeated API calls"""
        # Cache for 1 hour (3600 seconds)
        if self.ws.cached_city_name and (time.time() - self.ws.city_name_cached_at) < 3600:
            return self.ws.cached_city_name

        # Get fresh city name
        from weatherstar_modules import get_local_news
        self.ws.cached_city_name = get_local_news.get_city_name_from_coords(self.ws.lat, self.ws.lon)
        self.ws.city_name_cached_at = time.time()
        self.logger.main_logger.info(f"Updated cached city name: {self.ws.cached_city_name}")
        return self.ws.cached_city_name

    def fetch_real_news(self, source):
        """Fetch real news headlines from APIs (future enhancement)"""
        # This would use requests to fetch real headlines
        # For MSN: Could scrape or use news API
        # For Reddit: Use Reddit API or PRAW library
        pass

    def fetch_radar_image(self):
        """Fetch REAL radar from NOAA/weather.gov with regional zoom and animation"""
        try:
            import pygame
            import io
            from PIL import Image

            self.logger.main_logger.info(f"Fetching regional radar for lat:{self.ws.lat}, lon:{self.ws.lon}")

            # Try to get animated frames
            self.ws.radar_frames = []

            # Try to get multiple frames for animation (last 5 frames)
            for i in range(5, -1, -1):  # Get 6 frames, newest to oldest
                radar_urls = [
                    # Try higher resolution first
                    f"https://radar.weather.gov/ridge/standard/CONUS-LARGE_{i}.gif",
                    # Standard resolution fallback
                    f"https://radar.weather.gov/ridge/standard/CONUS_{i}.gif",
                    # Try lite version if others fail
                    f"https://radar.weather.gov/ridge/lite/N0R/CONUS_{i}.png",
                ]

                for url in radar_urls:
                    try:
                        response = requests.get(url, timeout=3, headers={'User-Agent': 'WeatherStar4000'})

                        if response.status_code == 200 and len(response.content) > 1000:
                            # Load the image
                            img_data = io.BytesIO(response.content)

                            # Use PIL to handle GIF properly
                            pil_img = Image.open(img_data)
                            # Convert to RGB if necessary
                            if pil_img.mode != 'RGB':
                                pil_img = pil_img.convert('RGB')

                            # Crop to zoom in on location
                            crop_box = self._calculate_crop_area(self.ws.lat, self.ws.lon, pil_img.size)
                            pil_img = pil_img.crop(crop_box)

                            # Use high-quality resizing with PIL before converting to pygame
                            # This gives much smoother results than pygame's scale
                            from PIL import Image
                            pil_img = pil_img.resize((500, 300), Image.LANCZOS)

                            # Apply slight blur to reduce pixelation
                            from PIL import ImageFilter
                            pil_img = pil_img.filter(ImageFilter.SMOOTH)

                            # Convert to pygame surface
                            img_bytes = io.BytesIO()
                            pil_img.save(img_bytes, 'PNG')
                            img_bytes.seek(0)
                            radar_img = pygame.image.load(img_bytes)

                            self.ws.radar_frames.append(radar_img)
                            self.logger.main_logger.debug(f"Loaded frame {i} from {url}")
                            break

                    except Exception as e:
                        self.logger.main_logger.debug(f"Failed to load frame {i} from {url}: {e}")
                        continue

            # If we got frames, set up animation
            if self.ws.radar_frames:
                # Reverse so oldest frame is first
                self.ws.radar_frames.reverse()
                self.ws.radar_image = self.ws.radar_frames[-1]  # Latest frame
                self.ws.radar_frame_index = 0
                self.logger.main_logger.info(f"Successfully loaded {len(self.ws.radar_frames)} radar frames")
                return True

            # If no frames loaded, try static image
            if not self.ws.radar_frames:
                # Try static GOES satellite image
                try:
                    # This is a free sample tile - no API key needed
                    url = "https://tile.openweathermap.org/map/precipitation_new/3/3/2.png?appid=1234567890"
                    response = requests.get(url, timeout=3)

                    if response.status_code == 200:
                        img_data = io.BytesIO(response.content)
                        radar_img = pygame.image.load(img_data)

                        # Create a base map
                        base = pygame.Surface((500, 300))
                        base.fill((0, 30, 60))

                        # Scale and center the radar tile
                        scaled = pygame.transform.scale(radar_img, (400, 240))
                        base.blit(scaled, (50, 30))

                        self.ws.radar_frames = [base]
                        self.ws.radar_image = base
                        radar_loaded = True
                        self.logger.main_logger.info("Loaded OpenWeatherMap radar tile")

                except:
                    pass

            if not radar_loaded:
                # Last resort - just create a placeholder
                self.logger.main_logger.warning("Could not fetch real radar, using placeholder")

                placeholder = pygame.Surface((500, 300))
                placeholder.fill((0, 30, 60))

                font = pygame.font.Font(None, 36)
                text1 = font.render("RADAR DATA", True, (255, 255, 255))
                text2 = font.render("TEMPORARILY UNAVAILABLE", True, (255, 255, 0))

                placeholder.blit(text1, (150, 120))
                placeholder.blit(text2, (80, 160))

                self.ws.radar_frames = [placeholder]
                self.ws.radar_image = placeholder

            return True

        except Exception as e:
            self.logger.main_logger.error(f"Failed to fetch real radar: {e}")
            return False

    def _get_regional_radar_id(self, lat, lon):
        """Get the best NOAA radar site ID for given coordinates"""
        # Virginia is at 38.09 lat, -78.56 lon
        # Should be in mid-Atlantic region, not Southeast

        # Regional radar sectors based on US regions
        if lon < -100:  # West
            if lat > 42:
                return "PACNORTHWEST"  # Pacific Northwest
            elif lat > 35:
                return "PACSOUTHWEST"  # California/Nevada
            else:
                return "SOUTHROCKIES"  # Southwest
        elif lon < -85:  # Central
            if lat > 42:
                return "NORTHROCKIES"  # Northern Plains
            elif lat > 35:
                return "SOUTHPLAINS"  # Southern Plains
            else:
                return "SOUTHMISSVLY"  # Texas/Louisiana
        else:  # East (lon >= -85)
            if lat > 40:  # North of DC line
                return "NORTHEAST"  # Northeast/New England
            elif lat > 36:  # Virginia/NC/Mid-Atlantic
                return "CENTGRTLAKES"  # Central/Great Lakes (covers mid-Atlantic better)
            elif lat > 30:  # Deep South
                return "SOUTHEAST"  # Southeast
            else:
                return "SOUTHEAST"  # Florida

    def _calculate_crop_area(self, lat, lon, img_size):
        """Calculate crop area for zooming into CONUS radar"""
        width, height = img_size

        # CONUS map bounds (approximate)
        # West to East: -125 to -65 (60 degrees)
        # South to North: 24 to 50 (26 degrees)

        # Normalize coordinates to 0-1 range
        # For X: Map -125 (west) to 0, and -65 (east) to 1
        x_norm = (lon + 125) / 60  # Add 125 to make positive, then divide by range

        # For Y: Map 24 (south) to 1, and 50 (north) to 0 (inverted for image coords)
        y_norm = (50 - lat) / 26   # Subtract from north edge, divide by range

        # Clamp to valid range
        x_norm = max(0, min(1, x_norm))
        y_norm = max(0, min(1, y_norm))

        # Calculate center point in image
        center_x = int(width * x_norm)
        center_y = int(height * y_norm)

        # Crop box (zoom level - smaller = more zoomed)
        box_width = width // 5  # Show 1/5 of the width (more zoomed in)
        box_height = height // 5  # Show 1/5 of the height

        # Calculate crop boundaries
        left = max(0, center_x - box_width // 2)
        top = max(0, center_y - box_height // 2)

        # Adjust if we're at the edge
        if left + box_width > width:
            left = width - box_width
        if top + box_height > height:
            top = height - box_height

        right = min(width, left + box_width)
        bottom = min(height, top + box_height)

        return (left, top, right, bottom)

    def _create_realistic_radar_frame(self, frame_num):
        """Create a single realistic radar frame"""
        import pygame
        import pygame.gfxdraw
        import random
        import math

        # Create surface
        radar = pygame.Surface((512, 512), pygame.SRCALPHA)
        radar.fill((0, 20, 40, 255))  # Dark blue background

        # Draw US map outline
        self._draw_detailed_us_map(radar)

        # Create realistic weather systems
        # 1. Major frontal system moving west to east
        front_x = 150 + (frame_num * 30)  # Moving eastward

        # Draw the main frontal band
        for segment in range(8):
            y = 140 + segment * 30
            x = front_x + random.randint(-20, 20)

            # Create storm cells along the front
            for offset in range(-60, 60, 15):
                cell_x = x + offset + random.randint(-10, 10)
                cell_y = y + random.randint(-15, 15)

                if 50 < cell_x < 480 and 100 < cell_y < 380:
                    # Intensity varies along the front
                    if -20 < offset < 20:
                        # Core of the storm
                        self._draw_storm_cell(radar, cell_x, cell_y, 'heavy', frame_num)
                    elif -40 < offset < 40:
                        # Moderate precipitation
                        self._draw_storm_cell(radar, cell_x, cell_y, 'moderate', frame_num)
                    else:
                        # Light precipitation
                        self._draw_storm_cell(radar, cell_x, cell_y, 'light', frame_num)

        # 2. Add scattered showers
        for _ in range(random.randint(3, 6)):
            x = random.randint(100, 450)
            y = random.randint(150, 350)
            self._draw_storm_cell(radar, x, y, 'scattered', frame_num)

        # 3. Add lake effect snow (Great Lakes region)
        if frame_num % 2 == 0:
            # Near Great Lakes
            for _ in range(random.randint(2, 4)):
                x = random.randint(320, 380)
                y = random.randint(140, 180)
                self._draw_storm_cell(radar, x, y, 'snow', frame_num)

        return radar

    def _draw_storm_cell(self, surface, x, y, intensity, frame_num):
        """Draw a realistic storm cell"""
        import pygame.gfxdraw
        import random

        # Define colors and sizes for different intensities
        configs = {
            'heavy': {
                'colors': [(255, 0, 0, 180), (255, 100, 0, 150), (255, 200, 0, 120)],
                'size': random.randint(25, 35),
                'layers': 3
            },
            'moderate': {
                'colors': [(255, 200, 0, 150), (255, 255, 0, 120), (100, 255, 100, 90)],
                'size': random.randint(20, 30),
                'layers': 3
            },
            'light': {
                'colors': [(100, 255, 100, 120), (0, 200, 0, 90), (0, 150, 0, 60)],
                'size': random.randint(15, 25),
                'layers': 2
            },
            'scattered': {
                'colors': [(0, 200, 255, 100), (0, 150, 200, 80)],
                'size': random.randint(10, 20),
                'layers': 2
            },
            'snow': {
                'colors': [(200, 200, 255, 140), (150, 150, 255, 100)],
                'size': random.randint(20, 30),
                'layers': 2
            }
        }

        config = configs.get(intensity, configs['light'])

        # Draw layered circles for realistic radar appearance
        for i, color in enumerate(config['colors'][:config['layers']]):
            radius = config['size'] - (i * 5)
            if radius > 0:
                # Add some noise to make it look more realistic
                for _ in range(3):
                    offset_x = random.randint(-3, 3)
                    offset_y = random.randint(-3, 3)
                    pygame.gfxdraw.filled_circle(surface, x + offset_x, y + offset_y, radius, color)

    def _draw_detailed_us_map(self, surface):
        """Draw a more detailed US map outline"""
        import pygame

        # Continental US outline (more detailed)
        us_outline = [
            # West Coast
            (80, 180), (75, 200), (70, 240), (75, 280), (85, 320),
            # Southwest
            (120, 340), (160, 345), (200, 340),
            # Gulf Coast
            (240, 345), (280, 350), (320, 355), (360, 350),
            # Florida
            (380, 340), (390, 360), (385, 380), (380, 360), (380, 340),
            # East Coast
            (400, 320), (420, 280), (430, 240), (440, 200), (445, 160),
            # Northeast
            (440, 140), (420, 120), (380, 115),
            # Great Lakes
            (340, 120), (300, 115), (260, 120),
            # Northern Border
            (220, 115), (180, 120), (140, 115), (100, 120),
            # Pacific Northwest
            (85, 140), (80, 160), (80, 180)
        ]

        # Draw main outline
        pygame.draw.lines(surface, (100, 100, 100), True, us_outline, 2)

        # Add Great Lakes
        lakes = [
            # Lake Superior
            [(280, 130), (320, 125), (340, 130), (320, 135), (280, 130)],
            # Lake Michigan
            [(300, 145), (305, 170), (295, 170), (300, 145)],
            # Lake Erie
            [(360, 155), (390, 150), (380, 160), (360, 155)]
        ]

        for lake in lakes:
            pygame.draw.lines(surface, (50, 50, 150), True, lake, 1)

        # Add major state boundaries
        state_lines = [
            # California-Nevada
            [(85, 180), (95, 320)],
            # Texas borders
            [(200, 340), (200, 280), (240, 280)],
            # Mississippi River region
            [(250, 140), (255, 340)],
            # Eastern seaboard divisions
            [(380, 140), (380, 340)]
        ]

        for line in state_lines:
            pygame.draw.lines(surface, (60, 60, 60), False, line, 1)

    def _add_map_overlay(self, surface):
        """Add simple US map overlay to radar"""
        try:
            import pygame.gfxdraw
            # Draw simple US boundaries
            # Very basic outline - just for reference
            points = [
                (100, 200), (150, 180), (200, 170), (250, 175),
                (300, 180), (350, 190), (400, 200), (420, 220),
                (400, 250), (380, 280), (350, 300), (300, 310),
                (250, 305), (200, 300), (150, 280), (120, 250),
                (100, 220), (100, 200)
            ]

            # Draw outline
            for i in range(len(points) - 1):
                pygame.draw.line(surface, (100, 100, 100), points[i], points[i+1], 1)
        except:
            pass

    def _create_base_map(self):
        """Create a base map with US outline"""
        try:
            import pygame

            # Create base surface
            base = pygame.Surface((512, 512), pygame.SRCALPHA)
            base.fill((0, 20, 40, 255))  # Dark blue background

            # Draw simple US outline
            # Continental US approximate outline
            us_points = [
                (100, 200), (150, 180), (200, 170), (280, 165),
                (360, 170), (420, 180), (450, 200), (460, 250),
                (450, 300), (420, 330), (360, 340), (280, 345),
                (200, 340), (150, 320), (100, 280), (90, 240),
                (100, 200)
            ]

            # Draw outline
            pygame.draw.lines(base, (80, 80, 80), True, us_points, 2)

            # Add state boundaries (simplified)
            # Vertical lines for major state boundaries
            pygame.draw.line(base, (60, 60, 60), (180, 180), (180, 320), 1)  # Western states
            pygame.draw.line(base, (60, 60, 60), (250, 170), (250, 330), 1)  # Central
            pygame.draw.line(base, (60, 60, 60), (320, 170), (320, 335), 1)  # Eastern
            pygame.draw.line(base, (60, 60, 60), (390, 175), (390, 330), 1)  # East coast

            # Horizontal lines
            pygame.draw.line(base, (60, 60, 60), (100, 240), (450, 240), 1)  # Northern tier
            pygame.draw.line(base, (60, 60, 60), (120, 280), (440, 280), 1)  # Southern tier

            return base
        except Exception as e:
            self.logger.main_logger.error(f"Error creating base map: {e}")
            import pygame
            base = pygame.Surface((512, 512), pygame.SRCALPHA)
            base.fill((0, 20, 40, 255))
            return base

    def _generate_simple_radar(self):
        """Generate a simple radar display with realistic weather patterns"""
        try:
            import pygame
            import random
            import math

            # Use base map
            radar_surface = self._create_base_map()

            # Add realistic weather patterns based on common US weather
            # Simulate a frontal system moving across the country
            front_x = random.randint(150, 350)

            # Draw frontal band
            for y in range(150, 350):
                for x in range(front_x - 40, front_x + 40):
                    if 0 <= x < 512 and 0 <= y < 512:
                        # Varying intensity along the front
                        distance = abs(x - front_x)
                        if distance < 10:
                            color = (255, 0, 0, 120)  # Heavy (red)
                        elif distance < 20:
                            color = (255, 140, 0, 100)  # Moderate (orange)
                        elif distance < 30:
                            color = (255, 255, 0, 80)  # Light (yellow)
                        else:
                            color = (0, 100, 0, 60)  # Very light (green)

                        # Add some noise for realism
                        if random.random() < 0.7:
                            pygame.draw.circle(radar_surface, color, (x, y), 2)

            # Add some scattered showers
            for _ in range(random.randint(5, 10)):
                x = random.randint(100, 450)
                y = random.randint(180, 320)
                size = random.randint(15, 35)
                intensity = random.choice([
                    (0, 100, 0, 80),      # Light green
                    (255, 255, 0, 100),   # Yellow
                ])
                pygame.draw.circle(radar_surface, intensity, (x, y), size)

            # Store as both static and single frame
            self.ws.radar_image = radar_surface
            self.ws.radar_frames = [radar_surface]
            self.logger.main_logger.info("Generated simple radar display")
        except Exception as e:
            self.logger.main_logger.error(f"Error generating simple radar: {e}")
            # Ultimate fallback - just dark blue
            import pygame
            radar_surface = pygame.Surface((512, 512), pygame.SRCALPHA)
            radar_surface.fill((0, 20, 40, 255))
            self.ws.radar_image = radar_surface
            self.ws.radar_frames = [radar_surface]

    def update_scroll_text(self):
        """Update scroll text with current weather information"""
        try:
            location_str = f"WeatherStar 4000+ - {self.ws.location.get('city', '')}, {self.ws.location.get('state', '')}"

            # Add current conditions
            current = self.ws.weather_data.get('current', {})
            if current:
                temp_c = current.get('temperature', {}).get('value')
                if temp_c is not None:
                    temp_f = int(temp_c * 9/5 + 32)
                    conditions = current.get('textDescription', '')
                    humidity = current.get('relativeHumidity', {}).get('value')

                    weather_str = f"  •  Currently: {temp_f}°F, {conditions}"
                    if humidity:
                        weather_str += f", {int(humidity)}% humidity"

                    # Add forecast summary
                    forecast = self.ws.weather_data.get('forecast', {})
                    if forecast and forecast.get('periods'):
                        period = forecast['periods'][0]
                        weather_str += f"  •  {period.get('name', '')}: {period.get('shortForecast', '')}"

                    self.ws.scroller.current_text = location_str + weather_str
                else:
                    self.ws.scroller.current_text = location_str
            else:
                self.ws.scroller.current_text = location_str

        except Exception as e:
            self.logger.log_error("Failed to update scroll text", e)
            self.ws.scroller.current_text = f"WeatherStar 4000+ - {self.ws.location.get('city', 'Loading')}"