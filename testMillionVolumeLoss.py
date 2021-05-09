import yfinance as yf

ticker = "GME"

gme = yf.Ticker(ticker).history(period="1d", interval="1m", start="2021-05-05", end="2021-05-06")
gmeDay = yf.Ticker(ticker).history(period="1d", interval="1d",start="2021-05-06", end="2021-05-06" )


print("Sum of hourlys:",gme["Volume"].sum())
print("Just the daily:",gmeDay["Volume"].sum())

volumeDiff = gme["Volume"].sum() - gmeDay["Volume"].sum()

print("Ticker:",ticker)
print("Volume Diff:",volumeDiff)
print("Percentage:",volumeDiff * 100.0 / gme["Volume"].sum(),"%")