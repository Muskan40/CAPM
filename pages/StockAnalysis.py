import streamlit as st
import pandas as pd
import yfinance as yf
import os
import plotly.graph_objects as go
import datetime
import pandas_ta as pta
from pages.utils.plotly_figure import plotly_table
from pages.utils.plotly_figure import close_chart, RSI, MACD, Moving_average, candlestick

# ---------------- Streamlit setup ----------------
st.set_page_config(page_title="Stock Analysis", page_icon="📄", layout='wide')
st.title("📊 Stock Analysis")

# ---------------- Load ticker list ----------------
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

# ---------------- Cached function for stock info ----------------
@st.cache_data(ttl=3600)  # cache for 1 hour
def get_stock_info(ticker):
    try:
        return yf.Ticker(ticker).info
    except Exception:
        return {}

stock = yf.Ticker(ticker)
info = get_stock_info(ticker)

# ---------------- Display company info safely ----------------
if info:
    st.write(info.get('longBusinessSummary', '❌ Company description not available (rate limited).'))
    st.write("**Sector:**", info.get('sector', 'N/A'))
    st.write("**Industry:**", info.get('industry', 'N/A'))
    st.write("**Employees:**", info.get('fullTimeEmployees', 'N/A'))
    st.write("**Website:**", info.get('website', 'N/A'))
else:
    st.error("⚠️ Could not fetch company details. Please try again later.")

# ---------------- Company Metrics ----------------
col1, col2 = st.columns(2)

with col1:
    df = pd.DataFrame(index=['Market Cap', 'Beta', 'EPS', 'PE Ratio'])
    df[''] = [
        info.get('marketCap', 'N/A'),
        info.get('beta', 'N/A'),
        info.get('trailingEps', 'N/A'),
        info.get('trailingPE', 'N/A')
    ]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)

with col2:
    df = pd.DataFrame(index=['Quick Ratio', 'Revenue per Share', 'Profit Margins',
                             'Debt to Equity', 'Return on Equity'])
    df[''] = [
        info.get('quickRatio', 'N/A'),
        info.get('revenuePerShare', 'N/A'),
        info.get('profitMargins', 'N/A'),
        info.get('debtToEquity', 'N/A'),
        info.get('returnOnEquity', 'N/A')
    ]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)

# ---------------- Historical Data ----------------
data = yf.download(ticker, start=start_date, end=end_date)

col1, col2, col3 = st.columns(3)
daily_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
col1.metric("Daily Change", str(round(data['Close'].iloc[-1], 2)), str(round(daily_change, 2)))

last_10_df = data.tail(10).sort_index(ascending=False).round(3)
last_10_df.columns = [col[0] if isinstance(col, tuple) else col for col in last_10_df.columns]
fig_df = plotly_table(last_10_df)
st.write("##### Historical Data (Last 10 Days)")
st.plotly_chart(fig_df, use_container_width=True)

# ---------------- Chart Controls ----------------
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

num_period = ''
if col1.button("5D"): num_period = '5d'
if col2.button("1M"): num_period = '1mo'
if col3.button("6M"): num_period = '6mo'
if col4.button("YTD"): num_period = 'ytd'
if col5.button("1Y"): num_period = '1y'
if col6.button("5Y"): num_period = '5y'
if col7.button("MAX"): num_period = 'max'

col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    chart_type = st.selectbox("Chart Type", ("Line", "Candle"))
with col2:
    if chart_type == "Candle":
        indicators = st.selectbox('', ('RSI', 'MACD'))
    else:
        indicators = st.selectbox('', ('RSI', 'Moving Average', 'MACD'))

# ---------------- Chart Rendering ----------------
ticker_ = yf.Ticker(ticker)
new_df1 = ticker_.history(period='max')
data1 = ticker_.history(period='max')

if num_period == '':
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

else:
    if chart_type == 'Candle' and indicators == 'RSI':
        st.plotly_chart(candlestick(new_df1, num_period), use_container_width=True)
        st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)

    if chart_type == 'Candle' and indicators == 'MACD':
        st.plotly_chart(candlestick(new_df1, num_period), use_container_width=True)
        st.plotly_chart(MACD(new_df1, num_period), use_container_width=True)

    if chart_type == 'Line' and indicators == 'RSI':
        st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)
        st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)

    if chart_type == 'Line' and indicators == 'Moving Average':
        st.plotly_chart(Moving_average(new_df1, num_period), use_container_width=True)

    if chart_type == 'Line' and indicators == 'MACD':
        st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)
        st.plotly_chart(MACD(new_df1, num_period), use_container_width=True)
