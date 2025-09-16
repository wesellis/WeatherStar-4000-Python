"""
Optimized Base Display Module
Common functionality for all display screens
"""

import pygame
import os
from pathlib import Path
from typing import Optional, Tuple
from functools import lru_cache
import logging

from .config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT

logger = logging.getLogger(__name__)


class DisplayBase:
    """Base class for all weather displays with optimization"""

    # Class-level cache for loaded resources
    _background_cache = {}
    _font_cache = {}
    _icon_cache = {}

    def __init__(self, screen: pygame.Surface, assets_path: str = "weatherstar_assets"):
        self.screen = screen
        self.assets_path = Path(assets_path)

        # Font paths
        self.font_paths = self._get_font_paths()

        # Pre-load commonly used fonts
        self._preload_fonts()

        # Performance tracking
        self.frame_count = 0
        self.last_update = pygame.time.get_ticks()

    def _get_font_paths(self) -> dict:
        """Get paths to Star4000 fonts"""
        font_dir = self.assets_path / "fonts"
        return {
            'small': str(font_dir / "Star4000 Small.ttf"),
            'normal': str(font_dir / "Star4000.ttf"),
            'large': str(font_dir / "Star4000 Large.ttf"),
            'compressed': str(font_dir / "Star4000 Large Compressed.ttf"),
            'extended': str(font_dir / "Star4000 Extended.ttf"),
            'radar': str(font_dir / "Star 4 Radar.ttf")
        }

    def _preload_fonts(self):
        """Pre-load commonly used fonts for performance"""
        try:
            # Try to use authentic fonts
            self.small_font = self._get_cached_font('small', 16)
            self.normal_font = self._get_cached_font('normal', 20)
            self.large_font = self._get_cached_font('normal', 24)
            self.header_font = self._get_cached_font('large', 36)
            self.time_font = self._get_cached_font('normal', 18)
        except:
            # Fallback to system fonts
            logger.warning("Using fallback system fonts")
            self.small_font = pygame.font.Font(None, 16)
            self.normal_font = pygame.font.Font(None, 20)
            self.large_font = pygame.font.Font(None, 24)
            self.header_font = pygame.font.Font(None, 36)
            self.time_font = pygame.font.Font(None, 18)

    @classmethod
    def _get_cached_font(cls, font_type: str, size: int) -> pygame.font.Font:
        """Get cached font for better performance"""
        cache_key = f"{font_type}_{size}"

        if cache_key not in cls._font_cache:
            font_paths = cls._get_font_paths_static()
            font_path = font_paths.get(font_type)

            if font_path and os.path.exists(font_path):
                cls._font_cache[cache_key] = pygame.font.Font(font_path, size)
            else:
                cls._font_cache[cache_key] = pygame.font.Font(None, size)

        return cls._font_cache[cache_key]

    @classmethod
    def _get_font_paths_static(cls) -> dict:
        """Static method to get font paths"""
        font_dir = Path("weatherstar_assets/fonts")
        return {
            'small': str(font_dir / "Star4000 Small.ttf"),
            'normal': str(font_dir / "Star4000.ttf"),
            'large': str(font_dir / "Star4000 Large.ttf"),
            'compressed': str(font_dir / "Star4000 Large Compressed.ttf"),
            'extended': str(font_dir / "Star4000 Extended.ttf"),
            'radar': str(font_dir / "Star 4 Radar.ttf")
        }

    @lru_cache(maxsize=32)
    def _load_background(self, bg_name: str) -> Optional[pygame.Surface]:
        """Load and cache background image"""
        cache_key = f"bg_{bg_name}"

        if cache_key not in self._background_cache:
            bg_path = self.assets_path / "backgrounds" / f"BackGround{bg_name}.png"

            if bg_path.exists():
                try:
                    # Load and convert for better performance
                    bg = pygame.image.load(str(bg_path))
                    bg = bg.convert()
                    # Scale to screen size if needed
                    if bg.get_size() != (SCREEN_WIDTH, SCREEN_HEIGHT):
                        bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    self._background_cache[cache_key] = bg
                    logger.debug(f"Loaded background: {bg_name}")
                except Exception as e:
                    logger.error(f"Failed to load background {bg_name}: {e}")
                    return None
            else:
                logger.warning(f"Background not found: {bg_path}")
                return None

        return self._background_cache.get(cache_key)

    def draw_background(self, bg_name: str = '1'):
        """Draw background with caching"""
        # Try to load authentic background
        bg_surface = self._load_background(bg_name)

        if bg_surface:
            self.screen.blit(bg_surface, (0, 0))
        else:
            # Fallback to solid color
            if bg_name == '2':
                self.screen.fill(COLORS['dark_blue'])
            else:
                self.screen.fill(COLORS['blue'])

    def draw_header(self, title_top: str, title_bottom: Optional[str] = None, has_noaa: bool = False):
        """Draw optimized header"""
        # Header background
        header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 60)
        pygame.draw.rect(self.screen, COLORS['blue'], header_rect)
        pygame.draw.rect(self.screen, COLORS['orange'], header_rect, 3)

        # Title text
        title_text = self.header_font.render(title_top, True, COLORS['white'])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 20))
        self.screen.blit(title_text, title_rect)

        if title_bottom:
            subtitle_text = self.normal_font.render(title_bottom, True, COLORS['yellow'])
            subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 45))
            self.screen.blit(subtitle_text, subtitle_rect)

        # Time in corner
        from datetime import datetime
        current_time = datetime.now().strftime("%I:%M %p")
        time_text = self.time_font.render(current_time, True, COLORS['white'])
        self.screen.blit(time_text, (10, 10))

    @lru_cache(maxsize=64)
    def _load_weather_icon(self, condition: str) -> Optional[pygame.Surface]:
        """Load and cache weather icon"""
        # Map condition to icon filename
        icon_map = {
            'clear': 'Clear.gif',
            'sunny': 'Sunny.gif',
            'cloudy': 'Cloudy.gif',
            'partly cloudy': 'Partly-Cloudy.gif',
            'mostly cloudy': 'Mostly-Cloudy.gif',
            'rain': 'Rain.gif',
            'showers': 'Showers.gif',
            'thunderstorm': 'Thunderstorm.gif',
            'snow': 'Heavy-Snow.gif',
            'light snow': 'Light-Snow.gif',
            'fog': 'Fog.gif',
            'windy': 'Windy.gif'
        }

        icon_file = icon_map.get(condition.lower(), 'Cloudy.gif')
        icon_path = self.assets_path / "icons" / icon_file

        if icon_path.exists():
            try:
                icon = pygame.image.load(str(icon_path))
                # Scale to standard size for consistency
                icon = pygame.transform.scale(icon, (64, 64))
                return icon.convert_alpha()
            except Exception as e:
                logger.error(f"Failed to load icon {icon_file}: {e}")

        return None

    def draw_weather_icon(self, x: int, y: int, condition: str):
        """Draw weather icon with caching"""
        icon = self._load_weather_icon(condition)
        if icon:
            self.screen.blit(icon, (x, y))
        else:
            # Fallback to text
            text = self.normal_font.render(condition[:3].upper(), True, COLORS['white'])
            self.screen.blit(text, (x, y))

    def draw_text_centered(self, text: str, y: int, font=None, color=COLORS['white']):
        """Draw centered text"""
        if font is None:
            font = self.normal_font

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.screen.blit(text_surface, text_rect)

    def draw_text_wrapped(self, text: str, x: int, y: int, max_width: int,
                         font=None, color=COLORS['white'], line_height: int = 25):
        """Draw word-wrapped text efficiently"""
        if font is None:
            font = self.normal_font

        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            self.screen.blit(text_surface, (x, y + i * line_height))

    def update_performance_stats(self):
        """Track performance for optimization"""
        self.frame_count += 1
        current_time = pygame.time.get_ticks()

        if current_time - self.last_update > 1000:  # Every second
            fps = self.frame_count * 1000 / (current_time - self.last_update)
            logger.debug(f"FPS: {fps:.1f}")
            self.frame_count = 0
            self.last_update = current_time