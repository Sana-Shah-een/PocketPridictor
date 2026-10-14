import streamlit as st


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
    view["date"] = view.date.astype(str)
    st.dataframe(view.sort_values("date", ascending=False), use_container_width=True, hide_index=True)
    st.download_button(
        "Download transactions CSV",
        view.to_csv(index=False).encode("utf-8"),
        "pocketpredict_transactions.csv",
        "text/csv",
    )
    st.caption("To edit or remove records in this starter version, edit expenses.csv and click Reload expenses.csv.")
