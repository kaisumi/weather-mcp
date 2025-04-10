import aiohttp
import json
from typing import Dict, Any, Optional

class WeatherService:
    """Open-Meteo APIを使用して天気情報を取得するサービス"""
    
    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
    
    async def get_coordinates(self, city: str) -> Dict[str, Any]:
        """都市名から緯度経度を取得する"""
        async with aiohttp.ClientSession() as session:
            params = {
                "name": city,
                "count": 1,
                "language": "ja",
                "format": "json"
            }
            async with session.get(self.GEOCODING_URL, params=params) as response:
                if response.status != 200:
                    raise Exception(f"Geocoding API error: {response.status}")
                
                data = await response.json()
                if not data.get("results"):
                    raise Exception(f"City '{city}' not found")
                
                return data["results"][0]
    
    async def get_weather(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """緯度経度から天気情報を取得する"""
        async with aiohttp.ClientSession() as session:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", 
                           "precipitation", "weather_code", "wind_speed_10m", "wind_direction_10m"],
                "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", 
                         "weather_code", "sunrise", "sunset"],
                "timezone": "auto"
            }
            async with session.get(self.WEATHER_URL, params=params) as response:
                if response.status != 200:
                    raise Exception(f"Weather API error: {response.status}")
                
                return await response.json()
    
    def get_weather_condition(self, code: int) -> str:
        """天気コードから天気の状態を取得する"""
        weather_codes = {
            0: "快晴",
            1: "晴れ",
            2: "一部曇り",
            3: "曇り",
            45: "霧",
            48: "霧氷",
            51: "軽い霧雨",
            53: "霧雨",
            55: "強い霧雨",
            56: "軽い霧雨（凍る）",
            57: "霧雨（凍る）",
            61: "小雨",
            63: "雨",
            65: "強い雨",
            66: "小雨（凍る）",
            67: "強い雨（凍る）",
            71: "小雪",
            73: "雪",
            75: "強い雪",
            77: "雪の粒",
            80: "小雨のシャワー",
            81: "雨のシャワー",
            82: "強い雨のシャワー",
            85: "小雪のシャワー",
            86: "強い雪のシャワー",
            95: "雷雨",
            96: "雷雨と雹",
            99: "強い雷雨と雹"
        }
        return weather_codes.get(code, "不明")
    
    async def get_weather_for_city(self, city: str) -> Dict[str, Any]:
        """都市名から天気情報を取得する"""
        try:
            # 都市名から緯度経度を取得
            location = await self.get_coordinates(city)
            
            # 緯度経度から天気情報を取得
            weather_data = await self.get_weather(location["latitude"], location["longitude"])
            
            # 現在の天気情報を整形
            current = weather_data["current"]
            current_condition = self.get_weather_condition(current["weather_code"])
            
            # 日次予報を整形
            daily = weather_data["daily"]
            daily_forecast = []
            
            for i in range(min(3, len(daily["time"]))):
                daily_forecast.append({
                    "date": daily["time"][i],
                    "max_temp": daily["temperature_2m_max"][i],
                    "min_temp": daily["temperature_2m_min"][i],
                    "precipitation": daily["precipitation_sum"][i],
                    "condition": self.get_weather_condition(daily["weather_code"][i]),
                    "sunrise": daily["sunrise"][i],
                    "sunset": daily["sunset"][i]
                })
            
            # 結果を整形
            result = {
                "location": {
                    "name": location["name"],
                    "country": location["country"],
                    "latitude": location["latitude"],
                    "longitude": location["longitude"],
                    "timezone": weather_data["timezone"]
                },
                "current": {
                    "temperature": current["temperature_2m"],
                    "feels_like": current["apparent_temperature"],
                    "humidity": current["relative_humidity_2m"],
                    "wind_speed": current["wind_speed_10m"],
                    "wind_direction": current["wind_direction_10m"],
                    "precipitation": current["precipitation"],
                    "condition": current_condition,
                    "weather_code": current["weather_code"]
                },
                "forecast": daily_forecast
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"天気情報の取得に失敗しました: {str(e)}") 
