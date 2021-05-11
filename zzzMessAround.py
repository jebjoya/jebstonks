import yfinance as yf

t = yf.Ticker("GME")

x = t.history(period="1mo",interval="1d")

print(x)