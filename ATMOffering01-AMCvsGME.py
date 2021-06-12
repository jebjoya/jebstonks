import yfinance
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Let's start by grabbing the tickers themselves, and pulling the data for the 11th June
gme = yfinance.Ticker("GME")
amc = yfinance.Ticker("AMC")
gme_prices = gme.history(period="1d",interval="1m",start="2021-06-11")
amc_prices = amc.history(period="1d",interval="1m",start="2021-06-11")

# Next up, using Plotly, we'll build the basic figure - just a simple 2 rows with shared x-axis
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, specs = [
                                                                [{}],
                                                                [{}]
                                                               ])

# Then let's add the Close prices to the Figure

fig.add_trace(go.Line(x=gme_prices.index, y=gme_prices['Close'], name="GME Close"), row=1, col=1)
fig.add_trace(go.Line(x=amc_prices.index, y=amc_prices['Close'], name="AMC Close"), row=2, col=1)

# Then display it

fig.update_layout(xaxis_rangeslider_visible=False,
                  template = 'plotly_dark')

fig.show()