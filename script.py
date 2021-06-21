import json
import requests
from requests.api import head


base_url = 'http://127.0.0.1:5000'

with open('./test_data.json') as f:
    data = json.load(f)
    quotes = data['optionQuotes']

headers = {
  'Content-Type': 'application/json'
}

count = 0
for quote in quotes:

    data = {
        "broker_stock_id": quote.get('underlyingId'),
        "symbol": quote.get('symbol'),
        "broker_id": quote.get('symbolId'),
        "bid_price": quote.get('bidPrice'),
        "bid_size": quote.get('bidSize'),
        "ask_price": quote.get('askPrice'),
        "ask_size": quote.get('askSize'),
        "last_trade_price_tr_hrs": quote.get('lastTradePriceTrHrs'),
        "last_trade_price": quote.get('lastTradePrice'),
        "last_trade_size": quote.get('lastTradeSize'),
        "last_trade_tick": quote.get('lastTradeTick'),
        "last_trade_time": quote.get('lastTradeTime'),
        "volume": quote.get('volume'),
        "open_price": quote.get('openPrice'),
        "high_price": quote.get('highPrice'),
        "low_price": quote.get('lowPrice'),
        "volatility": quote.get('volatility'),
        "delta": quote.get('delta'),
        "gamma": quote.get('gamma'),
        "theta": quote.get('theta'),
        "vega": quote.get('vega'),
        "rho": quote.get('rho'),
        "open_interest": quote.get('openInterest'),
        "delay": quote.get('delay'),
        "is_halted": quote.get('isHalted'),
        "vwap": quote.get('VWAP')
    }

    if data['broker_stock_id'] != 0:

        res = requests.request(
            'POST', 
            f'{base_url}/options_quotes',
            headers=headers,
            data=json.dumps(data))
        # count+=1
        # print(res.text)
        # print(res.text)
# print(count)