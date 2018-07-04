'''
Created on Jun 21, 2018

@author: karangm
'''
from flask import Flask
from flask import request
import service
from flask import json

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Welcome to portfolio management'

@app.route('/returns', methods=['GET'])
def get_returns():
    print(request.query_string)
    assets = request.args.get('assets')
    tickers = [x.strip() for x in assets.split(',')]
    start_date = request.args.get('start_date') 
    end_date = request.args.get('end_date')
    periodicity = request.args.get('periodicity')
    total_return = request.args.get('total_return')
    print("Assets: "+assets+ " Start Date: "+start_date+ " End Date: "+end_date+ " Periodicity: "+periodicity+ " Total Return: "+total_return)
    returns_df = service.get_return(tickers, start_date, end_date, periodicity, total_return)
    result = {}
    result['ticker'] = tickers
    result['datetime'] = returns_df.index.values.tolist()
    returns_list = []
    for ticker in tickers:
        returns_list.append(returns_df[ticker].fillna(0).values.tolist())
    result['daily_returns'] = returns_list
    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/risks', methods=['GET'])
def get_risks():
    print(request.query_string)
    assets = request.args.get('assets')
    tickers = [x.strip() for x in assets.split(',')]
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    periodicity = request.args.get('periodicity')
    total_return = request.args.get('total_return')
    weights = [x.strip() for x in request.args.get('weights').split(',')]
    window = int(request.args.get('window'))
    print("Assets: "+assets+ " Weights: "+request.args.get('weights')+ " Start Date: "+start_date+ " End Date: "+end_date+ " Periodicity: "+periodicity+ " Window: "+str(window))
    risks_df, component_contribution = service.get_risks(tickers, weights, start_date, end_date, total_return, periodicity, window)
    result = {}
    result["tickers"] = tickers
    result['datetime'] = risks_df.index.values.tolist()
    result["total_risk"] = risks_df['volatility'].values.tolist()
    result["component_contribution"] = component_contribution.tolist()
    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response