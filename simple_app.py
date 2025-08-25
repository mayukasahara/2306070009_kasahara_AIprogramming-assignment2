import streamlit as st
from quiz_logic import fetch_countries, generate_question

st.set_page_config(page_title="世界の首都クイズ")

def main():
    st.title("🌍 世界の首都クイズ 🌍")

    if "countries" not in st.session_state:
        st.session_state.countries = fetch_countries()
        st.session_state.score = 0
        st.session_state.question_number = 1
        st.session_state.asked = []
        st.session_state.game_over = False

    if not st.session_state.countries:
        st.error("国情報の取得に失敗しました。後で再度お試しください。")
        return

    if st.session_state.game_over:
        st.success(f"🎉 クイズ終了！あなたのスコアは {st.session_state.score} / 5 です！")
        if st.button("もう一度挑戦する"):
            st.session_state.score = 0
            st.session_state.question_number = 1
            st.session_state.asked = []
            st.session_state.game_over = False
        return

    country_name, correct_capital, options = generate_question(st.session_state.countries, st.session_state.asked)
    if country_name is None:
        st.error("もう出題できる問題がありません。")
        return

    st.write(f"### 第 {st.session_state.question_number} 問： {country_name} の首都はどれ？")

    answer = st.radio("選択肢", options)

    if st.button("回答する"):
        if answer == correct_capital:
            st.success("✅ 正解！")
            st.session_state.score += 1
        else:
            st.error(f"❌ 不正解。正解は「{correct_capital}」です。")
        st.session_state.asked.append(country_name)
        st.session_state.question_number += 1

        if st.session_state.question_number > 5:
            st.session_state.game_over = True

        st.experimental_rerun()

if __name__ == "__main__":
    main()
