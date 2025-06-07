import yfinance as yf
import pandas as pd

data = yf.download("AAPL", start="2018-01-01", end="2024-12-31")
data.to_csv("prices.csv")
