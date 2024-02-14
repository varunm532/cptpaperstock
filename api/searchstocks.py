from flask import Flask, render_template, Blueprint, jsonify, request
import requests
from flask_cors import CORS
import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
import sqlite3
from __init__ import app, db, cors, dbURI




from model.users import Stocks,User,Transactions

search_api = Blueprint('search_api', __name__,
                   url_prefix='/api/stock')
api = Api(search_api)

class SearchAPI(Resource):
    def __init__(self, name, import_name, **kwargs):
        super().__init__(name, import_name, **kwargs)

        self.route('/search', methods=['POST'])(self.search_stock)

    class search_stock(Resource):
        def post(self):
            try: 
                data = request.get_json()
                symbol = data['symbol']

                # Make a request to the FMP API to get stock information
                api_key = '034ce1b9ccc7ac857fc59ec5665cfc5e'  # Replace with your FMP API key
                url = f'https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={api_key}'
                response = requests.get(url)
                stock_data = response.json()

                # if response.status_code != 200:
                #     return {'error': 'Error Occured'}
                
                stock_info = {
                    'symbol': stock_data[0]['symbol'],
                    'name': stock_data[0]['name'],
                    'price': stock_data[0]['price'],
                    'changesPercentage': stock_data[0]['changesPercentage'],
                    'change': stock_data[0]['change'],
                    'dayLow': stock_data[0]['dayLow'],
                    'dayHigh': stock_data[0]['dayHigh'],
                    'yearHigh': stock_data[0]['yearHigh'],
                    'yearLow': stock_data[0]['yearLow'],
                    'marketCap': stock_data[0]['marketCap'],
                    'priceAvg50': stock_data[0]['priceAvg50'],
                    'priceAvg200': stock_data[0]['priceAvg200'],
                    'volume': stock_data[0]['volume'],
                    'avgVolume': stock_data[0]['avgVolume'],
                    'exchange': stock_data[0]['exchange'],
                    'open': stock_data[0]['open'],
                    'previousClose': stock_data[0]['previousClose'],
                    'eps': stock_data[0]['eps'],
                    'pe': stock_data[0]['pe'],
                    'earningsAnnouncement': stock_data[0]['earningsAnnouncement'],
                    'sharesOutstanding': stock_data[0]['sharesOutstanding'],
                    'timestamp': stock_data[0]['timestamp']
                }

                print(stock_info)

                return jsonify(stock_info)
            except Exception as e:
                return jsonify('Error Occured')
            
            
        
    api.add_resource(search_stock, '/search')


            
        
    
        
        