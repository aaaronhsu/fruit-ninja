from flask import Flask, request
from dotenv import load_dotenv
from flask_cors import CORS
import os
import psycopg2

app = Flask(__name__)
CORS(app)  # This will allow all domains by default, you can specify origins

load_dotenv()

database_user = os.getenv("DB_USER")
database_password = os.getenv("DB_PASSWORD")
database_name = os.getenv("DB_NAME")

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

if __name__ == "__main__":
    app.run(port=8000)
