

def calculate_spread_zscore(asset1, asset2, window=20):
    spread = asset1 - asset2  # Assuming beta = 1
    mean = spread.rolling(window=window).mean()
    std = spread.rolling(window=window).std()
    zscore = (spread - mean) / std
    return zscore, spread
