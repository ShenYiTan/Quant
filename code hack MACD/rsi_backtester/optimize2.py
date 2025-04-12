from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm  # Import tqdm for progress bar
from rsi_backtester.strategy import generate_macd_signals
from rsi_backtester.engine import BacktestEngine
from rsi_backtester.report import evaluate_performance

def evaluate_macd(params, data):
    fast, slow, signal = params
    try:
        print(f"Evaluating MACD({fast}, {slow}, {signal})")  # Debugging output
        macd_indicator, signals = generate_macd_signals(data, fast, slow, signal)
        engine = BacktestEngine(data, signals, initial_cash=10000)
        portfolio = engine.run()
        performance = evaluate_performance(portfolio)
        
        return (fast, slow, signal, performance["Sharpe Ratio"], portfolio, signals, engine.trade_results)  # Return all values
    except Exception as e:
        print(f"Error evaluating MACD({fast}, {slow}, {signal}): {e}")  # Log the error
        return fast, slow, signal, None, None, None, None  # Ensure consistent return

def optimize_macd_strategy(data, fast_range, slow_range, signal_range):
    best_sharpe = float('-inf')
    best_params = None
    best_portfolio = None
    best_signals = None
    best_trade_results = None

    param_combinations = [
        (fast, slow, signal)
        for fast in fast_range
        for slow in slow_range
        if fast < slow  # Ensure fast < slow
        for signal in signal_range
    ]

    total_combinations = len(param_combinations)

    for params in tqdm(param_combinations, desc="Evaluating MACD Parameters"):
        fast, slow, signal, sharpe, portfolio, signals, trade_results = evaluate_macd(params, data)  # Unpacking all values

        print(f"Evaluated: fast={fast}, slow={slow}, signal={signal}, Sharpe={sharpe:.4f}")  # Debugging output

        if sharpe is not None and sharpe > best_sharpe:
            best_sharpe = sharpe
            best_params = (fast, slow, signal)
            best_portfolio = portfolio
            best_signals = signals
            best_trade_results = trade_results

    if best_params is None:
        print("No valid parameters found during optimization.")
        return None, None, None, None, None  # Adjusted return

    return best_params, best_sharpe, best_portfolio, best_signals, best_trade_results
