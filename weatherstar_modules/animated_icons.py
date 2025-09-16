#!/usr/bin/env python3
"""
Animated Weather Icons Module for WeatherStar 4000
Handles loading and displaying animated GIF weather icons
"""

import pygame
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import time
import logging

try:
    from PIL import Image
except ImportError:
    Image = None
    print("Warning: PIL/Pillow not installed. Animated GIFs will show as static images.")

logger = logging.getLogger(__name__)


class AnimatedIcon:
    """Class to handle animated GIF icons"""

    def __init__(self, filepath: str):
        """Initialize animated icon from GIF file"""
        self.filepath = filepath
        self.frames = []
        self.durations = []
        self.current_frame = 0
        self.last_update = 0
        self.total_duration = 0
        self.static_image = None

        self.load_gif()

    def load_gif(self):
        """Load animated GIF frames"""
        if not Image:
            # Fallback to static image if PIL not available
            try:
                self.static_image = pygame.image.load(self.filepath)
            except:
                logger.warning(f"Failed to load icon: {self.filepath}")
            return

        try:
            # Open the GIF
            gif = Image.open(self.filepath)

            # Extract frames
            try:
                while True:
                    # Convert RGBA to RGB with white background
                    frame = gif.convert('RGBA')

                    # Create a white background
                    background = Image.new('RGBA', frame.size, (255, 255, 255, 0))

                    # Composite the frame onto the background
                    alpha_composite = Image.alpha_composite(background, frame)

                    # Convert PIL image to pygame surface
                    mode = alpha_composite.mode
                    size = alpha_composite.size
                    data = alpha_composite.tobytes()

                    # Create pygame surface
                    if mode == 'RGBA':
                        surface = pygame.image.fromstring(data, size, mode).convert_alpha()
                    else:
                        surface = pygame.image.fromstring(data, size, mode).convert()

                    self.frames.append(surface)

                    # Get frame duration (default to 100ms if not specified)
                    duration = gif.info.get('duration', 100)
                    self.durations.append(duration / 1000.0)  # Convert to seconds

                    # Move to next frame
                    gif.seek(gif.tell() + 1)
            except EOFError:
                # End of frames
                pass

            gif.close()

            # Calculate total duration
            self.total_duration = sum(self.durations)

            # If only one frame, treat as static
            if len(self.frames) == 1:
                self.static_image = self.frames[0]
                self.frames = []
                self.durations = []

            logger.info(f"Loaded animated icon: {os.path.basename(self.filepath)} ({len(self.frames)} frames)")

        except Exception as e:
            logger.warning(f"Failed to load animated GIF {self.filepath}: {e}")
            # Try loading as static image
            try:
                self.static_image = pygame.image.load(self.filepath)
            except:
                pass

    def get_current_frame(self) -> Optional[pygame.Surface]:
        """Get the current frame to display"""
        if self.static_image:
            return self.static_image

        if not self.frames:
            return None

        # Calculate which frame to show based on time
        current_time = time.time()

        if self.last_update == 0:
            self.last_update = current_time
            return self.frames[0]

        # Calculate elapsed time since last reset
        elapsed = current_time - self.last_update

        # Find which frame we should be on
        accumulated_time = 0
        for i, duration in enumerate(self.durations):
            accumulated_time += duration
            if elapsed < accumulated_time:
                self.current_frame = i
                return self.frames[i]

        # If we've exceeded total duration, reset
        self.last_update = current_time
        self.current_frame = 0
        return self.frames[0]

    def get_scaled_frame(self, width: int, height: int) -> Optional[pygame.Surface]:
        """Get current frame scaled to specified size"""
        frame = self.get_current_frame()
        if frame:
            return pygame.transform.scale(frame, (width, height))
        return None

    def reset_animation(self):
        """Reset animation to first frame"""
        self.current_frame = 0
        self.last_update = 0


class AnimatedIconManager:
    """Manager for loading and caching animated weather icons"""

    def __init__(self, icons_dir: str):
        """Initialize the icon manager"""
        self.icons_dir = Path(icons_dir)
        self.animated_icons: Dict[str, AnimatedIcon] = {}
        self.static_icons: Dict[str, pygame.Surface] = {}

        # Preload all icons
        self.load_all_icons()

    def load_all_icons(self):
        """Preload all weather icons"""
        if not self.icons_dir.exists():
            logger.warning(f"Icons directory not found: {self.icons_dir}")
            return

        # Load all GIF files
        for gif_file in self.icons_dir.glob("*.gif"):
            icon_name = gif_file.stem
            try:
                self.animated_icons[icon_name] = AnimatedIcon(str(gif_file))
            except Exception as e:
                logger.warning(f"Failed to load animated icon {icon_name}: {e}")

        # Also load PNG files as static fallbacks
        for png_file in self.icons_dir.glob("*.png"):
            icon_name = png_file.stem
            if icon_name not in self.animated_icons:  # Don't override animated versions
                try:
                    self.static_icons[icon_name] = pygame.image.load(str(png_file))
                except Exception as e:
                    logger.warning(f"Failed to load static icon {icon_name}: {e}")

        logger.info(f"Loaded {len(self.animated_icons)} animated icons and {len(self.static_icons)} static icons")

    def get_icon(self, icon_name: str, width: Optional[int] = None, height: Optional[int] = None) -> Optional[pygame.Surface]:
        """Get an icon (animated or static) by name"""
        # Try animated first
        if icon_name in self.animated_icons:
            icon = self.animated_icons[icon_name]
            if width and height:
                return icon.get_scaled_frame(width, height)
            else:
                return icon.get_current_frame()

        # Try static
        if icon_name in self.static_icons:
            icon = self.static_icons[icon_name]
            if width and height:
                return pygame.transform.scale(icon, (width, height))
            else:
                return icon

        # Try with different cases
        for key in self.animated_icons.keys():
            if key.lower() == icon_name.lower():
                icon = self.animated_icons[key]
                if width and height:
                    return icon.get_scaled_frame(width, height)
                else:
                    return icon.get_current_frame()

        for key in self.static_icons.keys():
            if key.lower() == icon_name.lower():
                icon = self.static_icons[key]
                if width and height:
                    return pygame.transform.scale(icon, (width, height))
                else:
                    return icon

        logger.warning(f"Icon not found: {icon_name}")
        return None

    def reset_all_animations(self):
        """Reset all animations to their first frame"""
        for icon in self.animated_icons.values():
            icon.reset_animation()