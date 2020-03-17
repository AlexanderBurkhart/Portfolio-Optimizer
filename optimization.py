import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from scipy.optimize import minimize
from util import get_data, plot_data

def calc_stats(df, single=False): 
    #cumulative return
    crs = []
    for symbol in df.columns:
        data = df[symbol]
        crs.append(data[-1]/data[0] - 1)
    cr = pd.Series(data=crs, index=df.columns)

    #average daily return and standard deviation of daily return
    df_daily = df.copy()
    df_daily[1:] = (df[1:]/df[:-1].values)-1
    df_daily.iloc[0,:] = 0

    adr = df_daily.mean()
    sddr = df_daily.std()

    #sharp ratio
    sr = adr / sddr

    if single:
        return cr[0], adr[0], sddr[0], sr[0]
    return cr, df_daily, adr, sddr, sr

def check_sum(weights):
    return np.sum(weights) - 1

def get_sharp(weights, prices_all, neg=True):
    cr, dr, adr, sddr, sr = calc_stats(prices_all)
    weights = np.array(weights)
    ret = np.sum(adr*weights)
    vol = np.sum(sddr*weights)
    sr = np.sqrt(252) * ret/vol
    if neg:
        return sr * -1
    return sr

def find_allocs(prices_all):
    cons = ({'type':'eq','fun':check_sum})
    bounds = [(0,1) for sym in prices_all.columns]
    init_guess = [1.0/len(prices_all.columns) for sym in prices_all.columns]
    opt_results = minimize(get_sharp,init_guess, prices_all, 'SLSQP', 
                            bounds=bounds, constraints=cons)
    return opt_results.x

def get_port_vals(alloc):
   pass 

def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):
    
    dates = pd.date_range(sd, ed)
    
    prices_all = get_data(syms, dates)
    
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    
    # find the allocations for the optimal portfolio
    allocs = find_allocs(prices_all)
    allocs_prices = (prices_all*allocs).sum(axis=1).to_frame(name='Portfolio')
    cr, adr, sddr, sr = calc_stats(allocs_prices, single=True) # Get daily portfolio value 
    
    if gen_plot:
        df_temp = pd.concat([allocs_prices, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        df_temp = df_temp/df_temp.iloc[0]
        df_temp.plot()
        plt.show()

    return allocs, cr, adr, sddr, sr

def test_code():
    start_date = dt.datetime(2010,2,1)
    end_date = dt.datetime(2010,12,31)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'IBM', 'SPY']
    
    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)
    # Print statistics
    print("Start Date:", start_date)
    print("End Date:", end_date)
    print("Symbols:", symbols)
    print ("Allocations:", allocations)
    print ("Sharpe Ratio:", sr)
    print("Volatility (stdev of daily returns):", sddr)
    print ("Average Daily Return:", adr)
    print ("Cumulative Return:", cr)
    
if __name__ == "__main__":
    test_code()
