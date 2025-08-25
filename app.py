# app.py
import streamlit as st
from quiz_logic import fetch_countries, generate_question

st.set_page_config(page_title="世界の首都クイズ", page_icon="🌍")

st.title("🌍 世界の首都クイズ 🌍")

# セッション状態の初期化
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.score = 0
    st.session_state.asked = []
    st.session_state.question = None

# 国データ取得
countries = fetch_countries()

if not countries:
    st.error("国情報の取得に失敗しました。後で再度お試しください。")
else:
    if st.session_state.step == 0:
        st.write("これから5問出題します！準備ができたら下のボタンをクリックしてください。")
        if st.button("スタート！"):
            st.session_state.step = 1
            st.session_state.question = generate_question(countries, st.session_state.asked)

    elif 1 <= st.session_state.step <= 5:
        q = st.session_state.question
        st.subheader(f"第 {st.session_state.step} 問")
        st.write(f"「{q['country']}」の首都はどれ？")
        choice = st.radio("選択肢:", q["options"])

        if st.button("回答する"):
            if choice == q["correct"]:
                st.success("✅ 正解！")
                st.session_state.score += 1
            else:
                st.error(f"❌ 不正解。正解は「{q['correct']}」です。")

            st.session_state.asked.append(q["country"])
            st.session_state.step += 1
            if st.session_state.step <= 5:
                st.session_state.question = generate_question(countries, st.session_state.asked)

    else:
        st.success(f"クイズ終了！あなたのスコアは {st.session_state.score} / 5 点です！")
        if st.button("もう一度挑戦する"):
            st.session_state.step = 0
            st.session_state.score = 0
            st.session_state.asked = []
