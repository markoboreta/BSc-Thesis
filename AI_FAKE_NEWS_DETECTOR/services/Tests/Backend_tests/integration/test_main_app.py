import unittest
from unittest.mock import patch, mock_open, MagicMock
from services.prediction_services_PA.app import PA_App
class TestLRApp(unittest.TestCase):
    def setUp(self):
        self.app = PA_App(__name__)
        self.app.testing = True
        self.client = self.app.test_client()

    def test_home_page(self):
        response = self.client.get('/LR_page')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Welcome</h1>', response.data)

if __name__ == '__main__':
    unittest.main()