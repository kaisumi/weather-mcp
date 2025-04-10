from mcp import Implementation
from mcp.server.fastmcp import FastMCP
from app.weather_service import WeatherService

implementation = Implementation(
    name="Weather MCP Server",
    version="0.1.0"
)
mcp = FastMCP(implementation)

weather_service = WeatherService()

@mcp.tool()
async def get_weather(city: str) -> dict:
    """指定した都市の天気情報を返すTool"""
    if not city:
        return {"error": "都市名が指定されていません"}
    
    try:
        result = await weather_service.get_weather_for_city(city)
        return result
    except Exception as e:
        return {
            "error": str(e)
        } 
