from flask import request, jsonify, current_app as app
from .serializers import OptionContractsSchema, StocksSchema
from .models import OptionContracts, Stocks
from .exceptions import InvalidUsage
from datetime import datetime
from . import db

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/', methods=['GET'])
def healthcheck():
    return "Health is good!"

@app.route('/stocks', methods=['GET', 'POST'])
def stocks():

    if request.method == 'GET':

        if len(request.args) > 1:
            raise InvalidUsage("Please specify only one of ['ticker', 'id', 'description', 'exchange', 'broker_id']")
        
        ticker = request.args.get('ticker')
        if ticker:
            res = Stocks.query.filter_by(ticker=ticker).first()
            return StocksSchema().dump(res)

        stock_id = request.args.get('id')
        if stock_id:
            res = Stocks.query.filter_by(id=stock_id).first()
            return StocksSchema().dump(res)

        description = request.args.get('description')
        if description:
            res = Stocks.query.filter_by(description=description).first()
            return StocksSchema().dump(res)
        
        res = Stocks.query.all()
        
        return jsonify(StocksSchema(many=True).dump(res))
    
    if request.method == 'POST':

        if not request.json:
            raise InvalidUsage("No input provided")
        
        request_obj = request.get_json()
        
        if not 'ticker' in request_obj:
            raise InvalidUsage("Ticker is required")
        
        if not 'description' in request_obj:
            raise InvalidUsage("Company description is required")

        if not 'broker_id' in request_obj:
            raise InvalidUsage("Broker stock ID is required")

        if not 'exchange' in request_obj:
            raise InvalidUsage("Exchange is required")

        stock = Stocks(
            ticker=request_obj['ticker'],
            description=request_obj['description'],
            broker_id=request_obj['broker_id'],
            exchange=request_obj['exchange'],)

        db.session.add(stock)
        db.session.commit()

        return StocksSchema().dump(Stocks.query.filter_by(ticker=request_obj['ticker']).first())

@app.route('/option_contracts', methods=['GET', 'POST'])
def option_contracts():
    
    if request.method == 'GET':

        res = OptionContracts.query

        type = request.args.get('type')
        if type:
            res = res.filter_by(type = type)

        res_serialized = OptionContractsSchema().dump(res.all(), many=True)

        return jsonify(res_serialized)

# @app.route('/option_quotes', methods=['GET', 'POST'])
# def options_quotes():

#     if request.method == 'GET':
        
#         type = request.args.get('type')
#         max_theta = request.args.get('max_theta')
#         min_theta = request.args.get('min_theta')

#         res = OptionsQuotes.query

#         if type:
#             res = res.filter_by(type = type)
#         if max_theta:
#             res = res.filter(OptionsQuotes.theta <= max_theta)
#         if min_theta:
#             res = res.filter(OptionsQuotes.theta >= min_theta)

#         res_serialized = OptionsQuotesSchema().dump(res.all(), many=True)

#         return jsonify(res_serialized)
    
#     if request.method == 'POST':

#         if not request.json:
#             raise InvalidUsage("No input provided")
        
#         request_obj = request.get_json()
        
#         if not 'broker_stock_id' in request_obj:
#             raise InvalidUsage("Underlying broker stock ID is required")
        
#         if not 'symbol' in request_obj:
#             raise InvalidUsage("Contract identifier is required (e.g. AMZN23Jul21P3360.00)")

#         if not 'broker_id' in request_obj:
#             raise InvalidUsage("Broker option ID is required")

#         symbol = request_obj['symbol']
#         broker_id = request_obj['broker_id']
#         stock = Stocks.query.filter_by(broker_id=request_obj['broker_stock_id']).first()
#         ticker = stock.ticker

#         bid_price = request_obj['bid_price']
#         bid_size = request_obj['bid_size']
#         ask_price = request_obj['ask_price']
#         ask_size = request_obj['ask_size']
#         last_trade_price_tr_hrs = request_obj['last_trade_price_tr_hrs']
#         last_trade_price = request_obj['last_trade_price']
#         last_trade_size = request_obj['last_trade_size']
#         last_trade_tick = request_obj['last_trade_tick']
#         last_trade_time = request_obj['last_trade_time']
#         volume = request_obj['volume']
#         open_price = request_obj['open_price']
#         high_price = request_obj['high_price']
#         low_price = request_obj['low_price']
#         volatility = request_obj['volatility']
#         delta = request_obj['delta']
#         gamma = request_obj['gamma']
#         theta = request_obj['theta']
#         vega = request_obj['vega']
#         rho = request_obj['rho']
#         open_interest = request_obj['open_interest']
#         delay = request_obj['delay']
#         is_halted = request_obj['is_halted']
#         vwap = request_obj['vwap']

#         offset = 7 if symbol[len(ticker)+1].isnumeric() else 6

#         option_type = symbol[len(ticker)+offset]

#         trade_date = last_trade_time[:10].split('-')
        
#         option = OptionsQuotes(
#             symbol=symbol,
#             stock_id=stock.id,
#             broker_id=broker_id,
#             type=option_type,
#             bid_price =bid_price,
#             bid_size = bid_size,
#             ask_price = ask_price,
#             ask_size = ask_size,
#             last_trade_price_tr_hrs = last_trade_price_tr_hrs,
#             last_trade_price = last_trade_price,
#             last_trade_size = last_trade_size,
#             last_trade_tick = last_trade_tick,
#             last_trade_time = datetime(int(trade_date[0]), int(trade_date[1]), int(trade_date[2])),
#             volume = volume,
#             open_price = open_price,
#             high_price = high_price,
#             low_price = low_price,
#             volatility = volatility,
#             delta = delta,
#             gamma = gamma,
#             theta = theta,
#             vega = vega,
#             rho = rho,
#             open_interest = open_interest,
#             delay = delay,
#             is_halted = is_halted,
#             vwap = vwap
#         )

#         db.session.add(option)
#         db.session.commit()

#         return OptionsQuotesSchema().dump(OptionsQuotes.query.filter_by(broker_id=request_obj['broker_id']).first())
