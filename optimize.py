import optuna
import pandas as pd
from strategy import run_backtest
import os
from datetime import datetime

price = pd.read_csv(os.getcwd() + "\\prices.csv")
price = price.drop(0)
price = price.drop(1)
price = price.rename(columns={'Price':'Date'})
price = price[['Date','Close']]

for i in range(len(price)):
    price['Close'].iloc[i] = float(price['Close'].iloc[i])
    price['Date'].iloc[i] = datetime.strptime(price['Date'].iloc[i], '%Y-%m-%d')

price = price.set_index('Date')

def objective(trial):
    sma_window = trial.suggest_int("sma_window", 5, 50)
    threshold = trial.suggest_float("threshold", 0.01, 0.05)

    result = run_backtest(price, sma_window, threshold)
    stats = result[0].stats
    sharpe = stats.loc["daily_sharpe"]
    return sharpe

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)
print("Лучшие параметры:", study.best_params)
