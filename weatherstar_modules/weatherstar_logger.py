#!/usr/bin/env python3
"""
WeatherStar 4000 Logging System
Comprehensive logging for debugging and monitoring
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
import json
import traceback

class WeatherStarLogger:
    """Custom logger for WeatherStar 4000"""

    def __init__(self, log_dir="logs", log_level=logging.DEBUG):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # Create timestamp for log files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Main log file
        self.main_log = self.log_dir / f"weatherstar_{timestamp}.log"

        # API log file
        self.api_log = self.log_dir / f"api_{timestamp}.log"

        # Error log file
        self.error_log = self.log_dir / f"error_{timestamp}.log"

        # System info log
        self.system_log = self.log_dir / f"system_{timestamp}.json"

        # Create latest symlinks for easy access
        self._create_latest_links(timestamp)

        # Setup loggers
        self.setup_loggers(log_level)

        # Log system info
        self.log_system_info()

    def _create_latest_links(self, timestamp):
        """Create 'latest' symlinks to current log files"""
        latest_main = self.log_dir / "weatherstar_latest.log"
        latest_api = self.log_dir / "api_latest.log"
        latest_error = self.log_dir / "error_latest.log"
        latest_system = self.log_dir / "system_latest.json"

        # Remove old symlinks if they exist
        for link in [latest_main, latest_api, latest_error, latest_system]:
            if link.exists() or link.is_symlink():
                link.unlink()

        # Create new symlinks (on systems that support it)
        try:
            latest_main.symlink_to(f"weatherstar_{timestamp}.log")
            latest_api.symlink_to(f"api_{timestamp}.log")
            latest_error.symlink_to(f"error_{timestamp}.log")
            latest_system.symlink_to(f"system_{timestamp}.json")
        except:
            # Symlinks not supported, copy instead
            pass

    def setup_loggers(self, log_level):
        """Setup different loggers for different components"""

        # Formatter
        detailed_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)-20s | %(funcName)-20s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        simple_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%H:%M:%S'
        )

        # Main logger
        self.main_logger = logging.getLogger('WeatherStar')
        self.main_logger.setLevel(log_level)

        # File handler for main log
        main_handler = logging.FileHandler(self.main_log)
        main_handler.setFormatter(detailed_formatter)
        self.main_logger.addHandler(main_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(simple_formatter)
        console_handler.setLevel(logging.INFO)  # Less verbose on console
        self.main_logger.addHandler(console_handler)

        # API logger
        self.api_logger = logging.getLogger('WeatherStar.API')
        self.api_logger.setLevel(logging.DEBUG)

        api_handler = logging.FileHandler(self.api_log)
        api_handler.setFormatter(detailed_formatter)
        self.api_logger.addHandler(api_handler)

        # Error logger
        self.error_logger = logging.getLogger('WeatherStar.ERROR')
        self.error_logger.setLevel(logging.ERROR)

        error_handler = logging.FileHandler(self.error_log)
        error_handler.setFormatter(detailed_formatter)
        self.error_logger.addHandler(error_handler)

    def log_system_info(self):
        """Log system information for debugging"""
        import platform

        system_info = {
            'timestamp': datetime.now().isoformat(),
            'python_version': sys.version,
            'platform': platform.platform(),
            'system': platform.system(),
            'processor': platform.processor(),
            'python_executable': sys.executable,
            'working_directory': str(Path.cwd()),
        }

        # Check for pygame
        try:
            import pygame
            pygame_info = {
                'version': pygame.version.ver,
                'SDL_version': pygame.version.SDL,
            }
            system_info['pygame'] = pygame_info
        except ImportError:
            system_info['pygame'] = 'Not installed'

        # Check for requests
        try:
            import requests
            system_info['requests_version'] = requests.__version__
        except ImportError:
            system_info['requests'] = 'Not installed'

        # Check display
        try:
            import pygame
            pygame.init()
            info = pygame.display.Info()
            system_info['display'] = {
                'width': info.current_w,
                'height': info.current_h,
                'hardware_accelerated': bool(info.hw),
            }
            pygame.quit()
        except:
            system_info['display'] = 'Could not detect'

        # Write system info
        with open(self.system_log, 'w') as f:
            json.dump(system_info, f, indent=2)

        self.main_logger.info(f"System: {platform.system()} {platform.release()}")
        self.main_logger.info(f"Python: {platform.python_version()}")

    def log_startup(self, lat, lon):
        """Log application startup"""
        self.main_logger.info("=" * 60)
        self.main_logger.info("WeatherStar 4000 Starting")
        self.main_logger.info(f"Location: {lat}, {lon}")
        self.main_logger.info("=" * 60)

    def log_api_call(self, url, response_code=None, error=None):
        """Log API calls"""
        if error:
            self.api_logger.error(f"API Error | {url} | {error}")
            self.error_logger.error(f"API failed: {url} | {error}")
        else:
            self.api_logger.info(f"API Call | {url} | Status: {response_code}")

    def log_weather_data(self, data_type, data):
        """Log weather data received"""
        if data:
            self.main_logger.debug(f"Weather Data | {data_type} | Keys: {list(data.keys())}")
            # Log sample data
            if data_type == "current":
                temp = data.get('temperature', {}).get('value')
                conditions = data.get('textDescription')
                self.main_logger.info(f"Current Weather | Temp: {temp}°C | {conditions}")
        else:
            self.main_logger.warning(f"No data received for {data_type}")

    def log_display_change(self, from_mode, to_mode):
        """Log display mode changes"""
        self.main_logger.debug(f"Display Change | {from_mode} -> {to_mode}")

    def log_asset_load(self, asset_type, asset_name, success=True):
        """Log asset loading"""
        if success:
            self.main_logger.debug(f"Asset Loaded | {asset_type} | {asset_name}")
        else:
            self.main_logger.warning(f"Asset Failed | {asset_type} | {asset_name}")

    def log_error(self, error_msg, exception=None):
        """Log errors with traceback"""
        self.error_logger.error(error_msg)
        if exception:
            tb = traceback.format_exc()
            self.error_logger.error(f"Traceback:\n{tb}")
            self.main_logger.error(f"Error: {error_msg} | {str(exception)}")

    def log_shutdown(self):
        """Log application shutdown"""
        self.main_logger.info("=" * 60)
        self.main_logger.info("WeatherStar 4000 Shutting Down")
        self.main_logger.info("=" * 60)

    def get_log_summary(self):
        """Get a summary of current session"""
        summary = {
            'main_log': str(self.main_log),
            'api_log': str(self.api_log),
            'error_log': str(self.error_log),
            'system_log': str(self.system_log),
        }
        return summary


# Global logger instance
logger = None

def init_logger(log_dir="logs", log_level=logging.DEBUG):
    """Initialize the global logger"""
    global logger
    logger = WeatherStarLogger(log_dir, log_level)
    return logger

def get_logger():
    """Get the global logger instance"""
    global logger
    if logger is None:
        logger = init_logger()
    return logger