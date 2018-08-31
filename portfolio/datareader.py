'''
Created on Jun 20, 2018

@author: karangm
'''
 
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like

import fix_yahoo_finance as yf
yf.pdr_override()
from pandas_datareader import data as pdr

import quandl
quandl.ApiConfig.api_key = "eB4ZdsvYD9f8ywu8XTKX"

def get_yahoo_stock_data_by_pdr(ticker, start_date, end_date, periodicity):
    data = pdr.get_data_yahoo(tickers = ticker, start=start_date, end=end_date, group_by = 'ticker')
    print(data.head())
    data_periodicised_df = data.resample(periodicity).agg({'Open': take_first, 'High': 'max', 'Low': 'min', 'Close': take_last, 'Adj Close': take_last, 'Volume': 'sum'})
    print(data_periodicised_df.shape)
    return(data_periodicised_df)
        
def get_quandl_stock_data_by_pdr(ticker, start_date, end_date, periodicity):
    symbol = 'WIKI' + '/' + ticker
    data = pdr.DataReader(symbol, 'quandl', start_date, end_date)
    data_filtered = data[['Open','High', 'Low', 'Close', 'AdjClose', 'Volume']]
    data_periodicised_df = data_filtered.resample(periodicity).agg({'Open': take_first, 'High': 'max', 'Low': 'min', 'Close': take_last, 'AdjClose': take_last, 'Volume': 'sum'})
    return(data_periodicised_df)

def get_quandl_stock_data(ticker, start_date, end_date, periodicity):
    symbol = 'WIKI' + '/' + ticker
    data = quandl.get(symbol, start_date=str(start_date), end_date=str(end_date))
    data_filtered = data[['Open','High', 'Low', 'Close', 'Adj. Close', 'Volume']]
    data_periodicised_df = data_filtered.resample(periodicity).agg({'Open': take_first, 'High': 'max', 'Low': 'min', 'Close': take_last, 'Adj. Close': take_last, 'Volume': 'sum'})
    return(data_periodicised_df)
    
def take_first(array_like):
    return array_like[0]

def take_last(array_like):
    return array_like[-1]