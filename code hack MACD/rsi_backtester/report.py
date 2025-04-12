import matplotlib.pyplot as plt
import numpy as np


def evaluate_performance(portfolio, risk_free_rate=0.0):
    portfolio = np.array(portfolio)
    returns = np.diff(portfolio) / portfolio[:-1]  # Daily returns

    excess_returns = returns - (risk_free_rate / (252*24))
    avg_excess_return = np.mean(excess_returns)
    std_dev = np.std(excess_returns)

    sharpe_ratio = np.nan
    if std_dev != 0:
        sharpe_ratio = (avg_excess_return / std_dev) * np.sqrt(252*24)

    total_return = (portfolio[-1] - portfolio[0]) / portfolio[0]
    annualized_return = (1 + total_return) ** (24*252 / len(portfolio)) - 1
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
        if drawdown > max_drawdown:
            max_drawdown = drawdown

    return max_drawdown


def print_summary(portfolio, trade_results):
    total_return = (portfolio[-1] - portfolio[0]) / portfolio[0] * 100

    metrics = calculate_metrics(portfolio, trade_results)

    print(f"Total Return: {metrics['Total Return (%)']:.2f}%")
    print(f"Total Trades: {metrics['Total Trades']}")
    print(f"Win Rate: {metrics['Win Rate (%)']:.2f}%")
    print(
        f"Average Return per Trade: {metrics['Average Return per Trade']:.2f}")
    print(f"Maximum Drawdown: {metrics['Maximum Drawdown (%)']:.2f}%")


def plot_results(data, rsi, signals, portfolio):
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # Price chart
    axs[0].plot(data.index, data['close'], label='Price', color='black')
    axs[0].set_ylabel("Price")
    axs[0].set_title("Price and Trade Signals")

    # Plot buy/sell signals
    buy_signals = data[[(s == 'BUY') for s in signals]]
    sell_signals = data[[(s == 'SELL') for s in signals]]

    axs[0].scatter(buy_signals.index, buy_signals['close'],
                   marker='^', color='green', label='BUY')
    axs[0].scatter(sell_signals.index, sell_signals['close'],
                   marker='v', color='red', label='SELL')
    axs[0].legend()

    # MACD + Signal Line
    axs[1].plot(data.index, rsi['macd'], label='MACD', color='blue')
    axs[1].plot(data.index, rsi['signal_line'],
                label='Signal Line', color='orange')
    axs[1].axhline(0, color='grey', linestyle='--', linewidth=1)
    axs[1].set_ylabel("MACD")
    axs[1].set_title("MACD Indicator")
    axs[1].legend()

    # Portfolio value
    axs[2].plot(data.index, portfolio, label='Portfolio Value', color='purple')
    axs[2].set_ylabel("Portfolio")
    axs[2].set_xlabel("Date")
    axs[2].set_title("Portfolio Value Over Time")

    plt.tight_layout()
    plt.show()
