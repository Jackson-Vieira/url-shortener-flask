import psycopg2

import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

SQL_CREATE_SHORT_URL_TABLE = """
    CREATE TABLE IF NOT EXISTS short_url (
        id SERIAL,
        longURL text NOT NULL,
        shortURL CHAR(7) NOT NULL UNIQUE,
        PRIMARY KEY (id)
    );
"""

def connect_to_db():
    return psycopg2.connect(DATABASE_URL)

def create_table(sql_create_table):
    with connect_to_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_create_table)
            conn.commit()

def perform_query(query, params=None):
    with connect_to_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)

            result = cursor.fetchone()
            return result[0] if result is not None else None

def perform_persist_query(query, params=None):
    with connect_to_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
        
if __name__ == "__main__":
    create_table(SQL_CREATE_SHORT_URL_TABLE)