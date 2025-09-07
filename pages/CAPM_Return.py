import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date, datetime  
import pandas_datareader.data as web
import capm_functions
# Streamlit UI setup
st.set_page_config(page_title="CAPM", page_icon="chart_with_upwards_trend", layout='wide')
st.title("Capital Asset Pricing Model")
with open("tickers.txt", "r") as f:
    valid_tickers = set([line.strip().upper() for line in f])

# Session state to store chosen tickers
if "selected_stocks" not in st.session_state:
    st.session_state.selected_stocks = []
# UI Inputs
col1, col2,col3 = st.columns([1, 1,1])      
with col1:
    # Dropdown from the valid ticker list
    selected_stock = st.selectbox(
        "Choose a stock",
        options=valid_tickers,  # ticker list from your file
        index=0  # default selection (first one)
    )

    # Add selected stock automatically to session_state
    if "selected_stocks" not in st.session_state:
        st.session_state.selected_stocks = []

    if selected_stock not in st.session_state.selected_stocks:
        st.session_state.selected_stocks.append(selected_stock)
        st.success(f"{selected_stock} added ✅")
    else:
        st.warning(f"{selected_stock} is already selected")
with col2:
    # Display selected stocks in a multiselect box
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

# ✅ Fixing the date logic

end = date.today()
# If the year is 1, we want to go back 1 year, if it's 2, we go back 2 years, etc.  

start = date(end.year - int(year), end.month, end.day)  # Go back 'year' years

# st.write(f"Fetching data from {start} to {end}")

SP500 = web.DataReader(['sp500'],'fred',start,end)
# print(SP500.tail())
stocks_df=pd.DataFrame()
for stock in stocks_list:
    data = yf.download(stock,period=f'{year}y')
    stocks_df[f'{stock}']=data['Close']

stocks_df.reset_index(inplace=True)
SP500.reset_index(inplace=True)
SP500.columns = ['Date','sp500']
stocks_df['Date'] = stocks_df['Date'].astype('datetime64[ns]')
# stocks_df['Date'] = stocks_df['Date'].apply(lambda x:str(x)[:10])
stocks_df = pd.merge(stocks_df,SP500,on='Date',how='inner')
col1,col2 = st.columns([1,1])

with col1:
    st.markdown('### Dataframe head')
    st.dataframe(stocks_df.head(),use_container_width=True)
with col2:
    st.markdown('### Dataframe tail')
    st.dataframe(stocks_df.tail(),use_container_width=True)

col1,col2 = st.columns([1,1])

with col1:
    st.markdown('### Price of all the Stocks')
    st.plotly_chart(capm_functions.interactive_plot(stocks_df))
with col2:
    st.markdown('### Price of all Stocks (After Normalizing)')
    st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize(stocks_df)))

stocks_daily_return = capm_functions.daily_returns(stocks_df)
#print(stocks_daily_return.head())
beta = {}
alpha = {}

for i in stocks_daily_return.columns:
    if i!='Date' and i!='SP500':
        b,a = capm_functions.calculate_beta(stocks_daily_return,i)

        beta[i]=b
        alpha[i]=a

#print(beta,alpha)

beta_df = pd.DataFrame(columns=['Stocks','Beta Value'])

beta_df['Stocks'] = beta.keys()
beta_df['Beta Value'] = beta.values()

with col1:
    st.markdown('### Calculated Beta Value')
    st.dataframe(beta_df,use_container_width=True)

rf = 0  # Risk-free rate
rm = stocks_daily_return['sp500'].mean() * 252

rtrn_value = []
for stock, value in beta.items():
     if stock.lower() != 'sp500':
        capm_return = rf + value * (rm - rf)
        rtrn_value.append(round(capm_return, 2))

#print(len(stocks_list), len(rtrn_value))

return_df = pd.DataFrame({
    'Stocks': stocks_list,
    'Return Value': rtrn_value
})

with col2:
    st.markdown('### Calculated Results using CAPM')
    st.dataframe(return_df, use_container_width=True)
