from flask import Flask, jsonify
from encoders import GreeklyJSONEncoder

def create_app(config):
    app = Flask(__name__)
    app.json_encoder = GreeklyJSONEncoder
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from views import StocksAPI, OptionsQuotesAPI
    from models import db
    from exceptions import InvalidUsage
    db.init_app(app)

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    stocks_api = StocksAPI.as_view('stocks_api')
    options_quotes_api = OptionsQuotesAPI.as_view('options_quotes_api')
    app.add_url_rule('/stocks', view_func=stocks_api)
    app.add_url_rule('/options_quotes', view_func=options_quotes_api)

    return app