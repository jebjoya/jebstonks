import os
import requests
import datetime
from datetime import date
import pandas as pd
from requests.api import options
import yfinance as yf
import numpy as np

def skipDate(d, weekends):
    if weekends and d.weekday() in [5,6]:
        return True
    if d in [date(2021,1,1),date(2021,1,18),date(2021,2,15),date(2021,4,2),date(2021,5,31),date(2021,7,5)]:
        return True
    return False   

def advanceDays(d, days, weekends=False):
    delta = datetime.timedelta(1)
    for x in range(days):
        d += delta
        while skipDate(d, weekends):
            d += delta
    return d

def getFTDTheoryDates(optionDate):
    r = []
    next = advanceDays(optionDate, 1, True)
    next = advanceDays(next, 35, False)
    r.append(next)
    next = advanceDays(next, 21, True)
    r.append(next)
    next = advanceDays(next, 21, True)
    r.append(next)
    next = advanceDays(next, 21, True)
    r.append(next)
    return r


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

def getOrDownloadNYSEShort(d,exchange):
    datestring = d.strftime("%Y%m%d")
    yearstring = d.strftime("%Y")
    yearmonthstring = d.strftime("%Y%m")
    try:
        k = open(exchange + 'DataSet/'+ exchange + 'shvol' + datestring + ".txt",'r')
        k.close()
        return exchange + 'DataSet/'+ exchange + 'shvol' + datestring + ".txt"
    except IOError:
        if not download("https://ftp.nyse.com/ShortData/" + exchange + "shvol/" + exchange + "shvol" + yearstring + "/" + exchange + "shvol" + yearmonthstring + "/" + exchange + "shvol" + datestring + ".txt", dest_folder=exchange + "DataSet"):
            return exchange + 'DataSet/'+ exchange + 'shvol' + datestring + ".txt"
        else:
            print("Unable to get data for " + datestring)
            print("https://ftp.nyse.com/ShortData/" + exchange + "shvol/" + exchange + "shvol" + yearstring + "/" + exchange + "shvol" + yearmonthstring + "/" + exchange + "shvol" + datestring + ".txt")
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

def returnNYSEShortData(exchange, fromDate, toDate=datetime.date.today()):
    now = fromDate
    while now < toDate:
        fileLocationString = getOrDownloadNYSEShort(now,exchange)
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
    