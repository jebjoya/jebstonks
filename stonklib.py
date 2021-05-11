import os
import requests
import datetime
import pandas as pd
import yfinance as yf
import numpy as np

def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    filename = url.split('/')[-1].replace(" ", "_")
    file_path = os.path.join(dest_folder, filename)
    r = requests.get(url, stream=True)
    if r.ok:
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:
        return True

def getOrDownloadFinra(d):
    datestring = d.strftime("%Y%m%d")
    try:
        k = open('dataSet/CNMSshvol' + datestring + ".txt",'r')
        k.close()
        return 'dataSet/CNMSshvol' + datestring + ".txt"
    except IOError:
        if not download("http://regsho.finra.org/CNMSshvol" + datestring + ".txt", dest_folder="dataSet"):
            return 'dataSet/CNMSshvol' + datestring + ".txt"
        else:
            return False

def returnFinraShortData(fromDate, toDate=datetime.date.today()):
    now = fromDate
    while now < toDate:
        fileLocationString = getOrDownloadFinra(now)
        if fileLocationString:
            tdf = pd.read_csv(fileLocationString, delimiter = "|")
            tdf = tdf[tdf["Date"] > 100000]
            try:
                df = pd.concat([df, tdf])
            except NameError:
                df = tdf
        now += datetime.timedelta(days=1)
    return df

def getMinGain(tickerString, date):
    ticker = yf.Ticker(tickerString)
    dateString = datetime.date.strftime(date, format="%Y-%m-%d")

    calls = ticker.option_chain(dateString)[0]
    puts = ticker.option_chain(dateString)[1]

    minGainValue = np.infty

    for price in np.arange(calls['strike'].min(), calls['strike'].max(),0.5):
        relevantCalls = calls[calls['strike'] < price]
        relevantPuts = puts[puts['strike'] > price]
        callValue = (relevantCalls['openInterest'] * 100 * (price - relevantCalls['strike'])).sum()
        putValue = (relevantPuts['openInterest'] * 100 * (relevantPuts['strike'] - price)).sum()
        totalValue = callValue + putValue
        if totalValue < minGainValue:
            minGainValue = totalValue
            minGain = price

    return round(minGain,2)

def calculateOBV(volume, close):
    lastClose = close.shift(1)
    