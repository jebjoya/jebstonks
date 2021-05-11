import yfinance as yf
import datetime as dt
import pandas as pd
from stonklib import returnFinraShortData
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date

# start date, end date exclusive
tickerString = "GME"
startDateString = '2021-01-07'
endDateString = '2021-05-11'
# end of editable

ticker = yf.Ticker(tickerString)
startDate = dt.datetime.strptime(startDateString, "%Y-%m-%d").date()
endDate = dt.datetime.strptime(endDateString, "%Y-%m-%d").date()

yahooData = ticker.history(interval="1d", start=startDate, end=endDate)
yahooData["Previous Close"] = yahooData["Close"].shift(1)
yahooData["Price Movement"] = yahooData["Close"] - yahooData["Previous Close"]
yahooData = yahooData[yahooData["Price Movement"].notna()]
yahooData["Price Movement Percent"] = yahooData["Price Movement"] * 100.0 / yahooData["Previous Close"]
yahooData["Abs Price Movement Percent"] = yahooData["Price Movement Percent"].apply(lambda x: abs(x))
yahooData = yahooData.drop(["Dividends", "Stock Splits"], axis=1)

finraData = returnFinraShortData(startDate+dt.timedelta(days=1), endDate)
finraData = finraData[finraData['Symbol'] == tickerString]
finraData['Date'] = pd.to_datetime(finraData['Date'], format="%Y%m%d")
finraData["Short Percentage"] = finraData["ShortVolume"] * 100.0 / finraData["TotalVolume"]
finraData["Short Volume"] = finraData["ShortVolume"]
finraData["Finra Volume"] = finraData["TotalVolume"]
finraData["Short Volume*Percent"] = finraData["Short Volume"] * finraData["Short Percentage"]
finraData = finraData.drop(["Symbol","ShortVolume","ShortExemptVolume","TotalVolume","Market"],axis=1)

df = pd.merge(yahooData, finraData, on="Date")

print(df)

fig = make_subplots(specs=[[{"secondary_y":True}]])


#fig.add_trace(go.Line(x=df["Date"], y=df["Short Volume*Percent"], name="Short Volume*Percent"))
#fig.add_trace(go.Line(x=df["Date"], y=df["Short Percentage"], name="Short Percentage"))
#fig.add_trace(go.Line(x=df["Date"], y=df["Short Volume"], name="Short Volume"))
fig.add_trace(go.Line(x=df["Date"], y=df["Volume"], name="Volume"))
#fig.add_trace(go.Bar(x=df["Date"], y=df["Price Movement Percent"], name="Price Movement Percent"), secondary_y=True)
fig.add_trace(go.Bar(x=df["Date"], y=df["Abs Price Movement Percent"], name="Abs Price Movement Percent"), secondary_y=True)

fig.update_xaxes(
    rangebreaks=[
        dict(bounds=["sat", "mon"]),
        dict(values=["2021-04-02", "2021-02-15", "2021-01-18", "2021-01-01", "2020-12-25", "2020-11-26"])
    ]
)


fig.update_layout(xaxis_rangeslider_visible=False,
                  template = 'plotly_dark')

fig.show()