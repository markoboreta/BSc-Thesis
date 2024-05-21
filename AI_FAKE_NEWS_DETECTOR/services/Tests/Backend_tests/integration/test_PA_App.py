import unittest
from unittest.mock import patch, mock_open, MagicMock
from prediction_services_PA.app import PA_App

class TestPAApp(unittest.TestCase):
    def setUp(self):
        self.app = PA_App(__name__)
        self.app.testing = True
        self.client = self.app.test_client()

    def test_home_page(self):
        response = self.client.get('/PA_page')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Passive Agressive Classifier</h1>', response.data)

    def test_predict_PA(self):
        with patch('PA.PAModel.predict_news_article') as mock_predict:
            mock_predict.return_value = 'Predicted result'
            response = self.client.post('/predict_PA', data=dict(message='Some news article content'))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'result': 'Predicted result'})

    def test_get_graph_data(self):
        with patch('builtins.open', mock_open(read_data='{"data": [1, 2, 3]}')):
            response = self.client.get('/getPAData')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'data': [1, 2, 3]})

    def test_get_WC_data(self):
        with patch('builtins.open', mock_open(read_data='{"data": [4, 5, 6]}')):
            response = self.client.get('/getWCData')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'data': [4, 5, 6]})

    def test_predict_together(self):
        with patch('common.classes.class_service.service_api.PredictLR.post') as mock_predict_lr_post:
            with patch('common.classes.class_service.service_api.PredictNB.post') as mock_predict_nb_post:
                mock_predict_lr_post.return_value = ({'result': 'LR result'}, 200)
                mock_predict_nb_post.return_value = ({'result': 'NB result'}, 200)
                response = self.client.post('/PA/get_result', data=dict(message='Some text data'))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json, {
                    'result': {
                        'result1': {'result': 'LR result'},
                        'result2': {'result': 'NB result'}
                    }
                })

if __name__ == '__main__':
    unittest.main()
