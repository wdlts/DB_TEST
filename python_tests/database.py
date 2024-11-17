import psycopg2
from contextlib import contextmanager


@contextmanager
def db_connection():
    conn = psycopg2.connect(dbname='test_db', user='test_user', password='password', host='127.0.0.1', port=5432)
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    finally:
        cursor.close()
        conn.close()
