import requests

API_URL = "https://api.exchangerate.host/latest"

def get_exchange_rate(base: str, target: str) -> float:
    """
    base通貨からtarget通貨への為替レートを取得
    """
    params = {
        "base": base.upper(),
        "symbols": target.upper()
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    data = response.json()

    if "rates" in data and target.upper() in data["rates"]:
        return data["rates"][target.upper()]
    else:
        raise ValueError("為替レートが見つかりませんでした。")
