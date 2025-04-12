import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import product
from time import time

from mean_revertor.loader import load_csv
from mean_revertor.strategy import generate_mean_reversion_signals
from mean_revertor.engine import BacktestEngine
from mean_revertor.report import print_summary, evaluate_performance, calculate_metrics

# Load CSV
DATA_PATH = "data/sample_data.csv"
data = load_csv(DATA_PATH)

# Parameter ranges
lookbacks = [10, 20, 30]
entry_thresholds = [1.0, 1.5, 2.0]
exit_thresholds = [0.1, 0.2]
cooldowns = [0, 1, 2]

# Store results
results = []
start_time = time()
total_combos = len(lookbacks) * len(entry_thresholds) * \
    len(exit_thresholds) * len(cooldowns)
current = 0

for lookback, entry, exit_, cooldown in product(lookbacks, entry_thresholds, exit_thresholds, cooldowns):
    current += 1
    print(f"[{current}/{total_combos}] Testing L={lookback}, E={entry}, X={exit_}, CD={cooldown}")

    signals = generate_mean_reversion_signals(
        data["close"],
        lookback=lookback,
        entry_threshold=entry,
        exit_threshold=exit_,
        cooldown_period=cooldown
    )

    engine = BacktestEngine(data, signals)
    portfolio = engine.run()

    # Evaluate and summarize performance
    performance = evaluate_performance(portfolio)
    summary = calculate_metrics(portfolio, engine.trade_results)

    results.append({
        "lookback": lookback,
        "entry": entry,
        "exit": exit_,
        "cooldown": cooldown,
        "sharpe": performance["Sharpe Ratio"],
        "total_return": summary['Total Return (%)'],
        "win_rate": summary['Win Rate (%)'],
        "avg_trade_return": summary['Average Return per Trade'],
        "max_drawdown": summary['Maximum Drawdown (%)']
    })

# Convert to DataFrame
results_df = pd.DataFrame(results)
results_df.dropna(inplace=True)

# Pivot for heatmap
pivot = results_df.pivot_table(
    index="lookback", columns="cooldown", values="sharpe", aggfunc=np.mean
)

# Plot heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(pivot, annot=True, fmt=".2f", cmap="coolwarm",
            cbar_kws={'label': 'Sharpe Ratio'})
plt.title("Sharpe Ratio Heatmap (Exit=Varied, Cooldown=Varied)")
plt.xlabel("Cooldown Threshold")
plt.ylabel("lookback Period")
plt.tight_layout()
plt.show()

print("Total runtime: {:.2f}s".format(time() - start_time))
