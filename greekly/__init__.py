from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()

def create_app(config = None):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    ma.init_app(app)
    db.init_app(app)

    with app.app_context():
        
        from . import routes
        from . import encoders

        app.json_encoder = encoders.GreeklyEncoder

        return app
