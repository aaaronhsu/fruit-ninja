import requests
import json
from datetime import datetime

from game_metadata import GameMetadata


def post_events(game_id: int, events: list):
    # Transform the events list into the expected payload format
    payload = {
        "events": [
            {
                "type": event.type,
                "game_id": game_id,
                "timestamp": datetime.fromtimestamp(event.timestamp).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "metadata": event.metadata
            }
            for event in events
        ]
    }

    # Make the POST request to the events endpoint
    try:
        response = requests.post(
            "http://ec2-34-195-221-35.compute-1.amazonaws.com/api/events",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        # Raise an exception for bad status codes
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        raise Exception(f"Failed to post events: {str(e)}")


def fetch_current_game() -> GameMetadata | None:
    # get and build current game info using the GET /api/current_game endpoint
    try:
        # Make GET request to the current game endpoint
        response = requests.get(
            "http://ec2-34-195-221-35.compute-1.amazonaws.com/api/current_game"
        )
        if response.status_code == 404:
            return None

        # Parse the response
        data = response.json()
        game_data = data["game"]

        # Extract values from the game data array
        game_id = game_data[0]
        game_type = game_data[1]
        num_lives = game_data[3]
        game_length = game_data[6]

        # Create and return a new GameMetadata instance
        return GameMetadata(
            game_id=game_id,
            num_lives=num_lives,
            total_game_length=game_length,
            game_type=game_type
        )

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch current game: {str(e)}")
    except (KeyError, IndexError) as e:
        raise Exception(f"Invalid game data format: {str(e)}")


def end_current_game(game_state: GameMetadata) -> None:
    # make end game request using the POST /api/end_game endpoint
    payload = {
        "game_id": game_state.game_id
    }

    try:
        # Make POST request to end game endpoint
        response = requests.post(
            "http://ec2-34-195-221-35.compute-1.amazonaws.com/api/end_game",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        # Raise an exception for bad status codes
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to end game: {str(e)}")
