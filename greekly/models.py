from . import db
from .enums import OptionTypes
from datetime import datetime
from werkzeug.security import check_password_hash

class GreeklyModel(db.Model):
    
    __abstract__ = True
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Users(GreeklyModel):

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Stocks(GreeklyModel):
    
    __tablename__ = 'stocks'
    
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(5), unique=True)
    description = db.Column(db.String(70))
    exchange = db.Column(db.String(10))
    broker_id = db.Column(db.Integer, unique=True)
    options = db.relationship('OptionContracts', backref='stocks', lazy=True)

    def __repr__(self):
        return f'Stocks(ticker={self.ticker}, description={self.description})'

class OptionContracts(GreeklyModel):

    __tablename__ = 'option_contracts'


    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(30), unique=True)
    type = db.Column(db.Enum(OptionTypes))
    broker_id = db.Column(db.Integer, unique=True)
    expiration_date = db.Column(db.DateTime)
    strike_price = db.Column(db.Numeric(14,2))
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'))
    option_contract_prices = db.relationship('OptionContractPrices', backref='option_contracts', lazy=True)

    def __repr__(self):
        return f'OptionContracts(symbol={self.symbol})'

class OptionContractPrices(GreeklyModel):

    __tablename__ = 'option_contract_prices'

    id = db.Column(db.Integer, primary_key=True)
    bid_price = db.Column(db.Numeric(14,2), nullable=True)
    bid_size = db.Column(db.Integer, default=0)
    ask_price = db.Column(db.Numeric(14,2), nullable=True)
    ask_size = db.Column(db.Integer, default=0)
    last_trade_price_tr_hrs = db.Column(db.Numeric(14,2), nullable=True)
    last_trade_price = db.Column(db.Numeric(14,2), nullable=True)
    last_trade_size = db.Column(db.Integer, default=0)
    last_trade_tick = db.Column(db.String(10), nullable = True)
    last_trade_time = db.Column(db.DateTime, nullable=True)
    volume = db.Column(db.Integer, default=0)
    open_price = db.Column(db.Numeric(14,2), nullable=True)
    high_price = db.Column(db.Numeric(14,2), nullable=True)
    low_price = db.Column(db.Numeric(14,2), nullable=True)
    volatility = db.Column(db.Numeric(14,2), nullable=True)
    delta = db.Column(db.Numeric(8,6), nullable=True)
    gamma = db.Column(db.Numeric(8,6), nullable=True)
    theta = db.Column(db.Numeric(8,6), nullable=True)
    vega = db.Column(db.Numeric(8,6), nullable=True)
    rho = db.Column(db.Numeric(8,6), nullable=True)
    open_interest = db.Column(db.Integer, default=0)
    delay = db.Column(db.Integer, default=0)
    is_halted = db.Column(db.Boolean)
    vwap = db.Column(db.Numeric(14,2), nullable=True)
    option_contract_id = db.Column(db.Integer, db.ForeignKey('option_contracts.id'))

    def __repr__(self):
        return f'OptionContractPrices(id={self.id}, option_contract_id={self.option_contract_id})'