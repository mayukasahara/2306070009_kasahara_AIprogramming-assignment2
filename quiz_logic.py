# quiz_logic.py
import json
import random
import os
import urllib.request

# 国データを取得（API or ローカルキャッシュ）
def fetch_countries():
    if os.path.exists("countries_cache.json"):
        with open("countries_cache.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        try:
            url = "https://restcountries.com/v3.1/all"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read())

            # キャッシュ保存
            with open("countries_cache.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            return []

    # 首都がある国だけフィルタ
    return [c for c in data if c.get("capital")]

# クイズ問題を作成
def generate_question(countries, asked):
    while True:
        country = random.choice(countries)
        if country["name"]["common"] not in asked:
            break

    correct_capital = country.get("capital", ["不明"])[0]
    country_name = country["name"]["common"]

    # 他の国から誤答を選ぶ
    incorrect = []
    while len(incorrect) < 3:
        choice = random.choice(countries)
        cap = choice.get("capital", [])
        if cap and cap[0] != correct_capital and cap[0] not in incorrect:
            incorrect.append(cap[0])

    options = incorrect + [correct_capital]
    random.shuffle(options)

    return {
        "country": country_name,
        "correct": correct_capital,
        "options": options
    }
