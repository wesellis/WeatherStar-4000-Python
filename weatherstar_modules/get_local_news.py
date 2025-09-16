#!/usr/bin/env python3
"""
Local news fetcher for WeatherStar 4000
Gets local news based on location
"""

import requests
import json
from typing import List, Tuple

def get_local_news_by_location(lat: float, lon: float) -> List[Tuple[str, str]]:
    """
    Get local news headlines based on coordinates
    Returns list of (headline, url) tuples
    """
    # For now, return simulated local news
    # In production, this would use a news API with location filtering

    # Could potentially use:
    # - NewsAPI with location parameters
    # - Google News RSS with location
    # - Bing News API with location

    headlines = [
        ("Local: City Council Approves New Community Center Development Downtown", "https://local.news/community-center"),
        ("Breaking: Traffic Alert - Major Accident on Interstate Causes Delays", "https://local.news/traffic"),
        ("Local: School District Announces Snow Day Policy Changes for Winter", "https://local.news/schools"),
        ("Emergency: Severe Weather Warning Issued for County Until Midnight", "https://local.news/weather-alert"),
        ("Local: Fire Department Responds to Structure Fire on Main Street", "https://local.news/fire"),
        ("Community: Local Food Bank Seeks Volunteers for Holiday Season", "https://local.news/volunteers"),
        ("Local: New Business Opens in Historic Downtown District", "https://local.news/business"),
        ("Alert: Water Main Break Affects Service in Several Neighborhoods", "https://local.news/water"),
        ("Local: High School Football Team Advances to State Championship", "https://local.news/sports"),
        ("Public Safety: Police Increase Patrols for Holiday Shopping Season", "https://local.news/safety"),
        ("Local: Hospital Announces Expansion of Emergency Department", "https://local.news/hospital"),
        ("Community: Annual Winter Festival Returns to City Park This Weekend", "https://local.news/festival")
    ]

    return headlines

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