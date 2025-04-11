import asyncio
import uvicorn
import logging
from fastapi import FastAPI, Request
from .mcp_server import mcp

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title="Weather MCP Server")

@app.post("/mcp")
async def handle_mcp_request(request: Request):
    """MCPリクエストを処理するエンドポイント"""
    try:
        # リクエストボディを取得
        body = await request.json()
        logger.debug(f"Received request: {body}")
        
        if body["method"] == "meta/name":
            return {"jsonrpc": "2.0", "result": "My Custom MCP Server", "id": body["id"]}
        if body["method"] == "meta/version":
            return {"jsonrpc": "2.0", "result": "0.1.0", "id": body["id"]}
        if body["method"] == "resources/list":
            return {
                "jsonrpc": "2.0",
                "result": [
                    {"name": "get_weather", "description": "天気を取得します"}
                ],
                "id": body["id"]
            }
        # MCPリクエストを処理
        if body["method"] == "call_tool":
            tool_name = body["params"]["name"]
            arguments = body["params"]["arguments"]
            
            if tool_name == "get_weather":
                result = await mcp.call_tool(tool_name, arguments)
                logger.debug(f"Tool result: {result}")
                return {"jsonrpc": "2.0", "result": result, "id": body["id"]}
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
        logger.error(f"Error processing request: {e}", exc_info=True)
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
