import urllib.request, json

url = "https://restcountries.com/v3.1/all"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    data = json.loads(res.read())

with open("countries_cache.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
