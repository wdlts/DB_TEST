# DB_TEST

PROJECT STRUCTURE

├── compose.yml - compose file to create containerized test environment
├── db_dump
│   └── test_db.sql - SQL code to creat test database
├── python_tests
│   ├── conftest.py - settings and fixtures with test data and test connections
│   ├── database.py - database settings file
│   ├── pytest.ini - pytest settings file
│   ├── requirements.txt - requirements for Python/Pytest
│   ├── t_data.py - test data
│   └── test_db_operations.py - tests
├── README.md
└── XLSX
    └── test_cases.xlsx - test cases

HOW TO

1. Clone the repository.
2. Install Docker/Compose or Podman/Compose on your machine.
3. Run the "docker-compose (or podman-compose) up --build --force-recreate -d" command from the root directory of the cloned project.
4. The test database will be available on localhost:5432. You can change the port in compose.yml file as needed.
5. The results will be available on localhost:9999. You can change the port in compose.yml file as needed.

TESTING REQUIREMENTS

