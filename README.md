# DATABASE TEST


Краткое описание: в данной среде поднимаются три сервиса в контенерах - база данных, тестирующее базу данных приложение, и простое приложение на фласке, предназначенное для вывода отчета по завершении тестирования. <br>
После запуска файла compose.yml будет развернута база на локалхосте (порт 5432), протестирована, а результаты тестирования будут доступны на локалхосте (порт 5000) (см. подробное описание ниже).


PROJECT STRUCTURE

├── compose.yml - compose file to create testing environment and run tests <br>
├── db_dump <br>
│&nbsp;&nbsp;&nbsp;└── test_db.sql - test_db.sql - basic test database schema <br>
├── Dockerfile.flask - dockerfile for flask application, exposing pytet report <br>
├── Dockerfile.pytest - dockerfile for pytest application, running database tests <br>
├── python_flask <br>
│&nbsp;&nbsp;&nbsp;├── flask_test_results.py - flask application exposing pytest report <br>
│&nbsp;&nbsp;&nbsp;├── requirements.txt - requirements to create flask application <br>
│&nbsp;&nbsp;&nbsp;└── templates - empty folder to store test report <br>
├── python_tests <br>
│&nbsp;&nbsp;&nbsp;├── conftest.py - basic settings/fixtures <br>
│&nbsp;&nbsp;&nbsp;├── database.py - database connection file <br>
│&nbsp;&nbsp;&nbsp;├── pytest.ini - pytest settings <br>
│&nbsp;&nbsp;&nbsp;├── requirements.txt - requirements to create pytest application <br>
│&nbsp;&nbsp;&nbsp;├── t_data.py - test data <br>
│&nbsp;&nbsp;&nbsp;└── test_db_operations.py - database tests <br>
├── README.md - readme file <br>
└── XLSX <br>
&nbsp;&nbsp;&nbsp;&nbsp;└── test_cases.xlsx - test cases in XLSX file <br>


HOW TO

1. Clone the repository.
2. Install Docker/Compose or Podman/Compose on your machine.
3. Run the "docker-compose (or podman-compose) up --build --force-recreate --remove-orphans -d" command from the root directory of the cloned project (where compose.yml is located).
4. The test database will be available on localhost:5432. You can change the port in compose.yml file as needed.
5. The results will be available on localhost:5000. You can change the port in compose.yml file as needed.

TESTING REQUIREMENTS

Условия задачи:
1. Создать новую базу данных PGSQL с именем test_db.

2. В базе данных создать таблицу с именем People, содержащую 3 столбца с разными типами данных (порядковый Index, FirstName, LastName, DataOfBirth), например: int, varchar[255], date.

Для данной таблицы необходимо написать позитивные и негативные сценарии наполнения таблицы данными и присутствия данных в таблице.
Необходимо использовать такие SQL команды как: Select, Insert, Update, Delete и т.д., дополнив их соответствующим WHERE или другими параметрами.

3. Предложить дополнительные позитивные и негативные сценарии DML операций.

4. Проанализировать и предложить сценарии нагрузочного тестирования и ожидаемый результат.
 
Ожидаемый результат:

1. Разработать тестовые сценарии (позитивные и негативные) и выполнить их вручную с использованием командной строки psql

2. Автоматизировать тестовые сценарии, разработанные в п.1. Для автоматизации использовать Python.
