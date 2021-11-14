
import json

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}

def test_create_stock(client):

    test_stock = {
        'ticker': 'DIS',
        'exchange': 'NYSE',
        'description': 'WALT DISNEY COMPANY (THE)',
        'broker_id': 16142
    }

    response = client.post('/stocks', data=json.dumps(test_stock), headers=headers)

    assert response.status_code == 200
    assert response.json['broker_id'] == 16142
    assert response.json['ticker'] == 'DIS'

def test_get_stocks(client):
    
    response = client.get('/stocks')

    assert response.status_code == 200
    assert response.json == []