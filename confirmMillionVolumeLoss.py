import yfinance as yf

ticker = "GME"

gme = yf.Ticker(ticker).history(period="1d", interval="1m",start="2021-05-05", end="2021-05-06")

print(gme[gme.index < "2021-05-05 11:32"]["Volume"].sum())

