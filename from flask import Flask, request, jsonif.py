from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TIINGO_API_KEY = "YOUR_TIINGO_API_KEY"

@app.route('/api/stock', methods=['GET'])
def get_stock_data():
    ticker = request.args.get('ticker', '').upper()
    if not ticker:
        return jsonify({'error': 'Ticker is required'}), 400

    try:
        # Fetching company outlook
        meta_url = f"https://api.tiingo.com/tiingo/daily/{ticker}?token={TIINGO_API_KEY}"
        meta_response = requests.get(meta_url)
        if meta_response.status_code != 200:
            return jsonify({'error': 'Invalid Ticker'}), 404

        meta_data = meta_response.json()

        # Fetching stock summary
        stock_url = f"https://api.tiingo.com/iex/{ticker}?token={TIINGO_API_KEY}"
        stock_response = requests.get(stock_url)
        if stock_response.status_code != 200:
            return jsonify({'error': 'Invalid Ticker'}), 404

        stock_data = stock_response.json()[0]

        # Combine responses
        return jsonify({
            'company': meta_data,
            'stock': stock_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
