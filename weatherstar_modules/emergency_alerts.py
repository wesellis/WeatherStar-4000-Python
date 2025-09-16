#!/usr/bin/env python3
"""
Emergency Weather Alert System for WeatherStar 4000
Monitors NOAA for severe weather alerts and displays emergency screens
"""

import pygame
import requests
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

# Alert severity colors
ALERT_COLORS = {
    'Extreme': (255, 0, 0),      # Red
    'Severe': (255, 140, 0),      # Dark Orange
    'Moderate': (255, 255, 0),    # Yellow
    'Minor': (255, 255, 255),     # White
    'Unknown': (200, 200, 200)    # Gray
}

# Alert urgency priorities (higher = more urgent)
URGENCY_PRIORITY = {
    'Immediate': 4,
    'Expected': 3,
    'Future': 2,
    'Past': 1,
    'Unknown': 0
}

class EmergencyAlertSystem:
    """Handles emergency weather alerts with audio and visual warnings"""

    def __init__(self, lat: float, lon: float):
        """Initialize the emergency alert system"""
        self.lat = lat
        self.lon = lon
        self.active_alerts = []
        self.last_check = 0
        self.check_interval = 60  # Check every minute
        self.current_alert_index = 0
        self.alert_display_time = 0
        self.alert_shown = False

        # Load alert sound if available
        self.alert_sound = None
        try:
            pygame.mixer.init()
            # You can add a custom alert sound file here
            # self.alert_sound = pygame.mixer.Sound("weatherstar_assets/sounds/alert.wav")
        except:
            logger.warning("Could not initialize alert sound")

    def check_for_alerts(self) -> bool:
        """Check for new emergency weather alerts"""
        current_time = time.time()

        # Only check if enough time has passed
        if current_time - self.last_check < self.check_interval:
            return len(self.active_alerts) > 0

        self.last_check = current_time

        try:
            # Query NOAA API for active alerts
            url = f"https://api.weather.gov/alerts/active?point={self.lat},{self.lon}"
            headers = {
                'User-Agent': 'WeatherStar4000/1.0',
                'Accept': 'application/json'
            }

            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code == 200:
                data = response.json()
                features = data.get('features', [])

                # Process alerts
                new_alerts = []
                for feature in features:
                    properties = feature.get('properties', {})

                    # Extract alert information
                    alert = {
                        'id': properties.get('id', ''),
                        'event': properties.get('event', 'Unknown Event'),
                        'severity': properties.get('severity', 'Unknown'),
                        'urgency': properties.get('urgency', 'Unknown'),
                        'certainty': properties.get('certainty', 'Unknown'),
                        'headline': properties.get('headline', ''),
                        'description': properties.get('description', ''),
                        'instruction': properties.get('instruction', ''),
                        'areas': properties.get('areaDesc', ''),
                        'effective': properties.get('effective', ''),
                        'expires': properties.get('expires', ''),
                        'onset': properties.get('onset', ''),
                        'ends': properties.get('ends', '')
                    }

                    # Only include significant alerts
                    if alert['severity'] in ['Extreme', 'Severe', 'Moderate']:
                        new_alerts.append(alert)

                # Sort by urgency and severity
                new_alerts.sort(key=lambda x: (
                    URGENCY_PRIORITY.get(x['urgency'], 0),
                    x['severity'] == 'Extreme',
                    x['severity'] == 'Severe'
                ), reverse=True)

                # Check if there are new alerts
                if new_alerts and not self.alert_shown:
                    # Play alert sound if new alerts
                    self.play_alert_sound()
                    self.alert_shown = True

                self.active_alerts = new_alerts

                if new_alerts:
                    logger.info(f"Found {len(new_alerts)} active weather alerts")

        except Exception as e:
            logger.error(f"Error checking for alerts: {e}")

        return len(self.active_alerts) > 0

    def play_alert_sound(self):
        """Play emergency alert sound"""
        try:
            if self.alert_sound:
                self.alert_sound.play()
            else:
                # Use system beep as fallback
                print('\a')  # System beep
        except:
            pass

    def draw_emergency_screen(self, screen: pygame.Surface, fonts: Dict):
        """Draw emergency alert screen"""
        if not self.active_alerts:
            return False

        # Get current alert
        alert = self.active_alerts[self.current_alert_index]

        # Fill background with alert color based on severity
        bg_color = ALERT_COLORS.get(alert['severity'], ALERT_COLORS['Unknown'])

        # Create pulsing effect for extreme alerts
        if alert['severity'] == 'Extreme':
            pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500.0
            bg_color = tuple(int(c * (0.7 + 0.3 * pulse)) for c in bg_color)

        # Draw background
        screen.fill((20, 20, 20))  # Dark background

        # Draw alert border
        border_width = 10
        pygame.draw.rect(screen, bg_color, (0, 0, 640, 480), border_width)

        # Draw header
        header_rect = pygame.Rect(border_width, border_width, 640 - border_width * 2, 80)
        pygame.draw.rect(screen, bg_color, header_rect)

        # Draw "EMERGENCY ALERT" text
        if 'font_title' in fonts:
            title_text = fonts['font_title'].render("EMERGENCY ALERT", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(320, 40))
            screen.blit(title_text, title_rect)

        # Draw severity and event type
        y_pos = 100
        if 'font_extended' in fonts:
            severity_text = f"{alert['severity'].upper()} - {alert['event']}"
            sev_surface = fonts['font_extended'].render(severity_text, True, bg_color)
            sev_rect = sev_surface.get_rect(center=(320, y_pos))
            screen.blit(sev_surface, sev_rect)
            y_pos += 40

        # Draw headline
        if alert['headline'] and 'font_normal' in fonts:
            # Word wrap headline
            words = alert['headline'].split()
            lines = []
            current_line = ""

            for word in words:
                test_line = f"{current_line} {word}".strip()
                if fonts['font_normal'].size(test_line)[0] <= 580:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word

            if current_line:
                lines.append(current_line)

            # Draw headline lines
            for line in lines[:3]:  # Max 3 lines
                text = fonts['font_normal'].render(line, True, (255, 255, 255))
                text_rect = text.get_rect(center=(320, y_pos))
                screen.blit(text, text_rect)
                y_pos += 30

        y_pos += 20

        # Draw affected areas
        if alert['areas'] and 'font_small' in fonts:
            areas_label = fonts['font_small'].render("AFFECTED AREAS:", True, bg_color)
            screen.blit(areas_label, (60, y_pos))
            y_pos += 25

            # Word wrap areas
            words = alert['areas'].split()
            lines = []
            current_line = ""

            for word in words:
                test_line = f"{current_line} {word}".strip()
                if fonts['font_small'].size(test_line)[0] <= 520:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word

            if current_line:
                lines.append(current_line)

            for line in lines[:3]:
                text = fonts['font_small'].render(line, True, (255, 255, 255))
                screen.blit(text, (80, y_pos))
                y_pos += 22

        y_pos += 20

        # Draw instructions if available
        if alert['instruction'] and 'font_small' in fonts:
            inst_label = fonts['font_small'].render("ACTION TO TAKE:", True, bg_color)
            screen.blit(inst_label, (60, y_pos))
            y_pos += 25

            # Word wrap instructions
            words = alert['instruction'].split()
            lines = []
            current_line = ""

            for word in words:
                test_line = f"{current_line} {word}".strip()
                if fonts['font_small'].size(test_line)[0] <= 520:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word

            if current_line:
                lines.append(current_line)

            for line in lines[:4]:  # Max 4 lines
                text = fonts['font_small'].render(line, True, (255, 255, 255))
                screen.blit(text, (80, y_pos))
                y_pos += 22

        # Draw expiration time
        if alert['expires'] and 'font_small' in fonts:
            try:
                expires = datetime.fromisoformat(alert['expires'].replace('Z', '+00:00'))
                exp_text = f"Valid Until: {expires.strftime('%I:%M %p %m/%d')}"
                exp_surface = fonts['font_small'].render(exp_text, True, (255, 255, 255))
                exp_rect = exp_surface.get_rect(center=(320, 440))
                screen.blit(exp_surface, exp_rect)
            except:
                pass

        # Draw alert counter if multiple alerts
        if len(self.active_alerts) > 1 and 'font_small' in fonts:
            counter_text = f"Alert {self.current_alert_index + 1} of {len(self.active_alerts)}"
            counter_surface = fonts['font_small'].render(counter_text, True, (255, 255, 255))
            screen.blit(counter_surface, (520, 20))

        return True

    def update_alert_display(self):
        """Update alert display timing and rotation"""
        current_time = time.time()

        # Rotate through alerts every 10 seconds if multiple
        if len(self.active_alerts) > 1:
            if current_time - self.alert_display_time > 10:
                self.current_alert_index = (self.current_alert_index + 1) % len(self.active_alerts)
                self.alert_display_time = current_time

    def has_critical_alert(self) -> bool:
        """Check if there's a critical alert that should interrupt normal display"""
        for alert in self.active_alerts:
            if alert['severity'] == 'Extreme' or (
                alert['severity'] == 'Severe' and alert['urgency'] == 'Immediate'
            ):
                return True
        return False

    def get_alert_summary(self) -> str:
        """Get a summary of active alerts for the ticker"""
        if not self.active_alerts:
            return ""

        alert_types = []
        for alert in self.active_alerts[:3]:  # Show up to 3 alerts
            alert_types.append(f"{alert['severity']} {alert['event']}")

        return " *** WEATHER ALERT: " + " | ".join(alert_types) + " *** "