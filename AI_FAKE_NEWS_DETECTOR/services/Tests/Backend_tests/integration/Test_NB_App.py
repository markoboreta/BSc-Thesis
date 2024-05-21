import pytest
import json
import os
from unittest.mock import mock_open, patch, Mock
from prediction_services_NB.app import app, NBApp


@pytest.fixture
def client():
    app = NBApp(__name__)
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    with app.test_client() as client:
        yield client

def test_predict_NB_valid_data(client):
    data = {'message': 'Some news article content'}
    response = client.post('/predict_NB', data=data)
    assert response.status_code == 200
    result = json.loads(response.data)
    assert 'NB' in result['result']

def test_predict_NB_empty_data(client):
    data = {'message': ''}
    response = client.post('/predict_NB', data=data)
    assert response.status_code == 400
    result = json.loads(response.data)
    assert 'error' in result

def test_predict_together_valid_data(client):
    data = {'message': 'Some text data'}
    # Make a request to the Flask route
    response = client.post("/NB/get_result", data=data)
    # Validate the response status code and content
    assert response.status_code == 200
    result = response.json
    assert 'result' in result
    assert 'LR' in result['result']['result1']['result']
    assert 'PA' in result['result']['result2']['result']

# unsupported media type test
def test_predict_together_empty_data(client):
    data = {'message': ''}
    response = client.post("/NB/get_result", data=data)
    assert response.status_code == 400
    assert b'error' in response.data

def test_handle_error_404(client):
    response = client.get('/random_route_101')
    assert response.status_code == 404
    assert b'You have reached the error 404 page' in response.data

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


