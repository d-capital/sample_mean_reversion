import pandas as pd
import yfinance as yf
from datetime import datetime
import os
from strategy import run_backtest

price = pd.read_csv(os.getcwd() + "\\prices.csv")
price = price.drop(0)
price = price.drop(1)
price = price.rename(columns={'Price':'Date'})
price = price[['Date','Close']]

for i in range(len(price)):
    price['Close'].iloc[i] = float(price['Close'].iloc[i])
    price['Date'].iloc[i] = datetime.strptime(price['Date'].iloc[i], '%Y-%m-%d')

price = price.set_index('Date')
result = run_backtest(price,sma_window=5,threshold=0.049)

import matplotlib.pyplot as plt
import seaborn as sns

# Рисуем кривую капитала
result.plot(title='Equity Curve (Cumulative Returns)')
plt.show()

# Гистограмма дневной доходности
returns = result[0].prices.pct_change().dropna()
sns.histplot(returns, bins=50, kde=True)
plt.title("Daily Returns Distribution")
plt.xlabel("Return")
plt.ylabel("Frequency")
plt.show()

stats = result[0].stats
print("Sharpe Ratio:", stats.loc["daily_sharpe"])
print("CAGR:", stats.loc["cagr"])
print("Max Drawdown:", stats.loc["max_drawdown"])