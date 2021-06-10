from app import db
from datetime import datetime

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