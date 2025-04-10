from .weather_service import WeatherService
from .mcp_server import mcp, get_weather
from .server import app, start_server
from .client import get_weather as client_get_weather

__version__ = "0.1.0" 
