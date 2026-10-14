from datetime import timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

from utils import TYPES, money, totals


def render(df, today):
    st.subheader("📊 Expense Dashboard")
    if df.empty:
        st.info("Add your first income or expense transaction to populate the dashboard.")
        return

    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    periods = {
        "Today": df[df.date == today],
        "This week": df[(df.date >= week_start) & (df.date <= today)],
        "This month": df[(df.date >= month_start) & (df.date <= today)],
        "All time": df,
    }
    chosen = st.segmented_control("Summary period", list(periods), default="This month")
    income, expenses, balance = totals(periods[chosen])
    column1, column2, column3 = st.columns(3)
    column1.metric("💰 Income", money(income))
    column2.metric("💸 Expenses", money(expenses))
    column3.metric("🪙 Remaining balance", money(balance))

    left, right = st.columns(2)
    with left:
        st.markdown("#### Expenses by category")
        categories = df[df.type == "Expense"].groupby("category", as_index=False).amount.sum()
        if categories.empty:
            st.info("No expenses to chart yet.")
        else:
            st.plotly_chart(px.pie(categories, names="category", values="amount", hole=.55), use_container_width=True)
    with right:
        st.markdown("#### Income vs expenses by day")
        daily = df.copy()
        daily["date"] = pd.to_datetime(daily.date)
        pivot = daily.pivot_table(index="date", columns="type", values="amount", aggfunc="sum", fill_value=0).reset_index()
        for transaction_type in TYPES:
            if transaction_type not in pivot.columns:
                pivot[transaction_type] = 0
        chart_data = pivot.melt(id_vars="date", value_vars=TYPES, var_name="Type", value_name="Amount")
        st.plotly_chart(px.bar(chart_data, x="date", y="Amount", color="Type", barmode="group"), use_container_width=True)

    st.markdown("#### Recent transactions")
    recent = df.sort_values("date", ascending=False).head(10).copy()
    recent["date"] = recent.date.astype(str)
    st.dataframe(recent, use_container_width=True, hide_index=True)
    with st.expander("View daily, weekly, monthly and all-time totals"):
        summary = []
        for name, part in periods.items():
            income, expenses, balance = totals(part)
            summary.append({"Period": name, "Income (PKR)": income, "Expenses (PKR)": expenses, "Balance (PKR)": balance})
        st.dataframe(pd.DataFrame(summary), use_container_width=True, hide_index=True)
