import streamlit as st

from utils import save_data


def render(df, key_prefix="delete_transaction", empty_message="No transactions available to delete."):
    st.subheader("🗑️ Delete a transaction")
    if df.empty:
        st.info(empty_message)
        return

    delete_options = {
        index: (
            f"{row.date} | {row.type} | {row.category} | "
            f"Rs. {row.amount:,.0f} | {row.description or 'No description'}"
        )
        for index, row in df.sort_values("date", ascending=False).iterrows()
    }
    selected_index = st.selectbox(
        "Select transaction to delete",
        list(delete_options),
        format_func=delete_options.get,
        key=f"{key_prefix}_selection",
    )
    confirm_delete = st.checkbox(
        "I understand this transaction will be permanently removed.",
        key=f"{key_prefix}_confirmation",
    )
    if st.button(
        "Delete selected transaction",
        type="secondary",
        disabled=not confirm_delete,
        key=f"{key_prefix}_button",
    ):
        st.session_state.transactions = (
            st.session_state.transactions.drop(index=selected_index).reset_index(drop=True)
        )
        save_data(st.session_state.transactions)
        st.success("Transaction deleted.")
        st.rerun()
