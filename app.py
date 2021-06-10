from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import Stocks


@app.route('/stocks', methods=['POST', 'GET'])
def stocks():
    if request.method == 'GET':
        
        ticker = request.args.get('ticker')
        
        if ticker:
            res = Stocks.query.filter_by(ticker='ticker').first()

            return res if res else ''
        
        return Stocks.query.all()

if __name__ == "__main__":
    app.run(debug=True)