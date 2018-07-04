'''
Created on Jun 30, 2018

@author: karangm
'''

import datareader
import pandas as pd
import numpy as np

def get_closing_price(tickers, start_date, end_date, periodicity):
    closing_price_df = pd.DataFrame()
    for ticker in tickers:
        data = datareader.get_quandl_stock_data(ticker, start_date, end_date, periodicity)
        closing_price_df[ticker] = data['Close']
    return(closing_price_df)

def get_adjusted_closing_price(tickers, start_date, end_date, periodicity):
    closing_price_df = pd.DataFrame()
    for ticker in tickers:
        data = datareader.get_quandl_stock_data(ticker, start_date, end_date, periodicity)
        closing_price_df[ticker] = data['Adj Close']
    return(closing_price_df)

def get_return(tickers, start_date, end_date, periodicity, total_return):
    returns_df = pd.DataFrame()
    for ticker in tickers:
        data = datareader.get_quandl_stock_data(ticker, start_date, end_date, periodicity)
        data_parsed = parser_data(data, total_return)
        daily_returns = (data_parsed/data_parsed.shift(1))-1
        returns_df[ticker] = daily_returns.iloc[:,0].fillna(0)
    return(returns_df)  

def parser_data(data, total_return):
    if(total_return == 'True'):
        return(data[['Adj. Close']])
    else:
        return(data[['Close']])

def get_annulizing_multiplier(periodicity):
    if periodicity == 'D':
        return 252
    elif periodicity == 'W':
        return 52
    elif periodicity == 'M':
        return 12
        
def calculate_portfolio_volatility(weights, returns_df, periodicity, window):  
    covariance_df = returns_df.rolling(window).cov().dropna()
    date_index_list = list(set(covariance_df.index.get_level_values(0).values))
    covariances = covariance_df.values.reshape(len(date_index_list), len(returns_df.columns), len(returns_df.columns))
    annulizing_multiplier = get_annulizing_multiplier(periodicity)
    portfolio_volatility_list = []
    component_contribution_list = []
    for i in range(len(covariances)):
        portfolio_volatility = np.dot(weights.T, np.dot(covariances[i] * annulizing_multiplier, weights)) ** 0.5
        marginal_contribution = np.dot(weights.T, covariances[i] * annulizing_multiplier) / portfolio_volatility
        component_contribution = marginal_contribution * weights 
        portfolio_volatility_list.append(portfolio_volatility)
        component_contribution_list.append(component_contribution)
    return (date_index_list, portfolio_volatility_list, component_contribution_list)

def get_risks(tickers, weights, start_date, end_date, total_return, periodicity, window):
    weights = np.array(weights, dtype="float64")
    risks_df = pd.DataFrame() 
    for ticker in tickers:
        data = datareader.get_quandl_stock_data(ticker, start_date, end_date, periodicity)
        risks_df[ticker] = (data['Close']/data['Close'].shift(1))-1
    date_index_list, portfolio_volatility_list, component_contribution_list = calculate_portfolio_volatility(weights, risks_df, periodicity, window)
    result_df = pd.DataFrame(index=date_index_list)
    result_df['volatility'] = portfolio_volatility_list
    component_contribution = np.array(component_contribution_list)
    return(result_df, component_contribution)