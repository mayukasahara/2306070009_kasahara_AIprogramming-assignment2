# quiz_logic.py
import json
import os
import urllib.request
import random

# 国データ取得（キャッシュあり）
def load_country_data():
    cache_file = "countries_cache.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        try:
            url = "https://restcountries.com/v3.1/all"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read())

            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return data
        except Exception as e:
            print(f"[ERROR] 国データ取得失敗: {e}")
            return []

# クイズ生成（入力国のみ対象）
def generate_question_from_input(countries_data, input_country_names):
    questions = []
    valid_countries = [c for c in countries_data if c.get("capital") and c["name"]["common"] in input_country_names]

    selected = random.sample(valid_countries, min(5, len(valid_countries)))

    for country in selected:
        country_name = country["name"]["common"]
        correct_capital = country["capital"][0]

        # 誤答選択肢を作成
        wrong = []
        while len(wrong) < 3:
            rand = random.choice(countries_data)
            cap = rand.get("capital", [])
            if cap and cap[0] != correct_capital and cap[0] not in wrong:
                wrong.append(cap[0])

        options = wrong + [correct_capital]
        random.shuffle(options)

        questions.append({
            "country": country_name,
            "correct": correct_capital,
            "options": options
        })

    return questions
