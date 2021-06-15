from app import ma
from models import Stocks, OptionsQuotes

class StocksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Stocks
        load_instance = True

class OptionsQuotesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OptionsQuotes
        load_instance = True