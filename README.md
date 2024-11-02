[![Backend Test Cases](https://github.com/DragNBuy/buzzaar/actions/workflows/backend-tests.yml/badge.svg)](https://github.com/DragNBuy/buzzaar/actions/workflows/backend-tests.yml)
[![Frontend Test Cases](https://github.com/DragNBuy/buzzaar/actions/workflows/frontend-tests.yml/badge.svg)](https://github.com/DragNBuy/buzzaar/actions/workflows/frontend-tests.yml)

# Buzzaar Backend Documentation

This guide will help you set up and run the backend for the Buzzaar project.

## Prerequisites
- Python 3.12.x installed on your system
- pip, pip-dev, pip-venv installed

## Installation Steps

1. Clone the repository:

   ```bash
   git clone git@github.com:DragNBuy/buzzaar.git
   ```

2. Navigate to the backend directory:

   ```bash
   cd buzzaar-backend
   ```

3. Create a virtual environment inside the folder:

   ```bash
   python3.12 -m venv venv
   ```

4. Activate the virtual environment (specific to your shell):
   - **Bash**:
     ```bash
     source venv/bin/activate
     ```
   - **Fish**:
     ```fish
     source venv/bin/activate.fish
     ```

5. Install all requirements into the virtual environment:

   ```bash
   pip install -r requirements.txt
   ```

6. Install PostgreSQL and create the database:

   - Install PostgreSQL:
     ```bash
     sudo apt update
     sudo apt install postgresql postgresql-contrib
     ```

   - Switch to the PostgreSQL user and open the PostgreSQL prompt:
     ```bash
     sudo -i -u postgres
     psql
     ```

   - Create the database and user:
     ```sql
     CREATE DATABASE buzzaar_db;
     CREATE USER buzzaar_user WITH PASSWORD 'secure password';
     ```

   - Grant all privileges to the user on the database:
     ```sql
     GRANT ALL PRIVILEGES ON DATABASE buzzaar_db TO buzzaar_user;
     
     ```

   - Exit the PostgreSQL prompt:
     ```sql
     \q
     ```

   - Exit from the PostgreSQL user:
     ```bash
     exit
     ```

7. Navigate to the core application:

   ```bash
   cd buzzaar-core
   ```

8. Create a `.env` file in the directory with the following content:

   ```
   DEBUG=True
   SECRET_KEY=A Django secret key, that needs to be generated using from django.core.management.utils import get_random_secret_key

   POSTGRES_DB=buzzaar_db
   POSTGRES_USER=buzzaar_user
   POSTGRES_PASSWORD=secure password
   POSTGRES_HOST_AUTH_METHOD=md5
   DATABASE_PORT=5432
   ```

   To generate the `SECRET_KEY`, run the following commands:
   
   ```bash
   python3.12 manage.py shell
   ```
   
   Then, in the Python shell:
   
   ```python
   from django.core.management.utils import get_random_secret_key
   get_random_secret_key()
   ```
   
   Copy the generated key, and then press `CTRL+D` to exit the shell.

9. Apply migrations to set up the database:

   ```bash
   python3.12 manage.py makemigrations
   python3.12 manage.py migrate
   ```

10. Start the development server:

   ```bash
   python3.12 manage.py runserver
   ```

11. The server should now be running and accessible at `http://127.0.0.1:8000/`.
