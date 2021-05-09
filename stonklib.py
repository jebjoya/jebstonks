import os
import requests
import datetime
import pandas as pd

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

