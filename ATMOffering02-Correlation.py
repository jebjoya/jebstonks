import yfinance
from scipy.stats import pearsonr

# Let's start by grabbing the tickers themselves, and pulling the data for the 11th June, and bring it down to just the Close
gme = yfinance.Ticker("GME")
amc = yfinance.Ticker("AMC")
gme_prices = gme.history(period="1d",interval="1m",start="2021-06-11")["Close"]
amc_prices = amc.history(period="1d",interval="1m",start="2021-06-11")["Close"]

# Now let's chop these up into morning and afternoon
gme_morning = gme_prices[gme_prices.index <= "2021-06-11 12:30:00.000"]
gme_afternoon = gme_prices[gme_prices.index > "2021-06-11 12:30:00.000"]
amc_morning = amc_prices[amc_prices.index <= "2021-06-11 12:30:00.000"]
amc_afternoon = amc_prices[amc_prices.index > "2021-06-11 12:30:00.000"]

# And let's take a quick look at how well they're correlated
print(pearsonr(gme_morning,amc_morning))
print(pearsonr(gme_afternoon,amc_afternoon))


