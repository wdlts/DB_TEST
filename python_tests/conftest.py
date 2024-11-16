import pytest
import psycopg2
from psycopg2 import sql

import pytest
from database import db_connection


@pytest.fixture(scope="module")
def setup_database():
    with db_connection() as cursor:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS People (index SERIAL PRIMARY KEY, firstname VARCHAR(255), lastname VARCHAR(255), dateofbirth DATE);")
        yield cursor
        cursor.execute("DELETE FROM People;")
