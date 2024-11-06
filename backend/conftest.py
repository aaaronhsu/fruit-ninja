import pytest
from server import app
from dao import get_connection

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def db_connection():
    """Fixture to provide a database connection for testing."""
    conn = get_connection()
    yield conn
    conn.close()

@pytest.fixture
def init_games_table(client):
    """Fixture to initialize the games table before running tests."""
    client.post('/api/init_game_table')
