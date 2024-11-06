import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
database_user = os.getenv("DB_USER")
database_password = os.getenv("DB_PASSWORD")
database_name = os.getenv("DB_NAME")

def get_connection():
    conn = psycopg2.connect(
        dbname=database_name,
        user=database_user,
        password=database_password,
        host='localhost'
    )
    return conn
