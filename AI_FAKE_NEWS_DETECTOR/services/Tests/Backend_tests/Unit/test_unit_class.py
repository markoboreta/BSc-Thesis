import pytest
import json
import importlib
from unittest.mock import patch, mock_open
from flask import jsonify
import sys


app_modules = {
    "LRApp": "prediciton_services_LR.app",
    "NBApp": "prediction_services_NB.app",
    "PAApp": "prediction_services_PA.app"
}

# Test configurations for each app
app_configs = {
    "LRApp": {
        "client_function": "app",
        "base_url": "/predict_LR",
        "home_page_url": "/LR_page",
        "result_key": "LR",
        "together_url": "/LR/get_result",
        "together_key": "NB",
        "wc_url": "/getWCData",
        "tf_url" : "/getTFData",
        "wc_data_keys": ["Fake", "Real"],
        "tf_data_keys": ["Fake", "Real"]
    },
    "NBApp": {
        "client_function": "app",
        "base_url": "/predict_NB",
        "home_page_url": "/NB_page",
        "result_key": "NB",
        "together_url": "/NB/get_result",
        "together_key": "LR",
        "wc_url": "/getWCData",
        "tf_url" : "/getNBData",
        "wc_data_keys": ["Fake", "Real"],
        "tf_data_keys": ["Fake", "Real"]
    },
    "PAApp": {
        "client_function": "app",
        "base_url": "/predict_PA",
        "home_page_url": "/PA_page",
        "result_key": "PA",
        "together_url": "/PA/get_result",
        "together_key": "LR",
        "wc_url": "/getPAData",
        "tf_url" : "/getWCData",
        "wc_data_keys": ["Fake", "Real"],
        "tf_data_keys": ["Fake", "Real"]
    }
}

@pytest.fixture(scope="module", params=["LRApp", "NBApp", "PAApp"])
def client(request):
    app_module = importlib.import_module(app_modules[request.param])
    app = getattr(app_module, app_configs[request.param]['client_function'])
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    client = app.test_client()
    return client, app_configs[request.param]

def test_home_page(client):
    client_instance, config = client
    response = client_instance.get(config['home_page_url'])
    assert response.status_code == 200

def test_get_graph_data(client):
    client_instance, config = client
    with patch('builtins.open', mock_open(read_data='{"data": [1, 2, 3]}')):
        response = client_instance.get(config['tf_url'])
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == {'data': [1, 2, 3]}

def test_predict_valid_input(client):
    client_instance, config = client
    with patch(f'{app_modules[config["client_function"].split(".")[-2]]}.{config["client_function"].split(".")[-1]}.Model.predict_news_article', return_value='Prediction'):
        response = client_instance.post(config['base_url'], data={'message': 'valid input'})
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['result'] == 'Prediction'

def test_predict_together_valid_input(client):
    client_instance, config = client
    with patch('common.classes.class_service.service_api.PredictLR.post', return_value=({'result': 'LR result'}, 200)):
        with patch('common.classes.class_service.service_api.PredictNB.post', return_value=({'result': 'NB result'}, 200)):
            response = client_instance.post(config['together_url'], data={'message': 'Some data'})
            assert response.status_code == 200
            result = json.loads(response.data)
            assert result['result'] == {'result1': {'result': 'LR result'}, 'result2': {'result': 'NB result'}}

def test_predict_no_input(client):
    client_instance, config = client
    response = client_instance.post(config['base_url'], data={'message': ''})
    assert response.status_code == 415
    result = json.loads(response.data)
    assert 'error' in result

def test_predict_invalid_method(client):
    client_instance, config = client
    response = client_instance.get(config['base_url'])
    assert response.status_code == 405

def test_predict_exception_handling(client):
    client_instance, config = client
    with patch(f'{app_modules[config["client_function"].split(".")[-2]]}.{config["client_function"].split(".")[-1]}.Model.predict_news_article', side_effect=Exception('Test Error')):
        response = client_instance.post(config['base_url'], data={'message': 'valid input'})
        assert response.status_code == 500
        result = json.loads(response.data)
        assert 'error' in result

def test_file_not_found_error(client):
    client_instance, config = client
    with patch('builtins.open', mock_open()) as mocked_file:
        mocked_file.side_effect = FileNotFoundError
        response = client_instance.get(config['wc_url'])
        assert response.status_code == 404
        result = json.loads(response.data)
        assert 'error' in result

def test_json_decode_error(client):
    client_instance, config = client
    with patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "document", 0)):
        response = client_instance.get(config['tf_url'])
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result

def test_combined_results_error_handling(client):
    client_instance, config = client
    with patch('common.classes.class_service.service_api.PredictNB.post', return_value=(jsonify(error="NB failed"), 400)):
        response = client_instance.post(config['together_url'], data={'message': 'Some data'})
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
