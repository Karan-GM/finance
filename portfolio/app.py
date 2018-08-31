'''
Created on Jul 3, 2018

@author: karangm
'''

import dash
from dash.dependencies import Input, Output, Event, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import service
import pandas as pd
from datetime import datetime
import flask
import math
from controller import app as server

app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard')

nsdq = pd.read_csv('input/NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)
options = []
for tic in nsdq.index:
    options.append({'label':'{} {}'.format(tic,nsdq.loc[tic]['Name']), 'value':tic})

app.layout = html.Div([
    html.Div([
        html.H2('Quandl Finance Explorer',
                style={
                       'text-align': 'center',
                       'font-size': '2.65em',
                       'font-weight': 'bolder',
                       'font-family': 'Product Sans',
                       'color': "rgba(117, 117, 117, 0.95)",
                       'margin-top': '20px',
                       'margin-bottom': '20px'
                       }
                )
        ]
    ),
    html.Div([
            html.Div([
                html.H3('Choose:'),
                dcc.Dropdown(
                    id='choose',
                    options=[
                        {'label': 'Get Stock Prices', 'value': 1},
                        {'label': 'Calculate Returns', 'value': 2},
                        {'label': 'Measure Portfolio Risk', 'value': 3}
                    ],
                )
            ], style={'padding-left' : '5%', 'padding-right' : '5%'}),
            
            html.Div([
                html.H3('Select stock symbols:'),
                dcc.Dropdown(
                    id='ticker_symbol',
                    options=options,
                    value=['TSLA', 'AAPL'],
                    multi=True
                )
            ], style={'padding-left' : '5%', 'padding-right' : '5%'}),
            
            html.Div([
                html.H3('Periodicity:'),
                dcc.Dropdown(
                    id='periodicity',
                    options=[
                        {'label': 'Daily', 'value': 'D'},
                        {'label': 'Weekly', 'value': 'W'},
                        {'label': 'Monthly', 'value': 'M'}
                    ],
                    value='W'
                )
            ], style={'verticalAlign':'top', 'padding-left' : '5%', 'padding-right' : '5%'}),
            
            html.Div([
                html.H3('Adjusted Close Price?'),
                dcc.Dropdown(
                    id='total_return',
                    options=[
                        {'label': 'True', 'value': True},
                        {'label': 'False', 'value': False}
                    ],
                    value=False
                )
            ], style={'verticalAlign':'top', 'padding-left' : '5%', 'padding-right' : '5%'}),
            
            html.Div(
                id='portfolio_controls',
                children=[
                    html.Div([
                            html.H3('Weights:'),
                            dcc.Input(id='weights', placeholder='0.5, 0.5', type='text', value='0.5, 0.5', style={'width':'100%', 'height':'2vh'})
                        ], style={'verticalAlign':'top', 'padding-left' : '5%', 'padding-right' : '5%'},
                    ),
                    html.Div([
                            html.H3('Rolling Period(Window):'),
                            dcc.Input(id='rolling_period', placeholder='10', type='number', value=10, style={'width':'100%', 'height':'2vh'})
                        ], style={'verticalAlign':'top', 'padding-left' : '5%', 'padding-right' : '5%'},
                    )
                ], style={'display': 'none'}
            ),
            
            html.Div([
                html.H3('Select start and end dates:'),
                dcc.DatePickerRange(
                    id='my_date_picker',
                    max_date_allowed=datetime.today(),
                    start_date=datetime(2018, 1, 1),
                    end_date=datetime.today()
                )
            ], style={'verticalAlign':'top', 'padding-left' : '5%', 'padding-right' : '5%'}),
            
            html.Div([
                html.Button(
                    id='submit-button',
                    n_clicks=0,
                    children='Submit',
                    style={'fontSize':24, 'margin-left':'35%', 'margin-right':'35%', 'margin-top': '5%', 'margin-bottom': '5%'}
                ),
            ], style={'padding-left' : '5%', 'padding-right' : '5%'})
            
        ], style={'width':'40vh', 'height':'100%' , 'margin-top': '5vh', 'margin-left': '5vh', 'border':'1px solid black', 'background-color': '#eff0f1', 'float': 'left'}
    ),
    html.Div([
        html.Div(id='output')
    ], style={'margin-top': '5vh', 'margin-left' : '5vh', 'margin-right' : '5vh', 'border':'1px solid black', 'float': 'left', 'width': '65%'})
])

@app.callback(
    Output('portfolio_controls', 'style'),
    [
        Input('choose', 'value')
    ]
)
def update_layout(choose_value):
    if choose_value == 3:
        return {'display': 'block'}
    else:
        return {'display': 'none'}
    

@app.callback(
    Output('output', 'children'), 
    [
        Input('submit-button', 'n_clicks')
    ],
    [
        State('choose', 'value'),
        State('ticker_symbol', 'value'),
        State('my_date_picker', 'start_date'),
        State('my_date_picker', 'end_date'),
        State('periodicity', 'value'),
        State('total_return', 'value'),
        State('weights', 'value'),
        State('rolling_period', 'value')
    ]
)
def display_content(n_clicks, choose_option, tickers, start_date, end_date, periodicity, total_return, weights, rolling_period):
    start_date = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end_date = datetime.strptime(end_date[:10], '%Y-%m-%d')
    if choose_option == 1:
        price_df = pd.DataFrame()
        layout = {}
        ## Get Close/Adjusted Close values
        if total_return == True:
            ## Closing Price
            price_df = service.get_closing_price(tickers, start_date, end_date, periodicity)
            layout =  {'title': 'Closing Price'}
        else:
            ## Adjusted Closing Price
            price_df = service.get_closing_price(tickers, start_date, end_date, periodicity)
            layout =  {'title': 'Closing Price'}
        ## Creating the plot
        price_traces = [ go.Scatter(x=price_df.index, y=price_df[column_name], mode='lines',name=column_name) for column_name in price_df.columns]
        price_figure = {
            'data': price_traces,
            'layout': layout
        }
        price_graph = [dcc.Graph(id='closing_price_graph', figure=price_figure)]
        return price_graph
    elif choose_option == 2:
        ## Get returns
        returns_df = service.get_return(tickers, start_date, end_date, periodicity, total_return)
        traces = [ go.Scatter(x=returns_df.index, y=returns_df[column_name], mode='lines',name=column_name) for column_name in returns_df.columns]
        figure = {
            'data': traces,
            'layout': {
                'title': 'Returns'
            }
        }
        graph = [dcc.Graph(id='returns_graph', figure=figure)]
        return graph
    elif choose_option == 3:
        ## Measure portfolio risk
        weights_float = [float(i) for i in weights.split(",")]
        if len(tickers) != len(weights_float):
            error_message = 'Error: Make sure number of weights separated by comma are {} in number and sum up to 1'.format(len(tickers)) 
            return html.H3(error_message, style={'text-align': 'center', 'color': 'red'})
        elif int(math.ceil(sum(weights_float))) != 1:
            error_message = 'Error: Make sure number of weights separated by comma are {} in number and sum up to 1'.format(len(tickers)) 
            return html.H3(error_message, style={'text-align': 'center', 'color': 'red'})
        else:
            risks_df, component_contribution = service.get_risks(tickers, weights_float, start_date, end_date, total_return, periodicity, rolling_period)
            component_contribution_list = [str(i) for i in component_contribution]
            trace1 = go.Scatter(x=risks_df.index,
                                 y=risks_df['volatility'], 
                                 mode='lines',
                                 text = component_contribution_list,
                                 hoverinfo = "x+y+text"
                                 )
            figure = {
                'data': [trace1],
                'layout': {
                    'title': 'Portfolio Volatility Risk'
                }
            }
            risk_graph = [dcc.Graph(id='risk_graph', figure=figure)]
            return risk_graph
    else:
        return html.H3('Error: Select an option for Choose field', style={'text-align': 'center', 'color': 'red'})

@server.route('/dashboard') 
def render_dashboard():
    return flask.redirect('/dash')

if __name__ == '__main__':
#     app.run_server(debug=True)
    server.run()