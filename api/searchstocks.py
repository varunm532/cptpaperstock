from flask import Flask, render_template, Blueprint, jsonify, request
import requests


class StockBlueprint(Blueprint):
    def __init__(self, name, import_name, **kwargs):
        super().__init__(name, import_name, **kwargs)

        self.route('/search', methods=['POST'])(self.search_stock)

    def search_stock(self):
        try:
            data = request.get_json()
            symbol = data['symbol']

            # Make a request to the FMP API to get stock information
            api_key = '034ce1b9ccc7ac857fc59ec5665cfc5e'  # Replace with your FMP API key
            url = f'https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={api_key}'
            response = requests.get(url)
            stock_data = response.json()

            if not stock_data:
                return jsonify({'error': 'No data available for the given symbol'}), 404

            # Extract relevant information from the API response
            stock_info = {
                'symbol': stock_data[0]['symbol'],
                'current_price': stock_data[0]['price'],
            }

            return jsonify(stock_info)

        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Create an instance of the StockBlueprint class and register it under the '/api/stock' URL prefix
search_bp = StockBlueprint('stock', __name__)

