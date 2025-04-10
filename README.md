# Weather MCP

Model Context Protocol (MCP)を使用した天気予報アプリケーション

## 概要

このアプリケーションは、Open-Meteo APIを使用して天気予報データを取得・表示するMCPサーバーです。MCPプロトコルを通じて、LLMアプリケーションから天気情報にアクセスすることができます。

## 機能

- 現在の天気情報の表示
- 3日間の天気予報の表示
- 位置情報に基づく天気情報の取得
- MCPプロトコルを通じたアクセス

## セットアップ

1. 依存関係のインストール:
```bash
pip install -e .
```

2. 環境変数の設定:
`.env`ファイルを作成し、必要な環境変数を設定してください。

```
MCP_API_KEY=your_api_key_here
MCP_BASE_URL=http://localhost:8000
```

3. MCPサーバーの起動:
```bash
python -m app.server
```

4. クライアントの実行:
```bash
python -m app.client
```

## MCPツール

### get_weather

指定した都市の現在の天気情報と3日間の予報を取得します。

**パラメータ:**
- `city`: 天気情報を取得する都市名（例: 東京、New York）

**レスポンス例:**
```json
{
  "location": {
    "name": "東京",
    "country": "日本",
    "latitude": 35.6895,
    "longitude": 139.6917,
    "timezone": "Asia/Tokyo"
  },
  "current": {
    "temperature": 22.5,
    "feels_like": 23.1,
    "humidity": 65,
    "wind_speed": 3.2,
    "wind_direction": 180,
    "precipitation": 0,
    "condition": "晴れ",
    "weather_code": 1
  },
  "forecast": [
    {
      "date": "2023-04-10",
      "max_temp": 24.5,
      "min_temp": 15.2,
      "precipitation": 0,
      "condition": "晴れ",
      "sunrise": "05:30",
      "sunset": "18:15"
    },
    ...
  ]
}
```

## ライセンス

MIT 
