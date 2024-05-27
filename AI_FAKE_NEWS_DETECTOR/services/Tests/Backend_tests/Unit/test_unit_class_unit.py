import pytest
import json
from unittest.mock import patch, mock_open, Mock
from flask import Response, jsonify

# Importing Flask app instances directly
from main_app.app import app as mainApp
from prediciton_services_LR.app import app as LRApp
from prediction_services_NB.app import app as NBApp
from prediction_services_PA.app import app as PAApp

# mock setup for testing pytest and unittest combination


app_configs = {
    "mainApp":{
        "client_app": mainApp,
        "home_page_url": "/"
    },
    "LRApp": {
        "client_app": LRApp,
        "base_url": "/predict_LR",
        "patch_base": "prediciton_services_LR.LR.LR_model.predict_news_article",
        "patch_api_url_1": 'common.classes.class_service.service_api.PredictNB.post',
        "patch_api_url_2": 'common.classes.class_service.service_api.PredictPA.post',
        "home_page_url": "/LR_page",
        "result_key": "LR",
        "together_url": "/LR/get_result",
        "together_key": "NB",
        "wc_url": "/getWCData",
        "tf_url": "/getTFData",
    },
    "NBApp": {
        "client_app": NBApp,
        "base_url": "/predict_NB",
        "patch_base": 'prediction_services_NB.NB.NB_model.predict_news_article',
        "patch_api_url_1": 'common.classes.class_service.service_api.PredictLR.post',
        "patch_api_url_2": 'common.classes.class_service.service_api.PredictPA.post',
        "home_page_url": "/NB_page",
        "result_key": "NB",
        "together_url": "/NB/get_result",
        "together_key": "LR",
        "wc_url": "/getWCData",
        "tf_url": "/getNBData",
    },
    "PAApp": {
        "client_app": PAApp,
        "base_url": "/predict_PA",
        "patch_base": 'prediction_services_PA.PA.PA_Model.predict_news_article',
        "patch_api_url_1": 'common.classes.class_service.service_api.PredictLR.post',
        "patch_api_url_2": 'common.classes.class_service.service_api.PredictNB.post',
        "home_page_url": "/PA_page",
        "result_key": "PA",
        "together_url": "/PA/get_result",
        "together_key": "LR",
        "wc_url": "/getPAData",
        "tf_url": "/getWCData",
    }
}

app_param = [
    ("LRApp", LRApp, app_configs["LRApp"]),
    ("NBApp", NBApp, app_configs["NBApp"]),
    ("PAApp", PAApp, app_configs["PAApp"])
]


# test the page of the model
@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"]), (mainApp, app_configs["mainApp"])])
def test_home_page(app_instance, config):
    with patch('werkzeug.test.Client.open', return_value=Response(response="Homepage", status=200)):
        client = app_instance.test_client()
        response = client.get(config['home_page_url'])
        assert response.status_code == 200
        assert response.data.decode('utf-8') == "Homepage"

# error of the model page
@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"]), (mainApp, app_configs["mainApp"])])
def test_home_page(app_instance, config):
    with patch('werkzeug.test.Client.open', return_value=Mock(status_code=404, data=json.dumps({'error': 'Page not found'}))):
        client = app_instance.test_client()
        response = client.get('/aaaaaaa')
        assert response.status_code == 404

# retrieve JSON data
@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"])])
def test_get_graph_data(app_instance, config):
    client = app_instance.test_client()
    with patch('builtins.open', mock_open(read_data='{"data": [1, 2, 3]}')):
        response = client.get(config['tf_url'])
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == {'data': [1, 2, 3]}


# correct prediction
@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"])])
def test_predict_valid_input(app_instance, config):
    client = app_instance.test_client()
    with patch(config['patch_base'], return_value='Prediction'):
        response = client.post(config['base_url'], data={'message': 'valid input'})
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['result'] == 'Prediction'


# predcition for the API communication test
@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"])])
def test_predict_together_valid_input(app_instance, config):
    client = app_instance.test_client()
    with patch(config['patch_api_url_1'], return_value=({'result': 'LR result'}, 200)):
        with patch(config['patch_api_url_2'], return_value=({'result': 'NB result'}, 200)):
            response = client.post(config['together_url'], data={'message': 'Some data'})
            assert response.status_code == 200
            result = json.loads(response.data)
            assert result['result'] == {'result1': {'result': 'LR result'}, 'result2': {'result': 'NB result'}}

# empty article error test
@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"])])
def test_predict_no_input(app_instance, config):
    client = app_instance.test_client()
    with patch(config['patch_base'], return_value='No data provided'):
        response = client.post(config['base_url'], data={'message': ''})
        assert response.status_code == 415
        result = json.loads(response.data)
        assert 'error' in result

# incorrect method, non post test 
@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"])])
def test_predict_invalid_method(app_instance, config):
    client = app_instance.test_client()
    with patch('werkzeug.test.Client.open', return_value=Mock(status_code=405, data=json.dumps({'error': 'Method Not Allowed'}))):
        response = client.get(config['base_url'])
        assert response.status_code == 405
        result = json.loads(response.data)
        assert 'error' in result

# random error on the model side, returns 500
@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"])])
def test_predict_exception_handling(app_instance, config):
    client = app_instance.test_client()
    with patch(config['patch_base'], side_effect=Exception('Test Error')):
        response = client.post(config['base_url'], data={'message': 'valid input'})
        assert response.status_code == 500
        result = json.loads(response.data)
        assert 'error' in result

# JSON file not existant
@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"])])
def test_file_not_found_error(app_instance, config):
    client = app_instance.test_client()
    with patch('builtins.open', mock_open()) as mocked_file:
        mocked_file.side_effect = FileNotFoundError
        response = client.get(config['wc_url'])
        assert response.status_code == 404
        result = json.loads(response.data)
        assert 'error' in result

# incorrect file
@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"])])
def test_json_decode_error(app_instance, config):
    client = app_instance.test_client()
    with patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "document", 0)):
        response = client.get(config['tf_url'])
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result


@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"])])
def test_combined_results_error_handling(app_instance, config):
    client = app_instance.test_client()
    with app_instance.app_context():
        with patch(config['patch_api_url_2'], return_value=(jsonify(error="Method failed"), 500)):
            response = client.post(config['together_url'], data={'message': 'Some data'})
            assert response.status_code == 500
            result = json.loads(response.data)
            assert 'error' in result
