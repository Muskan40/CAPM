import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date
import pandas_datareader.data as web
import capm_functions

# Streamlit UI setup
st.set_page_config(page_title="CAPM", page_icon="chart_with_upwards_trend", layout='wide')
st.title("Capital Asset Pricing Model")

# Load valid tickers from file
with open("tickers.txt", "r") as f:
    valid_tickers = set([line.strip().upper() for line in f])

# Session state for selected stocks
if "selected_stocks" not in st.session_state:
    st.session_state.selected_stocks = []

# UI Inputs
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    selected_stock = st.selectbox(
        "Choose a stock",
        options=valid_tickers,
        index=0
    )
    if selected_stock not in st.session_state.selected_stocks:
        st.session_state.selected_stocks.append(selected_stock)
        st.success(f"{selected_stock} added ✅")
    else:
        st.warning(f"{selected_stock} is already selected")

with col2:
    stocks_list = st.multiselect(
        "Chosen Stocks",
        st.session_state.selected_stocks,
        default=st.session_state.selected_stocks
    )

with col3:
    year = st.number_input("Number of years", 1, 10)

if not stocks_list:
    st.warning("Please select at least one stock to proceed.")
    st.stop()

# Dates
end = date.today()
start = date(end.year - int(year), end.month, end.day)

# Fetch SP500 data
SP500 = web.DataReader(['sp500'], 'fred', start, end).reset_index()

# Flatten SP500 columns if multiindex
if isinstance(SP500.columns, pd.MultiIndex):
    SP500.columns = [col[0] if isinstance(col, tuple) else col for col in SP500.columns]

SP500.columns = ['Date', 'sp500']

# Fetch stock data
stocks_df = pd.DataFrame()
for stock in stocks_list:
    data = yf.download(stock, period=f'{year}y')[['Close']]

    # Flatten columns if multiindex
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]

    data = data.rename(columns={'Close': stock}).reset_index()

    if stocks_df.empty:
        stocks_df = data
    else:
        stocks_df = pd.merge(stocks_df, data, on="Date", how="outer")

# Merge with SP500
stocks_df = pd.merge(stocks_df, SP500, on="Date", how="inner")

# Show head/tail
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown('### Dataframe head')
    st.dataframe(stocks_df.head(), use_container_width=True)
with col2:
    st.markdown('### Dataframe tail')
    st.dataframe(stocks_df.tail(), use_container_width=True)

# Stock plots
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown('### Price of all the Stocks')
    st.plotly_chart(capm_functions.interactive_plot(stocks_df))
with col2:
    st.markdown('### Price of all Stocks (After Normalizing)')
    st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize(stocks_df)))

# Daily returns
stocks_daily_return = capm_functions.daily_returns(stocks_df)

beta, alpha = {}, {}
for i in stocks_daily_return.columns:
    if i != 'Date' and i.lower() != 'sp500':
        b, a = capm_functions.calculate_beta(stocks_daily_return, i)
        beta[i] = b
        alpha[i] = a

# Beta values
beta_df = pd.DataFrame({
    'Stocks': beta.keys(),
    'Beta Value': beta.values()
})

with col1:
    st.markdown('### Calculated Beta Value')
    st.dataframe(beta_df, use_container_width=True)

# CAPM Return
rf = 0  # Risk-free rate
rm = stocks_daily_return['sp500'].mean() * 252

rtrn_value = []
for stock, value in beta.items():
    if stock.lower() != 'sp500':
        capm_return = rf + value * (rm - rf)
        rtrn_value.append(round(capm_return, 2))

return_df = pd.DataFrame({
    'Stocks': list(beta.keys()),
    'Return Value': rtrn_value
})

with col2:
    st.markdown('### Calculated Results using CAPM')
    st.dataframe(return_df, use_container_width=True)
