import yfinance as yf
import numpy as np

gme = yf.Ticker("GME")
date = '2021-05-07'

calls = gme.option_chain(date)[0]
puts = gme.option_chain(date)[1]

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

print(round(minGain,2))
print(round(minGainValue,2))
