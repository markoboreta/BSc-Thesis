import unittest
from unittest.mock import patch, mock_open
from flask import jsonify
import json
from prediction_services_NB.app import NBApp#, base_dir, app # Ensure this imports correctly
import json
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) 
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, "static")

class TestNBApp(unittest.TestCase):
    def setUp(self):
        self.app = NBApp(__name__, template_dir, static_dir)
        self.app.testing = True
        self.client = self.app.test_client()

    def test_home_page(self):
        response = self.client.get('/NB_page')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Naive Bayes</title>', response.data)

    def test_get_graph_data(self):
        with patch('builtins.open', mock_open(read_data='{"data": [1, 2, 3]}')):
            response = self.client.get('/getNBData')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'data': [1, 2, 3]})

    def test_predict_NB_valid_input(self):
        with patch('prediction_services_NB.NB.NBModel.predict_news_article', return_value='Prediction'):
            response = self.client.post('/predict_NB', data={'message': 'valid input'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data)['result'], 'Prediction')
            
    def test_predict_together_valid_input(self):
        with patch('common.classes.class_service.service_api.PredictLR.post', return_value=({'result': 'LR result'}, 200)):
            with patch('common.classes.class_service.service_api.PredictPA.post', return_value=({'result': 'PA result'}, 200)):
                response = self.client.post('/NB/get_result', data={'message': 'Some data'})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json['result'], {'result1': {'result': 'LR result'}, 'result2': {'result': 'PA result'}})

    # Error handling tests
    def test_predict_NB_no_input(self):
        response = self.client.post('/predict_NB', data={'message': ''})
        self.assertEqual(response.status_code, 415)
        self.assertIn('Invalid input', response.json['error'])

    def test_predict_NB_invalid_method(self):
        response = self.client.get('/predict_NB')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'title>Error</title>', response.data)

    def test_predict_NB_exception_handling(self):
        with patch('prediction_services_NB.NB.NBModel.predict_news_article', side_effect=Exception('Test Error')):
            response = self.client.post('/predict_NB', data={'message': 'valid input'})
            self.assertEqual(response.status_code, 500)
            self.assertIn('Error occurred while processing data', response.json['error'])


    def test_file_not_found_error(self):
        with patch('builtins.open', mock_open()) as mocked_file:
            mocked_file.side_effect = FileNotFoundError
            response = self.client.get('/getWCData')
            self.assertEqual(response.status_code, 404)
            self.assertIn('File not found', response.json['error'])

    def test_json_decode_error(self):
        with patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "document", 0)):
            response = self.client.get('/getNBData')
            self.assertEqual(response.status_code, 404)
            self.assertIn('File not found', response.json['error'])

    def test_combined_results_error_handling(self):
        with self.app.app_context():  # Set up an application context
            with patch('common.classes.class_service.service_api.PredictLR.post',
                    return_value=(jsonify(error="NB failed"), 400)):
                response = self.client.post('/NB/get_result', data={'message': 'Some data'})
                self.assertEqual(response.status_code, 400)
                self.assertIn('NB failed', response.json['error'])
                
if __name__ == '__main__':
    unittest.main()
