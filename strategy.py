import bt
import pandas as pd
import yfinance as yf
from datetime import datetime
import os

def mean_reversion_strategy(price, sma_window=20, threshold=0.02):
    sma = price.rolling(window=sma_window).mean()
    zscore = (price - sma) / price.std()

    signals = -zscore  # если цена выше средней — шорт, если ниже — лонг
    signals = signals.clip(-1, 1)  # ограничим размер позиции

    return signals

def run_backtest(price, sma_window=20, threshold=0.02):
    signals = mean_reversion_strategy(price, sma_window, threshold)

    strategy = bt.Strategy(
        'MeanReversion',
        [
            bt.algos.RunDaily(),
            bt.algos.SelectAll(),
            bt.algos.WeighTarget(signals),
            bt.algos.Rebalance()
        ]
    )

    backtest = bt.Backtest(strategy, price)
    result = bt.run(backtest)
    return result
