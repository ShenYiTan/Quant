import pandas as pd

def load_csv(path):
    df = pd.read_csv(path, parse_dates=['datetime'])
    df.set_index('datetime', inplace=True)

    return df
