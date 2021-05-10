import yfinance as yf

gme = yf.Ticker("GME").history(period="6mo",interval="1d")

gme['LastClose'] = gme['Close'].shift(1)

gme['SSR Trigger'] = (gme['Low'] < (gme['LastClose'] * 0.9))

print(gme[gme['SSR Trigger']])