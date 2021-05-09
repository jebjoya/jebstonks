import yfinance as yf

ticker = yf.Ticker("GME")

hist = ticker.history(period="1d",interval="1m")

hist["Volume*Low"] = hist["Volume"] * hist["Low"]
hist["Volume*High"] = hist["Volume"] * hist["High"]

print(hist["Volume*Low"].sum())
print(hist["Volume*High"].sum())

ticker = yf.Ticker("AMC")

hist = ticker.history(period="1d",interval="1m")

hist["Volume*Low"] = hist["Volume"] * hist["Low"]
hist["Volume*High"] = hist["Volume"] * hist["High"]

print(hist["Volume*Low"].sum())
print(hist["Volume*High"].sum())
