import pytest
import json
import importlib
import os
from mainApp.app import mainPage, base_dir

@pytest.fixture(scope="module")
def main_page_client():
    app = mainPage(__name__, os.path.join(base_dir, 'templates'), os.path.join(base_dir, 'static'))
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    client = app.test_client()
    return client

def test_main_page_home(main_page_client):
    """
    Test that the home page of the main app loads correctly.
    """
    response = main_page_client.get("/")
    assert response.status_code == 200
    assert "Detector" in response.get_data(as_text=True)