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
 
def get_stock_data(tickers, start_date, end_date, periodicity):
    data = pdr.get_data_yahoo(tickers = tickers, start=start_date, end=end_date, group_by = 'ticker')
    data_periodicised_df = data.resample(rule=periodicity, how={'Open': take_first, 'High': 'max', 'Low': 'min', 'Close': take_last, 'Adj Close': take_last, 'Volume': 'sum'})
    return(data_periodicised_df)

def take_first(array_like):
    return array_like[0]

def take_last(array_like):
    return array_like[-1]