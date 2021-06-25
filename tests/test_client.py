from models import Stocks
from app import create_app, db
import pytest


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with app.app_context():
        
        with app.test_client() as client:
            
            db.create_all()

            stock = Stocks(
                ticker='DIS',
                description='Disney',
                broker_id=1234,
                exchange='NYSE'
            )

            db.session.add(stock)
            db.session.commit()
            
            yield client


def test_status(client):
    response = client.get('/stocks?id=1')
    assert response.status_code == 200
    assert response.json['ticker'] == 'DIS'