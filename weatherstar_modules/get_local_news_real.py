#!/usr/bin/env python3
"""
Real local news fetcher for WeatherStar 4000
Gets actual local news based on location using Google News RSS
"""

import requests
import xml.etree.ElementTree as ET
from typing import List, Tuple
from urllib.parse import quote
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def clean_html(text: str) -> str:
    """Remove HTML tags from text"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def get_local_news_by_location(lat: float, lon: float) -> List[Tuple[str, str]]:
    """
    Get real local news headlines based on coordinates
    Returns list of (headline, url) tuples
    """
    headlines = []

    try:
        # First, get the city name for the location
        city_name = get_city_name_from_coords(lat, lon)

        # Try multiple news sources
        headlines = fetch_google_news(city_name)

        # If we don't get enough headlines, add some weather-specific ones
        if len(headlines) < 5:
            headlines.extend(fetch_weather_alerts(lat, lon))

        # If still not enough, use fallback headlines
        if len(headlines) < 3:
            headlines = get_fallback_headlines(city_name)

    except Exception as e:
        logger.warning(f"Error fetching real news: {e}")
        # Return fallback headlines on error
        headlines = get_fallback_headlines("Local Area")

    return headlines[:12]  # Return max 12 headlines

def fetch_google_news(location: str) -> List[Tuple[str, str]]:
    """Fetch news from Google News RSS"""
    headlines = []

    try:
        # Build Google News RSS URL
        # Use location-specific search
        query = quote(f"{location} news")
        url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"

        # Fetch RSS feed
        headers = {
            'User-Agent': 'WeatherStar4000/1.0 (Python RSS Reader)'
        }
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            # Parse RSS XML
            root = ET.fromstring(response.content)

            # Find all news items
            for item in root.findall('.//item')[:10]:
                title_elem = item.find('title')
                link_elem = item.find('link')
                pub_date_elem = item.find('pubDate')

                if title_elem is not None and link_elem is not None:
                    title = clean_html(title_elem.text)
                    # Remove source suffix like " - CNN" from title
                    if ' - ' in title:
                        title = title.rsplit(' - ', 1)[0]

                    # Add "Local:" prefix for local news feel
                    if not title.startswith(('Breaking:', 'Alert:', 'Emergency:')):
                        title = f"Local: {title}"

                    link = link_elem.text
                    headlines.append((title[:100], link))  # Limit title length

        # Also try location-specific topics
        if len(headlines) < 5:
            # Try more specific searches
            specific_searches = [
                f"{location} weather",
                f"{location} traffic",
                f"{location} events",
                f"{location} city council",
                f"{location} schools"
            ]

            for search in specific_searches[:2]:  # Just get a couple more
                query = quote(search)
                url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"

                try:
                    response = requests.get(url, headers=headers, timeout=3)
                    if response.status_code == 200:
                        root = ET.fromstring(response.content)
                        for item in root.findall('.//item')[:2]:
                            title_elem = item.find('title')
                            link_elem = item.find('link')

                            if title_elem is not None and link_elem is not None:
                                title = clean_html(title_elem.text)
                                if ' - ' in title:
                                    title = title.rsplit(' - ', 1)[0]
                                if not any(title.startswith(prefix) for prefix in ['Breaking:', 'Alert:', 'Local:']):
                                    title = f"Local: {title}"
                                headlines.append((title[:100], link))
                except:
                    pass  # Ignore errors for additional searches

    except Exception as e:
        logger.warning(f"Error fetching Google News: {e}")

    return headlines

def fetch_weather_alerts(lat: float, lon: float) -> List[Tuple[str, str]]:
    """Fetch weather-related alerts from NOAA"""
    alerts = []

    try:
        # Get weather alerts from NOAA
        url = f"https://api.weather.gov/alerts/active?point={lat},{lon}"
        headers = {
            'User-Agent': 'WeatherStar4000/1.0',
            'Accept': 'application/json'
        }

        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            features = data.get('features', [])

            for alert in features[:3]:  # Get up to 3 alerts
                properties = alert.get('properties', {})
                event = properties.get('event', '')
                severity = properties.get('severity', '')

                if event:
                    # Format as news headline
                    if severity in ['Extreme', 'Severe']:
                        headline = f"Alert: {event} in Effect"
                    else:
                        headline = f"Weather: {event} Issued"

                    # Use NOAA alert URL
                    alert_id = properties.get('id', '')
                    url = f"https://www.weather.gov/alerts/{alert_id}" if alert_id else "https://www.weather.gov"

                    alerts.append((headline, url))

    except Exception as e:
        logger.debug(f"No weather alerts or error: {e}")

    return alerts

def get_fallback_headlines(city_name: str) -> List[Tuple[str, str]]:
    """Get fallback headlines when real news isn't available"""
    # Use the city name in generic headlines
    return [
        (f"Local: {city_name} Community News and Updates", "https://news.google.com"),
        (f"Weather: Check Latest Conditions for {city_name}", "https://weather.gov"),
        (f"Traffic: Current Road Conditions in {city_name} Area", "https://511.org"),
        (f"Local: {city_name} Events Calendar This Week", "https://local.com/events"),
        (f"Community: {city_name} Announcements and Notices", "https://local.com"),
        ("Breaking: Stay Tuned for Latest Local Updates", "https://news.google.com"),
        (f"Local: {city_name} School District Information", "https://education.com"),
        ("Public Safety: Emergency Services Information", "https://ready.gov"),
        (f"Local: {city_name} Business and Economic News", "https://local.com/business"),
        ("Health: Local Hospital and Clinic Updates", "https://health.gov")
    ]

def get_city_name_from_coords(lat: float, lon: float) -> str:
    """
    Get city name from coordinates using reverse geocoding
    """
    try:
        # Use Nominatim reverse geocoding (free, no API key required)
        url = f"https://nominatim.openstreetmap.org/reverse"
        params = {
            'lat': lat,
            'lon': lon,
            'format': 'json'
        }
        headers = {'User-Agent': 'WeatherStar4000/1.0'}

        response = requests.get(url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            address = data.get('address', {})

            # Try to get city, town, or village
            city = address.get('city') or address.get('town') or address.get('village')
            state = address.get('state', '')

            if city and state:
                return f"{city}, {state}"
            elif city:
                return city

    except Exception:
        pass

    return "Local Area"