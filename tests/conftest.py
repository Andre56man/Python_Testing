import pytest
from server import app  # ton fichier principal

@pytest.fixture
def client():
    """Client Flask de test"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
