import yfinance as yf
import datetime as dt
import pandas as pd
from stonklib import returnFinraShortData
import plotly.graph_objects as go

# start date inclusive, end date exclusive
tickerString = "GME"
startDateString = '2021-04-10'
endDateString = '2021-05-08'
# end of editable

ticker = yf.Ticker(tickerString)
startDate = dt.datetime.strptime(startDateString, "%Y-%m-%d").date()
endDate = dt.datetime.strptime(endDateString, "%Y-%m-%d").date()

dailyYahooVolumeData = ticker.history(interval="1d", start=startDate+dt.timedelta(days=1), end=endDate)["Volume"]

minVolumes = []

for day in [d.date() for d in pd.date_range(start=startDate, end=endDate-dt.timedelta(days=1))]:
    minVolumesYahoo = ticker.history(interval="1m", start=day, end=day+dt.timedelta(days=1))
    if minVolumesYahoo["Volume"].sum() != 0:
        minVolumes.append(minVolumesYahoo["Volume"].sum())

dailyYahooVolumeData = dailyYahooVolumeData.T.reset_index()
dailyYahooVolumeData['dailyVolume'] = dailyYahooVolumeData['Volume']
dailyYahooVolumeData = dailyYahooVolumeData.drop('Volume',1)
dailyYahooVolumeData['minuteVolume'] = minVolumes

finraData = returnFinraShortData(startDate, endDate)
finraData = finraData[finraData['Symbol'] == tickerString]
finraData['Date'] = pd.to_datetime(finraData['Date'], format="%Y%m%d")
finraData['finraShort'] = finraData['ShortVolume']
finraData['finraVolume'] = finraData['TotalVolume']

finraData = finraData.drop(['Market','ShortExemptVolume','Symbol','ShortVolume','TotalVolume'],1)
results = pd.merge(dailyYahooVolumeData, finraData, on="Date")
print(results)

fig=go.Figure()

fig.add_trace(go.Line(x=results['Date'], y=results['dailyVolume'], name="Daily Yahoo Volume"))
fig.add_trace(go.Line(x=results['Date'], y=results['minuteVolume'], name="Minute Yahoo Volume"))
fig.add_trace(go.Line(x=results['Date'], y=results['finraShort'], name="Finra Short Volume"))
fig.add_trace(go.Line(x=results['Date'], y=results['finraVolume'], name="Finra Total Volume"))

fig.show()
