import streamlit as st

from utils import save_data


def render(df):
    st.subheader("📋 Transaction history")
    if df.empty:
        st.info("No transactions yet. Add one from the sidebar.")
        return

    column1, column2 = st.columns(2)
    with column1:
        type_filter = st.selectbox("Type", ["All", "Income", "Expense"])
    with column2:
        category_filter = st.selectbox("Category", ["All"] + sorted(df.category.unique().tolist()))

    view = df.copy()
    if type_filter != "All":
        view = view[view.type == type_filter]
    if category_filter != "All":
        view = view[view.category == category_filter]

    st.caption(f"Showing {len(view)} of {len(df)} transactions")
    display_view = view.sort_values("date", ascending=False).copy()
    display_view["date"] = display_view.date.astype(str)
    st.dataframe(display_view, use_container_width=True, hide_index=True)

    st.markdown("#### Delete a transaction")
    if view.empty:
        st.info("No transactions match the selected filters.")
    else:
        delete_options = {
            f"{row.date} | {row.type} | {row.category} | Rs. {row.amount:,.0f} | {row.description or 'No description'}": index
            for index, row in view.sort_values("date", ascending=False).iterrows()
        }
        selected_label = st.selectbox("Select transaction to delete", list(delete_options))
        confirm_delete = st.checkbox("I understand this transaction will be permanently removed.")
        if st.button("Delete selected transaction", type="secondary", disabled=not confirm_delete):
            selected_index = delete_options[selected_label]
            st.session_state.transactions = df.drop(index=selected_index).reset_index(drop=True)
            save_data(st.session_state.transactions)
            st.success("Transaction deleted.")
            st.rerun()

    st.download_button(
        "Download filtered transactions CSV",
        display_view.to_csv(index=False).encode("utf-8"),
        "pocketpredict_transactions.csv",
        "text/csv",
    )
