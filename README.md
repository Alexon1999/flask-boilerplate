# Flask Boilerplate

- Flask-SQLAlchemy (ORM)
- Flask-Migrate (database migrations)
- Flask-JWT-Extended (JWT token authentication)
- Marshmallow (Serialization, Deserialization and Validation)
- Flask-Smorest (helps with input validation, serialization, OPENAPI documentation)
- Flask-Injector (Dependency Injection)
- Flask-Secrets to quickly generate secure random tokens you can use for various things
- Linting, formatting and testing:
  - flake8 is used to lint the code base
  - isort is used to auto-sort Python imports
  - black is used to format the code base
  - pytest and pytest-cov for writing tests and reporting test coverage

# Design Patterns

- Factory Pattern : The factory pattern is used to create an instance of a class (ex: Flask app) based on a set of parameters.
- Repository Pattern : The repository pattern is used to separate the logic that retrieves the data from the database from the business logic.
- Service Pattern : The service pattern is used to separate the business logic from the controller.
- Singleton Pattern : The singleton pattern is used to ensure that a class has only one instance and provide a global point of access to it.
- Dependency Injection : The dependency injection pattern is used to inject the dependencies into the class.

# Run

- Create a virtual environment
```bash
python3 -m venv env
```

- Activate the virtual environment
Linux, Unix, MacOS 
```bash
source env/bin/activate
```
windows
```bash
$ .\env\Scripts\activate
```

- Install the dependencies
```bash
pip install -r requirements.txt
```

- Generate a secret key for Flask and JWT secret key
```bash
flask secrets --help
flask secrets
flask secrets --length=30
```

- Update the environment variables in the `.env` file

- Set the environment variables
Linux, Unix, MacOS 
```bash
$ cp .env.example .env

# or
$ source scripts/load_env.sh .env
```

Windows
```bash
# powershell
$ .\scripts\loadenv.ps1 .env

# cmd
$ .\scripts\loadenv.bat .env
```


- Run the flask app
```bash
flask run

# Run the flask app in development mode
flask run --reload

# or 
python3 run.py
```

# Migration

- Initialize the migration environment
```bash
flask db init
```
- Create a migration
```bash
flask db migrate
flask db migrate -m "Initial migration."
```
- Apply migration to the database
```bash
flask db upgrade
```
- Downgrade the migration
```bash
flask db downgrade
```


# Shell

- Debugging the database
```bash
sqlite3 db.sqlite3
.tables
.schema
.schema User
```

- Run the flask shell
```bash
flask shell

# Example
>>> from authentication.models import User
>>> User.query.all()

>>> app
>>> app.configs
>>> db

>>> exit()
```

# Testing

- Run the tests
```bash
pytest
```

- Run the tests with coverage
```bash
pytest --cov=.
```

- Run the tests with coverage and generate an HTML report
```bash
pytest --cov=. --cov-report=html
```

# Documentation

- Swagger UI is available at `/doc`


