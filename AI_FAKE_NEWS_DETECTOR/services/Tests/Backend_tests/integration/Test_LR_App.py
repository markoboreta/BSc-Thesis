import pytest
from flask import Flask
from AI_FAKE_NEWS_DETECTOR.services.prediciton_services_LR.LR import LRApp  # Ensure this imports correctly
import json

@pytest.fixture
def client():
    app = LRApp(__name__)
    # Setting the app configuration for testing
    app.config['TESTING'] = True
    app.config['DEBUG'] = False

    # Activating the application context
    with app.app_context():
        with app.test_client() as client:
            yield client

# Now, your tests below will automatically run within the application context
def test_predict_LR_valid_data(client):
    data = {'message': 'Some news article content'}
    response = client.post('/predict_LR', data=data)
    assert response.status_code == 200
    result = json.loads(response.data)
    assert 'LR' in result['result']

def test_home_page_LR(client):
    response = client.get('/LR_page')
    assert response.status_code == 200
    assert 'Logistic Regression' in response.data.decode('utf-8')

def test_predict_LR_empty_data(client):
    data = {'message': ''}
    response = client.post('/predict_LR', data=data)
    assert response.status_code == 415
    result = json.loads(response.data)
    assert 'error' in result

def test_predict_together_valid_data(client):
    data = {'message': 'Some text data'}
    response = client.post("/LR/get_result", data=data)
    assert response.status_code == 200
    result = response.json
    assert 'result' in result
    assert 'NB' in result['result']['result1']['result']
    assert 'PA' in result['result']['result2']['result']

def test_predict_together_empty_data(client):
    data = {'message': ''}
    response = client.post("/LR/get_result", data=data)
    assert response.status_code == 400
    assert 'error' in response.data.decode('utf-8')

def test_handle_error_404(client):
    response = client.get('/aaaaa')
    assert response.status_code == 404

def test_get_graph_data(client):
    response = client.get('/getTFData')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == {"Fake": 22850, "Real": 21416}

def test_get_wc_data(client):
    response = client.get('/getWCData')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == {"Fake": 1310, "Real": 2167}
