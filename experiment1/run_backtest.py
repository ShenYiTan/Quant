from mean_revertor.loader import load_csv
from mean_revertor.strategy import generate_mean_reversion_signals
from mean_revertor.engine import BacktestEngine
from mean_revertor.report import print_summary, evaluate_performance, plot_results

# Load the CSV
data = load_csv("data/sample_data.csv")  # Expects 'close' column

# Generate signals
signals = generate_mean_reversion_signals(
    data['close'], lookback=10, entry_threshold=2.0, exit_threshold=1.0,  cooldown_period=2
)

# Backtest
engine = BacktestEngine(data, signals, initial_cash=10000)
portfolio = engine.run()

# Summary
print_summary(portfolio, engine.trade_results)
performance = evaluate_performance(portfolio)
print("\nPerformance Metrics:")
for k, v in performance.items():
    print(f"{k}: {v:.4f}")

# Plot results
plot_results(data, signals, portfolio)
