import numpy as np


def generate_mean_reversion_signals(prices, lookback=10, entry_threshold=1.5, exit_threshold=2.0, cooldown_period=2):
    signals = []
    position = None
    cooldown = 0

    rolling_mean = prices.rolling(window=lookback).mean()
    rolling_std = prices.rolling(window=lookback).std()

    for i in range(len(prices)):
        if i < lookback or np.isnan(rolling_std[i]):
            signals.append("HOLD")
            continue

        z_score = (prices[i] - rolling_mean[i]) / rolling_std[i]

        if cooldown > 0:
            cooldown -= 1
            signals.append("HOLD")
            continue

        if position is None:
            if z_score < -entry_threshold:
                signals.append("BUY")
                position = "LONG"
                cooldown = cooldown_period
            elif z_score > entry_threshold:
                signals.append("SELL")
                position = "SHORT"
                cooldown = cooldown_period
            else:
                signals.append("HOLD")
        elif position == "LONG" and z_score > -exit_threshold:
            signals.append("SELL")
            position = None
            cooldown = cooldown_period
        elif position == "SHORT" and z_score < exit_threshold:
            signals.append("BUY")
            position = None
            cooldown = cooldown_period
        else:
            signals.append("HOLD")

    return signals
