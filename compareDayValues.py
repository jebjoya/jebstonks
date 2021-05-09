import yfinance as yf
import datetime as dt
import pandas as pd

# start date inclusive, end date exclusive
tickerString = "GME"
startDateString = '2021-05-05'
endDateString = '2021-05-08'
# end of editable

ticker = yf.Ticker(tickerString)
startDate = dt.datetime.strptime(startDateString, "%Y-%m-%d").date()
endDate = dt.datetime.strptime(endDateString, "%Y-%m-%d").date()

dailyYahooVolumeData = ticker.history(interval="1d", start=startDate, end=endDate)["Volume"]

for day in [d.date() for d in pd.date_range(start=startDate, end=endDate-dt.timedelta(days=1))]:
    minVolumesYahoo = ticker.history(interval="1m", start=day, end=day+dt.timedelta(days=1))
    print(day, "-", minVolumesYahoo["Volume"].sum())