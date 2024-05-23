import unittest
from unittest.mock import patch, mock_open
from flask import Flask, jsonify
import json
import os

class UnitClass(unittest.TestCase):
    def setUpApp(self, app_class, template_dir, static_dir):
        self.app = app_class(__name__, template_dir=template_dir, static_dir=static_dir)
        self.app.testing = True
        self.client = self.app.test_client()

    def test_home_page(self, endpoint, title):
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertIn(title, response.data)

    def test_predict_valid_input(self, predict_endpoint, predict_mock_path, input_data, mock_return, expected_result):
        with patch(predict_mock_path, return_value=mock_return):
            response = self.client.post(predict_endpoint, data={'message': input_data})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data)['result'], expected_result)

    def test_error_handling_no_input(self, predict_endpoint):
        response = self.client.post(predict_endpoint, data={'message': ''})
        self.assertEqual(response.status_code, 415)
        self.assertIn('Invalid input', response.json['error'])

    def test_error_handling_invalid_method(self, predict_endpoint):
        response = self.client.get(predict_endpoint)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'title>Error</title>', response.data)

    def test_exception_handling(self, predict_endpoint, predict_mock_path):
        with patch(predict_mock_path, side_effect=Exception('Test Error')):
            response = self.client.post(predict_endpoint, data={'message': 'valid input'})
            self.assertEqual(response.status_code, 500)
            self.assertIn('Error occurred while processing data', response.json['error'])

    def test_file_not_found_error(self, get_data_endpoint):
        with patch('builtins.open', mock_open()) as mocked_file:
            mocked_file.side_effect = FileNotFoundError
            response = self.client.get(get_data_endpoint)
            self.assertEqual(response.status_code, 404)
            self.assertIn('File not found', response.json['error'])

    def test_json_decode_error(self, get_data_endpoint):
        with patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "document", 0)):
            response = self.client.get(get_data_endpoint)
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid JSON', response.json['error'])