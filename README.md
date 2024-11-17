# DATABASE TEST

PROJECT STRUCTURE

├── compose.yml - compose file to create testing environment and run tests <br>
├── db_dump <br>
│   └── test_db.sql - test_db.sql - basic test database schema <br>
├── Dockerfile.flask - dockerfile for flask application, exposing pytet report <br>
├── Dockerfile.pytest - dockerfile for pytest application, running database tests <br>
├── python_flask <br>
│   ├── flask_test_results.py - flask application exposing pytest report <br>
│   ├── requirements.txt - requirements to create flask application <br>
│   └── templates - empty folder to store test report <br>
├── python_tests <br>
│   ├── conftest.py - basic settings/fixtures <br>
│   ├── database.py - database connection file <br>
│   ├── pytest.ini - pytest settings <br>
│   ├── requirements.txt - requirements to create pytest application <br>
│   ├── t_data.py - test data <br>
│   └── test_db_operations.py - database tests <br>
├── README.md - readme file <br>
└── XLSX <br>
    └── test_cases.xlsx - test cases in XLSX file <br>


HOW TO

1. Clone the repository.
2. Install Docker/Compose or Podman/Compose on your machine.
3. Run the "docker-compose (or podman-compose) up --build --force-recreate --rempve-orphans -d" command from the root directory of the cloned project (where compose.yml is located).
4. The test database will be available on localhost:5433. You can change the port in compose.yml file as needed.
5. The results will be available on localhost:5000. You can change the port in compose.yml file as needed.

TESTING REQUIREMENTS

