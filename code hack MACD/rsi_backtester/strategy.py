
def generate_macd_signals(data, short_window=12, long_window=26, signal_window=9):
    df = data.copy()
    
    # Calculate EMA
    df['ema_short'] = df['close'].ewm(span=short_window, adjust=False).mean()
    df['ema_long'] = df['close'].ewm(span=long_window, adjust=False).mean()
    
    # MACD line and signal line
    df['macd'] = df['ema_short'] - df['ema_long']
    df['signal_line'] = df['macd'].ewm(span=signal_window, adjust=False).mean()

    # Generate signals
    df['signal'] = 'HOLD'
    df.loc[(df['macd'] > df['signal_line']) & (df['macd'].shift(1) <= df['signal_line'].shift(1)), 'signal'] = 'BUY'
    df.loc[(df['macd'] < df['signal_line']) & (df['macd'].shift(1) >= df['signal_line'].shift(1)), 'signal'] = 'SELL'

    return df[['macd', 'signal_line']], df['signal'].tolist()
