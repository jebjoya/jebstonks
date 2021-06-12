import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date, datetime
from stonklib import getFTDTheoryDates

gme = yf.Ticker("GME")
df = gme.history(period="1y")

def sma(length, source):
    return source.rolling(length).apply(lambda val: sum(val)/length, raw=True)

def ema(length, source):
    smaX = sma(length, source)
    adjSource = source.copy()
    adjSource.iloc[0:length] = smaX[0:length]
    return adjSource.ewm(span=length, adjust=False).mean()

def rsi(length, close):
    change = close - close.shift()
    upward = change.apply(lambda x: x if x > 0 else 0)
    downward = change.apply(lambda x: -x if x < 0 else 0)
    rs = ema(length, upward) / ema(length, downward)
    return rs.apply(lambda x: 100 - (100 / (1 + x)))
    
def macd(fast, slow, source):
    fastEMA = ema(fast, source)
    slowEMA = ema(slow, source)
    return fastEMA - slowEMA

def vwmacd(fast, slow, volume, source):
    fastVWEMA = ema(fast, volume * source) / ema(fast, volume)
    slowVWEMA = ema(slow, volume * source) / ema(slow, volume)
    return fastVWEMA - slowVWEMA

df['macd'] = macd(12,26,df['Close'])
df['signal'] = ema(9, df['macd'])
df['vwmacd'] = vwmacd(12, 26, df['Volume'], df['Close'])
df['vwsignal'] = ema(9, df['vwmacd'])
df['rsi'] = rsi(14, df['Close'])
df['vwbsSignal'] = df['vwmacd'] - df['vwsignal']
df['bsSignal'] = df['macd'] - df['signal']
df['ema20'] = ema(20, df['Close'])
df['vwema20'] = ema(20, df['Close'] * df['Volume']) / ema(20, df['Volume'])

fig = make_subplots(rows=5, cols=1, shared_xaxes=True, specs = [
                                                                [{"rowspan": 2, "secondary_y":True}],
                                                                [None],
                                                                [{}],
                                                                [{}],
                                                                [{}]
                                                               ])

fig.add_trace(go.Ohlc(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name = "Price"),
                row = 1, col = 1)

fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name="Volume", marker_color = 'rgba(30,30,165,0.3)'), row=1, col=1, secondary_y=True)
fig.add_trace(go.Line(x=df.index, y=df['ema20'], name="EMA (20d)"), row=1, col=1)
fig.add_trace(go.Line(x=df.index, y=df['vwema20'], name="VW EMA (20d)"), row=1, col=1)

fig.add_trace(go.Bar(x=df.index, y=df['vwbsSignal'], name="VW MACD/Signal Buy/Sell", marker_color = 'rgba(165,30,30,0.3)'), row=3, col=1)
fig.add_trace(go.Line(x = df.index, y = df['vwmacd'], name="VW MACD"), row = 3, col = 1)
fig.add_trace(go.Line(x = df.index, y = df['vwsignal'], name="VW Signal"), row = 3, col = 1)

fig.add_trace(go.Bar(x=df.index, y=df['bsSignal'], name="MACD/Signal Buy/Sell", marker_color = 'rgba(165,30,30,0.3)'), row=4, col=1)
fig.add_trace(go.Line(x = df.index, y = df['macd'], name="MACD"), row = 4, col = 1)
fig.add_trace(go.Line(x = df.index, y = df['signal'], name="Signal"), row = 4, col = 1)

fig.add_trace(go.Line(x = df.index, y = df['rsi'], name = "RSI (14d)"), row=5, col = 1)

fig.add_hline(50, row=5, col=1)
fig.add_hline(70, row=5, col=1)
fig.add_hline(30, row=5, col=1)

optionDates = [date(2021,1,15),date(2021,2,5),date(2021,4,16)]
for d in optionDates:
    l = getFTDTheoryDates(d)
    for x in l:
        if x < date.today():
            fig.add_vline(x=datetime.combine(x,datetime.min.time()).timestamp() * 1000, annotation_text=x.strftime("%Y-%m-%d"))

fig.update_xaxes(
    rangebreaks=[
        dict(bounds=["sat", "mon"]),
        dict(values=["2021-04-02", "2021-02-15", "2021-01-18", "2021-01-01", "2020-12-25", "2020-11-26"])
    ]
)


fig.update_layout(xaxis_rangeslider_visible=False,
                  xaxis_range=['2020-12-01',date.today()],
                  template = 'plotly_dark')

fig.show()