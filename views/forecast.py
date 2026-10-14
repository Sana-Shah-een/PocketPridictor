import plotly.express as px
import streamlit as st

from utils import forecast_week, money


def render(df):
    st.subheader("🔮 Next 7 days — Linear Regression")
    st.write("The model learns a straight-line trend from daily total expenses. Forecasts are estimates, not guarantees.")
    forecast, mae, error = forecast_week(df)
    if error:
        st.warning(error)
        return

    predicted_total = float(forecast.predicted_expense.sum())
    column1, column2, column3 = st.columns(3)
    column1.metric("Predicted 7-day expenses", money(predicted_total))
    column2.metric("Average predicted per day", money(predicted_total / 7))
    column3.metric("Training MAE per day", money(mae))
    st.caption("Training MAE is measured on the same historical data used to fit the model, so it may understate real-world forecast error.")
    st.plotly_chart(
        px.line(
            forecast,
            x="date",
            y="predicted_expense",
            markers=True,
            title="Predicted daily expenses",
            labels={"date": "Date", "predicted_expense": "Predicted expenses (PKR)"},
        ),
        use_container_width=True,
    )
    table = forecast.copy()
    table["date"] = table.date.dt.strftime("%Y-%m-%d")
    st.dataframe(table, use_container_width=True, hide_index=True)
    st.markdown("#### Budget warning")
    budget = st.number_input("Your budget for the next 7 days (PKR)", min_value=0.0, value=10000.0, step=500.0)
    if budget > 0:
        if predicted_total > budget:
            st.error(f"Potential overspending: forecast is {money(predicted_total - budget)} above your budget.")
        else:
            st.success(f"Forecast is {money(budget - predicted_total)} below your budget.")
    st.caption("This starter model predicts total expenses, not separate category forecasts. Sudden changes in habits can make predictions inaccurate.")
