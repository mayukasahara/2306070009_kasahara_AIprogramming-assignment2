import json
import random
import urllib.request
import streamlit as st

@st.cache_data
def fetch_country_data():
    url = "https://restcountries.com/v3.1/all"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
    # 首都のある国だけに絞る
    countries_with_capital = [c for c in data if c.get("capital")]
    return countries_with_capital

def generate_question(all_countries, asked_countries):
    while True:
        country = random.choice(all_countries)
        if country["name"]["common"] not in asked_countries:
            correct_answer = country["capital"][0]
            country_name = country["name"]["common"]
            break

    incorrect_choices = []
    while len(incorrect_choices) < 3:
        c = random.choice(all_countries)
        cap = c.get("capital", [])
        if cap and cap[0] != correct_answer and cap[0] not in incorrect_choices:
            incorrect_choices.append(cap[0])

    options = incorrect_choices + [correct_answer]
    random.shuffle(options)
    return country_name, correct_answer, options

def main():
    st.title("🌍 世界の国クイズ（首都編）🌍")
    st.write("5問出題されます。がんばってください！")

    all_countries = fetch_country_data()

    if "score" not in st.session_state:
        st.session_state.score = 0
    if "question_number" not in st.session_state:
        st.session_state.question_number = 1
    if "asked_countries" not in st.session_state:
        st.session_state.asked_countries = []

    if st.session_state.question_number > 5:
        st.write(f"🎉 クイズ終了！あなたのスコアは {st.session_state.score}/5 でした！")
        if st.button("もう一度やる"):
            st.session_state.score = 0
            st.session_state.question_number = 1
            st.session_state.asked_countries = []
        return

    if "current_question" not in st.session_state:
        country_name, correct_answer, options = generate_question(all_countries, st.session_state.asked_countries)
        st.session_state.current_question = (country_name, correct_answer, options)

    country_name, correct_answer, options = st.session_state.current_question

    st.write(f"### 第{st.session_state.question_number}問：「{country_name}」の首都はどれ？")

    selected = st.radio("選んでください", options)

    if st.button("回答する"):
        if selected == correct_answer:
            st.success("✅ 正解！")
            st.session_state.score += 1
        else:
            st.error(f"❌ 不正解。正解は「{correct_answer}」です。")
        st.session_state.asked_countries.append(country_name)
        st.session_state.question_number += 1
        del st.session_state.current_question

if __name__ == "__main__":
    main()
