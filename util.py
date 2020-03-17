import pandas as pd
import matplotlib.pyplot as plt
import os

def symbol_to_path(symbol, base_dir='data'):
    return os.path.join(base_dir, '{}.csv'.format(str(symbol)))

def get_data(symbols, dates):
    df_final = pd.DataFrame(index=dates)
    for symbol in symbols:
        file_path = symbol_to_path(symbol)
        df_temp = pd.read_csv(file_path, parse_dates=True, index_col='Date', 
                                usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df_final = df_final.join(df_temp)
    df_final = fill_missing_values(df_final)
    return df_final

def plot_data(df_data):
    ax = df_data.plot(title='Stock Data', fontsize=2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.show()

def fill_missing_values(df_data):
    df_data.fillna(method='ffill', inplace=True)
    df_data.fillna(method='bfill', inplace=True)
    return df_data
