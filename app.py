from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from encoders import GreeklyJSONEncoder
import os

app = Flask(__name__)
app.json_encoder = GreeklyJSONEncoder
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)

from views import StocksAPI, OptionsQuotesAPI

stocks_api = StocksAPI.as_view('stocks_api')
options_quotes_api = OptionsQuotesAPI.as_view('options_quotes_api')
app.add_url_rule('/stocks', view_func=stocks_api)
app.add_url_rule('/options_quotes', view_func=options_quotes_api)

if __name__ == "__main__":
    app.run(debug=True)