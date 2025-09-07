import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
from pages.utils.plotly_figure import plotly_table, close_chart, RSI, MACD, Moving_average, candlestick

st.set_page_config(page_title="Stock Analysis", page_icon="📈", layout='wide')
st.title("Stock Analysis")

# --- Load tickers ---
with open("tickers.txt", "r") as f:
    valid_tickers = set([line.strip().upper() for line in f])

col1, col2, col3 = st.columns(3)
today = datetime.date.today()

with col1:
    ticker = st.selectbox("Choose stock ticker:", options=valid_tickers, index=0)
with col2:
    start_date = st.date_input("Choose Start Date", datetime.date(today.year - 1, today.month, today.day))
with col3:
    end_date = st.date_input("Choose End Date", today)

st.subheader(ticker)
stock = yf.Ticker(ticker)

# --- Fetch company info safely ---
company_info = {}
try:
    company_info = stock.get_info()
except Exception:
    st.warning("⚠️ Could not fetch detailed company info (rate limit). Limited data will be shown.")

# --- Always fetch fast info (more reliable) ---
fast_info = stock.fast_info

# --- Business Summary ---
if company_info.get("longBusinessSummary"):
    st.write(company_info.get("longBusinessSummary", "N/A"))
    st.write("**Sector:**", company_info.get("sector", "N/A"))
    st.write("**Industry:**", company_info.get("industry", "N/A"))
    st.write("**Employees:**", company_info.get("fullTimeEmployees", "N/A"))
    st.write("**Website:**", company_info.get("website", "N/A"))
else:
    st.error("⚠️ Could not fetch company details. Please try again later.")

# --- Financial metrics ---
col1, col2 = st.columns(2)

with col1:
    df = pd.DataFrame(index=['Market Cap','Beta','EPS','PE Ratio'])
    df[''] = [
        fast_info.get("market_cap", "N/A"),
        fast_info.get("beta", "N/A"),
        company_info.get("trailingEps", "N/A"),
        company_info.get("trailingPE", "N/A")
    ]
    st.plotly_chart(plotly_table(df), use_container_width=True)

with col2:
    df = pd.DataFrame(index=['Quick Ratio','Revenue per Share','Profit Margins','Debt to Equity','Return on Equity'])
    df[''] = [
        company_info.get("quickRatio", "N/A"),
        company_info.get("revenuePerShare", "N/A"),
        company_info.get("profitMargins", "N/A"),
        company_info.get("debtToEquity", "N/A"),
        company_info.get("returnOnEquity", "N/A")
    ]
    st.plotly_chart(plotly_table(df), use_container_width=True)

# --- Download stock data ---
data = yf.download(ticker, start=start_date, end=end_date)

col1, col2, col3 = st.columns(3)
if len(data) > 1:
    daily_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
    col1.metric("Daily Change", str(round(data['Close'].iloc[-1], 2)), str(round(daily_change, 2)))

    last_10_df = data.tail(10).sort_index(ascending=False).round(3)
    last_10_df.columns = [col[0] if isinstance(col, tuple) else col for col in last_10_df.columns]
    fig_df = plotly_table(last_10_df)
    st.write("##### Historical Data (Last 10 Days)")
    st.plotly_chart(fig_df, use_container_width=True)
else:
    st.warning("⚠️ Not enough stock data available for metrics.")

# --- Chart controls ---
col1, col2, col3 = st.columns([1,1,4])
with col1:
    chart_type = st.selectbox("Chart Type", ("Line", "Candle"))
with col2:
    if chart_type == "Candle":
        indicators = st.selectbox('',('RSI','MACD'))
    else:
        indicators = st.selectbox('',('RSI','Moving Average','MACD'))

# --- Preload history safely ---
try:
    ticker_ = yf.Ticker(ticker)
    data1 = ticker_.history(period='max')
except Exception:
    st.error("⚠️ Failed to fetch stock history. Try again later.")
    st.stop()

# --- Charts ---
if chart_type == 'Candle' and indicators == 'RSI':
    st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
    st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

if chart_type == 'Candle' and indicators == 'MACD':
    st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
    st.plotly_chart(MACD(data1, '1y'), use_container_width=True)

if chart_type == 'Line' and indicators == 'RSI':
    st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
    st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

if chart_type == 'Line' and indicators == 'Moving Average':
    st.plotly_chart(Moving_average(data1, '1y'), use_container_width=True)

if chart_type == 'Line' and indicators == 'MACD':
    st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
    st.plotly_chart(MACD(data1, '1y'), use_container_width=True)
