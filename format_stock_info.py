import pandas as pd

def format_stock_info(info):
    """ 株式情報を見やすい Pandas DataFrame に変換 """
    formatted_data = {
        "項目": ["企業名", "時価総額", "通貨", "PBR"],
        "値": [
            info.get("longName", "N/A"),
            f"{info.get('marketCap', 0):,}円",
            info.get("currency", "N/A"),
            f"{info.get('priceToBook', 0):.2f}"
        ]
    }
    return pd.DataFrame(formatted_data)
