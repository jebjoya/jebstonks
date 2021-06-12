from datetime import date, timedelta
import yfinance

# Just setting up a few variables and our tickers as usual
most_correlated_days = [date(2021, 5, 14), date(2021,5,28), date(2021,5,3), date(2021,5,25), date(2021,6,2)]
one_day = timedelta(days=1)
mid_day = timedelta(hours=12, minutes=30)
gme = yfinance.Ticker("GME")
amc = yfinance.Ticker("AMC")

# I'm terrible at comments - hopefully this makes sense below:
for day in most_correlated_days:
    start_date = day.strftime("%Y-%m-%d")
    end_date = (day + one_day).strftime("%Y-%m-%d")
    gme_data = gme.history(interval="5m",start=start_date,end=end_date)["Volume"]
    amc_data = amc.history(interval="5m",start=start_date,end=end_date)["Volume"]
    gme_am = sum(gme_data[gme_data.index <= (day.strftime("%Y-%m-%d") + " 12:30:00.000")])
    gme_pm = sum(gme_data[gme_data.index > (day.strftime("%Y-%m-%d") + " 12:30:00.000")])
    gme_ratio = gme_am * 1.0 / (gme_am + gme_pm)
    amc_am = sum(amc_data[amc_data.index <= (day.strftime("%Y-%m-%d") + " 12:30:00.000")])
    amc_pm = sum(amc_data[amc_data.index > (day.strftime("%Y-%m-%d") + " 12:30:00.000")])
    amc_ratio = amc_am * 1.0 / (amc_am + amc_pm)
    print("Date:",start_date,"GME:",gme_ratio,"AMC:",amc_ratio)