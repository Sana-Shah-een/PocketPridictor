# PocketPredict

A beginner-friendly expense dashboard using Python, Streamlit, Pandas, Plotly, and Scikit-learn Linear Regression.

## Features
- Daily, weekly, monthly, and all-time income, expense, and balance summaries
- Fuel, food, family support, personal, maintenance, bills, and other categories
- Add and save transactions to CSV
- Category pie chart and income-vs-expenses chart
- Seven-day expense forecast using Linear Regression
- Optional budget warning
- Download transaction history

## Run on Windows
Open PowerShell in this folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

## Vercel note

`app.py` is the Streamlit application entrypoint. Vercel serverless functions
require a top-level `app`, so `api/index.py` exposes the Streamlit ASGI app and
points it at `app.py`.

## CSV format
`date,type,category,amount,description`

The included `expenses.csv` has synthetic demo data covering 35 days so the charts and forecast can be tested. Replace it with real records before relying on the estimates. Forecasts are educational estimates, not financial advice.
