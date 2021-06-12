import yfinance as yf
import numpy as np

ticker = "GME"

ticker = yf.Ticker(ticker)

putMax = ticker.info['previousClose'] * 0.05
float = ticker.info['floatShares']

#print(ticker.options)
x = 0

minStrike = 10000000000

for optiondate in ticker.options:
    puts = ticker.option_chain(optiondate)[1]
    minStrikeDate = min(puts['strike'])
    if minStrikeDate < minStrike:
        minStrike = minStrikeDate

print(minStrike)

for optiondate in ticker.options:
    puts = ticker.option_chain(optiondate)[1]
    #y = puts[puts['strike'] <= putMax]['openInterest']
    #y = puts[puts['strike'] == min(puts['strike'])]['openInterest']
    y = puts[puts['strike'] == minStrike]['openInterest']
    x += np.nansum(y)

x*=100

print("OTM Puts",x,"Total Float",float,"Percentage",(x/float)*100.0,"%")