# Tasks

## Instalation
1. Go to the Tasks directory
2. Create virtual environment: python -m venv venv_name
3. Activate virtual environment: source venv/bin/activate (Linux/Mac), venv\Scripts\activate (Windows)
4. Install the required dependencies: pip install -r requirements.txt
5. Prepare your MySQL database: install mysql server directly or via docker, create user, database, grant permission to user. (or just use sqlite3 instead) 
6. Create .env file in the Tasks directory for storing sensitive data, copy all variables from env_example.txt to .env and assign your data.
7. Run django management command: python manage.py migrate
8. Run tests: python manage.py test
9. Your are ready to go, run python manage.py runserver to be able to access all endpoints