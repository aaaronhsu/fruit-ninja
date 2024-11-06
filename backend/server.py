import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from enums import GameEvent
import dao

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def hello_world():
    return "<p>Fruit Ninja!</p>"

@app.post("/api/init_game_table")
def init_tables():
    dao.init_game_table()
    return {"message": "Table Created."}, 201

@app.post("/api/reset_game_table")
def reset_tables():
    dao.reset_game_table()
    return {"message": "Game table dropped."}, 201

@app.post("/api/events")
def game_events():
    data = request.get_json()

    # validate payload
    if not data or 'events' not in data:
        return jsonify({"error": "Invalid input, 'events' key is missing"}), 400

    events = data['events']
    parsed_events = []

    for event in events:
        if 'type' in event and 'game_id' in event and 'timestamp' in event:
            new_event = {
                "type": event['type'],
                "game_id": event['game_id'],
                "timestamp": event['timestamp'],
                "metadata": event.get('metadata', {})
            }

            # process event based on type
            match event['type']:
                case GameEvent.FRUIT_SLICED:
                    dao.update_points(event['game_id'], event['metadata']['points'])
                case GameEvent.BOMB_SLICED:
                    dao.update_lives(event['game_id'], -event['metadata']['damage'])
                case GameEvent.GAME_END:
                    dao.end_game(event['game_id'])

            socketio.emit("game_event", new_event)
            parsed_events.append(new_event)
        else:
            return jsonify({"error": "Invalid event format"}), 400

    return jsonify({"parsed_events": parsed_events}), 200

@app.get("/api/current_game")
def fetch_current_game():
    game = dao.fetch_current_game()
    if game is None:
        return jsonify({"message": "No active games"}), 404
    return jsonify({"game": game}), 200

@app.post("/api/start_game")
def start_game():
    data = request.get_json()
    lives = data.get('lives', 3)
    game_length = data.get('game_length', 60)

    new_game = dao.start_game(lives, game_length)
    if new_game is None:
        return jsonify({"message": "Failed to start game"}), 500

    return jsonify({"message": "Game started", "game_data": new_game}), 201

@app.post("/api/end_game")
def end_game():
    data = request.get_json()
    game_id = data.get('game_id', None)

    if game_id is None:
        dao.end_game(game_id)
        return jsonify({"message": "All games ended"}), 200

    dao.end_game(game_id)
    return jsonify({"message": f"Game {game_id} ended"}), 200

@app.post("/api/log_game")
def log_game():
    data = request.get_json()
    game_id = data.get('game_id', None)
    player_name = data.get('player_name', None)

    if game_id is None:
        return jsonify({"message": "Game ID not provided"}), 400
    elif player_name is None:
        return jsonify({"message": "Player name not provided"}), 400

    dao.log_game(game_id, player_name)
    return jsonify({"message": f"Game {game_id} logged with user {player_name}"}), 200

@app.get("/api/games")
def fetch_games():
    games = dao.fetch_games()
    if not games:
        return jsonify({"message": "No games found"}), 404
    return jsonify({"games": games}), 200

@app.get("/api/leaderboard")
def fetch_leaderboard():
    leaderboard = dao.fetch_leaderboard()
    if not leaderboard:
        return jsonify({"message": "No games found"}), 404
    return jsonify({"leaderboard": leaderboard}), 200

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8000)
