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
            category = st.selectbox("Categories", CATEGORIES)
            yango_number = None
            if category == "Yango Drive":
                yango_number = st.selectbox(
                    "Yango Drive number",
                    list(range(1, 13)),
                    format_func=lambda number: f"Yango Drive {number}",
                )
            description = st.text_input("Description", placeholder="e.g. fuel for today's shift")
        submit = st.form_submit_button("Save transaction", type="primary", use_container_width=True)
        if submit:
            if amount <= 0:
                st.error("Enter an amount greater than zero.")
            else:
                saved_description = description.strip()
                if category == "Yango Drive":
                    drive_label = f"Yango Drive {yango_number}"
                    saved_description = f"{drive_label} - {saved_description}" if saved_description else drive_label
                row = pd.DataFrame([{
                    "date": trans_date,
                    "type": trans_type,
                    "category": category,
                    "amount": amount,
                    "description": saved_description,
                }])
                st.session_state.transactions = (
                    pd.concat([transactions, row], ignore_index=True)
                    .sort_values("date")
                    .reset_index(drop=True)
                )
                save_data(st.session_state.transactions)
                st.success("Transaction saved.")
                st.rerun()
