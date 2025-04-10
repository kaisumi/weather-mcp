import asyncio
import uvicorn
from fastapi import FastAPI, Request
from .mcp_server import mcp

app = FastAPI(title="Weather MCP Server")

@app.post("/mcp")
async def handle_mcp_request(request: Request):
    """MCPリクエストを処理するエンドポイント"""
    try:
        # リクエストボディを取得
        body = await request.json()
        
        # MCPリクエストを処理
        if body["method"] == "call_tool":
            tool_name = body["params"]["name"]
            arguments = body["params"]["arguments"]
            
            if tool_name == "get_weather":
                result = await mcp.call_tool(tool_name, arguments)
                return result
            else:
                return {
                    "success": False,
                    "error": f"未知のツール: {tool_name}"
                }
        else:
            return {
                "success": False,
                "error": f"未知のメソッド: {body['method']}"
            }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"リクエストの処理中にエラーが発生しました: {str(e)}"
        }

@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "name": "Weather MCP Server",
        "version": "0.1.0",
        "description": "Open-Meteo APIを使用した天気情報を提供するMCPサーバー",
        "tools": [
            {
                "name": "get_weather",
                "description": "指定した都市の現在の天気情報と3日間の予報を取得します",
                "parameters": {
                    "city": {
                        "type": "string",
                        "description": "天気情報を取得する都市名（例: 東京、New York）"
                    }
                }
            }
        ]
    }

def start_server(host: str = "0.0.0.0", port: int = 8000):
    """サーバーを起動する"""
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server() 