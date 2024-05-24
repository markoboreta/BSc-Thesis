import pytest
from unittest.mock import patch
from flask import Response
import os
from main_app.app import MainPage, base_dir


@pytest.fixture(scope="module")
def main_page_client():
    app = MainPage(__name__, os.path.join(base_dir, 'templates'), os.path.join(base_dir, 'static'))
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    client = app.test_client()
    return client

def test_home_page(main_page_client):
    with patch('werkzeug.test.Client.open', return_value=Response(response="Homepage", status=200)):
        response = main_page_client.get('/')
        assert response.status_code == 200
        assert response.data.decode('utf-8') == "Homepage"
