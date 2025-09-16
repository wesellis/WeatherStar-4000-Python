#!/usr/bin/env python3
"""
WeatherStar 4000+ News Display Functions Module

News-specific display methods extracted from the main weatherstar4000.py file
to reduce the main file size and improve organization.
"""

import pygame
import time
from weatherstar_modules.weatherstar_logger import get_logger
from weatherstar_modules import get_local_news

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


class WeatherStarNewsDisplays:
    """News display methods for WeatherStar 4000+"""

    def __init__(self, weatherstar_instance):
        """Initialize with reference to main WeatherStar instance"""
        self.ws = weatherstar_instance
        self.logger = get_logger()

    def draw_msn_news(self):
        """Display MSN news with colored categories"""
        self.ws.draw_background('1')
        self.ws.draw_header("MSN", "Top Stories")

        # Enhanced headlines with categories
        headlines = [
            ("[BREAKING]", "Major Winter Storm System Moving Across United States", "https://msn.com/weather"),
            ("[TECH]", "Apple Announces Revolutionary New Product Line", "https://msn.com/technology"),
            ("[SPORTS]", "Underdog Team Wins Championship in Overtime", "https://msn.com/sports"),
            ("[WORLD]", "Global Climate Summit Concludes with Agreement", "https://msn.com/world"),
            ("[BUSINESS]", "Stock Market Reaches All-Time High", "https://msn.com/money"),
            ("[ENTERTAINMENT]", "Surprise Winners at Annual Award Show", "https://msn.com/entertainment"),
        ]

        self._display_categorized_headlines(headlines, "msn")
        self.logger.main_logger.debug("Drew MSN news display")

    def get_cached_city_name(self):
        """Get city name with caching to avoid repeated API calls"""
        # Cache for 1 hour (3600 seconds)
        if self.ws.cached_city_name and (time.time() - self.ws.city_name_cached_at) < 3600:
            return self.ws.cached_city_name

        # Get fresh city name
        self.ws.cached_city_name = get_local_news.get_city_name_from_coords(self.ws.lat, self.ws.lon)
        self.ws.city_name_cached_at = time.time()
        self.logger.main_logger.info(f"Updated cached city name: {self.ws.cached_city_name}")
        return self.ws.cached_city_name

    def draw_local_news(self):
        """Display local news headlines"""
        self.ws.draw_background('1')

        # Draw header without city name
        self.ws.draw_header("Local News")

        # Draw city name with appropriately sized font
        city_name = self.get_cached_city_name()
        # Use normal font for city name (readable size)
        city_text = self.ws.font_normal.render(city_name.upper(), True, COLORS['yellow'])
        # Center it below LOCAL NEWS
        city_rect = city_text.get_rect(centerx=320, y=65)
        self.ws.screen.blit(city_text, city_rect)

        # Get local news headlines - try real news first, fallback to simulated
        try:
            from weatherstar_modules import get_local_news_real
            headlines = get_local_news_real.get_local_news_by_location(self.ws.lat, self.ws.lon)
        except Exception as e:
            # Fallback to simulated news if real news fails
            self.logger.main_logger.debug(f"Using simulated news: {e}")
            headlines = get_local_news.get_local_news_by_location(self.ws.lat, self.ws.lon)

        # Display with normal styling
        self._display_scrolling_headlines(headlines, "local")
        self.logger.main_logger.debug("Drew local news display")

    def draw_reddit_news(self):
        """Display Reddit news with colored subreddits"""
        self.ws.draw_background('1')
        self.ws.draw_header("Reddit", "Top Posts")

        # Headlines with subreddits - more stories for scrolling
        headlines = [
            ("r/news", "Major Scientific Discovery Announced Today by Researchers", "https://reddit.com/r/news"),
            ("r/technology", "New Open Source Project Gains Massive Traction", "https://reddit.com/r/technology"),
            ("r/worldnews", "International Summit Reaches Historic Agreement on Trade", "https://reddit.com/r/worldnews"),
            ("r/science", "Researchers Make Breakthrough in Climate Science Study", "https://reddit.com/r/science"),
            ("r/gaming", "Highly Anticipated Game Releases Tomorrow Worldwide", "https://reddit.com/r/gaming"),
            ("r/AskReddit", "What's the Most Interesting Fact You Know?", "https://reddit.com/r/AskReddit"),
            ("r/todayilearned", "TIL About This Amazing Historical Event", "https://reddit.com/r/todayilearned"),
            ("r/space", "New Images from James Webb Telescope Released", "https://reddit.com/r/space"),
            ("r/programming", "Python Overtakes JavaScript in Developer Survey", "https://reddit.com/r/programming"),
            ("r/dataisbeautiful", "Visualization of Global Internet Usage Patterns", "https://reddit.com/r/dataisbeautiful"),
            ("r/funny", "Hilarious Video Goes Viral on Social Media", "https://reddit.com/r/funny"),
            ("r/movies", "Director Announces Sequel to Popular Film Series", "https://reddit.com/r/movies"),
            ("r/books", "Best-Selling Author Releases New Novel Today", "https://reddit.com/r/books"),
            ("r/food", "Chef Shares Secret Recipe for Perfect Pasta", "https://reddit.com/r/food"),
            ("r/DIY", "Complete Guide to Building Your Own Computer", "https://reddit.com/r/DIY"),
        ]

        self._display_categorized_headlines(headlines, "reddit")
        self.logger.main_logger.debug("Drew Reddit news display")

    def _display_categorized_headlines(self, headlines, source):
        """Display scrolling headlines with colored categories"""
        # Initialize scroll position if needed
        if not hasattr(self.ws, 'news_vertical_scroll'):
            self.ws.news_vertical_scroll = {}
        if source not in self.ws.news_vertical_scroll:
            self.ws.news_vertical_scroll[source] = 0

        # Category colors
        category_colors = {
            # MSN categories
            '[BREAKING]': COLORS['red'],
            '[TECH]': COLORS['cyan'],
            '[SPORTS]': (0, 255, 0),  # Green
            '[WORLD]': COLORS['yellow'],
            '[BUSINESS]': (255, 140, 0),  # Orange
            '[ENTERTAINMENT]': (255, 0, 255),  # Magenta
            '[HEALTH]': (100, 255, 100),  # Light green
            '[POLITICS]': (200, 100, 255),  # Purple
            '[SCIENCE]': (0, 200, 255),  # Light blue
            '[LOCAL]': (255, 200, 100),  # Peach
            # Reddit subreddits
            'r/news': COLORS['red'],
            'r/technology': COLORS['cyan'],
            'r/worldnews': COLORS['yellow'],
            'r/science': (0, 255, 0),  # Green
            'r/gaming': (255, 0, 255),  # Magenta
            'r/AskReddit': (255, 140, 0),  # Orange
            'r/todayilearned': (100, 200, 255),  # Sky blue
            'r/space': (150, 100, 255),  # Purple
            'r/programming': (0, 255, 200),  # Teal
            'r/dataisbeautiful': (255, 255, 100),  # Light yellow
            'r/funny': (255, 100, 100),  # Light red
            'r/movies': (200, 100, 200),  # Light purple
            'r/books': (150, 255, 150),  # Light green
            'r/food': (255, 200, 0),  # Gold
            'r/DIY': (200, 150, 100),  # Brown
        }

        # Margins - 20px thinner (65px from edges), 40px less height
        left_margin = 65
        right_margin = 65
        top_margin = 100
        display_width = 640 - left_margin - right_margin  # 510px width

        # Scrolling setup
        line_height = 26
        max_visible_height = 300  # Reduced by 40px (was 340)
        total_height = len(headlines) * line_height
        max_scroll = max(0, total_height - max_visible_height)

        # Current y position for rendering
        current_y = top_margin - self.ws.news_vertical_scroll[source]

        for item in headlines:
            category = item[0] if len(item) > 0 else ""
            headline = item[1] if len(item) > 1 else ""
            url = item[2] if len(item) > 2 else ""

            # Only render if within visible area
            if current_y > top_margin - line_height and current_y < 440:
                # Draw category with color
                cat_color = category_colors.get(category, COLORS['cyan'])
                cat_text = self.ws.font_tiny.render(category, True, cat_color)
                self.ws.screen.blit(cat_text, (left_margin, current_y))

                # Draw headline in white (truncate to fit display width)
                max_headline_chars = 60  # Adjusted for narrower width
                display_headline = headline[:max_headline_chars] if len(headline) > max_headline_chars else headline
                headline_text = self.ws.font_tiny.render(display_headline, True, COLORS['white'])
                self.ws.screen.blit(headline_text, (left_margin + 110, current_y))

            current_y += line_height

        # Auto-scroll logic
        current_time = time.time()
        if not hasattr(self.ws, 'last_news_scroll_time'):
            self.ws.last_news_scroll_time = current_time

        # Smooth scrolling
        if current_time - self.ws.last_news_scroll_time > 0.05:  # Scroll every 50ms
            self.ws.news_vertical_scroll[source] += 1
            if self.ws.news_vertical_scroll[source] > max_scroll + 100:  # Reset with padding
                self.ws.news_vertical_scroll[source] = -50
            self.ws.last_news_scroll_time = current_time

    def _display_scrolling_headlines(self, headlines, source):
        """Display scrolling news headlines with proper spacing"""
        # Initialize scroll position if needed
        if not hasattr(self.ws, 'news_vertical_scroll'):
            self.ws.news_vertical_scroll = {}
        if source not in self.ws.news_vertical_scroll:
            self.ws.news_vertical_scroll[source] = 0

        # FIXED: Proper margins - 40px from edges, 60px from top
        left_margin = 40
        right_margin = 40
        top_margin = 60
        display_width = 640 - left_margin - right_margin  # 560px width

        # Start drawing position
        start_y = top_margin + 40  # Start text 40px below header area
        line_height = 22
        max_visible_height = 340  # Adjusted for new top position
        total_height = len(headlines) * line_height
        max_scroll = max(0, total_height - max_visible_height)

        # Clear clickable headlines
        if not hasattr(self.ws, 'clickable_headlines'):
            self.ws.clickable_headlines = []
        else:
            self.ws.clickable_headlines.clear()

        # Colors based on source
        if source == "reddit":
            text_color = COLORS['cyan']
        elif source == "local":
            text_color = COLORS['red']  # Emergency-style red for local news
        else:  # MSN
            text_color = COLORS['white']

        # Track the current y position for rendering
        current_y = start_y - self.ws.news_vertical_scroll[source]

        # Draw visible headlines
        for i, headline in enumerate(headlines):
            text = headline[0] if isinstance(headline, tuple) else headline
            url = headline[1] if isinstance(headline, tuple) and len(headline) > 1 else None

            # Only render if within visible area
            if current_y > -line_height and current_y < 480:
                # Truncate text to fit within display width
                max_chars = int(display_width / 6)  # Approximate character width
                if len(text) > max_chars:
                    text = text[:max_chars-3] + "..."

                # Render text using smaller font for better fit
                font_to_use = self.ws.font_tiny if hasattr(self.ws, 'font_tiny') else self.ws.font_normal
                text_surface = font_to_use.render(text, True, text_color)
                text_rect = pygame.Rect(left_margin, current_y, display_width, line_height)
                self.ws.screen.blit(text_surface, text_rect)

                # Track clickable area if URL exists
                if url and current_y >= start_y and current_y < start_y + max_visible_height:
                    self.ws.clickable_headlines.append({
                        'rect': text_rect,
                        'url': url,
                        'text': text
                    })

            current_y += line_height

        # Auto-scroll logic
        current_time = time.time()
        if not hasattr(self.ws, 'last_news_scroll_time'):
            self.ws.last_news_scroll_time = current_time

        # Scroll every 0.1 seconds
        if current_time - self.ws.last_news_scroll_time > 0.1:
            self.ws.news_vertical_scroll[source] += 2
            if self.ws.news_vertical_scroll[source] > max_scroll + 100:  # Extra padding before reset
                self.ws.news_vertical_scroll[source] = -50  # Start from slightly above
            self.ws.last_news_scroll_time = current_time