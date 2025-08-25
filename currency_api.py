import requests

API_URL = "https://api.exchangerate.host/latest"

def get_exchange_rate(base: str, target: str) -> float:
    params = {
        "base": base.upper(),
        "symbols": target.upper()
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    data = response.json()

    print("APIレスポンス:", data)  # ここでレスポンス全体を表示

    rates = data.get("rates")
    if rates and target.upper() in rates:
        return float(rates[target.upper()])
    else:
        raise ValueError(f"為替レートが見つかりませんでした: {base} → {target}")
