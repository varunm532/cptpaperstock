from flask import Blueprint, request, jsonify, Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS  # Import the CORS extension
from alpha_vantage.timeseries import TimeSeries

search_api = Blueprint('search_api', __name__, url_prefix='/api/stock')
api = Api(search_api)
app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

class SearchAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('symbol', type=str, required=True, help='No stock symbol provided', location='json')
        super(SearchAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        stock_symbol = args['symbol']

        if not stock_symbol:
            return jsonify({'error': 'Missing stock symbol or incorrect format.'}), 400

        try:
            ts = TimeSeries(key='H6POU8JVDEI52Y0K', output_format='pandas')
            stock_data, _ = ts.get_quote_endpoint(symbol=stock_symbol)
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve stock data: {e}'}), 500

        if '05. price' in stock_data:
            current_price = stock_data['05. price']
            response_data = {
                'symbol': stock_symbol,
                'current_price': current_price.item()  # Convert Series to a JSON serializable format
            }
            return jsonify(response_data)
        else:
            return jsonify({'error': 'Failed to retrieve stock data'}), 500

api.add_resource(SearchAPI, '/search')

# Replace 'YOUR_ALPHA_VANTAGE_API_KEY' with your actual Alpha Vantage API key
if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(search_api)

    app.run(debug=True)