from datetime import date

import pandas as pd
import streamlit as st

from utils import CATEGORIES, TYPES, save_data


def render(transactions):
    st.subheader("➕ Add a transaction")
    with st.form("add_transaction", clear_on_submit=True):
        column1, column2 = st.columns(2)
        with column1:
            trans_date = st.date_input("Date", value=date.today(), max_value=date.today())
            trans_type = st.selectbox("Type", TYPES)
            amount = st.number_input("Amount (PKR)", min_value=0.0, value=0.0, step=100.0)
        with column2:
            if trans_type == "Income":
                category = st.selectbox("Income source", ["Driving Income", "Salary", "Business", "Other Income"])
            else:
                category = st.selectbox("Expense category", CATEGORIES)
            description = st.text_input("Description", placeholder="e.g. fuel for today's shift")
        submit = st.form_submit_button("Save transaction", type="primary", use_container_width=True)
        if submit:
            if amount <= 0:
                st.error("Enter an amount greater than zero.")
            else:
                row = pd.DataFrame([{
                    "date": trans_date,
                    "type": trans_type,
                    "category": category,
                    "amount": amount,
                    "description": description.strip(),
                }])
                st.session_state.transactions = (
                    pd.concat([transactions, row], ignore_index=True)
                    .sort_values("date")
                    .reset_index(drop=True)
                )
                save_data(st.session_state.transactions)
                st.success("Transaction saved.")
                st.rerun()
