from werkzeug.security import generate_password_hash
from greekly import create_app, db
from greekly.models import Stocks, Users
import pytest


@pytest.fixture
def client():
    
    app = create_app('config.TestingConfig')

    with app.test_client() as client:
        
        with app.app_context():

            db.create_all()

            # add test data to database
            greekly_user = Users(email='greekly@test.com', password_hash=generate_password_hash('greeklyTest123'))
            greekly_stock = Stocks(ticker='GREEK', description='Greekly Inc.', exchange='NASDAQ', broker_id=1234)

            db.session.add(greekly_user)
            db.session.add(greekly_stock)
            db.session.commit()
            
            db.create_all()
            
        yield client

