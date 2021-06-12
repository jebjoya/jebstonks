import yfinance

# Grabbing our tickers and the data together here
gme_data = yfinance.Ticker("GME").history(period="1d",interval="1m",start="2021-06-11")
amc_data = yfinance.Ticker("AMC").history(period="1d",interval="1m",start="2021-06-11")

gme_am = sum(gme_data[gme_data.index <= "2021-06-11 12:30:00.000"]["Volume"])
gme_pm = sum(gme_data[gme_data.index > "2021-06-11 12:30:00.000"]["Volume"])
amc_am = sum(amc_data[amc_data.index <= "2021-06-11 12:30:00.000"]["Volume"])
amc_pm = sum(amc_data[amc_data.index > "2021-06-11 12:30:00.000"]["Volume"])

amc_ratio = amc_am * 1.0 / (amc_am + amc_pm)
print("AMC Ratio:", amc_ratio)
print("GME PM Volume:", gme_pm)
theoretical_gme_volume = gme_pm / (1.0 - amc_ratio)
print("AMC Implied Total Volume for GME:", theoretical_gme_volume)
excess_volume = (gme_am + gme_pm) - theoretical_gme_volume
print("Excess Volume for GME:", excess_volume)