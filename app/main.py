from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mcp import MCPClient
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Weather MCP")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MCPクライアントの初期化
mcp_client = MCPClient(
    api_key=os.getenv("MCP_API_KEY"),
    base_url=os.getenv("MCP_BASE_URL", "https://api.modelcontextprotocol.io")
)

@app.get("/")
async def root():
    return {"message": "Weather MCP API"}

@app.get("/weather/{location}")
async def get_weather(location: str):
    try:
        # MCPを使用して天気情報を取得
        response = await mcp_client.query(
            prompt=f"Get current weather for {location}",
            context={"location": location}
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 