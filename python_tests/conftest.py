import pytest
from database import db_connection


@pytest.fixture(scope="function")
def setup_database():
    with db_connection() as cursor:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS People (id SERIAL PRIMARY KEY, firstname VARCHAR(255), lastname VARCHAR(255), dateofbirth DATE);")
        yield cursor
        cursor.execute("DELETE FROM People;")


@pytest.fixture(scope="function")
def long_firstname():
    return "ИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИван"


@pytest.fixture(scope="function")
def long_lastname():
    return "Иванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИван"


@pytest.fixture(scope="function")
def test_data():
    return [
        ('Иван', 'Иванов-Сергеев', '2000-12-15'),
        (
            'ИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИва',
            'И', '2000-12-15'),
        ('И',
         'Иванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИва',
         '2000-12-15'),
    ]


@pytest.fixture
def insert_sample_person(setup_database):
    with db_connection() as cursor:
        cursor.execute(
            "INSERT INTO People (firstname, lastname, dateofbirth) VALUES ('Paul-Frank', 'John', '2000-12-15')")
        cursor.execute("SELECT * FROM People WHERE firstname = 'Paul-Frank' AND lastname = 'John'")
        return cursor.fetchall()


@pytest.fixture
def insert_multiple_persons(setup_database):
    with db_connection() as cursor:
        cursor.execute("""
            INSERT INTO People (firstname, lastname, dateofbirth) VALUES
                ('Paul-Frank', 'John', '2000-12-15'),
                ('Paul-Frank', 'John', '2000-12-15'),
                ('Paul-Frank', 'John', '2000-12-15')
            """)
        cursor.execute("SELECT * FROM People")
        return cursor.fetchall()
