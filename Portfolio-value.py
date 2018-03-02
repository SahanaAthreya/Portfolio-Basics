# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 11:30:56 2018

@author: sathreya
"""

import os
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 

''' Read: http://pandas.pydata.org/pandas-docs/stable/api.html#api-dataframe-stats '''

def symbol_to_path(symbol, base_dir = 'data'):
	return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def dates_creator(start_date, end_date):
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
	return df / df.iloc[0,:]

def plot(df, title):
	ax = df.plot(title = title, fontsize = 12)
	ax.set_xlabel('Date')
	ax.set_ylabel(title)
	plt.show()

def calculate_portfolio_value(normalized_df, init_investment, symbols, allocation_fraction):
        stock_investment = init_investment * allocation_fraction
        stock_values = normalized_df[symbols] * stock_investment
        portfolio_value = stock_values.sum(axis = 1)
        plot(portfolio_value, 'Portfolio value')
        print(portfolio_value)

if __name__ == "__main__":
    start_date = '2013-03-01'
    end_date = '2018-02-01'
    symbols = ['SPY', 'AAPL', 'GOOG', 'FB']
    
    dates = dates_creator(start_date, end_date)
    df = get_data(symbols, dates)
    # Daily portfolio
    
    normalized = normalize_data(df)
    
    allocation_fraction = np.array([0.15, 0.4, 0.2, 0.25])
    start_investment = 1e6 # in USD
    
    calculate_portfolio_value(normalized, start_investment, symbols, allocation_fraction)