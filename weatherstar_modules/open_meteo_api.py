#!/usr/bin/env python3
"""
Open Meteo Weather API for international weather support
Free, no API key required, works globally
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class OpenMeteoAPI:
    """Open Meteo Weather API client for international weather data"""

    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1"
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1"
        self.cache = {}
        self.cache_time = {}

    def _is_cache_valid(self, key: str, max_age: int = 300) -> bool:
        """Check if cached data is still valid"""
        if key not in self.cache_time:
            return False
        return (time.time() - self.cache_time[key]) < max_age

    def _cache_data(self, key: str, data: any):
        """Cache data with timestamp"""
        self.cache[key] = data
        self.cache_time[key] = time.time()

    def get_location_name(self, lat: float, lon: float) -> str:
        """Get location name from coordinates"""
        cache_key = f"location_{lat}_{lon}"

        if self._is_cache_valid(cache_key, 3600):  # Cache for 1 hour
            return self.cache[cache_key]

        try:
            # Use geocoding API for reverse lookup
            url = f"{self.geocoding_url}/search"
            params = {
                'name': f"{lat},{lon}",
                'count': 1,
                'language': 'en',
                'format': 'json'
            }

            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('results'):
                    result = data['results'][0]
                    city = result.get('name', '')
                    country = result.get('country', '')
                    admin1 = result.get('admin1', '')  # State/Province

                    if city and country:
                        location = f"{city}, {admin1 if admin1 else country}"
                        self._cache_data(cache_key, location)
                        return location
        except Exception as e:
            print(f"Error getting location name: {e}")

        return f"{lat:.2f}, {lon:.2f}"

    def get_current_weather(self, lat: float, lon: float, units: str = 'imperial') -> Dict:
        """Get current weather conditions"""
        cache_key = f"current_{lat}_{lon}_{units}"

        if self._is_cache_valid(cache_key, 300):  # Cache for 5 minutes
            return self.cache[cache_key]

        try:
            temp_unit = 'fahrenheit' if units == 'imperial' else 'celsius'
            wind_unit = 'mph' if units == 'imperial' else 'kmh'
            precip_unit = 'inch' if units == 'imperial' else 'mm'

            url = f"{self.base_url}/forecast"
            params = {
                'latitude': lat,
                'longitude': lon,
                'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,pressure_msl,wind_speed_10m,wind_direction_10m,wind_gusts_10m',
                'temperature_unit': temp_unit,
                'wind_speed_unit': wind_unit,
                'precipitation_unit': precip_unit,
                'timezone': 'auto'
            }

            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                current = data.get('current', {})

                # Map weather codes to conditions
                weather_code = current.get('weather_code', 0)
                conditions = self._get_weather_condition(weather_code)

                result = {
                    'temperature': current.get('temperature_2m'),
                    'feels_like': current.get('apparent_temperature'),
                    'humidity': current.get('relative_humidity_2m'),
                    'pressure': current.get('pressure_msl'),
                    'wind_speed': current.get('wind_speed_10m'),
                    'wind_direction': current.get('wind_direction_10m'),
                    'wind_gust': current.get('wind_gusts_10m'),
                    'precipitation': current.get('precipitation'),
                    'weather_code': weather_code,
                    'conditions': conditions,
                    'timezone': data.get('timezone'),
                    'location': self.get_location_name(lat, lon)
                }

                self._cache_data(cache_key, result)
                return result

        except Exception as e:
            print(f"Error fetching current weather: {e}")

        return {}

    def get_forecast(self, lat: float, lon: float, days: int = 7, units: str = 'imperial') -> Dict:
        """Get weather forecast"""
        cache_key = f"forecast_{lat}_{lon}_{days}_{units}"

        if self._is_cache_valid(cache_key, 1800):  # Cache for 30 minutes
            return self.cache[cache_key]

        try:
            temp_unit = 'fahrenheit' if units == 'imperial' else 'celsius'
            wind_unit = 'mph' if units == 'imperial' else 'kmh'
            precip_unit = 'inch' if units == 'imperial' else 'mm'

            url = f"{self.base_url}/forecast"
            params = {
                'latitude': lat,
                'longitude': lon,
                'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,snowfall_sum,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,sunrise,sunset',
                'hourly': 'temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,wind_direction_10m',
                'temperature_unit': temp_unit,
                'wind_speed_unit': wind_unit,
                'precipitation_unit': precip_unit,
                'timezone': 'auto',
                'forecast_days': days
            }

            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()

                # Process daily forecast
                daily_data = data.get('daily', {})
                daily_forecast = []

                for i in range(len(daily_data.get('time', []))):
                    day_forecast = {
                        'date': daily_data['time'][i],
                        'high': daily_data['temperature_2m_max'][i],
                        'low': daily_data['temperature_2m_min'][i],
                        'precipitation': daily_data['precipitation_sum'][i],
                        'rain': daily_data['rain_sum'][i],
                        'snow': daily_data['snowfall_sum'][i],
                        'precipitation_probability': daily_data['precipitation_probability_max'][i],
                        'wind_speed': daily_data['wind_speed_10m_max'][i],
                        'wind_gust': daily_data['wind_gusts_10m_max'][i],
                        'weather_code': daily_data['weather_code'][i],
                        'conditions': self._get_weather_condition(daily_data['weather_code'][i]),
                        'sunrise': daily_data['sunrise'][i],
                        'sunset': daily_data['sunset'][i]
                    }
                    daily_forecast.append(day_forecast)

                # Process hourly forecast
                hourly_data = data.get('hourly', {})
                hourly_forecast = []

                for i in range(min(48, len(hourly_data.get('time', [])))):  # 48 hours
                    hour_forecast = {
                        'time': hourly_data['time'][i],
                        'temperature': hourly_data['temperature_2m'][i],
                        'humidity': hourly_data['relative_humidity_2m'][i],
                        'precipitation': hourly_data['precipitation'][i],
                        'weather_code': hourly_data['weather_code'][i],
                        'conditions': self._get_weather_condition(hourly_data['weather_code'][i]),
                        'wind_speed': hourly_data['wind_speed_10m'][i],
                        'wind_direction': hourly_data['wind_direction_10m'][i]
                    }
                    hourly_forecast.append(hour_forecast)

                result = {
                    'daily': daily_forecast,
                    'hourly': hourly_forecast,
                    'timezone': data.get('timezone'),
                    'location': self.get_location_name(lat, lon)
                }

                self._cache_data(cache_key, result)
                return result

        except Exception as e:
            print(f"Error fetching forecast: {e}")

        return {}

    def _get_weather_condition(self, code: int) -> str:
        """Convert Open Meteo weather code to condition string"""
        weather_codes = {
            0: "Clear",
            1: "Mostly Clear",
            2: "Partly Cloudy",
            3: "Cloudy",
            45: "Fog",
            48: "Freezing Fog",
            51: "Light Drizzle",
            53: "Drizzle",
            55: "Heavy Drizzle",
            56: "Light Freezing Drizzle",
            57: "Freezing Drizzle",
            61: "Light Rain",
            63: "Rain",
            65: "Heavy Rain",
            66: "Light Freezing Rain",
            67: "Freezing Rain",
            71: "Light Snow",
            73: "Snow",
            75: "Heavy Snow",
            77: "Snow Grains",
            80: "Light Showers",
            81: "Showers",
            82: "Heavy Showers",
            85: "Light Snow Showers",
            86: "Snow Showers",
            95: "Thunderstorm",
            96: "Thunderstorm with Light Hail",
            99: "Thunderstorm with Heavy Hail"
        }

        return weather_codes.get(code, "Unknown")

    def get_air_quality(self, lat: float, lon: float) -> Dict:
        """Get air quality data"""
        cache_key = f"aqi_{lat}_{lon}"

        if self._is_cache_valid(cache_key, 1800):  # Cache for 30 minutes
            return self.cache[cache_key]

        try:
            url = "https://air-quality-api.open-meteo.com/v1/air-quality"
            params = {
                'latitude': lat,
                'longitude': lon,
                'current': 'us_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone',
                'timezone': 'auto'
            }

            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                current = data.get('current', {})

                result = {
                    'aqi': current.get('us_aqi'),
                    'pm10': current.get('pm10'),
                    'pm25': current.get('pm2_5'),
                    'co': current.get('carbon_monoxide'),
                    'no2': current.get('nitrogen_dioxide'),
                    'so2': current.get('sulphur_dioxide'),
                    'o3': current.get('ozone'),
                    'category': self._get_aqi_category(current.get('us_aqi', 0))
                }

                self._cache_data(cache_key, result)
                return result

        except Exception as e:
            print(f"Error fetching air quality: {e}")

        return {}

    def _get_aqi_category(self, aqi: int) -> str:
        """Get AQI category from value"""
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 150:
            return "Unhealthy for Sensitive Groups"
        elif aqi <= 200:
            return "Unhealthy"
        elif aqi <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous"