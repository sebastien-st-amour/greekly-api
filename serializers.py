
from flask_marshmallow import Marshmallow
from models import Stocks, OptionsQuotes

ma = Marshmallow()

class StocksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Stocks
        load_instance = True

class OptionsQuotesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OptionsQuotes
        load_instance = True