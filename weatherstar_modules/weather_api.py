"""
Optimized Weather API Module
Handles both NOAA (US) and Open Meteo (International) weather data
"""

import time
import requests
import logging
from typing import Dict, Optional, Any
from functools import lru_cache
import json

logger = logging.getLogger(__name__)


class WeatherAPIBase:
    """Base class for weather APIs with optimized caching"""

    def __init__(self, cache_ttl: int = 300):
        self.cache = {}
        self.cache_time = {}
        self.cache_ttl = cache_ttl
        self.session = requests.Session()  # Reuse connection
        self.session.headers.update({'User-Agent': 'WeatherStar4000/2.0'})

    def _cache_key(self, *args) -> str:
        """Generate cache key from arguments"""
        return json.dumps(args, sort_keys=True)

    def _is_cache_valid(self, key: str, max_age: Optional[int] = None) -> bool:
        """Check if cached data is still valid"""
        if key not in self.cache_time:
            return False
        age = time.time() - self.cache_time[key]
        ttl = max_age if max_age else self.cache_ttl
        return age < ttl

    def _get_cached(self, key: str, max_age: Optional[int] = None) -> Optional[Any]:
        """Get cached data if valid"""
        if self._is_cache_valid(key, max_age):
            logger.debug(f"Cache hit: {key[:50]}...")
            return self.cache.get(key)
        return None

    def _set_cache(self, key: str, data: Any):
        """Store data in cache"""
        self.cache[key] = data
        self.cache_time[key] = time.time()
        logger.debug(f"Cached: {key[:50]}...")

    def _fetch_json(self, url: str, params: Dict = None, timeout: int = 10) -> Optional[Dict]:
        """Fetch JSON data with error handling"""
        try:
            response = self.session.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {e}")
            return None


class NOAAWeatherAPI(WeatherAPIBase):
    """Optimized NOAA Weather API for US locations"""

    def __init__(self):
        super().__init__(cache_ttl=300)
        self.base_url = "https://api.weather.gov"

    @lru_cache(maxsize=128)
    def get_grid_point(self, lat: float, lon: float) -> Optional[Dict]:
        """Get weather grid point data with caching"""
        key = self._cache_key("grid", lat, lon)
        cached = self._get_cached(key, 3600)  # Cache for 1 hour
        if cached:
            return cached

        url = f"{self.base_url}/points/{lat:.4f},{lon:.4f}"
        data = self._fetch_json(url)

        if data and 'properties' in data:
            result = data['properties']
            self._set_cache(key, result)
            return result
        return None

    def get_forecast(self, lat: float, lon: float) -> Optional[Dict]:
        """Get weather forecast"""
        # First get grid point
        grid = self.get_grid_point(lat, lon)
        if not grid:
            return None

        key = self._cache_key("forecast", lat, lon)
        cached = self._get_cached(key, 600)  # Cache for 10 minutes
        if cached:
            return cached

        forecast_url = grid.get('forecast')
        if not forecast_url:
            return None

        data = self._fetch_json(forecast_url)
        if data and 'properties' in data:
            result = data['properties']
            self._set_cache(key, result)
            return result
        return None

    def get_current_conditions(self, lat: float, lon: float) -> Optional[Dict]:
        """Get current weather conditions"""
        grid = self.get_grid_point(lat, lon)
        if not grid:
            return None

        stations_url = grid.get('observationStations')
        if not stations_url:
            return None

        key = self._cache_key("current", lat, lon)
        cached = self._get_cached(key, 300)  # Cache for 5 minutes
        if cached:
            return cached

        # Get stations
        stations_data = self._fetch_json(stations_url)
        if not stations_data or 'features' not in stations_data:
            return None

        stations = stations_data.get('features', [])
        if not stations:
            return None

        # Try first few stations
        for station in stations[:3]:
            station_id = station.get('properties', {}).get('stationIdentifier')
            if station_id:
                obs_url = f"{self.base_url}/stations/{station_id}/observations/latest"
                obs_data = self._fetch_json(obs_url)
                if obs_data and 'properties' in obs_data:
                    result = obs_data['properties']
                    self._set_cache(key, result)
                    return result

        return None


class OpenMeteoAPI(WeatherAPIBase):
    """Optimized Open Meteo API for international weather"""

    def __init__(self):
        super().__init__(cache_ttl=600)
        self.base_url = "https://api.open-meteo.com/v1"
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1"

    def get_current_weather(self, lat: float, lon: float, units: str = 'imperial') -> Optional[Dict]:
        """Get current weather with optimized caching"""
        key = self._cache_key("current", lat, lon, units)
        cached = self._get_cached(key, 300)  # 5 minute cache
        if cached:
            return cached

        temp_unit = 'fahrenheit' if units == 'imperial' else 'celsius'
        wind_unit = 'mph' if units == 'imperial' else 'kmh'

        params = {
            'latitude': lat,
            'longitude': lon,
            'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,pressure_msl,wind_speed_10m,wind_direction_10m',
            'temperature_unit': temp_unit,
            'wind_speed_unit': wind_unit,
            'timezone': 'auto'
        }

        url = f"{self.base_url}/forecast"
        data = self._fetch_json(url, params)

        if data and 'current' in data:
            result = self._process_current_data(data)
            self._set_cache(key, result)
            return result
        return None

    def get_forecast(self, lat: float, lon: float, days: int = 7, units: str = 'imperial') -> Optional[Dict]:
        """Get weather forecast with smart caching"""
        key = self._cache_key("forecast", lat, lon, days, units)
        cached = self._get_cached(key, 1800)  # 30 minute cache
        if cached:
            return cached

        temp_unit = 'fahrenheit' if units == 'imperial' else 'celsius'
        wind_unit = 'mph' if units == 'imperial' else 'kmh'

        params = {
            'latitude': lat,
            'longitude': lon,
            'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max',
            'hourly': 'temperature_2m,precipitation,weather_code',
            'temperature_unit': temp_unit,
            'wind_speed_unit': wind_unit,
            'timezone': 'auto',
            'forecast_days': days
        }

        url = f"{self.base_url}/forecast"
        data = self._fetch_json(url, params)

        if data:
            result = self._process_forecast_data(data)
            self._set_cache(key, result)
            return result
        return None

    def _process_current_data(self, data: Dict) -> Dict:
        """Process current weather data"""
        current = data.get('current', {})
        return {
            'temperature': current.get('temperature_2m'),
            'feels_like': current.get('apparent_temperature'),
            'humidity': current.get('relative_humidity_2m'),
            'pressure': current.get('pressure_msl'),
            'wind_speed': current.get('wind_speed_10m'),
            'wind_direction': current.get('wind_direction_10m'),
            'precipitation': current.get('precipitation'),
            'weather_code': current.get('weather_code'),
            'conditions': self._get_weather_condition(current.get('weather_code', 0))
        }

    def _process_forecast_data(self, data: Dict) -> Dict:
        """Process forecast data efficiently"""
        daily = data.get('daily', {})
        hourly = data.get('hourly', {})

        # Process daily forecast
        daily_forecast = []
        for i in range(len(daily.get('time', []))):
            daily_forecast.append({
                'date': daily['time'][i],
                'high': daily['temperature_2m_max'][i],
                'low': daily['temperature_2m_min'][i],
                'precipitation': daily['precipitation_sum'][i],
                'wind_speed': daily['wind_speed_10m_max'][i],
                'weather_code': daily['weather_code'][i],
                'conditions': self._get_weather_condition(daily['weather_code'][i])
            })

        # Process hourly forecast (limit to 48 hours for performance)
        hourly_forecast = []
        for i in range(min(48, len(hourly.get('time', [])))):
            hourly_forecast.append({
                'time': hourly['time'][i],
                'temperature': hourly['temperature_2m'][i],
                'precipitation': hourly['precipitation'][i],
                'weather_code': hourly['weather_code'][i]
            })

        return {
            'daily': daily_forecast,
            'hourly': hourly_forecast
        }

    @lru_cache(maxsize=256)
    def _get_weather_condition(self, code: int) -> str:
        """Convert weather code to condition string (cached)"""
        conditions = {
            0: "Clear", 1: "Mostly Clear", 2: "Partly Cloudy", 3: "Cloudy",
            45: "Fog", 48: "Freezing Fog", 51: "Light Drizzle", 53: "Drizzle",
            61: "Light Rain", 63: "Rain", 65: "Heavy Rain", 71: "Light Snow",
            73: "Snow", 75: "Heavy Snow", 95: "Thunderstorm"
        }
        return conditions.get(code, "Unknown")


class UnifiedWeatherAPI:
    """Unified API that intelligently chooses between NOAA and Open Meteo"""

    def __init__(self):
        self.noaa = NOAAWeatherAPI()
        self.open_meteo = OpenMeteoAPI()
        self._is_us_cache = {}

    @lru_cache(maxsize=512)
    def _is_us_location(self, lat: float, lon: float) -> bool:
        """Check if coordinates are in US (cached)"""
        # Continental US bounds
        us_bounds = {
            'lat_min': 24.0, 'lat_max': 49.0,
            'lon_min': -125.0, 'lon_max': -66.0
        }

        # Check continental US
        if (us_bounds['lat_min'] <= lat <= us_bounds['lat_max'] and
            us_bounds['lon_min'] <= lon <= us_bounds['lon_max']):
            return True

        # Check Alaska
        if 51 <= lat <= 72 and -180 <= lon <= -129:
            return True

        # Check Hawaii
        if 18 <= lat <= 23 and -161 <= lon <= -154:
            return True

        return False

    def get_weather(self, lat: float, lon: float, prefer_international: bool = False) -> Dict:
        """Get weather from appropriate source"""
        if not prefer_international and self._is_us_location(lat, lon):
            # Try NOAA first for US locations
            logger.info(f"Using NOAA API for US location: {lat}, {lon}")
            current = self.noaa.get_current_conditions(lat, lon)
            forecast = self.noaa.get_forecast(lat, lon)

            if current or forecast:
                return {
                    'source': 'NOAA',
                    'current': current,
                    'forecast': forecast
                }

        # Use Open Meteo for international or as fallback
        logger.info(f"Using Open Meteo API for location: {lat}, {lon}")
        current = self.open_meteo.get_current_weather(lat, lon)
        forecast = self.open_meteo.get_forecast(lat, lon)

        return {
            'source': 'Open Meteo',
            'current': current,
            'forecast': forecast
        }