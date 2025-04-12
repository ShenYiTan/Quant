from rsi_backtester.loader import load_csv
from rsi_backtester.indicators import calculate_rsi
from rsi_backtester.strategy import generate_macd_signals
from rsi_backtester.engine import BacktestEngine
from rsi_backtester.report import print_summary,plot_results, evaluate_performance
from rsi_backtester.optimize3 import optimize_macd_strategy  # assume you save the optimizer here

if __name__ == '__main__':
    # Load your data here
    data = load_csv("data/sample_data.csv")

    # Run optimization
    best_params, best_sharpe, portfolio, signals, trade_results = optimize_macd_strategy(
        data,
        fast_range=range(5, 20),    # Adjusted range for fast
        slow_range=range(21, 31),   # Adjusted range for slow
        signal_range=range(5, 15)    # Adjusted range for signal
    )

    # Check if any valid parameters were found
    if best_params is None or portfolio is None or trade_results is None:
        print("No valid MACD parameters were found. Please check the optimization ranges and conditions.")
    else:
        # Print results
        print("Best MACD Params:", best_params)
        print("Best Sharpe Ratio:", best_sharpe)

        print_summary(portfolio, trade_results)
        performance = evaluate_performance(portfolio)

        print("Performance Metrics:")
        for k, v in performance.items():
            print(f"{k}: {v:.4f}")

        # Generate MACD for plotting using the best parameters
        macd, _ = generate_macd_signals(data, *best_params)
        plot_results(data, macd, signals, portfolio)


