# Weather MCP サーバーの実装

## 概要
Weather MCPサーバーを実装し、天気情報を取得・提供するAPIを構築しました。

## 主な変更点
- FastMCPを使用したサーバーの実装
- 天気情報を取得するエンドポイントの追加
- 環境変数による設定管理
- クライアントライブラリの実装

## 技術スタック
- Python 3.11
- FastMCP
- Poetry（依存関係管理）

## セットアップ方法
1. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集して必要な値を設定
```

2. 依存関係のインストール
```bash
poetry install
```

3. サーバーの起動
```bash
poetry run python -m app.server
```

## 動作確認方法
1. サーバーを起動
2. クライアントを使用して天気情報を取得
```bash
poetry run python -m app.client
```

## 注意点
- 環境変数`MCP_API_KEY`と`MCP_BASE_URL`の設定が必要です
- 天気情報の取得には有効な都市名が必要です 
