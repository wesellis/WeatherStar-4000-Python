"""
Optimized News Display Module
Handles MSN, Reddit, and Local News with smooth scrolling
"""

import pygame
import time
import webbrowser
from typing import List, Tuple
from functools import lru_cache
import logging

from .display_base import DisplayBase
from .config import COLORS, SCREEN_WIDTH

logger = logging.getLogger(__name__)


class NewsDisplay(DisplayBase):
    """Optimized news display with caching and smooth scrolling"""

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)

        # Scrolling state
        self.news_vertical_scroll = {}
        self.clickable_headlines = []

        # Cache for headlines
        self._headline_cache = {}
        self._cache_time = {}

        # Performance optimization
        self.scroll_speed = 2  # Pixels per frame
        self.last_scroll_update = 0

    @lru_cache(maxsize=3)
    def _get_msn_headlines(self) -> List[Tuple[str, str]]:
        """Get MSN headlines (cached)"""
        return [
            ("Breaking: Major Winter Storm System Moving Across United States", "https://www.msn.com/weather"),
            ("Technology: Apple Announces Revolutionary New Product Line", "https://www.msn.com/technology"),
            ("Sports: Underdog Team Wins Championship in Dramatic Overtime", "https://www.msn.com/sports"),
            ("World News: Global Climate Summit Concludes with Historic Agreement", "https://www.msn.com/world"),
            ("Business: Stock Market Reaches All-Time High", "https://www.msn.com/money"),
            ("Entertainment: Surprise Winners at Annual Award Show", "https://www.msn.com/entertainment"),
            ("Health: Scientists Announce Major Medical Breakthrough", "https://www.msn.com/health"),
            ("Science: Space Mission Successfully Launches", "https://www.msn.com/news/technology"),
            ("Politics: Congress Passes Landmark Legislation", "https://www.msn.com/politics"),
            ("Weather: Hurricane Season Expected to Be More Active", "https://www.weather.com"),
        ]

    @lru_cache(maxsize=3)
    def _get_reddit_headlines(self) -> List[Tuple[str, str]]:
        """Get Reddit headlines (cached)"""
        return [
            ("r/news: Major Storm System Approaching East Coast", "https://reddit.com/r/news"),
            ("r/worldnews: International Summit Concludes", "https://reddit.com/r/worldnews"),
            ("r/technology: New AI Breakthrough Announced", "https://reddit.com/r/technology"),
            ("r/science: Scientists Discover New Species", "https://reddit.com/r/science"),
            ("r/gaming: Popular Game Gets Major Update", "https://reddit.com/r/gaming"),
            ("r/movies: Independent Film Breaks Records", "https://reddit.com/r/movies"),
            ("r/sports: Underdog Team's Cinderella Story", "https://reddit.com/r/sports"),
            ("r/space: New Images from Webb Telescope", "https://reddit.com/r/space"),
            ("r/AskReddit: Most Interesting Historical Facts", "https://reddit.com/r/AskReddit"),
            ("r/todayilearned: TIL Honey Never Spoils", "https://reddit.com/r/todayilearned"),
        ]

    def _get_local_headlines(self, city_name: str) -> List[Tuple[str, str]]:
        """Get local news headlines"""
        return [
            (f"Local: {city_name} Council Approves New Development", "https://local.news/development"),
            ("Breaking: Traffic Alert on Major Interstate", "https://local.news/traffic"),
            (f"Local: {city_name} Schools Announce Policy Changes", "https://local.news/schools"),
            ("Emergency: Severe Weather Warning Issued", "https://local.news/weather-alert"),
            ("Local: Fire Department Responds to Structure Fire", "https://local.news/fire"),
            ("Community: Food Bank Seeks Holiday Volunteers", "https://local.news/volunteers"),
            ("Local: New Business Opens Downtown", "https://local.news/business"),
            ("Alert: Water Main Break Affects Service", "https://local.news/water"),
            ("Local: High School Team Advances to Championship", "https://local.news/sports"),
            ("Public Safety: Holiday Shopping Patrol Increase", "https://local.news/safety"),
        ]

    def draw_msn_news(self):
        """Draw MSN news display"""
        self.draw_background('1')
        self.draw_header("MSN", "Top Stories")
        headlines = self._get_msn_headlines()
        self._display_scrolling_headlines(headlines, "msn")

    def draw_reddit_news(self):
        """Draw Reddit news display"""
        self.draw_background('1')
        self.draw_header("Reddit", "Headlines")
        headlines = self._get_reddit_headlines()
        self._display_scrolling_headlines(headlines, "reddit")

    def draw_local_news(self, city_name: str = "Local Area"):
        """Draw local news display"""
        self.draw_background('1')
        self.draw_header("Local News", city_name)
        headlines = self._get_local_headlines(city_name)
        self._display_scrolling_headlines(headlines, "local")

    def _display_scrolling_headlines(self, headlines: List[Tuple[str, str]], source: str):
        """Optimized scrolling headlines display"""
        # Initialize scroll position for this source
        if source not in self.news_vertical_scroll:
            self.news_vertical_scroll[source] = 200

        # Clear clickable areas
        self.clickable_headlines = []

        # Set up clipping for scroll area
        clip_rect = pygame.Rect(55, 100, 530, 298)
        self.screen.set_clip(clip_rect)

        # Scroll speed control
        current_time = pygame.time.get_ticks()
        if current_time - self.last_scroll_update > 50:  # Update every 50ms
            self.news_vertical_scroll[source] -= self.scroll_speed
            self.last_scroll_update = current_time

            # Reset scroll when all headlines have passed
            total_height = len(headlines) * 80  # Approximate height per headline
            if self.news_vertical_scroll[source] < -total_height:
                self.news_vertical_scroll[source] = 400

        # Draw headlines
        y_pos = self.news_vertical_scroll[source]
        line_height = 28
        headline_spacing = 15

        for i, (headline_text, headline_url) in enumerate(headlines[:20], 1):
            # Only render visible headlines (performance optimization)
            if -200 < y_pos < 500:
                # Draw number
                num_color = COLORS['yellow']
                num_text = self.large_font.render(f"{i}.", True, num_color)
                self.screen.blit(num_text, (65, y_pos))

                # Word wrap and draw headline
                lines = self._word_wrap(headline_text, 470)

                # Track clickable area
                if headline_url and 100 < y_pos < 398:
                    headline_height = len(lines) * line_height
                    clickable_rect = pygame.Rect(65, y_pos, 520, headline_height)
                    self.clickable_headlines.append((clickable_rect, headline_url))

                # Draw lines with color coding
                line_y = y_pos
                for line in lines:
                    if 95 < line_y < 398:  # Only draw visible lines
                        self._draw_colored_line(line, line_y, source)
                    line_y += line_height

                y_pos += len(lines) * line_height + headline_spacing
            else:
                # Skip rendering but update position
                lines_count = len(self._word_wrap(headline_text, 470))
                y_pos += lines_count * line_height + headline_spacing

        # Reset clipping
        self.screen.set_clip(None)

    @lru_cache(maxsize=256)
    def _word_wrap(self, text: str, max_width: int) -> List[str]:
        """Cached word wrapping for performance"""
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if self.normal_font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    def _draw_colored_line(self, line: str, y: int, source: str):
        """Draw line with appropriate color coding"""
        x_pos = 95

        if source == "reddit" and "r/" in line:
            # Color Reddit subreddits
            parts = line.split()
            for part in parts:
                if part.startswith("r/"):
                    color = COLORS['cyan']
                elif part.startswith("[") and part.endswith("]"):
                    color = COLORS['yellow']
                else:
                    color = COLORS['white']

                text = self.normal_font.render(part, True, color)
                self.screen.blit(text, (x_pos, y))
                x_pos += text.get_width() + 5

        elif source == "msn" and ":" in line:
            # Color MSN categories
            parts = line.split(":", 1)
            if len(parts) == 2:
                category = parts[0]
                if category in ["BREAKING", "Breaking"]:
                    cat_color = COLORS['red']
                elif category == "UPDATE":
                    cat_color = COLORS['yellow']
                else:
                    cat_color = COLORS['cyan']

                cat_text = self.normal_font.render(category + ":", True, cat_color)
                self.screen.blit(cat_text, (x_pos, y))
                rest_text = self.normal_font.render(parts[1], True, COLORS['white'])
                self.screen.blit(rest_text, (x_pos + cat_text.get_width(), y))
            else:
                text = self.normal_font.render(line, True, COLORS['white'])
                self.screen.blit(text, (x_pos, y))

        elif source == "local":
            # Color local news
            if ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    category = parts[0]
                    if any(word in category.upper() for word in ["EMERGENCY", "BREAKING", "ALERT"]):
                        cat_color = COLORS['red']
                    else:
                        cat_color = COLORS['cyan']

                    cat_text = self.normal_font.render(category + ":", True, cat_color)
                    self.screen.blit(cat_text, (x_pos, y))
                    rest_text = self.normal_font.render(parts[1], True, COLORS['white'])
                    self.screen.blit(rest_text, (x_pos + cat_text.get_width(), y))
                else:
                    text = self.normal_font.render(line, True, COLORS['white'])
                    self.screen.blit(text, (x_pos, y))
            else:
                text = self.normal_font.render(line, True, COLORS['white'])
                self.screen.blit(text, (x_pos, y))
        else:
            # Default white text
            text = self.normal_font.render(line, True, COLORS['white'])
            self.screen.blit(text, (x_pos, y))

    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """Handle click on headlines to open URLs"""
        for rect, url in self.clickable_headlines:
            if rect.collidepoint(pos):
                logger.info(f"Opening URL: {url}")
                webbrowser.open(url)
                return True
        return False