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

        # Enhanced headlines with categories - more stories for better scrolling
        headlines = [
            ("[BREAKING]", "Major Winter Storm System Moving Across United States", "https://msn.com/weather"),
            ("[TECH]", "Apple Announces Revolutionary New Product Line for 2025", "https://msn.com/technology"),
            ("[SPORTS]", "Underdog Team Wins Championship in Overtime Thriller", "https://msn.com/sports"),
            ("[WORLD]", "Global Climate Summit Concludes with Historic Agreement", "https://msn.com/world"),
            ("[BUSINESS]", "Stock Market Reaches All-Time High Amid Economic Growth", "https://msn.com/money"),
            ("[ENTERTAINMENT]", "Surprise Winners at Annual Award Show Last Night", "https://msn.com/entertainment"),
            ("[HEALTH]", "New Medical Breakthrough Could Change Treatment Options", "https://msn.com/health"),
            ("[SCIENCE]", "NASA Announces Discovery of Earth-Like Exoplanet", "https://msn.com/science"),
            ("[POLITICS]", "Congress Passes Major Infrastructure Bill", "https://msn.com/politics"),
            ("[LOCAL]", "City Council Approves New Development Project Downtown", "https://msn.com/local"),
            ("[TECH]", "Artificial Intelligence Makes Major Leap Forward", "https://msn.com/tech"),
            ("[SPORTS]", "Local High School Team Advances to State Finals", "https://msn.com/sports"),
            ("[BUSINESS]", "Major Company Announces Expansion Plans", "https://msn.com/business"),
            ("[WORLD]", "International Trade Agreement Signed by Multiple Nations", "https://msn.com/world"),
            ("[ENTERTAINMENT]", "New Streaming Series Breaks Viewing Records", "https://msn.com/tv"),
            ("[HEALTH]", "Study Shows Benefits of New Exercise Routine", "https://msn.com/fitness"),
            ("[SCIENCE]", "Researchers Make Progress on Renewable Energy", "https://msn.com/energy"),
            ("[BREAKING]", "Emergency Services Respond to Major Incident", "https://msn.com/breaking"),
            ("[TECH]", "Social Media Platform Introduces New Features", "https://msn.com/social"),
            ("[SPORTS]", "Olympic Athlete Sets New World Record", "https://msn.com/olympics"),
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

        # Headlines with subreddits - expanded for better scrolling experience
        headlines = [
            ("r/news", "Major Scientific Discovery Announced Today by International Research Team", "https://reddit.com/r/news/1"),
            ("r/technology", "New Open Source Project Gains Massive Traction in Developer Community", "https://reddit.com/r/technology/1"),
            ("r/worldnews", "International Summit Reaches Historic Agreement on Global Trade", "https://reddit.com/r/worldnews/1"),
            ("r/science", "Researchers Make Breakthrough in Climate Science Study", "https://reddit.com/r/science/1"),
            ("r/gaming", "Highly Anticipated Game Releases Tomorrow Worldwide", "https://reddit.com/r/gaming/1"),
            ("r/AskReddit", "What's the Most Interesting Fact You Know About Space?", "https://reddit.com/r/AskReddit/1"),
            ("r/todayilearned", "TIL About This Amazing Historical Event from Ancient Rome", "https://reddit.com/r/todayilearned/1"),
            ("r/space", "New Images from James Webb Telescope Released Today", "https://reddit.com/r/space/1"),
            ("r/programming", "Python Overtakes JavaScript in Latest Developer Survey", "https://reddit.com/r/programming/1"),
            ("r/dataisbeautiful", "Visualization of Global Internet Usage Patterns [OC]", "https://reddit.com/r/dataisbeautiful/1"),
            ("r/funny", "Hilarious Video Goes Viral on Social Media Platform", "https://reddit.com/r/funny/1"),
            ("r/movies", "Director Announces Sequel to Popular Film Series", "https://reddit.com/r/movies/1"),
            ("r/books", "Best-Selling Author Releases New Novel in Fantasy Series", "https://reddit.com/r/books/1"),
            ("r/food", "Chef Shares Secret Recipe for Perfect Italian Pasta", "https://reddit.com/r/food/1"),
            ("r/DIY", "Complete Guide to Building Your Own Gaming Computer", "https://reddit.com/r/DIY/1"),
            ("r/news", "Breaking: Major Policy Change Announced by Government", "https://reddit.com/r/news/2"),
            ("r/technology", "AI Company Reveals Revolutionary New Technology", "https://reddit.com/r/technology/2"),
            ("r/gaming", "Indie Game Developer Shares Success Story", "https://reddit.com/r/gaming/2"),
            ("r/science", "New Study Reveals Surprising Facts About Human Brain", "https://reddit.com/r/science/2"),
            ("r/worldnews", "Economic Summit Addresses Global Financial Challenges", "https://reddit.com/r/worldnews/2"),
            ("r/AskReddit", "What Life Skill Should Everyone Learn Before 30?", "https://reddit.com/r/AskReddit/2"),
            ("r/space", "SpaceX Successfully Launches New Mission to ISS", "https://reddit.com/r/space/2"),
            ("r/programming", "New Programming Language Gaining Popularity", "https://reddit.com/r/programming/2"),
            ("r/movies", "Classic Film Gets 4K Restoration and Re-release", "https://reddit.com/r/movies/2"),
            ("r/books", "Book Club Discussion: This Month's Selection", "https://reddit.com/r/books/2"),
        ]

        self._display_categorized_headlines(headlines, "reddit")
        self.logger.main_logger.debug("Drew Reddit news display")

    def _display_categorized_headlines(self, headlines, source):
        """Display scrolling headlines with colored categories - single line"""
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

        # Center content in 4:3 display box (640x480) - fine-tuned margins
        # The content area should be centered with larger margins
        left_margin = 65    # +5px more inward
        right_margin = 80   # +20px more inward
        top_margin = 120    # Perfect as is
        display_width = 640 - left_margin - right_margin  # 495px width

        # Clear clickable headlines list
        if not hasattr(self.ws, 'clickable_headlines'):
            self.ws.clickable_headlines = []
        else:
            self.ws.clickable_headlines.clear()

        # Scrolling setup - fit in 4:3 display box with fine-tuned margins
        line_height = 26
        max_visible_height = 270  # Reduced by 20px for more bottom margin (480 - 120 top - 90 bottom)
        total_height = len(headlines) * line_height
        max_scroll = max(0, total_height - max_visible_height)

        # Current y position for rendering
        current_y = top_margin - self.ws.news_vertical_scroll[source]

        for item in headlines:
            category = item[0] if len(item) > 0 else ""
            headline = item[1] if len(item) > 1 else ""
            url = item[2] if len(item) > 2 else ""

            # Only render if within visible area
            if current_y > top_margin - line_height and current_y < (top_margin + max_visible_height):
                # Calculate space for category
                cat_width = 100  # Fixed width for category column (adjusted for centering)

                # Draw category with color
                cat_color = category_colors.get(category, COLORS['cyan'])
                cat_text = self.ws.font_tiny.render(category, True, cat_color)
                self.ws.screen.blit(cat_text, (left_margin, current_y))

                # Calculate remaining space for headline (allow word wrap)
                headline_x = left_margin + cat_width
                headline_width = display_width - cat_width

                # Word wrap the headline if needed
                words = headline.split()
                lines = []
                current_line = []
                current_length = 0
                max_chars_per_line = int(headline_width / 7)  # Approximate char width

                for word in words:
                    word_length = len(word) + 1  # +1 for space
                    if current_length + word_length <= max_chars_per_line:
                        current_line.append(word)
                        current_length += word_length
                    else:
                        if current_line:
                            lines.append(' '.join(current_line))
                        current_line = [word]
                        current_length = word_length

                if current_line:
                    lines.append(' '.join(current_line))

                # Display wrapped text
                for i, line in enumerate(lines[:2]):  # Max 2 lines
                    line_y = current_y + (i * 13)  # Half line height for wrapped text
                    if line_y < (top_margin + max_visible_height):
                        headline_text = self.ws.font_tiny.render(line, True, COLORS['white'])
                        self.ws.screen.blit(headline_text, (headline_x, line_y))

                # Store clickable area with URL
                if url:
                    self.ws.clickable_headlines.append({
                        'rect': pygame.Rect(left_margin, current_y, display_width, line_height),
                        'url': url,
                        'text': headline
                    })

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