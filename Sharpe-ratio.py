# -*- coding: utf-8 -*-
"""

@author: sathreya
"""

import os
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 



def symbol_to_path(symbol, base_dir = 'data'):
	return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def dates_creator():
	start_date = '2017-01-01'
	end_date = '2018-02-01'
	dates = pd.date_range(start_date, end_date)
	return dates

def get_data(symbols, dates):
	df = pd.DataFrame(index = dates)
	if 'SPY' not in symbols: # adding SPY as the main reference
		symbols.insert(0, 'SPY')
	for symbol in symbols:
		df_temp = pd.read_csv(symbol_to_path(symbol),
			index_col = 'Date',
			parse_dates = True,
			usecols = ['Date', 'Adj Close'],
			na_values = ['nan'])
		df_temp = df_temp.rename(columns = {'Adj Close': symbol})
		df = df.join(df_temp)
	
		if symbol == 'SPY':
			df = df.dropna(subset = ['SPY'])
	return df

def normalize_data(df):
	return df / df.ix[0,:]

def plot(df, title):
	ax = df.plot(title = title, fontsize = 12)
	ax.set_xlabel('Date')
	ax.set_ylabel(title)
	plt.show()

def get_daily_returns(df):
	daily_returns = df.copy()
	# Calculating daily returns
	daily_returns[1:] = (df / df.shift(1)) - 1 
	# Setting daily returns for row 0 to 0.
	daily_returns.ix[0, :] = 0
	return daily_returns
     
def annualised_sharpe(returns, N=252):
    return np.sqrt(N) * returns.mean() / returns.std()

if __name__ == "__main__":
   
    symbols = ['SPY', 'AAPL', 'GOOG', 'IBM', 'TSLA']
    dates = dates_creator()
    df = get_data(symbols, dates)
    daily_returns = get_daily_returns(df)
    # Sharpe ratio
    annualized_sharpe_ratio = annualised_sharpe(daily_returns, N=252)
    print('Annualized Sharpe ratio:')
    print(annualized_sharpe_ratio)