import json
import random
import urllib.request

API_URL = "https://restcountries.com/v3.1/all"

def fetch_countries():
    try:
        with urllib.request.urlopen(API_URL) as res:
            data = json.loads(res.read())
        # 首都がある国だけに絞る
        countries = [c for c in data if c.get("capital")]
        return countries
    except Exception as e:
        print("API取得エラー:", e)
        return []

def generate_question(countries, asked_countries):
    # まだ出題していない国から選ぶ
    available = [c for c in countries if c["name"]["common"] not in asked_countries and c.get("capital")]
    if not available:
        return None, None, None  # 問題なし

    country = random.choice(available)
    correct_capital = country["capital"][0]
    country_name = country["name"]["common"]

    # 選択肢作成（正解＋ランダムに3つの不正解）
    options = set()
    options.add(correct_capital)
    while len(options) < 4:
        c = random.choice(countries)
        cap = c.get("capital")
        if cap:
            options.add(cap[0])
    options = list(options)
    random.shuffle(options)

    return country_name, correct_capital, options
