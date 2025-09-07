import plotly.graph_objects as go
#notes: pandas_ta is not part of the official pandas library — it’s a third-party add-on.
# pandas → general-purpose data analysis library.
# pandas_ta → a separate Python library built on top of pandas, designed specifically for technical analysis of financial time series (stock prices, crypto, forex, etc.).
import pandas_ta as pta
import dateutil
from datetime import datetime

def plotly_table(dataframe):
    headerColor = 'grey'
    rowEvenColor = '#f8fafd'
    rowOddColor = '#e1efff'

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['<b></b>']+['<b>'+str(i)[:10]+'</b>' for i in dataframe.columns],
            line_color='#007bff', fill_color='#007bff',
            align='center', font=dict(color='white', size=15), height=35,
        ),
        cells=dict(
            values=[['<b>'+str(i)+'</b>' for i in dataframe.index]] + [dataframe[i] for i in dataframe.columns],
            fill_color=[[rowOddColor, rowEvenColor]*len(dataframe)],
            align='left', line_color=['white'],
            font=dict(color=['black'], size=15)
        )
    )])

    fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
    return fig

def filter_data(dataframe, num_period):
    if num_period == '1mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-1)
    elif num_period == '5d':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days=-5)
    elif num_period == '6mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-6)
    elif num_period == '1y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1)
    elif num_period == '5y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5)
    elif num_period == 'ytd':
        date = datetime.datetime(dataframe.index[-1].year, 1, 1).strftime('%Y-%m-%d')
    else:
        date = dataframe.index[0]

    return dataframe.reset_index()[dataframe.reset_index()['Date'] > date]

def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe["Date"], y=dataframe['Open'],
                             mode='lines',
                             name='open', line=dict(width=2, color='#5a87ff')))
    fig.add_trace(go.Scatter(x=dataframe["Date"], y=dataframe['Close'],
                             mode='lines',
                             name='close', line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=dataframe["Date"], y=dataframe['High'],
                             mode='lines',
                             name='High', line=dict(width=2, color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe["Date"], y=dataframe['Low'],
                             mode='lines',
                             name='Low', line=dict(width=2, color='red')))
    
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500, margin=dict(l=0, r=20, t=20, b=0),
                      legend=dict(yanchor="top", xanchor="right"))
    return fig
def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=dataframe["Date"],
                                 open=dataframe['Open'],
                                 high=dataframe['High'],
                                 low=dataframe['Low'],
                                 close=dataframe['Close']))
    
    fig.update_layout(showlegend=False,
                      height=500,
                      margin=dict(l=0, r=20, t=20, b=0),
                     )
    return fig

def RSI(dataframe, num_period):
    dataframe['RSI'] = pta.rsi(dataframe['Close'])
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()

    # Check if Date is a column or index
    if 'Date' in dataframe.columns:
        x_vals = dataframe['Date']
    else:
        x_vals = dataframe.index

    fig.add_trace(go.Scatter(
        x=x_vals,
        y=dataframe['RSI'],
        name='RSI',
        line=dict(width=2, color='orange')
    ))

    fig.add_trace(go.Scatter(
        x=x_vals,
        y=[70] * len(dataframe),
        name='Overbought',
        line=dict(width=2, color='red', dash='dash')
    ))

    fig.add_trace(go.Scatter(
        x=x_vals,
        y=[30] * len(dataframe),
        fill='tonexty',
        name='Oversold',
        line=dict(width=2, color='#79da84', dash='dash')
    ))

    fig.update_layout(
        yaxis_range=[0, 100],
        height=200,
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", y=1.02, yanchor="top", xanchor="right", x=1)
    )

    return fig

def MACD(dataframe, num_period):
    macd = pta.macd(dataframe['Close']).iloc[:, 0]
    macd_signal = pta.macd(dataframe['Close']).iloc[:, 1]
    macd_hist = pta.macd(dataframe['Close']).iloc[:, 2]

    dataframe['MACD'] = macd
    dataframe['MACD Signal'] = macd_signal
    dataframe['MACD Hist'] = macd_hist
    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD'],
        name='MACD',
        marker_color='orange',
        line=dict(width=2, color='orange')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD Signal'],
        name='Signal',
        marker_color='red',
        line=dict(width=2, color='red', dash='dash')
    ))

    c = ['red' if cl < 0 else 'green' for cl in macd_hist]

    fig.update_layout(
        height=200,
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", yanchor="top",y=1.02, xanchor="right", x=1)
    )

    return fig

def Moving_average(dataframe, num_period):

    dataframe['SMA_50'] = pta.sma(dataframe['Close'], 50)
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Open'],
        mode='lines',
        name='Open', line=dict(width=2, color='#5ab7ff')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Close'],
        mode='lines',
        name='Close', line=dict(width=2, color='black')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['High'],
        mode='lines',
        name='High', line=dict(width=2, color='#0078ff')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['Low'],
        mode='lines',
        name='Low', line=dict(width=2, color='red')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'], y=dataframe['SMA_50'],
        mode='lines',
        name='SMA 50', line=dict(width=2, color='purple')
    ))

    fig.update_xaxes(rangeslider_visible=True)

    fig.update_layout(
        height=500,
        margin=dict(l=0, r=0, t=20, b=0),
        legend=dict(orientation="h", yanchor="top", xanchor="right"))

    return fig


def Moving_average_forecast(forecast):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=forecast.index[:-30], y=forecast['Close'].iloc[:-30],
                             mode='lines',
                             name='Close Price', line=dict(width=2, color='yellow')))
    
    fig.add_trace(go.Scatter(x=forecast.index[-31:], y=forecast['Close'].iloc[-31:],
                             mode='lines', name='Future Close Price', line=dict(width=2, color='red')))

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500, margin=dict(l=0, r=20, t=20, b=0),
                      legend=dict(
                          yanchor="top",
                          y=0.99,
                          xanchor="right",
                          x=0.99
                      ))
    
    return fig

# def Moving_average_forecast(forecast):
    fig = go.Figure()

    # Historical data (up to the last original date)
    historical = forecast.loc[forecast.index <= datetime.now()]
    # Forecasted data (future dates only)
    future = forecast.loc[forecast.index > datetime.now()]

    # Plot historical close prices
    fig.add_trace(go.Scatter(
        x=historical.index,
        y=historical['Close'],
        mode='lines',
        name='Close Price',
        line=dict(width=2, color='yellow')
    ))

    # Plot forecasted future close prices
    fig.add_trace(go.Scatter(
        x=future.index,
        y=future['Close'],
        mode='lines',
        name='Future Close Price',
        line=dict(width=2, color='red')
    ))

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        )
    )

    return fig

