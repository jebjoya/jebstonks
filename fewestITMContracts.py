import yfinance as yf
import numpy as np

gme = yf.Ticker("GME")
date = '2021-05-07'

calls = gme.option_chain(date)[0]
puts = gme.option_chain(date)[1]

maxPainValue = 0

for price in np.arange(calls['strike'].min(), calls['strike'].max(),0.5):
    relevantCalls = calls[calls['strike'] >= price]
    relevantPuts = puts[puts['strike'] <= price]
    callValue = relevantCalls['openInterest'].sum()
    putValue = relevantPuts['openInterest'].sum()
    totalValue = callValue + putValue
    if totalValue > maxPainValue:
        maxPainValue = totalValue
        maxPain = price

print(round(maxPain,2))
print(round(maxPainValue,2))
