from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()


def create_app(config = None):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
        
    from . import routes
    from . import encoders

    app.register_blueprint(routes.bp)
    app.json_encoder = encoders.GreeklyEncoder

    return app
