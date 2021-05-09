import yfinance as yf

gme = yf.Ticker("GME").history(period="MAX", interval="1d")

gme["range"] = gme["High"] - gme["Low"]
gme["rangePercent"] = gme["range"] / gme["Low"]

print(gme[gme["range"] <= 7.169999].tail(20))

print(gme[gme["rangePercent"] <= 0.045285])