import yfinance as yf
import datetime as dt
import pandas as pd
from stonklib import returnFinraShortData
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date

# start date, end date exclusive
tickerString = "GME"
startDateString = '2021-01-01'
endDateString = '2021-05-11'
# end of editable

ticker = yf.Ticker(tickerString)
startDate = dt.datetime.strptime(startDateString, "%Y-%m-%d").date()
endDate = dt.datetime.strptime(endDateString, "%Y-%m-%d").date()

df = ticker.history(interval="1h", start=startDate, end=endDate)
df["Previous Close"] = df["Close"].shift(1)
df["Previous Volume"] = df["Volume"].shift(1)
df["Price Movement"] = df["Close"] - df["Previous Close"]
df["Price Direction"] = df["Price Movement"].apply(lambda x: 1 if x > 0 else -1)
df["OBV Change"] = df["Volume"] * df["Price Direction"]
df = df[df["Price Movement"].notna()]
df["OBV"] = df["OBV Change"].cumsum()
df = df.drop(["Dividends","Stock Splits","Previous Close", "Previous Volume", "Price Movement", "Price Direction", "OBV Change"], axis=1)

fig = make_subplots(specs=[[{"secondary_y":True}]])

fig.add_trace(go.Ohlc(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name = "Price"))

fig.add_trace(go.Line(x=df.index, y=df["OBV"], name="OBV"),secondary_y=True)

fig.update_xaxes(
    rangebreaks=[
        dict(bounds=["sat", "mon"]),
        dict(bounds=[16, 9], pattern="hour"),
    ]
)



fig.update_layout(xaxis_rangeslider_visible=False,
                  template = 'plotly_dark')

fig.show()


