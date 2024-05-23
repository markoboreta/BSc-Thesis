import pytest
import os
from flask import Flask
from prediction_services_NB.app import NBApp, base_dir # Ensure this imports correctly
import json

#base_dir = os.path.abspath(os.path.dirname(__file__)) 
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, "static")

@pytest.fixture
def client():
    app = NBApp(__name__, template_dir, static_dir)
    # Setting the app configuration for testing
    app.config['TESTING'] = True
    app.config['DEBUG'] = True

    # Activating the application context
    with app.app_context():
        with app.test_client() as client:
            yield client

# Now, your tests below will automatically run within the application context
def test_predict_NB_valid_data(client):
    data = {'message': 'Some news article content'}
    response = client.post('/predict_NB', data=data)
    assert response.status_code == 200
    result = json.loads(response.data)
    #assert 'NB' in result['result']

def test_home_page_NB(client):
    response = client.get('/NB_page')
    assert response.status_code == 200
    assert 'Naive Bayes' in response.data.decode('utf-8')

def test_predict_NB_empty_data(client):
    data = {'message': ''}
    response = client.post('/predict_NB', data=data)
    assert response.status_code == 415
    result = json.loads(response.data)
    assert 'error' in result

def test_predict_together_valid_data(client):
    data = {'message': 'Some text data'}
    response = client.post("/NB/get_result", data=data)
    assert response.status_code == 200
    result = response.json
    assert 'result' in result
    assert 'LR' in result['result']['result1']['result']
    assert 'PA' in result['result']['result2']['result']

def test_predict_together_empty_data(client):
    data = {'message': ''}
    response = client.post("/NB/get_result", data=data)
    assert response.status_code == 400
    assert 'error' in response.data.decode('utf-8')

def test_handle_error_404(client):
    response = client.get('/aaaaa')
    assert response.status_code == 404

def test_get_graph_data(client):
    response = client.get('/getNBData')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == {"Fake": 22850, "Real": 21416}

def test_get_wc_data(client):
    response = client.get('/getWCData')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == {"Fake": 1310, "Real": 2167}
""