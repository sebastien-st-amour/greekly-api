from greekly import create_app, db
# from greekly.models import Stocks
import pytest


@pytest.fixture
def client():
    
    app = create_app('config.TestingConfig')

    with app.test_client() as client:
        
        with app.app_context():
            
            db.create_all()
            
            yield client

