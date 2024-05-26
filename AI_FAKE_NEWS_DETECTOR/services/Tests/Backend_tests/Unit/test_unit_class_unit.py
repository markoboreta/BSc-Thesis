import pytest
import json
import importlib
from unittest.mock import patch, mock_open, Mock
from flask import Response, jsonify
import sys

# classes for unit testing the application, they will rotate
# more compact testing
app_classes = {
    "LRApp": "prediciton_services_LR.app",
    "NBApp": "prediction_services_NB.app",
    "PAApp": "prediction_services_PA.app"
}

# Test configurations for each of the apps
app_configs = {
    "LRApp": {
        "client_app": "app",
        "base_url": "/predict_LR",
        "patch_base": "prediciton_services_LR.LR.LR_model.predict_news_article",
        "patch_api_url_1": 'common.classes.class_service.service_api.PredictNB.post',
        "patch_api_url_2": 'common.classes.class_service.service_api.PredictPA.post',
        "home_page_url": "/LR_page",
        "result_key": "LR",
        "together_url": "/LR/get_result",
        "together_key": "NB",
        "wc_url": "/getWCData",
        "tf_url" : "/getTFData",
    },
    "NBApp": {
        "client_app": "app",
        "base_url": "/predict_NB",
        "patch_base": 'prediction_services_NB.NB.NB_model.predict_news_article',
        "patch_api_url_1": 'common.classes.class_service.service_api.PredictLR.post',
        "patch_api_url_2": 'common.classes.class_service.service_api.PredictPA.post',
        "home_page_url": "/NB_page",
        "result_key": "NB",
        "together_url": "/NB/get_result",
        "together_key": "LR",
        "wc_url": "/getWCData",
        "tf_url" : "/getNBData",
    },
    "PAApp": {
        "client_app": "app",
        "base_url": "/predict_PA",
        "patch_base": 'prediction_services_PA.PA.PA_Model.predict_news_article',
        "patch_api_url_1": 'common.classes.class_service.service_api.PredictLR.post',
        "patch_api_url_2": 'common.classes.class_service.service_api.PredictNB.post',
        "home_page_url": "/PA_page",
        "result_key": "PA",
        "together_url": "/PA/get_result",
        "together_key": "LR",
        "wc_url": "/getPAData",
        "tf_url" : "/getWCData",
    }
}

@pytest.fixture(scope="module", params=["LRApp", "NBApp", "PAApp"])
def my_client(request):
    app_class = importlib.import_module(app_classes[request.param])
    app = getattr(app_class, app_configs[request.param]['client_app'])
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    my_client = app.test_client()
    return my_client, app, app_configs[request.param]


def test_home_page(my_client):
    client_instance, app, config = my_client
    with patch('werkzeug.test.Client.open', return_value=Response(response="Homepage", status=200)):
        response = client_instance.get(config['home_page_url'])
        assert response.status_code == 200
        assert response.data.decode('utf-8') == "Homepage"

        
def test_get_graph_data(my_client):
    client_instance, app, config = my_client
    with patch('builtins.open', mock_open(read_data='{"data": [1, 2, 3]}')):
        response = client_instance.get(config['tf_url'])
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == {'data': [1, 2, 3]}

def test_predict_valid_input(my_client):
    client_instance, app, config = my_client
    with patch(config['patch_base'], return_value='Prediction'):
        response = client_instance.post(config['base_url'], data={'message': 'valid input'})
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['result'] == 'Prediction'

def test_predict_together_valid_input(my_client):
    client_instance, app, config = my_client
    with patch(config['patch_api_url_1'], return_value=({'result': 'LR result'}, 200)):
        with patch(config['patch_api_url_2'], return_value=({'result': 'NB result'}, 200)):
            response = client_instance.post(config['together_url'], data={'message': 'Some data'})
            assert response.status_code == 200
            result = json.loads(response.data)
            assert result['result'] == {'result1': {'result': 'LR result'}, 'result2': {'result': 'NB result'}}

def test_predict_no_input(my_client):
    client_instance, app, config = my_client
    with patch(config['patch_base'], return_value='No data provided'):
        response = client_instance.post(config['base_url'], data={'message': ''})
        assert response.status_code == 415
        result = json.loads(response.data)
        assert 'error' in result

def test_predict_invalid_method(my_client):
    client_instance, app, config = my_client
    with patch('werkzeug.test.Client.open', return_value=Mock(status_code=405, data=json.dumps({'error': 'Method Not Allowed'}))):
        response = client_instance.get(config['base_url'])
        assert response.status_code == 405
        result = json.loads(response.data)
        assert 'error' in result

def test_predict_exception_handling(my_client):
    client_instance, app, config = my_client
    with patch(config['patch_base'], side_effect=Exception('Test Error')):
        response = client_instance.post(config['base_url'], data={'message': 'valid input'})
        assert response.status_code == 500
        result = json.loads(response.data)
        assert 'error' in result

def test_file_not_found_error(my_client):
    client_instance, app, config = my_client
    with patch('builtins.open', mock_open()) as mocked_file:
        mocked_file.side_effect = FileNotFoundError
        response = client_instance.get(config['wc_url'])
        assert response.status_code == 404
        result = json.loads(response.data)
        assert 'error' in result

def test_json_decode_error(my_client):
    client_instance, app, config = my_client
    with patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "document", 0)):
        response = client_instance.get(config['tf_url'])
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result

def test_combined_results_error_handling(my_client):
    client_instance, app, config = my_client
    with app.app_context():
        with patch(config['patch_api_url_2'], return_value=(jsonify(error="Method failed"), 500)):
            response = client_instance.post(config['together_url'], data={'message': 'Some data'})
            assert response.status_code == 500
            result = json.loads(response.data)
