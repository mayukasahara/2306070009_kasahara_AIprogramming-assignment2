import json
import random
import urllib.request

# APIから国の情報を取得
def fetch_country_data():
    url = "https://restcountries.com/v3.1/all"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    return data

# クイズを1問出題
def ask_capital_quiz(country, all_countries):
    correct_answer = country.get("capital", ["なし"])[0]
    country_name = country["name"]["common"]

    # 不正解用の選択肢（ランダムに他の国から首都を選ぶ）
    incorrect_choices = []
    while len(incorrect_choices) < 3:
        c = random.choice(all_countries)
        cap = c.get("capital", [])
        if cap and cap[0] != correct_answer and cap[0] not in incorrect_choices:
            incorrect_choices.append(cap[0])

    # 正解と不正解を混ぜて選択肢に
    options = incorrect_choices + [correct_answer]
    random.shuffle(options)

    # 問題表示
    print(f"\n【問題】「{country_name}」の首都はどれ？")
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")

    # ユーザーの回答受付
    while True:
        try:
            choice = int(input("番号で答えてください（1-4）: "))
            if 1 <= choice <= 4:
                break
            else:
                print("1〜4の数字を入力してください。")
        except ValueError:
            print("数字を入力してください。")

    selected_answer = options[choice - 1]

    # 結果判定
    if selected_answer == correct_answer:
        print("✅ 正解！")
        return True
    else:
        print(f"❌ 不正解。正解は「{correct_answer}」です。")
        return False

# メイン関数
def main():
    print("🌍 世界の国クイズ（首都編）🌍")
    print("5問出題されます。がんばってください！")

    all_countries = fetch_country_data()
    score = 0

    for i in range(5):
        print(f"\n--- 第{i + 1}問 ---")
        country = random.choice(all_countries)

        # 首都情報がある国に限定
        while not country.get("capital"):
            country = random.choice(all_countries)

        if ask_capital_quiz(country, all_countries):
            score += 1

    print(f"\n🎉 クイズ終了！あなたのスコアは {score}/5 でした！")

if __name__ == "__main__":
    main()
