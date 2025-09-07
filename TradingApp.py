import streamlit as st
import pandas as pd
import yfinance as yf
import os

base_path= os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_path,"app.jpg")
# Streamlit UI setup
st.set_page_config(page_title="Trading App", page_icon="heavy_dollar_sign:", layout='wide')
st.title("Trading Guide App :bar_chart:")
st.header("We provide you with the best trading strategies and tools to maximize your profits!")
st.image(image_path, use_container_width=True)

st.markdown("## We provide the following services:")

st.markdown("### :one: Stock Information")
st.write("Through this page you can get information about stocks, their prices, and historical data.")

st.markdown("### :two: Stock Prediction")
st.write("You can explore predicted closing prices for the next 30days based on historical stock data and advanced forecasting models .")

st.markdown("### :three: CAPM Return")
st.write("This page allows you to calculate the expected return of a stock based on its risk and the market's expected return using the Capital Asset Pricing Model (CAPM).")

