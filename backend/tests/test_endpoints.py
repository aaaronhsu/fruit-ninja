def test_hello_world(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Fruit Ninja!" in response.data

def test_init_game_table(client):
    response = client.post('/api/init_game_table')
    assert response.status_code == 201
    assert response.get_json() == {"message": "Table Created."}

def test_reset_game_table(client):
    response = client.post('/api/reset_game_table')
    assert response.status_code == 201
    assert response.get_json() == {"message": "Game table dropped."}

def test_game_events(client):
    # Test with valid event data
    valid_event_data = {
        "events": [
            {
                "type": "FRUIT_SLICED",
                "game_id": 1,
                "timestamp": "2024-11-06T03:39:30Z",
                "metadata": {"fruit": "apple"}
            },
            {
                "type": "BOMB_SLICED",
                "game_id": 1,
                "timestamp": "2024-11-06T03:40:00Z"
            }
        ]
    }
    response = client.post('/api/events', json=valid_event_data)
    assert response.status_code == 200
    parsed_events = response.get_json().get('parsed_events', [])
    assert len(parsed_events) == 2
    assert parsed_events[0]['type'] == "FRUIT_SLICED"
    assert parsed_events[1]['type'] == "BOMB_SLICED"

    # Test with invalid event data (missing 'events' key)
    invalid_event_data = {}
    response = client.post('/api/events', json=invalid_event_data)
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid input, 'events' key is missing"}

    # Test with invalid event format (missing required fields)
    invalid_event_format = {
        "events": [
            {
                "type": "FRUIT_SLICED",
                "timestamp": "2024-11-06T03:39:30Z"
            }
        ]
    }
    response = client.post('/api/events', json=invalid_event_format)
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid event format"}


def test_start_game(client, init_games_table):
    response = client.post('/api/start_game', json={'lives': 3, 'game_length': 60})
    assert response.status_code == 201
    assert "Game started" in response.get_json()['message']

def test_end_game(client, init_games_table):
    # Start a new game first
    client.post('/api/start_game', json={'lives': 3, 'game_length': 60})
    response = client.post('/api/end_game', json={'game_id': 1})
    assert response.status_code == 200
    assert "Game 1 ended" in response.get_json()['message']

def test_log_game(client, init_games_table):
    # Start a new game first
    client.post('/api/start_game', json={'lives': 3, 'game_length': 60})
    response = client.post('/api/log_game', json={'game_id': 1, 'player_name': 'Player1'})
    assert response.status_code == 200
    assert "Game 1 logged with user Player1" in response.get_json()['message']

def test_fetch_games(client, init_games_table):
    response = client.get('/api/games')
    assert response.status_code == 200
    # Check if the response contains game data (adjust the assertion as needed)

def test_fetch_leaderboard(client, init_games_table):
    response = client.get('/api/leaderboard')
    assert response.status_code == 200
    # Check if the response contains leaderboard data (adjust the assertion as needed)
