import pytest
from unittest.mock import patch, mock_open
from services.prediction_services_PA.app import PA_App

@pytest.fixture
def client():
    app = PA_App(__name__)
    app.testing = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/LR_page')
    assert response.status_code == 200
    assert b'<h1>Passive Agressive Classifier</h1>' in response.data

def test_predict_LR(client):
    with patch('LR.LRModel.predict_news_article') as mock_predict:
        mock_predict.return_value = 'Predicted result'
        response = client.post('/predict_LR', data=dict(message='Some news article content'))
        assert response.status_code == 200
        assert response.json == {'result': 'Predicted result'}

def test_get_graph_data(client):
    with patch('builtins.open', mock_open(read_data='{"data": [1, 2, 3]}')):
        response = client.get('/getTFData')
        assert response.status_code == 200
        assert response.json == {'data': [1, 2, 3]}

def test_get_WC_data(client):
    with patch('builtins.open', mock_open(read_data='{"data": [4, 5, 6]}')):
        response = client.get('/getWCData')
        assert response.status_code == 200
        assert response.json == {'data': [4, 5, 6]}

def test_predict_together(client):
    with patch('common.classes.class_service.service_api.PredictLR.post') as mock_predict_lr_post, \
         patch('common.classes.class_service.service_api.PredictNB.post') as mock_predict_nb_post:
        mock_predict_lr_post.return_value = ({'result': 'NB result'}, 200)
        mock_predict_nb_post.return_value = ({'result': 'PA result'}, 200)
        response = client.post('/LR/get_result', data=dict(message='Some text data'))
        assert response.status_code == 200
        assert response.json == {
            'result': {
                'result1': {'result': 'NB result'},
                'result2': {'result': 'PA result'}
            }
        }
