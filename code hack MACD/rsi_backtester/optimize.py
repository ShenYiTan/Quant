from rsi_backtester.strategy import generate_macd_signals
from rsi_backtester.engine import BacktestEngine
from rsi_backtester.report import evaluate_performance
from tqdm import tqdm

def optimize_macd_strategy(data, fast_range, slow_range, signal_range):
    best_sharpe = float('-inf')
    best_params = None
    best_portfolio = None
    best_signals = None
    best_trade_results = None
    #total_combinations = len(fast_range) * len(slow_range) * len(signal_range)
    #count = 0

    for fast in tqdm(fast_range, desc="Fast EMA"):
        for slow in slow_range:
            if fast >= slow:
                continue  # MACD fast must be less than slow
            for signal in signal_range:
                #count += 1
                #print(f"Running {count}/{total_combinations} - MACD({fast}, {slow}, {signal})")
                try:
                    macd_indicator, signals = generate_macd_signals(data, fast, slow, signal)
                    engine = BacktestEngine(data, signals, initial_cash=10000)
                    portfolio = engine.run()
                    performance = evaluate_performance(portfolio)
                    sharpe = performance["Sharpe Ratio"]

                    if sharpe is not None and sharpe > best_sharpe:
                        best_sharpe = sharpe
                        best_params = (fast, slow, signal)
                        best_portfolio = portfolio
                        best_signals = signals
                        best_trade_results = engine.trade_results
                except Exception as e:
                    print(f"Error with MACD({fast}, {slow}, {signal}): {e}")
                    continue

    return best_params, best_sharpe, best_portfolio, best_signals, best_trade_results
