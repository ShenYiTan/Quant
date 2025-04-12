class BacktestEngine:
    def __init__(self, data, signals, initial_cash=10000):
        self.data = data
        self.signals = signals
        self.cash = initial_cash
        self.initial_cash = initial_cash
        self.position = 0
        self.trades = []
        self.portfolio = []
        self.trade_results = []

    def run(self):
        self.last_buy_price = None

        for i in range(len(self.data)):
            price = self.data['close'].iloc[i]
            signal = self.signals[i]

            if signal == 'BUY' and self.cash > 0:
                self.position = float(self.cash) / price
                self.last_buy_price = price
                self.cash = 0
                self.trades.append(('BUY', price))

            elif signal == 'SELL' and self.position > 0:
                trade_profit = (price - self.last_buy_price) * self.position
                self.trade_results.append(trade_profit)

                self.cash = self.position * price
                self.position = 0
                self.trades.append(('SELL', price))

            portfolio_value = self.cash + self.position * price
            self.portfolio.append(portfolio_value)

        return self.portfolio
