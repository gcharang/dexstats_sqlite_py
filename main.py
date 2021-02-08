import flask
from stats_utils import get_availiable_pairs, summary_for_pair, ticker_for_pair, orderbook_for_pair, trades_for_pair

path_to_db = '/DB/43ec929fe30ee72be42c9162c56dde910a05e50d/MM2.db'
app = flask.Flask(__name__)

#available_pairs = get_availiable_pairs(mycur)

# for pair in available_pairs:
#     summary_for_pair(pair, rpc_password)

@app.route('/api/v1/summary', methods=['GET'])
def summary():
    # TODO: get data for all pairs - have to activate all coins first :)
    summary_data = summary_for_pair(("RICK", "MORTY"), path_to_db)
    return flask.jsonify(summary_data)


@app.route('/api/v1/ticker', methods=['GET'])
def ticker():
    # TODO: get data for all pairs - have to activate all coins first :)
    ticker_data = ticker_for_pair(("RICK", "MORTY"), path_to_db)
    return flask.jsonify(ticker_data)


@app.route('/api/v1/orderbook/<market_pair>', methods=['GET'])
def orderbook(market_pair="KMD_BTC"):
    orderbook_data = orderbook_for_pair(market_pair)
    return flask.jsonify(orderbook_data)


@app.route('/api/v1/trades/<market_pair>', methods=['GET'])
def trades(market_pair="KMD_BTC"):
    trades_data = trades_for_pair(market_pair, path_to_db)
    return flask.jsonify(trades_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
