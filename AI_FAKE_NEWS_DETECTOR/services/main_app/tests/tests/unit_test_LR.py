import unittest
from unittest.mock import patch, mock_open
from flask import jsonify
import json
from main_app.app import base_dir, mainPage # Ensure this imports correctly
import json
import os

#base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) 
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, "static")

class TestMainApp(unittest.TestCase):
    def setUp(self):
        self.app = mainPage(__name__, template_dir, static_dir)
        self.app.testing = True
        self.client = self.app.test_client()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Fake News Detector</title>', response.data)

   

if __name__ == '__main__':
    unittest.main()
