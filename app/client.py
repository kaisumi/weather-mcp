import asyncio
import json
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def get_weather(city: str):
    """指定した都市の天気情報を取得する"""
    try:
        # HTTPクライアントを初期化
        base_url = os.getenv("MCP_BASE_URL", "http://localhost:8000")
        async with httpx.AsyncClient(base_url=base_url) as client:
            # 天気情報を取得
            response = await client.post(
                "/mcp",
                json={
                    "jsonrpc": "2.0",
                    "method": "call_tool",
                    "params": {
                        "name": "get_weather",
                        "arguments": {"city": city}
                    },
                    "id": 1
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # レスポンスを表示
            if "result" in data and isinstance(data["result"], list) and len(data["result"]) > 0:
                result = data["result"][0]
                if "text" in result:
                    weather_data = json.loads(result["text"])
                    if "error" in weather_data:
                        print(f"エラー: {weather_data['error']}")
                        return
                    
                    location = weather_data["location"]
                    current = weather_data["current"]
                    forecast = weather_data["forecast"]
                    
                    print(f"\n{city}の天気情報:")
                    print(f"場所: {location['name']}, {location['country']}")
                    print(f"緯度: {location['latitude']}, 経度: {location['longitude']}")
                    print(f"タイムゾーン: {location['timezone']}")
                    
                    print("\n現在の天気:")
                    print(f"  気温: {current['temperature']}°C")
                    print(f"  体感温度: {current['feels_like']}°C")
                    print(f"  湿度: {current['humidity']}%")
                    print(f"  風速: {current['wind_speed']}m/s")
                    print(f"  風向: {current['wind_direction']}°")
                    print(f"  降水量: {current['precipitation']}mm")
                    print(f"  天気: {current['condition']}")
                    
                    print("\n天気予報:")
                    for day in forecast:
                        print(f"\n{day['date']}:")
                        print(f"  最高気温: {day['max_temp']}°C")
                        print(f"  最低気温: {day['min_temp']}°C")
                        print(f"  降水量: {day['precipitation']}mm")
                        print(f"  天気: {day['condition']}")
                        print(f"  日の出: {day['sunrise']}")
                        print(f"  日の入: {day['sunset']}")
                else:
                    print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

async def main():
    """メイン関数"""
    city = input("天気情報を取得する都市名を入力してください: ")
    await get_weather(city)

if __name__ == "__main__":
    asyncio.run(main()) 
