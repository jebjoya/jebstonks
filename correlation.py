import yfinance as yf
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr

x = yf.download('GME AMC',start='2021-01-01', end='2021-05-29',interval="1d")['Close']
x['GME Yesterday'] = x['GME'].shift(1)
x['GME Change'] = (x['GME'] - x['GME Yesterday']) / x['GME Yesterday']
x['AMC Yesterday'] = x['AMC'].shift(1)
x['AMC Change'] = (x['AMC'] - x['AMC Yesterday']) / x['AMC Yesterday']

print(x[x['AMC Change'] > 2.5])



#x.plot.scatter(x='GME Change',y='AMC Change')

#print(pearsonr(x['GME'],x['AMC']))
#print(spearmanr(x['GME'],x['AMC']))

#plt.show()
