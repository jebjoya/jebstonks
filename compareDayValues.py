import yfinance as yf
import datetime as dt
import pandas as pd
from stonklib import returnFinraShortData, getFTDTheoryDates
import plotly.graph_objects as go

# start date inclusive, end date exclusive
tickerString = "GME"
startDateString = '2021-01-01'
endDateString = '2021-05-18'
# end of editable

ticker = yf.Ticker(tickerString)
startDate = dt.datetime.strptime(startDateString, "%Y-%m-%d").date()
endDate = dt.datetime.strptime(endDateString, "%Y-%m-%d").date()

dailyYahooVolumeData = ticker.history(interval="1d", start=startDate+dt.timedelta(days=1), end=endDate)["Volume"]

dates = []
minVolumes = []

for day in [d.date() for d in pd.date_range(start=startDate, end=endDate-dt.timedelta(days=1))]:
    minVolumesYahoo = ticker.history(interval="1h", start=day, end=day+dt.timedelta(days=1), prepost=True)
    if minVolumesYahoo["Volume"].sum() != 0:
        dates.append(day)
        minVolumes.append(minVolumesYahoo["Volume"].sum())

minVolumesYahoo = pd.DataFrame({"Date":dates, "minuteVolume":minVolumes},columns=["Date","minuteVolume"])
minVolumesYahoo["Date"] = pd.to_datetime(minVolumesYahoo['Date'], format="%Y-%m-%d")

dailyYahooVolumeData = dailyYahooVolumeData.T.reset_index()
dailyYahooVolumeData['dailyVolume'] = dailyYahooVolumeData['Volume']
dailyYahooVolumeData = dailyYahooVolumeData.drop('Volume',1)


yahooData = pd.merge(dailyYahooVolumeData, minVolumesYahoo, on="Date")

finraData = returnFinraShortData(startDate, endDate)
finraData = finraData[finraData['Symbol'] == tickerString]
finraData['Date'] = pd.to_datetime(finraData['Date'], format="%Y%m%d")
finraData['finraShort'] = finraData['ShortVolume']
finraData['finraVolume'] = finraData['TotalVolume']
finraData['finraPercent'] = finraData['finraShort'] / finraData['finraVolume']

finraData = finraData.drop(['Market','ShortExemptVolume','Symbol','ShortVolume','TotalVolume'],1)
results = pd.merge(yahooData, finraData, on="Date")

fig=go.Figure()

#fig.add_trace(go.Line(x=results['Date'], y=results['dailyVolume'], name="Daily Yahoo Volume"))
#fig.add_trace(go.Line(x=results['Date'], y=results['minuteVolume'], name="Hourly Yahoo Volume"))
#fig.add_trace(go.Line(x=results['Date'], y=results['finraShort'], name="Finra Short Volume"))
#fig.add_trace(go.Line(x=results['Date'], y=results['finraVolume'], name="Finra Total Volume"))
fig.add_trace(go.Line(x=results['Date'], y=results['finraPercent'], name="Finra Short Percent"))

optionDates = [dt.date(2021,1,15),dt.date(2021,2,5),dt.date(2021,4,16)]
for d in optionDates:
    l = getFTDTheoryDates(d)
    for x in l:
        if x < endDate:
            fig.add_vline(x=dt.datetime.combine(x,dt.datetime.min.time()).timestamp() * 1000, annotation_text=x.strftime("%Y-%m-%d"))



fig.show()
