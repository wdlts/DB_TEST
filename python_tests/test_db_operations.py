import time

import psycopg2
import pytest

from database import db_connection
from t_data import t_data


class TestDatabaseOperations:
    # CRUD-тесты (валидные)

    # CREATE - добавление данных

    @pytest.mark.parametrize("firstname, lastname, dateofbirth", t_data())
    def test_create_valid_data(self, setup_database, firstname, lastname, dateofbirth):
        with db_connection() as cursor:
            cursor.execute("INSERT INTO People (firstname, lastname, dateofbirth) VALUES (%s, %s, %s)",
                           (firstname, lastname, dateofbirth))
            cursor.execute("SELECT * FROM People WHERE firstname = %s AND lastname = %s", (firstname, lastname))
            result = cursor.fetchone()

            assert result is not None
            assert result[1] == firstname
            assert result[2] == lastname
            assert result[3].strftime("%Y-%m-%d") == dateofbirth

    def test_create_several_valid_rows(self, setup_database):
        with db_connection() as cursor:
            cursor.execute("INSERT INTO People VALUES(DEFAULT, 'Иван', 'Иванов-Сергеев', '2000-12-15'),"
                           " (DEFAULT, 'Иван', 'Иванов-Сергеев', '2000-12-14'),"
                           " (DEFAULT, 'Иван', 'Иванов-Сергеев', '2000-12-13')")
            cursor.execute("SELECT * FROM People;")
            result = cursor.fetchall()

            assert result is not None
            assert len(result) == 3

    # READ - чтение данных

    def test_read_valid_data_one_row(self, insert_sample_person):
        result = insert_sample_person
        assert result is not None
        assert len(result) == 1
        assert result[0][1] == "Paul-Frank"
        assert result[0][2] == "John"
        assert result[0][3].strftime("%Y-%m-%d") == "2000-12-15"

    def test_read_valid_data_several_rows(self, insert_multiple_persons):
        result = insert_multiple_persons
        assert result is not None
        assert len(result) == 3
        for r in result:
            assert r[1] == "Paul-Frank"
            assert r[2] == "John"
            assert r[3].strftime("%Y-%m-%d") == "2000-12-15"

    # UPDATE - обновление данных

    def test_update_valid_data_one_row(self, insert_sample_person):
        with db_connection() as cursor:
            cursor.execute("UPDATE people SET firstname = 'Nikolai' WHERE firstname = 'Paul-Frank'")
            cursor.execute("SELECT * FROM People WHERE firstname = 'Nikolai' AND lastname = 'John';")
            result = cursor.fetchall()
            assert result is not None
            assert len(result) == 1
            assert result[0][1] == "Nikolai"

    def test_update_valid_data_several_rows(self, insert_multiple_persons):
        with db_connection() as cursor:
            result = insert_multiple_persons
            assert result is not None
            assert len(result) == 3
            for r in result:
                assert r[1] == "Paul-Frank"
                assert r[2] == "John"
                assert r[3].strftime("%Y-%m-%d") == "2000-12-15"

            cursor.execute("UPDATE people SET firstname = 'Nikolai' WHERE firstname = 'Paul-Frank'")
            cursor.execute("SELECT * FROM People WHERE firstname = 'Nikolai' AND lastname = 'John';")
            result2 = cursor.fetchall()
            for r2 in result2:
                assert r2[1] == "Nikolai"
                assert r2[2] == "John"
                assert r2[3].strftime("%Y-%m-%d") == "2000-12-15"

    # DELETE - удаление данных

    def test_delete_valid_data_one_row(self, insert_sample_person):
        with db_connection() as cursor:
            result = insert_sample_person
            assert result is not None
            assert len(result) == 1

            cursor.execute("DELETE FROM people WHERE firstname = 'Paul-Frank'")
            cursor.execute("SELECT * FROM People")
            result2 = cursor.fetchall()

            assert len(result2) == 0

    def test_delete_valid_data_several_rows(self, insert_multiple_persons):
        with db_connection() as cursor:
            result = insert_multiple_persons

            assert result is not None
            assert len(result) == 3
            for r in result:
                assert r[1] == "Paul-Frank"
                assert r[2] == "John"
                assert r[3].strftime("%Y-%m-%d") == "2000-12-15"

            cursor.execute("DELETE FROM people WHERE firstname = 'Paul-Frank'")
            cursor.execute("SELECT * FROM People")
            result2 = cursor.fetchall()

            assert len(result2) == 0

    # CRUD-тесты (невалидные)

    # CREATE - добавление невалидных данных

    def test_create_one_invalid_row_with_invalid_firstname_as_null(self, setup_database):
        with db_connection() as cursor:
            try:
                cursor.execute("INSERT INTO People VALUES(DEFAULT, NULL, 'Иванов-Сергеев', '2000-12-15')")
            except psycopg2.Error as e:
                assert e.pgcode == '23502'

    def test_create_one_invalid_row_with_invalid_firstname_as_empty_space(self, setup_database):
        with db_connection() as cursor:
            try:
                cursor.execute("INSERT INTO People VALUES(DEFAULT, "", 'Иванов-Сергеев', '2000-12-15')")
            except psycopg2.Error as e:
                assert e.pgcode == '42601'

    def test_create_one_invalid_row_with_invalid_long_firstname(self, setup_database, long_firstname):
        with db_connection() as cursor:
            try:
                cursor.execute(f"INSERT INTO People VALUES(DEFAULT, {long_firstname}, 'Иванов-Сергеев', '2000-12-15')")
            except psycopg2.Error as e:
                assert e.pgcode == '42703'

    def test_create_one_invalid_row_with_invalid_lastname_as_null(self, setup_database):
        with db_connection() as cursor:
            try:
                cursor.execute("INSERT INTO People VALUES(DEFAULT, 'Иван', NULL, '2000-12-15')")
            except psycopg2.Error as e:
                assert e.pgcode == '23502'

    def test_create_one_invalid_row_with_invalid_lastname_as_empty_space(self, setup_database):
        with db_connection() as cursor:
            try:
                cursor.execute("INSERT INTO People VALUES(DEFAULT, 'Иван', "", '2000-12-15')")
            except psycopg2.Error as e:
                assert e.pgcode == '42601'

    def test_create_one_invalid_row_with_invalid_long_lastname(self, setup_database, long_lastname):
        with db_connection() as cursor:
            try:
                cursor.execute(f"INSERT INTO People VALUES(DEFAULT, 'Иван', {long_lastname}, '2000-12-15')")
            except psycopg2.Error as e:
                assert e.pgcode == '42703'

    def test_create_one_invalid_row_with_invalid_date_as_null(self, setup_database):
        with db_connection() as cursor:
            try:
                cursor.execute("INSERT INTO People VALUES(DEFAULT, 'Nikolai', 'Ivanov', NULL)")
            except psycopg2.Error as e:
                assert e.pgcode == '23502'

    def test_create_one_invalid_row_with_invalid_date_in_future(self, setup_database):
        with db_connection() as cursor:
            try:
                cursor.execute("INSERT INTO People VALUES(DEFAULT, 'Nikolai', 'Ivanov', '2026-12-12')")
            except psycopg2.Error as e:
                assert e.pgcode == '23514'

    def test_create_one_invalid_row_with_invalid_date_as_integer(self, setup_database):
        with db_connection() as cursor:
            try:
                cursor.execute("INSERT INTO People VALUES(DEFAULT, 'Nikolai', 'Ivanov', 2026-12-12)")
            except psycopg2.Error as e:
                assert e.pgcode == '42804'

    def test_create_one_invalid_row_with_invalid_nonexistent_date(self, setup_database):
        with db_connection() as cursor:
            try:
                cursor.execute("INSERT INTO People VALUES(DEFAULT, 'Nikolai', 'Ivanov', 2022-02-30)")
            except psycopg2.Error as e:
                assert e.pgcode == '42804'

    def test_create_one_invalid_row_with_invalid_nonexistent_index(self, setup_database):
        with db_connection() as cursor:
            cursor.execute("INSERT INTO People "
                           "VALUES (DEFAULT, 'Алексей', 'Иванов-Сергеев', '2000-12-15')",
                           )
            cursor.execute("SELECT * FROM People WHERE firstname = 'Алексей' AND lastname = 'Иванов-Сергеев'")
            result = cursor.fetchall()

            assert result is not None
            assert len(result) == 1
            assert result[0][1] == "Алексей"
            assert result[0][2] == "Иванов-Сергеев"
            assert result[0][3].strftime("%Y-%m-%d") == "2000-12-15"

            try:
                cursor.execute(f"INSERT INTO People VALUES({result[0][0] + 1}, 'Иван', 'Иванов', '2022-01-01')")
            except psycopg2.Error as e:
                assert e.pgcode == '42601'

    # READ - чтение невалидных данных

    def test_read_nonexistent_firstname(self, insert_sample_person):
        with db_connection() as cursor:
            cursor.execute("SELECT * FROM People WHERE firstname = 'Иван'")
            result = cursor.fetchall()
            assert result == []
            assert len(result) == 0

    def test_read_nonexistent_lastname(self, insert_sample_person):
        with db_connection() as cursor:
            cursor.execute("SELECT * FROM People WHERE lastname = 'Иван'")
            result = cursor.fetchall()
            assert result == []
            assert len(result) == 0

    def test_read_date_as_string(self, insert_sample_person):
        with db_connection() as cursor:
            try:
                cursor.execute("SELECT * FROM People WHERE dateofbirth = 'Иван'")
            except psycopg2.Error as e:
                assert e.pgcode == '22007'

    def test_read_nonexistent_index(self, setup_database):
        with db_connection() as cursor:
            cursor.execute("INSERT INTO People "
                           "VALUES (999999, 'Paul-Frank', 'John', '2000-12-15')",
                           )
            try:
                cursor.execute("SELECT * FROM People WHERE index = 999999")
            except psycopg2.Error as e:
                assert e.pgcode == '22007'

    # UPDATE - обновление невалидных данных

    def test_update_nonexistent_firstname(self, insert_sample_person):
        with db_connection() as cursor:
            result = insert_sample_person
            assert result is not None
            assert len(result) == 1
            assert result[0][1] == "Paul-Frank"
            assert result[0][2] == "John"
            assert result[0][3].strftime("%Y-%m-%d") == "2000-12-15"

            cursor.execute("UPDATE people SET firstname = 'Nikolai' WHERE firstname = 'Иван'")
            cursor.execute("SELECT * FROM People WHERE firstname = 'Иван' AND lastname = 'John';")
            result2 = cursor.fetchall()

            assert len(result2) == 0
            assert result2 == []

    def test_update_nonexistent_lastname(self, insert_sample_person):
        with db_connection() as cursor:
            result = insert_sample_person

            assert result is not None
            assert len(result) == 1
            assert result[0][1] == "Paul-Frank"
            assert result[0][2] == "John"
            assert result[0][3].strftime("%Y-%m-%d") == "2000-12-15"

            cursor.execute("UPDATE people SET lastname = 'Nikolai' WHERE lastname = 'Иван'")
            cursor.execute("SELECT * FROM People WHERE lastname = 'Nikolai' AND firstname = 'Алексей';")
            result2 = cursor.fetchall()

            assert len(result2) == 0
            assert result2 == []

    def test_update_by_nonexistent_date(self, insert_sample_person):
        with db_connection() as cursor:
            result = insert_sample_person

            assert result is not None
            assert len(result) == 1
            assert result[0][1] == "Paul-Frank"
            assert result[0][2] == "John"
            assert result[0][3].strftime("%Y-%m-%d") == "2000-12-15"

            cursor.execute("UPDATE people SET lastname = 'Nikolai' WHERE dateofbirth = '2011-12-15'")
            cursor.execute("SELECT * FROM People WHERE lastname = 'Nikolai' AND firstname = 'Алексей';")
            result2 = cursor.fetchall()

            assert len(result2) == 0
            assert result2 == []

    def test_update_by_nonexistent_index(self, insert_sample_person):
        with db_connection() as cursor:
            result = insert_sample_person

            assert result is not None
            assert len(result) == 1
            assert result[0][1] == "Paul-Frank"
            assert result[0][2] == "John"
            assert result[0][3].strftime("%Y-%m-%d") == "2000-12-15"

            cursor.execute("UPDATE people SET lastname = 'Nikolai' WHERE index = 99999999")
            cursor.execute("SELECT * FROM People WHERE lastname = 'Nikolai' AND firstname = 'Алексей';")
            result2 = cursor.fetchall()

            assert len(result2) == 0
            assert result2 == []

    #DELETE - удаление невалидных данных

    def test_delete_by_nonexistent_date(self, insert_sample_person):
        with db_connection() as cursor:
            result = insert_sample_person

            assert result is not None
            assert len(result) == 1
            assert result[0][1] == "Paul-Frank"
            assert result[0][2] == "John"
            assert result[0][3].strftime("%Y-%m-%d") == "2000-12-15"

            cursor.execute("DELETE FROM people WHERE dateofbirth = '2011-12-15'")
            cursor.execute("SELECT * FROM People WHERE lastname = 'John' AND firstname = 'Paul-Frank';")
            result2 = cursor.fetchall()

            assert len(result2) == 1
            assert result2[0][1] == "Paul-Frank"
            assert result2[0][2] == "John"
            assert result2[0][3].strftime("%Y-%m-%d") == "2000-12-15"

    def test_delete_by_nonexistent_firstname(self, insert_sample_person):
        with db_connection() as cursor:
            result = insert_sample_person

            assert result is not None
            assert len(result) == 1
            assert result[0][1] == "Paul-Frank"
            assert result[0][2] == "John"
            assert result[0][3].strftime("%Y-%m-%d") == "2000-12-15"

            cursor.execute("DELETE FROM people WHERE firstname = 'Arnold'")
            cursor.execute("SELECT * FROM People WHERE lastname = 'John' AND firstname = 'Paul-Frank';")
            result2 = cursor.fetchall()

            assert len(result2) == 1
            assert result2[0][1] == "Paul-Frank"
            assert result2[0][2] == "John"
            assert result2[0][3].strftime("%Y-%m-%d") == "2000-12-15"

    def test_delete_by_nonexistent_lastname(self, insert_sample_person):
        with db_connection() as cursor:
            result = insert_sample_person

            assert result is not None
            assert len(result) == 1
            assert result[0][1] == "Paul-Frank"
            assert result[0][2] == "John"
            assert result[0][3].strftime("%Y-%m-%d") == "2000-12-15"

            cursor.execute("DELETE FROM people WHERE lastname = 'Arnold'")
            cursor.execute("SELECT * FROM People WHERE lastname = 'John' AND firstname = 'Paul-Frank';")
            result2 = cursor.fetchall()

            assert len(result2) == 1
            assert result2[0][1] == "Paul-Frank"
            assert result2[0][2] == "John"
            assert result2[0][3].strftime("%Y-%m-%d") == "2000-12-15"

    def test_delete_by_nonexistent_index(self, insert_sample_person):
        with db_connection() as cursor:
            result = insert_sample_person

            assert result is not None
            assert len(result) == 1
            assert result[0][1] == "Paul-Frank"
            assert result[0][2] == "John"
            assert result[0][3].strftime("%Y-%m-%d") == "2000-12-15"

            cursor.execute("DELETE FROM people WHERE index = 99999898")
            cursor.execute("SELECT * FROM People WHERE lastname = 'John' AND firstname = 'Paul-Frank';")
            result2 = cursor.fetchall()

            assert len(result2) == 1
            assert result2[0][1] == "Paul-Frank"
            assert result2[0][2] == "John"
            assert result2[0][3].strftime("%Y-%m-%d") == "2000-12-15"

    # PERFORMANCE TESTS

    def test_create_read_many_rows_500000(self, setup_database):
        with db_connection() as cursor:
            start_create = time.time()
            cursor.execute(
                "do $$ begin for i in 1..500000 loop insert into people (firstname, lastname, dateofbirth) values ('Имя' || i, 'Фамилия' || i, '2021-01-01'); end loop; end; $$;")
            end_create = time.time()
            start_read = time.time()
            cursor.execute("SELECT * FROM People;")
            end_read = time.time()
            result = cursor.fetchall()

            assert result is not None
            assert len(result) == 500000
            assert end_create - start_create < 60
            assert end_read - start_read < 60

    def test_update_many_rows_500000(self, setup_database):
        with db_connection() as cursor:
            cursor.execute(
                "do $$ begin for i in 1..500000 loop insert into people (firstname, lastname, dateofbirth) values ('Имя' || i, 'Фамилия' || i, '2021-01-01'); end loop; end; $$;")
            cursor.execute("SELECT * FROM People;")
            result = cursor.fetchall()

            assert result is not None
            assert len(result) == 500000

            start_update = time.time()
            cursor.execute("UPDATE people SET lastname = 'Nikolai' where firstname LIKE 'Имя%';")
            end_update = time.time()
            cursor.execute("SELECT * FROM people where lastname = 'Nikolai';")
            result2 = cursor.fetchall()

            assert result2 is not None
            assert len(result2) == 500000
            assert end_update - start_update < 60

    def test_delete_many_rows_500000(self, setup_database):
        with db_connection() as cursor:
            cursor.execute(
                "do $$ begin for i in 1..500000 loop insert into people (firstname, lastname, dateofbirth) values ('Имя' || i, 'Фамилия' || i, '2021-01-01'); end loop; end; $$;")
            cursor.execute("SELECT * FROM People;")
            result = cursor.fetchall()

            assert result is not None
            assert len(result) == 500000

            start_delete = time.time()
            cursor.execute("DELETE FROM people where firstname LIKE 'Имя%';")
            end_delete = time.time()
            cursor.execute("SELECT * FROM people where firstname LIKE 'Имя%';")
            result2 = cursor.fetchall()

            assert result2 is not None
            assert len(result2) == 0
            assert end_delete - start_delete < 60
