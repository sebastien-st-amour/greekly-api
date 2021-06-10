from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)

class GreeklyModel(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Stocks(GreeklyModel):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(5), unique=True)
    description = db.Column(db.String(70))
    exchange = db.Column(db.String(10))
    broker_id = db.Column(db.Integer, unique=True)

    def __repr__(self):
        return f'Stocks(ticker={self.ticker}, description={self.description})'

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