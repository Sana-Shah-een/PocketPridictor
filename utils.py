from pathlib import Path

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

APP_DIR = Path(__file__).parent
DATA_FILE = APP_DIR / "expenses.csv"
CATEGORIES = ["Yango Drive","Fuel", "Food", "Family Support", "Bills", "Other"]
TYPES = ["Income", "Expense"]


def load_data():
    if not DATA_FILE.exists():
        pd.DataFrame(columns=["date", "type", "category", "amount", "description"]).to_csv(DATA_FILE, index=False)
    try:
        df = pd.read_csv(DATA_FILE)
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        df = pd.DataFrame(columns=["date", "type", "category", "amount", "description"])
    for col in ["date", "type", "category", "amount", "description"]:
        if col not in df.columns:
            df[col] = ""
    df = df[["date", "type", "category", "amount", "description"]].copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    df["type"] = df["type"].astype(str).str.strip().str.title()
    df["category"] = df["category"].fillna("Other").astype(str)
    df["description"] = df["description"].fillna("").astype(str)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    return (
        df.dropna(subset=["date", "amount"])
        .query("amount >= 0")
        .loc[lambda x: x["type"].isin(TYPES)]
        .sort_values("date")
        .reset_index(drop=True)
    )


def save_data(df):
    out = df.copy()
    out["date"] = pd.to_datetime(out["date"]).dt.strftime("%Y-%m-%d")
    out.to_csv(DATA_FILE, index=False)


def money(amount):
    return f"Rs. {amount:,.0f}"


def totals(df):
    income = df.loc[df.type == "Income", "amount"].sum()
    expenses = df.loc[df.type == "Expense", "amount"].sum()
    return float(income), float(expenses), float(income - expenses)


def daily_series(df):
    expenses = df[df.type == "Expense"].copy()
    if expenses.empty:
        return pd.DataFrame(columns=["date", "daily_expense", "day_number"])
    daily = expenses.groupby("date")["amount"].sum()
    daily.index = pd.to_datetime(daily.index)
    index = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
    daily = daily.reindex(index, fill_value=0).rename("daily_expense").rename_axis("date").reset_index()
    daily["day_number"] = (daily.date - daily.date.min()).dt.days
    return daily


def forecast_week(df):
    daily = daily_series(df)
    if len(daily) < 7:
        return None, None, "Add expense records spanning at least 7 days to train Linear Regression."
    model = LinearRegression()
    model.fit(daily[["day_number"]], daily["daily_expense"])
    mae = mean_absolute_error(daily["daily_expense"], model.predict(daily[["day_number"]]))
    dates = pd.date_range(daily.date.max() + pd.Timedelta(days=1), periods=7, freq="D")
    numbers = (dates - daily.date.min()).days.to_numpy().reshape(-1, 1)
    predictions = model.predict(numbers).clip(min=0)
    return pd.DataFrame({"date": dates, "predicted_expense": predictions}), mae, None
