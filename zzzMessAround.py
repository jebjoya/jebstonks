import yfinance as yf

t = yf.Ticker("GME")

x = t.history(period="1d", interval="1m", prepost=True)

print(x[x['Volume']!=0])