import pytest
import json
import os
from unittest.mock import mock_open, patch
from app import app
from flask_cors import CORS

def test_predict_PA_valid_data(client):
    data = {'message': 'Some news article content'}
    response = client.post('/predict_PA', data=data)
    assert response.status_code == 200
    result = json.loads(response.data)
    assert 'PA' in result['result']

def test_predict_PA_empty_data(client):
    data = {'message': ''}
    response = client.post('/predict_PA', data=data)
    assert response.status_code == 400
    result = json.loads(response.data)
    assert 'error' in result

def test_predict_together_valid_data(client):
    data = {'message': 'Some text data'}
    response = client.post('/PA/get_result', data=data)
    assert response.status_code == 200
    result = json.loads(response.data)
    assert 'result' in result
    assert 'LR' in result['result']['result1']['result']
    assert 'NB' in result['result']['result2']['result']

def test_predict_together_empty_data(client, mock_predict_lr, mock_predict_nb):
    data = {'message': ''}
    response = client.post('/PA/get_result', data=data)
    assert response.status_code == 400
    result = json.loads(response.data)
    assert 'error' in result

def test_handle_error_404(client):
    response = client.get('/non-existent-route')
    assert response.status_code == 404
    assert b'You have reached the error 404 page' in response.data


def test_get_graph_data(client):
    with patch('app.open', mock_open(read_data='{"data": [1, 2, 3]}')) as mock_file:
        response = client.get('/getPAData')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == {'data': [1, 2, 3]}


def test_get_wc_graph_data(client):
    with patch('app.open', mock_open(read_data='{"data": [1, 2, 3]}')) as mock_file:
        response = client.get('/getWCData')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == {'data': [1, 2, 3]}




