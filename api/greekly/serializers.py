
from . import ma
from .models import Stocks, OptionContracts, OptionContractPrices

class StocksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Stocks
        load_instance = True

class OptionContractsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OptionContracts
        load_instance = True

class OptionContractPricesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OptionContractPrices
        load_instance = True