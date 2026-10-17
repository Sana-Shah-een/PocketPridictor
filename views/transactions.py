import streamlit as st

from views import delete_transaction


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

    delete_transaction.render(
        view,
        key_prefix="transactions_delete",
        empty_message="No transactions match the selected filters.",
    )

    st.download_button(
        "Download filtered transactions CSV",
        display_view.to_csv(index=False).encode("utf-8"),
        "pocketpredict_transactions.csv",
        "text/csv",
    )
