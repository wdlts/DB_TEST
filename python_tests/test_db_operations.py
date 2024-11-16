import psycopg2
import pytest
from database import db_connection


class TestDatabaseOperations:
    @pytest.mark.parametrize("firstname, lastname, dateofbirth", [
        ('Иван', 'Иванов-Сергеев', '2000-12-15'),
        (
        'ИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИванИван',
        'И', '2000-12-15'),
        ('И',
         'Иванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-СергеевИванов-Сергеев',
         '2000-12-15'),
    ])
    def test_create_valid_data(self, setup_database, firstname, lastname, dateofbirth):
        """Тест для добавления записи с валидными данными"""
        with db_connection() as cursor:
            cursor.execute("INSERT INTO People (firstname, lastname, dateofbirth) VALUES (%s, %s, %s)",
                           (firstname, lastname, dateofbirth))
            cursor.execute("SELECT * FROM People WHERE firstname = %s AND lastname = %s", (firstname, lastname))
            result = cursor.fetchone()

            assert result is not None
            assert result[1] == firstname
            assert result[2] == lastname
            assert result[3] == dateofbirth

    # @pytest.mark.parametrize("firstname, lastname, dateofbirth", [
    #     (None, 'Иванов-Сергеев', '2000-12-15'),
    #     ('', 'Иванов-Сергеев', '2000-12-15'),
    #     ('Иван', None, '2000-12-15'),
    #     ('Иван', '', '2000-12-15'),
    #     ('Иван', 'Иванов-Сергеев', None),
    #     ('Иван', 'Иванов-Сергеев', ''),
    #     ('Иван', 'Иванов-Сергеев', '2026-12-12'),
    # ])
    # def test_create_invalid_data(self, setup_database, firstname, lastname, dateofbirth):
    #     """Негативный тест для добавления записи с невалидными данными"""
    #     with db_connection() as cursor:
    #         try:
    #             cursor.execute("INSERT INTO People (firstname, lastname, dateofbirth) VALUES (%s, %s, %s)",
    #                            (firstname, lastname, dateofbirth))
    #         except psycopg2.Error as e:
    #             assert e.pgcode == '23502'  # Код ошибки для violation of not-null constraint
    #
    # @pytest.mark.parametrize("firstname, lastname, dateofbirth", [
    #     ('Paul-Frank', 'John', '2023-12-15'),
    #     ('Иван', 'Иванов-Сергеев', '2000-12-15'),
    # ])
    # def test_read_single_record(self, setup_database, firstname, lastname, dateofbirth):
    #     """Чтение одной записи из таблицы People"""
    #     with db_connection() as cursor:
    #         cursor.execute("INSERT INTO People (firstname, lastname, dateofbirth) VALUES (%s, %s, %s)",
    #                        (firstname, lastname, dateofbirth))
    #         cursor.execute("SELECT * FROM People WHERE firstname = %s", (firstname,))
    #         result = cursor.fetchone()
    #
    #         assert result is not None
    #         assert result[1] == firstname
    #         assert result[2] == lastname
    #         assert result[3] == dateofbirth
    #
    # def test_update_record(self, setup_database):
    #     """Обновление записи в таблице People"""
    #     with db_connection() as cursor:
    #         cursor.execute("INSERT INTO People (firstname, lastname, dateofbirth) VALUES (%s, %s, %s)",
    #                        ('Paul-Frank', 'Иван', '2023-12-15'))
    #         cursor.execute("UPDATE People SET lastname = %s WHERE lastname = %s", ('Nikolai', 'Иван'))
    #         cursor.execute("SELECT * FROM People WHERE firstname = 'Paul-Frank' AND lastname = 'Nikolai'")
    #         result = cursor.fetchone()
    #
    #         assert result is not None
    #         assert result[1] == 'Paul-Frank'
    #         assert result[2] == 'Nikolai'
    #         assert result[3] == '2023-12-15'
    #
    # @pytest.mark.parametrize("firstname, lastname", [
    #     ('Arnold', 'Sinatra'),
    #     ('Иван', 'НеСуществующий'),
    # ])
    # def test_delete_record(self, setup_database, firstname, lastname):
    #     """Удаление записи из таблицы People"""
    #     with db_connection() as cursor:
    #         cursor.execute("INSERT INTO People (firstname, lastname, dateofbirth) VALUES (%s, %s, %s)",
    #                        ('Frank', 'Sinatra', '1995-12-15'))
    #         cursor.execute("DELETE FROM People WHERE firstname = %s AND lastname = %s", (firstname, lastname))
    #         cursor.execute("SELECT * FROM People WHERE firstname = %s AND lastname = %s", (firstname, lastname))
    #         result = cursor.fetchone()
    #
    #         assert result is None