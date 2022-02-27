
import json

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}

def test_health(client):
    
    response = client.get('/')

    assert response.status_code == 200
    assert response.data.decode() == 'Health is good!'

def login(client, email, password):
    
    return client.post('/login', data=json.dumps({'email': email, 'password': password}), headers=headers)

def test_login_success(client):
    
    response = login(client, 'greekly@test.com', 'greeklyTest123')

    assert response.status_code == 200
    assert "access_token" in response.json

def test_login_email_not_found(client):
    
    response = login(client, 'greeklyNotFound@test.com', 'greeklyTest123')

    assert response.status_code == 404
    assert response.json['message'] == 'User not found'

def test_login_invalid_password(client):
    
    response = login(client, 'greekly@test.com', 'incorrectPassword123')

    assert response.status_code == 401
    assert response.json['message'] == 'Invalid password'

def test_unapproved_login(client):
    
    login_response = login(client, 'notApproved@test.com', 'greeklyTest123')

    assert login_response.status_code == 401
    assert login_response.json['message'] == 'User is not approved to make requests'

def test_create_stock(client):

    test_stock = {
        'ticker': 'DIS',
        'exchange': 'NYSE',
        'description': 'WALT DISNEY COMPANY (THE)',
        'broker_id': 16142
    }

    login_response = login(client, 'greekly@test.com', 'greeklyTest123')
    access_token = login_response.json['access_token']
    headers['Authorization'] = 'Bearer ' + access_token
    response = client.post('/stocks', data=json.dumps(test_stock), headers=headers)

    assert response.status_code == 200
    assert response.json['broker_id'] == 16142
    assert response.json['ticker'] == 'DIS'

def test_get_stocks(client):

    login_response = login(client, 'greekly@test.com', 'greeklyTest123')
    access_token = login_response.json['access_token']
    headers['Authorization'] = 'Bearer ' + access_token
    
    response = client.get('/stocks', headers=headers)

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['ticker'] == 'GREEK'

def test_unauthenticated_get_stocks(client):
    
    response = client.get('/stocks')

    assert response.status_code == 401
    assert response.json['msg'] == 'Missing Authorization Header'