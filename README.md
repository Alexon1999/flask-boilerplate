# Flask Boilerplate

- Flask-SQLAlchemy (ORM)
- Flask-Migrate (database migrations)
- Flask-JWT-Extended (JWT token authentication)
- Flask-Secrets to quickly generate secure random tokens you can use for various things

# Migration

- Initialize the migration environment
```bash
flask db init
```
- Create a migration
```bash
flask db migrate
```
- Apply the migration
```bash
flask db upgrade
```
- Downgrade the migration
```bash
flask db downgrade
```

# Run

- Create a virtual environment
```bash
python3 -m venv env
```

- Activate the virtual environment
```bash
source env/bin/activate
```

- Install the dependencies
```bash
pip install -r requirements.txt
```

- Set the environment variables
```bash
cp .env.example .env
```

- Generate a secret key for Flask and JWT secret key
```bash
flask secrets --help
flask secrets
flask secrets --length=30
```

- Update the environment variables in the `.env` file

- Set environment variables
```bash
set -a; source .env; set +a;
```

- Run the flask app
```bash
flask run

# Run the flask app in development mode
flask run --reload

# or 
python3 run.py
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
>>> exit()
```