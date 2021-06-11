from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import Stocks
from exceptions import InvalidUsage

@app.route('/stocks', methods=['POST', 'GET'])
def stocks():
    
    if request.method == 'GET':
        
        if len(request.args) > 1:
            raise InvalidUsage("Please specify only one of ['ticker', 'id', 'description', 'exchange', 'broker_id']")
        
        ticker = request.args.get('ticker')
        if ticker:
            res = Stocks.query.filter_by(ticker=ticker).first()
            
            return jsonify(res) if res else ''
    
        return Stocks.query.all()
    
    elif request.method == 'POST':

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

        return Stocks.query.filter_by(ticker=request_obj['ticker']).first()

if __name__ == "__main__":
    app.run(debug=True)