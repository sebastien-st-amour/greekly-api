from app import ma
from models import Stocks

class StocksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Stocks
        load_instance = True