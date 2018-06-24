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
    returns = service.get_return(tickers, start_date, end_date, periodicity, total_return)
    print(returns)
    response = app.response_class(
        response=json.dumps(returns),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/risks', methods=['GET'])
def get_risks():
    print(request.query_string)
    assets = request.args.get('assets')
    tickers = [x.strip() for x in assets.split(',')]
    weights = [x.strip() for x in request.args.get('weights').split(',')]
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    periodicity = request.args.get('periodicity')
    duration = request.args.get('duration')
    print("Assets: "+assets+ " Weights: "+request.args.get('weights')+ " Start Date: "+start_date+ " End Date: "+end_date+ " Periodicity: "+periodicity+ " Duration: "+duration)
    risks = service.get_risks(tickers, weights, start_date, end_date, periodicity, duration)
    response = app.response_class(
        response=json.dumps(risks),
        status=200,
        mimetype='application/json'
    )
    return response
    
if __name__ == '__main__':  # Script executed directly?
    app.run()