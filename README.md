# Quant
Trading Strategy using MACD and mean revertor

## 📈 Strategies Implemented

### 1. 📉 Mean Reversion Strategy
- Based on **Bollinger Bands**
- **Buy Signal**: When price falls below the lower band
- **Sell Signal**: When price rises above the upper band
- Assumes prices tend to revert back to the mean over time

### 2. 📊 MACD Crossover Strategy
- Uses **MACD (Moving Average Convergence Divergence)**
- **Buy Signal**: When MACD line crosses above the Signal line
- **Sell Signal**: When MACD line crosses below the Signal line
- Captures momentum shifts in the market

---
## 🔁 Workflow Overview

1. **Data Collection**
   - Run `endpoint.py` to pull OHLCV data 
   - Saves hourly data as `.csv` in the `/data/` directory

2. **Strategy Execution**
   - Implemented in `strategy.py` for both Mean Reversion and MACD
   - Generates Buy/Sell/Short signals on historical price data

3. **Backtesting Engine**
   - Simulates trades based on signals using `engine.py`

4. **Performance Evaluation**
   - Evaluates metrics like Sharpe Ratio, Win Rate, Max Drawdown

5. **Visualization**
   - Uses `plot_results()` to show:
     - Buy/Sell signals over price chart
     - Portfolio value over time

Canva link:
https://www.canva.com/design/DAGkTvlNGso/SvlYpOM0mnf-e9Gi6dTCrg/edit?utm_content=DAGkTvlNGso&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
