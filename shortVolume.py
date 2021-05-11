import datetime
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from stonklib import download, returnFinraShortData

def sma(length, source):
    return source.rolling(length).apply(lambda val: sum(val)/length, raw=True)

df = returnFinraShortData(datetime.date(2021,1,7))

df["ShortVolumePercent"] = df["ShortVolume"] * 100.0 / df["TotalVolume"]
df["Date"] = pd.to_datetime(df["Date"], format="%Y%m%d")

#sdf = df[(df["Date"] > "2021-04-16") & (df["ShortVolumePercent"] >= 50) & (df["ShortVolumePercent"] <= 80)]

print(df[df["Symbol"]=="GME"].sort_values("ShortVolumePercent",ascending=False).head(20))


#fig = go.Figure()

def addLine(ticker, fig):
    fig.add_trace(go.Line(x=df[df["Symbol"]==ticker]["Date"], y=df[df["Symbol"]==ticker]["ShortVolumePercent"], name=ticker))
    fig.add_trace(go.Line(x=df[df["Symbol"]==ticker]["Date"] , y= sma(5, df[df["Symbol"]==ticker]["ShortVolumePercent"]), name=ticker+"SMA5"))



#addLine("HGEN", fig)
#addLine("BAC", fig)
#addLine("JNJ", fig)

#fig.update_xaxes(
#    rangebreaks=[
#        dict(bounds=["sat", "mon"]),
#        dict(values=["2021-04-02", "2021-02-15", "2021-01-18", "2021-01-01", "2020-12-25", "2020-11-26"])
#    ]
#)
#fig.show()