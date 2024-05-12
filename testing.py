import timeseries as ts
import yfinance as yf
import matplotlib.pyplot as plt

data = yf.download("MSFT",period="1y")["Adj Close"]

ts.drawdown_graph(data)

plt.show()

