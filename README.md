# DB_TEST

PROJECT STRUCTURE

├── compose.yml - compose file to create testing environment and run tests<\n>
    ├── db_dump<\n>
    │   └── test_db.sql - basic test database schema
    ├── Dockerfile.flask - dockerfile for flask application, exposing pytet report
    ├── Dockerfile.pytest - dockerfile for pytest application, running database tests
    ├── python_flask
    │   ├── flask_test_results.py - flask application exposing pytest report
    │   ├── requirements.txt - requirements to create flask application
    │   └── templates - empty folder to store test report
    ├── python_tests
    │   ├── conftest.py - basic settings/fixtures
    │   ├── database.py - database connection file
    │   ├── pytest.ini - pytest settings
    │   ├── requirements.txt - requirements to create pytest application
    │   ├── t_data.py - test data
    │   └── test_db_operations.py - database tests
    ├── README.md - readme file
    └── XLSX
        └── test_cases.xlsx - test cases in XLSX file
    

HOW TO

1. Clone the repository.
2. Install Docker/Compose or Podman/Compose on your machine.
3. Run the "docker-compose (or podman-compose) up --build --force-recreate --rempve-orphans -d" command from the root directory of the cloned project (where compose.yml is located).
4. The test database will be available on localhost:5433. You can change the port in compose.yml file as needed.
5. The results will be available on localhost:5000. You can change the port in compose.yml file as needed.

TESTING REQUIREMENTS

