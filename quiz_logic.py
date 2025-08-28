# quiz_logic.py
import json
import os
import urllib.request
import random

# 国データ取得（キャッシュ優先）
def fetch_countries():
    cache_file = "countries_cache.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        try:
            url = "https://restcountries.com/v3.1/all"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read())
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[ERROR] 国データ取得失敗: {e}")
            return []

    return [c for c in data if c.get("capital") and c.get("name", {}).get("common")]

# クイズ1問を生成
def generate_question(countries, asked):
    while True:
        country = random.choice(countries)
        if country["name"]["common"] not in asked:
            break

    country_name = country["name"]["common"]
    correct_capital = country["capital"][0]

    # 誤答を3つ作成
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
