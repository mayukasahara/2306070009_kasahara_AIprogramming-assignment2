import streamlit as st
from currency_api import get_exchange_rate

def main():
    st.title("💱 簡単通貨換算ツール")

    col1, col2 = st.columns(2)
    with col1:
        base_currency = st.text_input("元の通貨コード (例: USD, JPY, EUR)", value="USD")
    with col2:
        target_currency = st.text_input("換算先の通貨コード", value="JPY")

    amount = st.number_input("金額を入力してください", min_value=0.0, value=1.0, format="%.2f")

    if st.button("換算する"):
        try:
            rate = get_exchange_rate(base_currency, target_currency)
            converted = amount * rate
            st.success(f"{amount} {base_currency.upper()} は 約 {converted:.2f} {target_currency.upper()} です。")
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
