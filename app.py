import streamlit as st

from datetime import date
from pathlib import Path

from views import add_transaction, forecast, overview, transactions
from utils import load_data

st.set_page_config(page_title="PocketPredict", page_icon="💸", layout="wide")

css = (Path(__file__).parent / "styles.css").read_text(encoding="utf-8")
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
st.markdown("<div class=\"hero\"><h1>💸 PocketPredict</h1><p>Personal income, spending, and Linear Regression forecast dashboard.</p></div>", unsafe_allow_html=True)

if "transactions" not in st.session_state:
    st.session_state.transactions = load_data()
df = st.session_state.transactions.copy()
today = date.today()

with st.sidebar:
    st.header("PocketPredict")
    page = st.radio("Navigation",["Overview","Add Transaction","Transactions","Forecast"])
    st.caption("Currency: Pakistani Rupees (PKR)")
    if st.button("Reload expenses.csv",use_container_width=True):
        st.session_state.transactions = load_data()
        st.rerun()

if page == "Add Transaction":
    add_transaction.render(df)

elif page == "Transactions":
    transactions.render(df)

elif page == "Overview":
    overview.render(df, today)

elif page == "Forecast":
    forecast.render(df)
