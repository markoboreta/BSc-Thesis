import pytest
import json
from main_app.app import app as mainApp
from prediciton_services_LR.app import app as LRApp
from prediction_services_NB.app import app as NBApp
from prediction_services_PA.app import app as PAApp


# Application configurations
app_configs = {
    "mainApp":{
        "client_app": mainApp,
        "home_page_url": "/"
    },
    "LRApp": {
        "client_app": LRApp,
        "predict_url": "/predict_LR",
        "home_page_url": "/LR_page",
        "result_key": "LR",
        "together_url": "/LR/get_result",
        "together_key": "NB",
        "wc_url": "/getWCData",
        "tf_url": "/getTFData",
        "wc_data_keys": ["Fake", "Real"],
        "tf_data_keys": ["Fake", "Real"]
    },
    "NBApp": {
        "client_app": NBApp,
        "predict_url": "/predict_NB",
        "home_page_url": "/NB_page",
        "result_key": "NB",
        "together_url": "/NB/get_result",
        "together_key": "LR",
        "wc_url": "/getWCData",
        "tf_url": "/getNBData",
        "wc_data_keys": ["Fake", "Real"],
        "tf_data_keys": ["Fake", "Real"]
    },
    "PAApp": {
        "client_app": PAApp,
        "predict_url": "/predict_PA",
        "home_page_url": "/PA_page",
        "result_key": "PA",
        "together_url": "/PA/get_result",
        "together_key": "LR",
        "wc_url": "/getPAData",
        "tf_url": "/getWCData",
        "wc_data_keys": ["Fake", "Real"],
        "tf_data_keys": ["Fake", "Real"]
    }
}

# List of applications to be tested
app_param = [
    ("mainApp", mainApp, app_configs["mainApp"]),
    ("LRApp", LRApp, app_configs["LRApp"]),
    ("NBApp", NBApp, app_configs["NBApp"]),
    ("PAApp", PAApp, app_configs["PAApp"])
]


# test the page of the model
@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"]), (mainApp, app_configs["mainApp"])])
def test_home_page(app_instance, config):
    client = app_instance.test_client()
    response = client.get(config['home_page_url'])
    assert response.status_code == 200


@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"])])
def test_predict_valid_data(app_instance, config):
    client = app_instance.test_client()
    response = client.post(config["predict_url"], data={'message': 'Some news article content'})
    assert response.status_code == 200
    result = json.loads(response.data)
    assert config['result_key'] in result['result']

@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"])])
def test_predict_together_valid_data(app_instance, config):
    client = app_instance.test_client()
    data = {'message': 'Some news article content'}
    response = client.post(config['together_url'], data=data)
    assert response.status_code == 200
    result = json.loads(response.data)
    assert 'result' in result
    assert config['together_key'] in result['result']['result1']['result']

@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"])])
def test_predict_empty_data(app_instance, config):
    client = app_instance.test_client()
    response = client.post(config["predict_url"], data={'message': ''})
    assert response.status_code == 415
    result = json.loads(response.data)
    assert 'error' in result


@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"])])
def test_predict_wrong_method(app_instance, config):
    client = app_instance.test_client()
    response = client.get(config["predict_url"])
    assert response.status_code == 405
    result = json.loads(response.data)
    assert 'error' in result

@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"])])
def test_predict_wrong_method(app_instance, config):
    client = app_instance.test_client()
    data = {'message': ''}
    response = client.post(config['together_url'], data=data)
    assert response.status_code == 415
    result = json.loads(response.data)
    assert 'error' in result


@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"]), (mainApp, app_configs["mainApp"])])
def test_handle_error_404(app_instance, config):
    client = app_instance.test_client()
    response = client.get('/aaaaa')
    assert response.status_code == 404

@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"])])
def test_get_graph_data(app_instance, config):
    client = app_instance.test_client()
    response = client.get(config['tf_url'])
    assert response.status_code == 200
    data = json.loads(response.data)
    assert set(config['tf_data_keys']).issubset(data.keys())

@pytest.mark.parametrize("app_instance, config", [(LRApp, app_configs["LRApp"]), (NBApp, app_configs["NBApp"]), (PAApp, app_configs["PAApp"])])
def test_get_wc_data(app_instance, config):
    client = app_instance.test_client()
    response = client.get(config["wc_url"])
    assert response.status_code == 200
    data = json.loads(response.data)
    assert set(config['wc_data_keys']).issubset(data.keys())
