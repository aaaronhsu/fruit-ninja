from connections import get_connection

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS games (
    id SERIAL PRIMARY KEY,
    game_type INT NOT NULL DEFAULT 0,
    points INT NOT NULL DEFAULT 0,
    lives INT NOT NULL DEFAULT 3,
    start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    game_length INT NOT NULL DEFAULT 60,
    player_name VARCHAR(255)
);
"""

conn = get_connection()

# ---------------------- CONFIG ----------------------
def init_game_table():
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_TABLE)

def reset_game_table():
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS games;")

# ---------------------- EVENT LOGIC ----------------------
def update_points(game_id, points):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE games
                SET points = points + %s
                WHERE id = %s;
            """, (points, game_id))

def update_lives(game_id, lives):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE games
                SET lives = lives + %s
                WHERE id = %s;
            """, (lives, game_id))

def end_game(game_id):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE games
                SET end_time = CURRENT_TIMESTAMP
                WHERE id = %s;
            """, (game_id,))


# ---------------------- GAME MANAGEMENT ----------------------
def fetch_current_game():
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM games WHERE end_time IS NULL ORDER BY id DESC;")
            return cursor.fetchone()

def start_game(lives, game_length):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO games (lives, game_length)
                VALUES (%s, %s)
                RETURNING id;
            """, (lives, game_length))
            return cursor.fetchone()

def log_game(game_id, player_name):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE games
                SET player_name = %s
                WHERE id = %s;
            """, (player_name, game_id))

def fetch_games():
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM games;")
            return cursor.fetchall()

def fetch_leaderboard():
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM games ORDER BY points DESC LIMIT 10;")
            return cursor.fetchall()
