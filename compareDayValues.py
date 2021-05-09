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

dailyYahooVolumeData = ticker.history(interval="1d", start=startDate+dt.timedelta(days=1), end=endDate)["Volume"]

minVolumes = []

for day in [d.date() for d in pd.date_range(start=startDate, end=endDate-dt.timedelta(days=1))]:
    minVolumesYahoo = ticker.history(interval="1m", start=day, end=day+dt.timedelta(days=1))
    minVolumes.append(minVolumesYahoo["Volume"].sum())

dailyYahooVolumeData = dailyYahooVolumeData.T.reset_index()
dailyYahooVolumeData['dailyVolume'] = dailyYahooVolumeData['Volume']
dailyYahooVolumeData = dailyYahooVolumeData.drop('Volume',1)
dailyYahooVolumeData['minuteVolume'] = minVolumes

print(dailyYahooVolumeData)
