import yfinance as yf

t = yf.Ticker("GME")

x = t.history(period="1d", interval="5m",start="2021-05-05", end="2021-05-06")

print(x.head(50))