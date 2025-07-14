import streamlit as st

#タイトル表示
st.title("簡単な Streamlit アプリ")

#ユーザーにテキスト入力をしてもらう
name = st.text_input("あなたの名前を入力してください")

#ユーザーにスタイダーで入力してもらう(最小値、最大値、デフォルト値)
age = st.slider("年齢を選んでください",0,100,25)

if name:
    st.write(f"こんにちは {name}さん！ あなたは{age}歳ですね!")
    st.write(f"{age-5}歳にしか見えないですけど")
else:
    st.write("上の入力欄に名前を入力してください")