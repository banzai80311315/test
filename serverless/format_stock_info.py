import yfinance as yf
import pandas as pd

def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    
    # 企業情報を取得
    info = stock.info
    
    # 財務データ取得
    try:
        financials = stock.financials
        balance_sheet = stock.balance_sheet
    except Exception as e:
        print(f"Error fetching financial data: {e}")
        financials, balance_sheet = None, None
    
    # 各指標を取得
    data = {
        "営業利益": financials.loc["Total Revenue"][0] if financials is not None else None,
        "純利益": financials.loc["Net Income"][0] if financials is not None else None,
        "EPS": info.get("trailingEps"),
        "BPS": (balance_sheet.loc["Total Equity Gross Minority Interest"][0] / info["sharesOutstanding"]) 
               if balance_sheet is not None and info.get("sharesOutstanding") else None,
        "PER": info.get("trailingPE"),
        "PBR": info.get("priceToBook"),
        "配当金": info.get("dividendRate"),
        "配当利回り": info.get("dividendYield")
    }

    # DataFrameに変換（転置して見やすく）
    df = pd.DataFrame(data, index=[ticker]).T
    
    return df

# 使用例
# ticker = "7203.T"  # トヨタ自動車（日本株は .T を付ける）
# financial_df = get_financial_data(ticker)
# print(financial_df)