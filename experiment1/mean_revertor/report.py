import matplotlib.pyplot as plt
import numpy as np


def evaluate_performance(portfolio, risk_free_rate=0.0):
    portfolio = np.array(portfolio)
    returns = np.diff(portfolio) / portfolio[:-1]

    excess_returns = returns - (risk_free_rate / (24*252))
    avg_excess_return = np.mean(excess_returns)
    std_dev = np.std(excess_returns)

    sharpe_ratio = (avg_excess_return / std_dev) * \
        np.sqrt(24*252) if std_dev else np.nan
    total_return = (portfolio[-1] - portfolio[0]) / portfolio[0]
    annualized_return = (1 + total_return) ** (252*24 / len(portfolio)) - 1
    volatility = std_dev * np.sqrt(24*252)

    return {
        "Sharpe Ratio": sharpe_ratio,
        "Total Return": total_return,
        "Annualized Return": annualized_return,
        "Volatility": volatility
    }


def calculate_metrics(portfolio, trade_results):
    total_return = (portfolio[-1] - portfolio[0]) / portfolio[0] * 100
    total_trades = len(trade_results)
    win_trades = sum(1 for result in trade_results if result > 0)
    win_rate = (win_trades / total_trades * 100) if total_trades > 0 else 0
    average_return_per_trade = (
        sum(trade_results) / total_trades) if total_trades > 0 else 0
    max_drawdown = calculate_max_drawdown(portfolio)

    return {
        'Total Return (%)': total_return,
        'Total Trades': total_trades,
        'Win Rate (%)': win_rate,
        'Average Return per Trade': average_return_per_trade,
        'Maximum Drawdown (%)': max_drawdown
    }


def calculate_max_drawdown(portfolio):
    max_drawdown = 0
    peak = portfolio[0]
    for value in portfolio:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak * 100
        max_drawdown = max(max_drawdown, drawdown)
    return max_drawdown


def print_summary(portfolio, trade_results):
    metrics = calculate_metrics(portfolio, trade_results)
    print(f"Total Return: {metrics['Total Return (%)']:.2f}%")
    print(f"Total Trades: {metrics['Total Trades']}")
    print(f"Win Rate: {metrics['Win Rate (%)']:.2f}%")
    print(
        f"Average Return per Trade: {metrics['Average Return per Trade']:.2f}")
    print(f"Maximum Drawdown: {metrics['Maximum Drawdown (%)']:.2f}%")


def plot_results(data, signals, portfolio):
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    axs[0].plot(data.index, data['close'], label='Close Price', color='black')
    axs[0].set_title("Price with Buy/Sell Signals")
    for i, signal in enumerate(signals):
        if signal == "BUY":
            axs[0].scatter(data.index[i], data['close'].iloc[i],
                           marker="^", color="green")
        elif signal == "SELL":
            axs[0].scatter(data.index[i], data['close'].iloc[i],
                           marker="v", color="red")
    axs[0].legend()

    axs[1].plot(data.index, portfolio, label='Portfolio Value', color='purple')
    axs[1].set_title("Portfolio Over Time")
    axs[1].legend()

    plt.tight_layout()
    plt.show()
