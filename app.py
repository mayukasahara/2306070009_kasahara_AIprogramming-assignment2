# app.py
import streamlit as st
from quiz_logic import load_country_data, generate_question_from_input
import json

st.set_page_config(page_title="世界の首都クイズ", page_icon="🌎")
st.title("🌎 世界の首都クイズ")

# セッション状態初期化
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.score = 0
    st.session_state.questions = []
    st.session_state.current_q = None

# ファイルアップロード
uploaded_file = st.file_uploader("国名が書かれた.txtファイルをアップロードしてください", type="txt")

if uploaded_file:
    # 国名リストを取得
    user_countries = [line.strip() for line in uploaded_file.readlines()]
    user_countries = [c.decode("utf-8") for c in user_countries if c.strip()]

    if not user_countries:
        st.warning("国名がファイルに見つかりませんでした。")
    else:
        countries_data = load_country_data()

        if st.session_state.step == 0:
            st.write("アップロードされた国からクイズを出題します（最大5問）")
            if st.button("スタート！"):
                st.session_state.questions = generate_question_from_input(countries_data, user_countries)
                st.session_state.step = 1
                st.session_state.current_q = st.session_state.questions[0]

        elif 1 <= st.session_state.step <= len(st.session_state.questions):
            q = st.session_state.current_q
            st.subheader(f"第 {st.session_state.step} 問")
            st.write(f"「{q['country']}」の首都はどれ？")
            choice = st.radio("選択肢:", q["options"])

            if st.button("回答する"):
                if choice == q["correct"]:
                    st.success("✅ 正解！")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ 不正解。正解は「{q['correct']}」です。")

                st.session_state.step += 1
                if st.session_state.step <= len(st.session_state.questions):
                    st.session_state.current_q = st.session_state.questions[st.session_state.step - 1]

        else:
            st.success(f"クイズ終了！あなたのスコアは {st.session_state.score} / {len(st.session_state.questions)} 点です。")
            if st.button("もう一度挑戦する"):
                st.session_state.step = 0
                st.session_state.score = 0
                st.session_state.questions = []
