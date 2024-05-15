import pytest
import json
import os
from unittest.mock import mock_open, patch, Mock
from app import app
from app import create_app

# Reminder for the testing


@pytest.fixture
def client():
    app = create_app({'TESTING': True})  
    with app.test_client() as client:
        yield client

def test_predict_PA_valid_data(client):
    data = {'message': 'Some news article content'}
    response = client.post('/predict_NB', data=data)
    assert response.status_code == 200
    result = json.loads(response.data)
    assert 'LR' in result['result']

def test_predict_LR_empty_data(client):
    data = {'message': ''}
    response = client.post('/predict_LR', data=data)
    assert response.status_code == 400
    result = json.loads(response.data)
    assert 'error' in result

def test_predict_together_valid_data(client):
    data = {'message': 'Some text data'}

    # Make a request to route
    response = client.post("/LR/get_result", data=data)

    # Validate the response status code and content
    assert response.status_code == 200
    result = response.json
    assert 'result' in result
    assert 'NB' in result['result']['result1']['result']
    assert 'PA' in result['result']['result2']['result']

# unsupported media type test
def test_predict_together_empty_data(client):
    data = {'message': ''}
    response = client.post("/LR/get_result", data=data)
    assert response.status_code == 400
    assert b'error' in response.data


# non-existant page test
def test_handle_error_404(client):
    response = client.get('/random_route_101')
    assert response.status_code == 404
    assert b'You have reached the error 404 page' in response.data

# Test whether the backend for graph data is handled well
def test_get_graph_data(client):
    with patch('app.open', mock_open(read_data='{"data": [1, 2, 3]}')) as mock_file:
        response = client.get('/getLRData')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == {'data': [1, 2, 3]}

# the same test for the word count
def test_get_wc_data(client):
    with patch('app.open', mock_open(read_data='{"data": [1, 2, 3]}')) as mock_file:
        response = client.get('/getWCData')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == {'data': [1, 2, 3]}


