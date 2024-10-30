from flask import Flask, request
from dotenv import load_dotenv
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import psycopg2

app = Flask(__name__)
CORS(app)  # This will allow all domains by default, you can specify origins

load_dotenv()

database_user = os.getenv("DB_USER")
database_password = os.getenv("DB_PASSWORD")
database_name = os.getenv("DB_NAME")
secret_key = os.getenv("SECRET_KEY")

app.config['SECRET_KEY']

socketio = SocketIO(app, cors_allowed_origins="*")

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS test (
    id SERIAL PRIMARY KEY,
    points INT
);
"""

conn = psycopg2.connect(
    dbname=database_name,
    user=database_user,
    password=database_password,
    host='localhost'
)


@app.route("/")
def hello_world():
    return "<p>Fruit Ninja!</p>"

@app.post("/api/create_table")
def create_table():
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_TABLE)
    return {"message": "Table Created."}, 201

@app.post("/api/socket_test")
def socket_test():

    def get_points() -> int:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT points FROM test WHERE id = 0;")
                points = cursor.fetchone()
                if points is None:
                    cursor.execute("INSERT INTO test (points) VALUES (0);")
                    return 0
        return points[0]

    with conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE test SET points = points + 1 WHERE id = 0;")

    # emit the new point value using a socket
    new_points: int = get_points()
    socketio.emit("point_update", {"points": new_points})
    return {"message": f"There are now {new_points} points"}, 201

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8000)
