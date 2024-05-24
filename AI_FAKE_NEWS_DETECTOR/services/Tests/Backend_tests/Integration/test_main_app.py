import pytest
import os
from main_app.app import MainPage, base_dir

@pytest.fixture(scope="module")
def main_page_client():
    app = MainPage(__name__, os.path.join(base_dir, 'templates'), os.path.join(base_dir, 'static'))
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    client = app.test_client()
    return client

def test_main_page_home(main_page_client):
    response = main_page_client.get("/")
    assert response.status_code == 200
    assert "Detector" in response.get_data(as_text=True)