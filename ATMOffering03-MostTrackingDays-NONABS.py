import yfinance
from datetime import date, timedelta
from scipy.stats import pearsonr
import pandas as pd

# Grab our tickers
gme = yfinance.Ticker("GME")
amc = yfinance.Ticker("AMC")

# Set some basic variables
d = date(2021,4,14)
one_day = timedelta(days=1)
date_to_pearson = {}

# Iterate over dates, adding the date and Pearson value between GME and AMC on the 5m candles to a dictionary
while d < date(2021,6,12):
    start_date = d.strftime("%Y-%m-%d")
    d += one_day
    end_date = d.strftime("%Y-%m-%d")
    gme_prices = gme.history(interval="5m", start=start_date, end=end_date)["Close"]
    if len(gme_prices) > 0:
        amc_prices = amc.history(interval="5m", start=start_date, end=end_date)["Close"]
        date_to_pearson[start_date] = pearsonr(gme_prices,amc_prices)[0]

# Convert to a Pandas Dataframe (because I'm a sucker for Pandas)
df = pd.DataFrame(date_to_pearson.items(), columns=["Date","Pearson"])
df = df.sort_values("Pearson")

# And let's look at the top and bottom of this
print("Least Correlated:\n", df.head(5))
print("\n\nMost Correlated:\n", df.tail(5))