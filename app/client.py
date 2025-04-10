import asyncio
import json
import httpx
from mcp import Implementation
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
                    "method": "call_tool",
                    "params": {
                        "name": "get_weather",
                        "arguments": {"city": city}
                    }
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # レスポンスを表示
            if isinstance(data, list) and len(data) > 0 and "text" in data[0]:
                weather_data = json.loads(data[0]["text"])
                print(f"\n{city}の天気情報:")
                print("\n現在の天気:")
                print(f"  気温: {weather_data['current']['temperature']}°C")
                print(f"  体感温度: {weather_data['current']['feels_like']}°C")
                print(f"  湿度: {weather_data['current']['humidity']}%")
                print(f"  風速: {weather_data['current']['wind_speed']}m/s")
                print(f"  天気: {weather_data['current']['condition']}")
                
                print("\n天気予報:")
                for forecast in weather_data['forecast']:
                    date = forecast['date']
                    print(f"\n{date}:")
                    print(f"  最高気温: {forecast['max_temp']}°C")
                    print(f"  最低気温: {forecast['min_temp']}°C")
                    print(f"  天気: {forecast['condition']}")
                    print(f"  日の出: {forecast['sunrise']}")
                    print(f"  日の入: {forecast['sunset']}")
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