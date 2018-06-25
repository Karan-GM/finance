'''
Created on Jun 21, 2018

@author: karangm
'''

import datareader
import pandas as pd
import numpy as np

def get_return(tickers, start_date, end_date, periodicity, total_return):
    result = {} 
    for ticker in tickers:
        ticker_result = {}
        data = datareader.get_stock_data(ticker, start_date, end_date, periodicity)
        print(data)
        data_parsed = parser_data(data, total_return)
        profits = (data_parsed/data_parsed.iloc[0,0])-1
        daily_returns = (data_parsed/data_parsed.shift(1))-1
        ticker_result['profits'] = profits.iloc[:,0].fillna(0).values.tolist()
        ticker_result['daily_returns'] = daily_returns.iloc[:,0].fillna(0).values.tolist()
        result[ticker] = ticker_result
    return(result)  

def parser_data(data, total_return):
    if(total_return == True):
        return(data[['Adj Close']])
    else:
        return(data[['Close']])


def get_risks(tickers, weights, start_date, end_date, periodicity, duration):
    weights = np.array(weights, dtype="float64")
    returns_df = pd.DataFrame() 
    for ticker in tickers:
        data = datareader.get_stock_data(ticker, start_date, end_date, periodicity)
        print(data)
        returns_df[ticker] = (data['Close']/data['Close'].shift(1))-1
    portfolio_volatility = np.dot(weights.T, np.dot(returns_df.cov() * 250, weights)) ** 0.5
    marginal_contribution = np.dot(weights.T, returns_df.cov()*250) / portfolio_volatility
    component_contribution = marginal_contribution * weights 
    component_contribution_percentage = (component_contribution/component_contribution.sum()) * 100
    risks = {}
    risks["tickers"] = tickers
    risks["total_risk"] = portfolio_volatility
    risks["component_contribution"] = component_contribution.tolist()
    risks["component_contribution_percentage"] = component_contribution_percentage.tolist()
    return(risks) 

 