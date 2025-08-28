# create_cache.py
import urllib.request
import json

try:
    url = "https://restcountries.com/v3.1/all?fields=name,capital"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read())

    with open("countries_cache.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ countries_cache.json を作成しました！")
except Exception as e:
    print("❌ エラーが発生しました:", e)
