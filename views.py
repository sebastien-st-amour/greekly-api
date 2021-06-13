from app import db
from flask import request, jsonify
from flask.views import MethodView
from models import Stocks
from serializers import StocksSchema
from exceptions import InvalidUsage

class StocksAPI(MethodView):

    def get(self):
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
        
        return jsonify(StocksSchema().dump(res, many=True))
    
    def post(self):
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