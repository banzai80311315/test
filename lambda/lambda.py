import json
import boto3
import yfinance as yf

# DynamoDB クライアントを作成
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("JP_Stocks")

def get_tickers_from_dynamodb():
    """DynamoDB から企業リストを取得"""
    try:
        response = table.scan()  # 全件取得
        items = response.get("Items", [])
        tickers = [item["Ticker"] for item in items if "Ticker" in item]
        return tickers
    except Exception as e:
        print(f"Error fetching tickers from DynamoDB: {e}")
        return []

def get_pbr_batch(tickers):
    """複数の銘柄の PBR を取得"""
    try:
        stocks = yf.Tickers(" ".join(tickers))
        results = []

        for ticker in tickers:
            stock_info = stocks.tickers.get(ticker, {}).info
            pbr = stock_info.get("priceToBook", None)

            if pbr is not None and pbr <= 1:
                results.append({
                    "ticker": ticker,
                    "name": stock_info.get("longName", "N/A"),
                    "pbr": round(pbr, 2)
                })

        return results
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def lambda_handler(event, context):
    """Lambda のエントリポイント"""
    tickers = get_tickers_from_dynamodb()  # DynamoDB からティッカーを取得

    if not tickers:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Failed to retrieve tickers from DynamoDB"})
        }

    filtered_stocks = get_pbr_batch(tickers)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps(filtered_stocks, ensure_ascii=False)
    }
